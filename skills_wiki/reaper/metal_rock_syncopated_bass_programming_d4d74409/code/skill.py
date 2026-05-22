def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal/Rock Syncopated Bass pattern matched to a typical kick/guitar rhythm.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity, specifically reduced to 110 to avoid harsh 
                       pick attack sample layers in bass VSTs.
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR
    
    # Base MIDI note mapping (Octave 1 for deep bass / drop tunings)
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
                
    root_note = NOTE_MAP.get(key.upper(), 24) # Default to C1
    
    # Define a classic metalcore/djent syncopated chug rhythm for 1 bar
    # Format: (start_beat, duration_beats, pitch_offset, velocity_mod)
    # 1 beat = a quarter note. 0.25 beats = a 16th note.
    rhythm_pattern = [
        (0.0,  0.25,  0,  0),   # Beat 1
        (0.25, 0.25,  0,  -5),  # Beat 1 e
        (0.75, 0.25,  0,  -5),  # Beat 1 a
        (1.5,  0.25,  0,  0),   # Beat 2 +
        (2.0,  0.5,   0,  5),   # Beat 3 (longer chug)
        (2.75, 0.25,  12, 10),  # Beat 3 a (Octave jump variation)
        (3.0,  0.25,  0,  0),   # Beat 4
        (3.5,  0.25,  0,  -5),  # Beat 4 +
        (3.75, 0.25,  0,  -5)   # Beat 4 a
    ]
    
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
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Ensure MIDI item is enabled for editing
    RPR.RPR_MIDI_DisableSort(take)
    
    # === Step 4: Insert MIDI Notes ===
    # Convert standard REAPER MIDI ticks (960 PPQ)
    ticks_per_quarter = 960
    notes_added = 0
    
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Add variation on the last bar: extra octave jumps
        is_turnaround = (bar == bars - 1)
        
        for (start_beat, duration, pitch_offset, vel_mod) in rhythm_pattern:
            # If it's the turnaround bar, replace the last notes with octave jumps
            if is_turnaround and start_beat >= 3.0:
                pitch_offset = 12
                
            start_ppq = (bar_start_beat + start_beat) * ticks_per_quarter
            end_ppq = start_ppq + (duration * ticks_per_quarter)
            
            # Slightly shorten note duration (legato/staccato separation) to mimic palm mutes
            end_ppq -= 30 
            
            pitch = root_note + pitch_offset
            vel = min(127, max(1, velocity_base + vel_mod))
            
            RPR.RPR_MIDI_InsertNote(
                take, 
                False,           # selected
                False,           # muted
                int(start_ppq),  # startppqpos
                int(end_ppq),    # endppqpos
                0,               # chan (0-15)
                pitch,           # pitch
                vel,             # vol
                False            # noSort
            )
            notes_added += 1

    RPR.RPR_MIDI_Sort(take)
    
    # === Step 5: Add FX Chain Placeholder ===
    # Add ReaSynth to make the MIDI audible as a basic sine/square bass
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tune down ReaSynth to act as a bass placeholder (Shape: Square/Saw mix)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5)    # Tuning (C1 range)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.8)    # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)    # Saw mix

    # Add ReaEQ to roll off harsh highs if using ReaSynth
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 1.0) # High Shelf / Low Pass type

    RPR.RPR_UpdateArrange()
    
    return f"Created '{track_name}' with {notes_added} syncopated notes over {bars} bars at {bpm} BPM in key of {key}."
