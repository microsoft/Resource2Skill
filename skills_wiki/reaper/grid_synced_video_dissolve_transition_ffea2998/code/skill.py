def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Grid-Synced Video Dissolve",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Grid-Synced Video Dissolve Transition track.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total duration of the generated visual sequence.
        velocity_base: Base MIDI velocity (unused for video).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Video Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Video Processor FX ===
    # This built-in plugin is required to process video frames in REAPER
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)
    
    # Load the specific preset demonstrated in the tutorial that maps item volume to video opacity
    RPR.RPR_TrackFX_SetPreset(track, fx_idx, "Item fades affect video")

    # === Step 4: Calculate Grid-Synced Timing ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    
    # We will create a perfectly timed 1-bar dissolve crossfade
    clip_length = bar_length_sec * 2   # Each clip lasts 2 bars
    overlap_duration = bar_length_sec  # They crossfade over exactly 1 bar

    # === Step 5: Create Placeholder Item A (Outgoing Video) ===
    item_a = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item_a, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_a, "D_LENGTH", clip_length)
    
    take_a = RPR.RPR_AddTakeToMediaItem(item_a)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take_a, "P_NAME", "Drag Video A Here", True)
    
    # Apply fade-out to drive the video dissolve out
    RPR.RPR_SetMediaItemInfo_Value(item_a, "D_FADEOUTLEN", overlap_duration)
    RPR.RPR_SetMediaItemInfo_Value(item_a, "C_FADEOUTSHAPE", 0) # 0 = Linear crossfade

    # === Step 6: Create Placeholder Item B (Incoming Video) ===
    # Start Item B so it exactly overlaps Item A for the duration of the crossfade
    start_b = clip_length - overlap_duration
    
    item_b = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item_b, "D_POSITION", start_b)
    RPR.RPR_SetMediaItemInfo_Value(item_b, "D_LENGTH", clip_length)
    
    take_b = RPR.RPR_AddTakeToMediaItem(item_b)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take_b, "P_NAME", "Drag Video B Here", True)
    
    # Apply fade-in to drive the video dissolve in
    RPR.RPR_SetMediaItemInfo_Value(item_b, "D_FADEINLEN", overlap_duration)
    RPR.RPR_SetMediaItemInfo_Value(item_b, "C_FADEINSHAPE", 0) # 0 = Linear crossfade

    # Update REAPER UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with a perfect {overlap_duration:.2f}s (1 bar) video dissolve transition at {bpm} BPM."
