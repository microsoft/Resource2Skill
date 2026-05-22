def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale-Constrained Piano Roll Guide in the current REAPER project.
    Generates a muted MIDI item containing all notes of a scale to fold the piano roll.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created guide track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars for the guide item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10],
    }

    # Format inputs
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_key = scale.lower().replace(" ", "_")
    scale_intervals = SCALES.get(scale_key, SCALES["major"])

    # Calculate all valid MIDI notes for the given scale across all octaves
    valid_notes = []
    for octave in range(11):  # Covers MIDI notes 0-127
        for interval in scale_intervals:
            note = (octave * 12) + root_val + interval
            if note <= 127:
                valid_notes.append(note)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Dedicated Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track clearly so the user knows what it is
    full_track_name = f"{track_name} ({key} {scale.capitalize()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create and Format MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # MUTE the item so it acts purely as a visual guide
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert MIDI Notes ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for note in valid_notes:
        # insertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Fold the Piano Roll ===
    # Select the item so we can open it
    RPR.RPR_SetMediaItemInfo_Value(item, "B_UISEL", 1.0)
    
    # Open selected item in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Get active MIDI editor and run "View: Hide unused note rows" (Action 40452)
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        RPR.RPR_MIDIEditor_OnCommand(editor, 40452)

    return f"Created muted '{full_track_name}' guide track spanning {len(valid_notes)} diatonic notes, folding piano roll."
