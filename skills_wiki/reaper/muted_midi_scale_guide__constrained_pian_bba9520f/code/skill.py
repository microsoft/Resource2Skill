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
    Create a Muted MIDI Scale Guide in the current REAPER project and snap the Piano Roll.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Length of the guide item.
        velocity_base: Base MIDI velocity (irrelevant as notes are muted, but required for API).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Format inputs
    key = key.upper()
    scale = scale.lower()
    
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
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'"
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'"

    root_val = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track after the scale so it's clearly identifiable
    full_track_name = f"{key} {scale.title()} - {track_name}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create the MIDI item natively
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Get PPQ (Pulses Per Quarter Note) positions for start and end
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Populate with Muted Scale Notes ===
    note_count = 0
    for pitch in range(128):
        # Check if this pitch belongs to the scale
        if (pitch - root_val) % 12 in scale_intervals:
            # Insert note: (take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            # We set muted = True, selected = False, noSort = True (will sort after loop)
            RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateItemInProject(item)

    # === Step 5: Open in MIDI Editor & Hide Unused Rows ===
    # Unselect all items in the project to isolate our new item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open the item in the built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) # Item: Open in built-in MIDI editor
    
    # Trigger "View: Hide unused and unnamed note rows" in the active MIDI Editor
    # Action ID 40452
    RPR.RPR_MIDIEditor_LastFocused_OnCommand(40452, False)

    return f"Created '{full_track_name}' guide track with {note_count} muted notes. Piano roll constrained."
