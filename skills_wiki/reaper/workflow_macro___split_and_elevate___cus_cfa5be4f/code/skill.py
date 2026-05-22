def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Workflow_Source",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Simulates the 'Split and put item above' custom action demonstrated in the tutorial.
    It generates a baseline MIDI item, splits it at a specified bar, creates a new track 
    above the source, and moves the isolated slice to the new track.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created source track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of total bars to generate for the source media.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    # Music theory lookup tables for generating our placeholder media
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Source Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    src_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(src_track, "P_NAME", track_name, True)

    # === Step 3: Generate Baseline MIDI Item ===
    # We need media to perform the editing macro on.
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(src_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Populate the item with an 1/8th note arpeggio based on key/scale parameters
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 60 # Default to C4
    notes_per_bar = 8 
    note_length_ppq = 480 # 960 PPQ is 1/4 note, so 480 is 1/8th note
    
    for b in range(bars):
        for i in range(notes_per_bar):
            pitch = root_pitch + scale_intervals[i % len(scale_intervals)]
            start_ppq = int((b * notes_per_bar + i) * note_length_ppq)
            end_ppq = int(start_ppq + note_length_ppq - 10) # slight gap for articulation
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Execute "Split and Move Up" Macro Logic ===
    # The tutorial isolates an item at a time selection and moves it up a track.
    # We will simulate isolating "Bar 2" (from bar 2 start to bar 3 start)
    
    if bars >= 3:
        split_start = bar_length_sec * 1.0 # Start of Bar 2 (0-indexed 1)
        split_end = bar_length_sec * 2.0   # Start of Bar 3 (0-indexed 2)
        
        # Action: Split item at start of time selection
        # Note: RPR_SplitMediaItem returns the new item created to the RIGHT of the split point
        split_item_1 = RPR.RPR_SplitMediaItem(item, split_start) 
        
        # Action: Split the newly created remainder at the end of the time selection
        _ = RPR.RPR_SplitMediaItem(split_item_1, split_end)
        
        # Now, split_item_1 represents exactly the middle isolated slice (Bar 2)
        target_item = split_item_1
        
        # Action: Create track ABOVE source track
        # Since src_track is at track_idx, inserting at track_idx pushes src_track down to track_idx + 1
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        new_track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(new_track, "P_NAME", "Extracted_Slice (Macro Result)", True)
        
        # Action: Move isolated item to the new track
        RPR.RPR_MoveMediaItemToTrack(target_item, new_track)
        
        return f"Created base track, generated {bars} bars of media, and successfully executed 'Split and Move Up' macro logic on Bar 2."
    else:
        return f"Generated {bars} bars of media on '{track_name}'. (Need >= 3 bars to demonstrate the split macro logic properly)."
