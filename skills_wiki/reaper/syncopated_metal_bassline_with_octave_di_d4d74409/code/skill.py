def create_pattern(
    project_name: str = "MetalProject",
    track_name: str = "Programmed Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Lowered from 127 to tame VST harshness
    **kwargs,
) -> str:
    """
    Create a Syncopated Metal Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (unused here as it's a pedal-point riff, but kept for compatibility).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (capping at 110 to reduce string noise).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Calculate Root Pitch ===
    # Using C1 (MIDI 24) as the standard bass starting octave for modern metal
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    clean_key = key.upper().replace("MINOR", "").replace("MAJOR", "").strip()
    root_pitch = NOTE_MAP.get(clean_key, 0) + 24 

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Define Syncopated Rhythm Grid ===
    # 16th note breakdown pattern
    # Format: (16th_step_index, semitone_offset)
    pattern = [
        (0, 0),    # Beat 1
        (2, 0),    # Beat 1 &
        (3, 0),    # Beat 1 a
        (6, 0),    # Beat 2 &
        (7, 0),    # Beat 2 a
        (8, 0),    # Beat 3
        (10, 0),   # Beat 3 &
        (13, 12),  # Beat 4 e (Octave displacement!)
        (15, 12)   # Beat 4 a (Octave displacement!)
    ]

    step_length_sec = beat_length_sec / 4.0
    note_duration_sec = step_length_sec * 0.80  # 80% duration for a staccato "chug" feel

    # === Step 6: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        bar_offset = bar * bar_length_sec
        
        for step, pitch_offset in pattern:
            start_time = bar_offset + (step * step_length_sec)
            end_time = start_time + note_duration_sec
            
            # Convert time to PPQ (Pulses Per Quarter Note)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = root_pitch + pitch_offset
            
            # Add the note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity_base, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 7: Add Placeholder Bass Instrument ===
    # Adding ReaSynth configured for a sub/bass tone (Triangle/Square mix)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 0 = Vol, 1 = Tuning, 2 = Square mix, 3 = Saw mix, 4 = Triangle mix
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.4)  # Square mix 
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.1)  # Saw mix (slight bite)
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 1.0)  # Triangle mix (heavy sub)

    return f"Created '{track_name}' with {note_count} staccato notes over {bars} bars at {bpm} BPM, using syncopation and octave displacement."
