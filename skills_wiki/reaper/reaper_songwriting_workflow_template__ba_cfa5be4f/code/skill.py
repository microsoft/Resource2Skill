def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Songwriting Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Songwriting Layout' folder structure in the current REAPER project,
    inspired by the Reapertips workflow tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the master folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to initialize the placeholder item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Calculate item length in seconds
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars

    # === Step 2: Create Parent Folder Track ===
    start_track_idx = RPR.RPR_CountTracks(0)
    
    RPR.RPR_InsertTrackAtIndex(start_track_idx, True)
    parent_track = RPR.RPR_GetTrack(0, start_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    
    # Set as start of folder (+1)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1)

    # === Step 3: Create Child Tracks ===
    sub_tracks = ["Drums", "Bass", "Chords", "Melody"]
    
    for i, name in enumerate(sub_tracks):
        idx = start_track_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Set Track Name
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{name} (Placeholder)", True)

        # Add generic FX Placeholders so tracks can produce sound immediately
        if name == "Drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
        else:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # On the last child track, close the folder (-1)
        if i == len(sub_tracks) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", -1)

        # === Step 4: Add Placeholder MIDI Item to Chords Track ===
        if name == "Chords":
            item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
            take = RPR.RPR_GetActiveTake(item)
            
            # Calculate PPQ (Pulses Per Quarter Note) for exact grid alignment
            start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, item_length_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            # Insert a generic root-note drone based on the requested key
            base_note = NOTE_MAP.get(key, 0)
            note_val = base_note + 48  # Octave 3
            
            # Add the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val, velocity_base, False)
            RPR.RPR_MIDI_Sort(take)

    # Update UI
    RPR.RPR_TrackList_AdjustWindows(False)
    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' folder hierarchy with 4 sub-tracks and a placeholder {bars}-bar item at {bpm} BPM in {key} {scale}."
