def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Video Transitions",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create [Video Dissolve & Dip-to-Black via Item Fades] in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to base the timeline off of.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Calculate musical timing
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    fade_length = bar_length_sec  # 1-bar transitions

    # === Step 2: Create Video Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add the Native Video Processor
    # To fully activate the effect, the user selects "Basic helpers: Item fades affect video" in the GUI.
    RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)

    # === Step 3: Create Structural Timeline Scaffold ===
    
    # Item 1: Represents the intro clip. Fades out to black over 1 bar.
    item1_start = 0.0
    item1_length = bar_length_sec * 2.0
    item1 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_POSITION", item1_start)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", item1_length)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_FADEOUTLEN", fade_length)
    RPR.RPR_SetMediaItemInfo_Value(item1, "C_FADEOUTSHAPE", 0) # 0 = Linear fade
    
    # (Gap of 1 bar creating a synchronized Dip-to-Black)
    
    # Item 2: Fades in from black, then acts as the first half of a cross-dissolve.
    item2_start = bar_length_sec * 3.0
    item2_length = bar_length_sec * 3.0
    item2 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_POSITION", item2_start)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", item2_length)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_FADEINLEN", fade_length)
    RPR.RPR_SetMediaItemInfo_Value(item2, "C_FADEINSHAPE", 0)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_FADEOUTLEN", fade_length)
    RPR.RPR_SetMediaItemInfo_Value(item2, "C_FADEOUTSHAPE", 0)
    
    # Item 3: Overlaps with Item 2 perfectly to create a seamless cross-dissolve.
    item3_start = bar_length_sec * 5.0
    item3_length = bar_length_sec * 2.0
    item3 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item3, "D_POSITION", item3_start)
    RPR.RPR_SetMediaItemInfo_Value(item3, "D_LENGTH", item3_length)
    RPR.RPR_SetMediaItemInfo_Value(item3, "D_FADEINLEN", fade_length)
    RPR.RPR_SetMediaItemInfo_Value(item3, "C_FADEINSHAPE", 0)
    
    # Provide visual grouping/coloring so they look distinct
    RPR.RPR_SetMediaItemInfo_Value(item1, "I_CUSTOMCOLOR", 0x00FF00|0x1000000) # Green
    RPR.RPR_SetMediaItemInfo_Value(item2, "I_CUSTOMCOLOR", 0x0000FF|0x1000000) # Red
    RPR.RPR_SetMediaItemInfo_Value(item3, "I_CUSTOMCOLOR", 0xFF0000|0x1000000) # Blue

    # Update UI to show changes
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' scaffold featuring a 1-bar Dip-to-Black and a 1-bar Cross-Dissolve at {bpm} BPM."
