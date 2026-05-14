def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Video Transitions",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Tempo-Synced Video Transition Scaffolding in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused for video).
        scale: Scale type (unused for video).
        bars: Total length of the sequence in bars.
        velocity_base: Unused for video.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Dedicated Video Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Video Processor FX ===
    # This enables REAPER's video engine on the track. 
    # (The user will select the "Item fades affect video" preset inside the plugin)
    RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)

    # === Step 4: Create Tempo-Synced Placeholder Items ===
    # We calculate absolute time in seconds based on the BPM to ensure 
    # the visual crossfades land exactly on the bar lines.
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    
    # Item 1 (Placeholder for Scene 1): Lasts for 2 bars
    item1 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", bar_length_sec * 2)
    # 1-bar fade out (Dissolve out)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_FADEOUTLEN", bar_length_sec)
    
    # Item 2 (Placeholder for Scene 2): Overlaps Item 1 to create the crossfade
    item2 = RPR.RPR_AddMediaItemToTrack(track)
    # Starts exactly at Bar 2 (overlapping the fade out of Item 1)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_POSITION", bar_length_sec * 1) 
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", bar_length_sec * 2)
    # 1-bar fade in (Dissolve in)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_FADEINLEN", bar_length_sec)
    # 0.5-bar fade out at the very end (Fade to black)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_FADEOUTLEN", bar_length_sec * 0.5)

    # Add empty takes so the items are visible and interactable on the timeline
    RPR.RPR_AddTakeToMediaItem(item1)
    RPR.RPR_AddTakeToMediaItem(item2)

    return f"Created '{track_name}' with 1-bar tempo-synced crossfade scaffolding at {bpm} BPM"
