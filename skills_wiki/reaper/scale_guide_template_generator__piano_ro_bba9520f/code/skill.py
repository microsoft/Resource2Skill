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
    Create Scale Guide Template in the current REAPER project.
    Generates a track with muted notes defining a specific scale,
    then automatically hides unused note rows in the MIDI editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, whole_tone, etc.).
        bars: Number of bars the guide item should span.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., 'octaves' to define spread).

    Returns:
        Status string describing the created guide item.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Validate parameters
    if key not in NOTE_MAP: 
        key = "C"
    if scale not in SCALES: 
        scale = "major"
        
    octaves = kwargs.get("octaves", 8)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Label the track clearly so the user knows it's a structural guide
    full_track_name = f"{track_name} ({key} {scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Generate Muted Scale Notes ===
    root_pitch = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    notes_added = 0

    # Start from Octave 0/1 (MIDI note ~12) to avoid negative sub-bass errors
    for oct_offset in range(1, 1 + octaves):
        base_midi = (oct_offset * 12) + root_pitch
        
        for interval in scale_intervals:
            midi_pitch = base_midi + interval
            if midi_pitch <= 127:
                # Insert note with muted flag = True
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    True,           # MUTED (Critical for workflow)
                    start_ppq,      # start time
                    end_ppq,        # stretch across whole item
                    0,              # channel
                    int(midi_pitch),# pitch
                    velocity_base,  # velocity
                    False           # noSort
                )
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate MIDI Editor UI ===
    # Unselect all items in project, then select only our new item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open selected item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "View: Hide unused note rows" inside the active MIDI editor
    active_editor = RPR.RPR_MIDIEditor_GetActive()
    if active_editor:
        # Command ID 40452: View: Hide unused note rows
        RPR.RPR_MIDIEditor_OnCommand(active_editor, 40452)

    return f"Created '{full_track_name}' scale guide with {notes_added} muted notes spanning {octaves} octaves. Unused rows hidden."
