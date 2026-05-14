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
    Create Video Transition Automations (Crossfade / Dissolve) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B) - Unused for video layout.
        scale: Scale type - Unused for video layout.
        bars: Number of bars for each video clip placeholder.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Video Transitions' with a 1-bar crossfade between 4-bar placeholder clips at 120 BPM"
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add Video Processor (Required to render visuals)
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)
    
    # Attempt to set the preset mentioned in the tutorial to link item fades to opacity
    # Note: Preset names can vary slightly by REAPER version, but this is the standard helper
    RPR.RPR_TrackFX_SetPreset(track, fx_idx, "Item fades affect video")

    # === Step 3: Create Media Items (Simulating Video Clips) ===
    # We create two overlapping empty items to serve as visual placeholders
    # that demonstrate the crossfade transition timing snapped to the musical grid.
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # Clip length is total bars, crossfade will last exactly 1 bar
    clip_length = bar_length_sec * bars
    crossfade_len = bar_length_sec * 1.0

    # Curve shape 1 is typically a slow start/end (S-curve) equivalent in REAPER fades
    fade_shape = 1 

    # --- Item 1 (Dissolves out) ---
    item1 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", clip_length)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_FADEOUTLEN", crossfade_len)
    RPR.RPR_SetMediaItemInfo_Value(item1, "C_FADEOUTSHAPE", fade_shape)
    
    take1 = RPR.RPR_AddTakeToMediaItem(item1)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take1, "P_NAME", "Video Clip A (Placeholder)", True)

    # --- Item 2 (Dissolves in) ---
    # Starts 1 bar before Clip 1 ends to create the physical overlap
    item2_start = clip_length - crossfade_len
    item2 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_POSITION", item2_start)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", clip_length)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_FADEINLEN", crossfade_len)
    RPR.RPR_SetMediaItemInfo_Value(item2, "C_FADEINSHAPE", fade_shape)
    
    take2 = RPR.RPR_AddTakeToMediaItem(item2)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take2, "P_NAME", "Video Clip B (Placeholder)", True)

    # Force UI update
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with a 1-bar crossfade between {bars}-bar placeholder clips at {bpm} BPM"
