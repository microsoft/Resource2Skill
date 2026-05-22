def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rolling Bass",
    bpm: int = 126,
    key: str = "F#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Pitch-Bend "Rolling" Bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (124-128 is ideal for this genre).
        key: Root note (e.g., "F#").
        scale: Scale type (e.g., "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth to generate the raw bass tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate fundamental MIDI note (Octave 1/2 for bass)
    root_midi = NOTE_MAP.get(key, 0) + 24 # +24 puts C at C1 (MIDI 24)

    # Typical tech-house rolling syncopated 16th note grid
    # These are 16th-note indices (0-15) within a 4/4 bar where notes occur
    # Intentionally avoiding the downbeats (0, 4, 8, 12) where the kick sits
    rhythm_16ths = [2, 3, 6, 9, 11, 14] 
    
    # Pitch bend automation settings
    pb_center = 8192
    pb_peak = 10192 # roughly +2000 as stated in the tutorial
    pb_duration_beats = 0.1 # ~45ms at 126 BPM, a very fast transient
    pb_steps = 6 # number of MIDI CC events to draw the curve
    note_count = 0

    # === Step 4: Generate Notes and Pitch Bend Curves ===
    for bar in range(bars):
        # The tutorial shifts from F# to F natural on the second bar
        # We mimic this two-bar tension drop by lowering the pitch by 1 semitone on odd bars
        current_pitch = root_midi if (bar % 2 == 0) else root_midi - 1
        
        for step in rhythm_16ths:
            # 16th note timing
            start_time = (bar * bar_length_sec) + (step * 0.25 * beat_sec)
            # Make the note slightly staccato (shorter than a full 16th)
            end_time = start_time + (0.2 * beat_sec) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the MIDI Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, current_pitch, velocity_base, True)
            note_count += 1
            
            # Draw the Pitch Bend transient curve at the attack of the note
            pb_end_time = start_time + (pb_duration_beats * beat_sec)
            pb_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pb_end_time)
            pb_ppq_range = pb_end_ppq - start_ppq
            
            for i in range(pb_steps):
                fraction = i / (pb_steps - 1)
                # Linear ramp from pb_peak down to pb_center
                current_val = int(pb_center + (pb_peak - pb_center) * (1.0 - fraction))
                
                # Convert 14-bit integer to MIDI LSB / MSB
                lsb = current_val & 0x7F
                msb = (current_val >> 7) & 0x7F
                
                event_ppq = start_ppq + (fraction * pb_ppq_range)
                # 224 (0xE0) is the MIDI status byte for Pitch Bend
                RPR.RPR_MIDI_InsertCC(take, False, False, event_ppq, 224, 0, lsb, msb)

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} rolling bass notes over {bars} bars at {bpm} BPM, complete with Pitch Bend transient automation."
