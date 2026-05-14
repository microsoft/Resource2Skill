def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Kick-Locked Metal Bass pattern in the current REAPER project.
    Features staccato rhythms matching typical metal kicks, 110 velocity taming,
    and octave turnarounds.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (typical metal tempos: 110-160).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (usually minor or phrygian for metal).
        bars: Number of bars to generate (must be even for the 2-bar turnaround loop).
        velocity_base: Base MIDI velocity, intentionally set to 110 to reduce harshness.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Note map to calculate the root MIDI pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Metal bass is usually quite low. C1 = Note 24.
    root_midi = 24 + NOTE_MAP.get(key.upper().capitalize(), 0)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add a basic synth placeholder (so it can be heard immediately) ===
    # A saw wave works well as a placeholder for an aggressive bass
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Pitch the synth down 1 octave and adjust parameters for a bassy tone
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Tuning (0.5 is center/no offset)
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1) # Attack short
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3) # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.2) # Sustain low
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.1) # Release short

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate the Kick-Locked Rhythm ===
    # Each tuple: (start_beat, length_beats, pitch_offset, velocity)
    # The rhythm is a standard 2-bar djent/metalcore syncopated breakdown pattern.
    
    accent_vel = min(127, velocity_base + 10)
    norm_vel = velocity_base
    
    rhythm_loop = [
        # --- BAR 1 ---
        (0.0,  0.25, 0, accent_vel),  # Beat 1 downbeat
        (0.5,  0.25, 0, norm_vel),    # 8th note up
        (1.25, 0.25, 0, norm_vel),    # 16th syncopation before beat 2
        (1.75, 0.25, 0, norm_vel),
        (2.0,  0.25, 0, accent_vel),  # Beat 3 downbeat
        (2.5,  0.25, 0, norm_vel),    
        (3.0,  0.25, 0, norm_vel),    # Gallop starting beat 4
        (3.25, 0.25, 0, norm_vel),
        (3.5,  0.25, 0, norm_vel),

        # --- BAR 2 ---
        (4.0,  0.25, 0, accent_vel),  # Beat 1 downbeat
        (4.5,  0.25, 0, norm_vel),
        (5.25, 0.25, 0, norm_vel),
        (5.75, 0.25, 0, norm_vel),
        
        # 12th Fret Octave Turnaround Fill (Beat 3 and 4 of the second measure)
        (6.0,  0.25, 12, accent_vel), # Jump up 12 frets/semitones
        (6.5,  0.25, 12, norm_vel),
        (7.0,  0.25, 12, norm_vel),
        (7.5,  0.25, 12, norm_vel),
    ]

    # Calculate MIDI ticks (PPQ). REAPER default is 960 ticks per quarter note.
    PPQ = 960
    loop_length_beats = 8 # 2 bars
    num_loops = max(1, bars // 2) # Ensure we process at least the provided number of bars
    
    note_count = 0
    for loop_idx in range(num_loops):
        offset_beats = loop_idx * loop_length_beats
        for beat, length, pitch_offset, vel in rhythm_loop:
            abs_beat = offset_beats + beat
            
            # Stop adding notes if we exceed the requested total bar count
            if abs_beat >= bars * beats_per_bar:
                break
                
            start_ppq = int(abs_beat * PPQ)
            end_ppq = int((abs_beat + length) * PPQ)
            pitch = root_midi + pitch_offset
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort the MIDI stream after batch insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} metal bass notes over {bars} bars at {bpm} BPM (Tamed velocity: {velocity_base})."
