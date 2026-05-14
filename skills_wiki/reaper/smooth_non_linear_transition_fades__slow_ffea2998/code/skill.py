def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Transition Fade",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Smooth Non-Linear Transition Fades (Slow Start/End) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Transition Fade' with a 2.0s non-linear fade transition at 120 BPM"
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create Media Item Placeholder ===
    # This item acts as the media block (audio or video) that will be faded.
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)

    # === Step 4: Add Video Processor ===
    # As demonstrated in the tutorial, the Video Processor is the engine for visual edits.
    # In REAPER, item fades natively interact with video opacity when processors are present.
    RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)

    # === Step 5: Apply Non-Linear Fade-Out (Slow start/end) ===
    # The tutorial emphasizes avoiding linear fades. We set the fade to last exactly 1 bar.
    # Setting C_FADEOUTSHAPE = 1 applies a non-linear (curved/equal-power) fade which provides
    # the smooth "Slow start/end" S-curve characteristic highlighted in the tutorial.
    fade_duration = bar_length_sec  # Fade out lasts exactly 1 bar
    
    RPR.RPR_SetMediaItemInfo_Value(item, "D_FADEOUTLEN", fade_duration)
    RPR.RPR_SetMediaItemInfo_Value(item, "C_FADEOUTSHAPE", 1) 
    
    # Force UI update so the curve is immediately visible
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with a {fade_duration:.2f}s non-linear fade transition over {bars} bars at {bpm} BPM"
