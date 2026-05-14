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
    Create a Scale-Constrained Piano Roll workflow in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars for the active composition area.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created workflow setup.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # === Step 1: Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    key_norm = key.capitalize()
    if key_norm not in NOTE_MAP:
        key_norm = "C"
    root_midi = NOTE_MAP[key_norm]
    
    scale_norm = scale.lower()
    if scale_norm not in SCALES:
        scale_norm = "minor"
    scale_intervals = SCALES[scale_norm]

    # Calculate valid pitch classes (modulo 12)
    valid_pitch_classes = set((root_midi + interval) % 12 for interval in scale_intervals)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key_norm} {scale_norm})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # === Step 3: Create Active Composition Item ===
    # This is where the user will actually draw their notes
    comp_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(comp_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(comp_item, "D_LENGTH", bar_length_sec * bars)
    comp_take = RPR.RPR_AddTakeToMediaItem(comp_item)

    # === Step 4: Create Muted Scale Guide Item ===
    # We place this item immediately AFTER the composition item so it doesn't overlap
    guide_pos = bar_length_sec * bars
    guide_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(guide_item, "D_POSITION", guide_pos)
    RPR.RPR_SetMediaItemInfo_Value(guide_item, "D_LENGTH", bar_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(guide_item, "B_MUTE", 1.0) # Completely muted
    guide_take = RPR.RPR_AddTakeToMediaItem(guide_item)

    # Populate guide item with all 128 possible notes that fit the scale
    note_count = 0
    for pitch in range(128):
        if pitch % 12 in valid_pitch_classes:
            # Insert note: length is 1 quarter note (960 PPQ)
            RPR.RPR_MIDI_InsertNote(guide_take, False, True, 0, 960, 0, pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(guide_take)

    # === Step 5: Open in MIDI Editor & Filter Rows ===
    # Select both items so the MIDI editor calculates "used rows" based on the guide item
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_SelectAllMediaItems(0, False)
    RPR.RPR_SetMediaItemSelected(comp_item, True)
    RPR.RPR_SetMediaItemSelected(guide_item, True)
    
    # Open Built-In MIDI Editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Trigger 'View: Hide unused note rows' (Command 40452)
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)
        # Zoom to content so the rows fill the screen nicely
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40466)

    return f"Created '{full_track_name}' workspace. Generated {note_count} guide notes and hid unused piano roll rows."
