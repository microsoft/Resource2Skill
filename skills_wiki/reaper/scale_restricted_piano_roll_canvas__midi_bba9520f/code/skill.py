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
    Create Scale-Restricted Piano Roll Canvas in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the scale canvas.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Highlighted in tutorial
    }

    # Validate inputs
    root_offset = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key} {scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create Media Item & Take ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Mute the item so it acts purely as a visual GUI guide (as shown in tutorial)
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert Notes for Grid Population ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    note_count = 0
    # Generate scale notes across octaves 1 through 8
    for octave in range(1, 9):
        octave_base = 12 * octave
        for interval in scale_intervals:
            midi_pitch = octave_base + root_offset + interval
            if midi_pitch <= 127:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate MIDI Editor Layout ===
    # Unselect all items globally, then select ONLY our guide item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open selected item in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "Hide unused note rows" within the active MIDI editor
    hwnd = RPR.RPR_MIDIEditor_GetActive()
    if hwnd:
        RPR.RPR_MIDIEditor_OnCommand(hwnd, 40453) # View: Hide unused note rows

    return f"Created '{full_track_name}' with {note_count} scale notes over {bars} bars. MIDI Editor folded to scale."
