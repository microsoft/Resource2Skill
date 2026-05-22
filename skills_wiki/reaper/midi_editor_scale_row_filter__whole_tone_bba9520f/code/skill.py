def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a MIDI Editor Scale Row Filter in the current REAPER project.

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
        Status string describing the generated scale guide.
    """
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    import reaper_python as RPR

    root_val = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale, SCALES["whole_tone"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track for the Scale Guide ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{key} {scale.replace('_', ' ').title()} Guide", True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 4: Populate with Muted Notes Across All Octaves ===
    notes_added = 0
    end_ppq = 960.0 * beats_per_bar * bars
    
    for octave in range(-1, 10):  # MIDI octaves -1 to 9
        for interval in intervals:
            note_num = root_val + interval + (octave * 12)
            if 0 <= note_num <= 127:
                # take, selected (False), muted (True), startppq, endppq, chan, pitch, vel, noSortIn
                RPR.RPR_MIDI_InsertNote(take, False, True, 0.0, end_ppq, 0, note_num, velocity_base, True)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Open in MIDI Editor & Hide Unused Rows ===
    # Select the item so it opens properly
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Item: Open in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # Check the toggle state of "View: Hide unused note rows" (Cmd ID: 40453)
        # MIDI Editor Section ID is 32060
        toggle_state = RPR.RPR_GetToggleCommandStateEx(32060, 40453)
        if toggle_state == 0:
            # If it's off, trigger it to turn it on
            RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40453)

    return f"Created '{key} {scale}' Scale Guide with {notes_added} muted notes over {bars} bars. MIDI editor locked to scale."
