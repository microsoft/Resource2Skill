def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Funky Synth Bass",
    bpm: int = 100,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a P-Funk style syncopated synth bassline with ghost notes and pitch drops.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (classic funk tempo is ~95-105).
        key: Root note (e.g., "D").
        scale: Scale type (should be minor or pentatonic_minor).
        bars: Number of bars to generate (4 recommended for the progression).
        velocity_base: Base MIDI velocity for primary notes (0-127).
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Setup Key & Scale Math
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # We use a base octave of 2 (MIDI 24 for C1, 36 for C2) for bass
    BASE_OCTAVE = 24 
    root_pitch = NOTE_MAP.get(key.capitalize(), 2) + BASE_OCTAVE

    # The tutorial progression: i - v - iv - i
    # In D Minor: D (0), A (+7), G (+5), D (0)
    progression_offsets = [0, 7, 5, 0]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Standard REAPER PPQ is 960 per quarter note (beat)
    PPQ = 960

    # Define the 1-bar Funky Rhythm Motif
    # Format: (beat_start, duration_beats, pitch_offset_from_chord_root, velocity_mult)
    # pitch_offset: 0=root, 12=octave, 10=minor 7th, 3=minor 3rd
    funk_motif = [
        (0.00, 0.50, 0,  1.00), # Downbeat root
        (0.75, 0.20, 0,  0.40), # GHOST NOTE just before beat 2
        (1.00, 0.25, 12, 1.00), # Octave pop on beat 2
        (1.50, 0.25, 10, 0.80), # Minor 7th syncopation
        (2.00, 0.50, 0,  0.90), # Beat 3 downbeat
        (2.75, 0.20, 0,  0.40), # GHOST NOTE just before beat 4
        (3.00, 0.25, 3,  0.85), # Minor 3rd blues riff
        (3.50, 0.40, 0,  1.00)  # Root return
    ]

    note_count = 0

    for bar in range(bars):
        # Cycle through the i-v-iv progression
        chord_root = root_pitch + progression_offsets[bar % len(progression_offsets)]
        
        # If it's the 4th bar (or the last bar of the loop), leave space at the end for the pitch bend drop
        is_last_bar = (bar == bars - 1)
        
        for note in funk_motif:
            b_start, b_dur, p_offset, v_mult = note
            
            # On the final bar, skip notes on beat 3.5 to leave room for the dramatic drop
            if is_last_bar and b_start >= 3.0:
                if b_start == 3.0: 
                    b_dur = 1.0 # Extend beat 3 into the drop
                else:
                    continue
            
            start_ppq = int((bar * beats_per_bar + b_start) * PPQ)
            end_ppq = int((bar * beats_per_bar + b_start + b_dur) * PPQ)
            pitch = chord_root + p_offset
            vel = int(velocity_base * v_mult)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

        # Pitch Bend Logic (Drop an octave at the end of the phrase)
        if is_last_bar:
            # Drop from center (8192) to bottom (0) over beat 4
            pb_start_beat = bar * beats_per_bar + 3.0
            pb_end_beat = bar * beats_per_bar + 4.0
            
            # Insert a few CC points to make the glide
            steps = 8
            for i in range(steps + 1):
                fraction = i / steps
                current_beat = pb_start_beat + (fraction * 1.0)
                current_ppq = int(current_beat * PPQ)
                
                # Pitch bend ranges 0 to 16383. Center is 8192.
                pb_val = int(8192 * (1.0 - fraction)) 
                
                # Convert 14-bit pitch bend to LSB (msg2) and MSB (msg3)
                lsb = pb_val & 0x7F
                msb = (pb_val >> 7) & 0x7F
                
                # 0xE0 is Pitch Bend on Channel 1
                RPR.RPR_MIDI_InsertCC(take, False, False, current_ppq, 0xE0, 0, lsb, msb)
            
            # Snap pitch wheel back to center right before the next loop starts
            reset_ppq = int(pb_end_beat * PPQ)
            RPR.RPR_MIDI_InsertCC(take, False, False, reset_ppq, 0xE0, 0, 0, 64)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add a stock synth tuned for bass
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Lower the master volume of ReaSynth slightly to avoid clipping with multiple notes
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7) # Vol parameter
    
    # Add EQ to carve out the high end (simulate a 24dB lowpass on a Moog)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 is usually the high shelf. We turn it down to simulate a darker funk bass.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, -15.0) # Lower high-end gain

    return f"Created '{track_name}' with {note_count} funk notes and pitch drop over {bars} bars at {bpm} BPM."
