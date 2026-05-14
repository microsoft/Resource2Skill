def create_pattern(
    project_name: str = "MetalCore",
    track_name: str = "Bass (Kick Follower)",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a tight, kick-following Metal/Rock bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). (Represents the 'Drop' tuning open string).
        scale: Scale type (defaults to minor, but uses mostly root notes here).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (lowered to 110 to reduce VST string harshness).
        **kwargs: Additional overrides.
        
    Returns:
        Status string indicating the track generation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    # Create MIDI item spanning the designated bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Define Rhythmic Patterns (Step offset, duration in 16ths, pitch mod) ===
    # Simulates following a syncopated double-kick pattern
    base_pattern = [
        (0, 2, 0),   # Beat 1
        (3, 2, 0),   # Beat 1 "a"
        (6, 2, 0),   # Beat 2 "+"
        (8, 2, 0),   # Beat 3
        (12, 2, 0),  # Beat 4
        (14, 2, 0)   # Beat 4 "+"
    ]
    
    # Fast 16th note gallop for variation
    gallop_pattern = [
        (0, 2, 0), (3, 2, 0), (6, 2, 0), (8, 2, 0), 
        (12, 1, 0), (13, 1, 0), (14, 1, 0), (15, 1, 0)
    ]
    
    # 12th Fret (Octave) jumps at the end of a phrase
    octave_jump_pattern = [
        (0, 2, 0), (3, 2, 0), (6, 2, 0), (8, 2, 0), 
        (12, 2, 12), (14, 2, 12)
    ]

    # Map the requested key to the lowest usable bass octave (C1 range)
    root_pitch = NOTE_MAP.get(key, 0) + 24 

    # === Step 5: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        # Apply musical logic for variations based on bar position
        if bar == bars - 1:
            pattern = octave_jump_pattern
        elif bar > 0 and bar % 2 == 1:
            pattern = gallop_pattern
        else:
            pattern = base_pattern
            
        bar_offset_steps = bar * 16
        
        for step, dur, pitch_mod in pattern:
            start_qn = (bar_offset_steps + step) * 0.25
            end_qn = start_qn + (dur * 0.25)
            
            # Convert Quarter Notes to Project Time (Seconds)
            start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            
            # Convert Project Time to PPQ for the MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = root_pitch + pitch_mod
            
            # Note inserted, no sort flag enabled (False) until the end for efficiency
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity_base, False
            )
            note_count += 1
            
    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {note_count} kick-following syncopated notes over {bars} bars at {bpm} BPM."
