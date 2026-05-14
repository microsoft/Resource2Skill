def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale-Locked Piano Roll Guide Generator in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate for the guide block.
        velocity_base: Base MIDI velocity for guide notes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the scale guide track.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key.upper()} {scale.capitalize()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Mute track so guide notes never output audio
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create Background MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate valid pitches across all MIDI octaves (0-127)
    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    valid_pitches = []
    for oct in range(11):
        for interval in scale_intervals:
            pitch = root_val + interval + (oct * 12)
            if 0 <= pitch <= 127:
                valid_pitches.append(pitch)

    start_qn = 0.0
    end_qn = bars * beats_per_bar
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # Draw continuous guide notes covering the item length
    for pitch in valid_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: UI Actions (Open MIDI Editor & Hide Unused Rows) ===
    # Isolate selection to the newly generated item
    RPR.RPR_SelectAllMediaItems(0, False)
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Retrieve active MIDI editor window and trigger "Hide unused note rows"
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        RPR.RPR_MIDIEditor_OnCommand(editor, 40452)

    return f"Created '{full_track_name}' guide track containing {len(valid_pitches)} mapped pitches over {bars} bars. Piano roll successfully locked to scale."
