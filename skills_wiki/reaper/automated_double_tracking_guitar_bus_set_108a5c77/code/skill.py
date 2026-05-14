def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rhythm GTR",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Double-Tracking Guitar Bus Setup in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created tracking bus.
        bpm: Tempo in BPM.
        key: Root note (unused for audio routing, kept for signature consistency).
        scale: Scale type (unused for audio routing, kept for signature consistency).
        bars: Number of bars (unused for audio routing, kept for signature consistency).
        velocity_base: Base MIDI velocity (unused).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track architecture.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track Architecture ===
    # Get current total tracks to append at the end
    start_idx = RPR.RPR_CountTracks(0)

    # 2a. Parent Bus Track
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    bus_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", f"{track_name} Bus", True)
    # Set as Folder Parent (Depth = +1)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1)
    # Ensure monitoring is enabled for tracking
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_RECMON", 1) 

    # 2b. Child Track - Left
    RPR.RPR_InsertTrackAtIndex(start_idx + 1, True)
    left_track = RPR.RPR_GetTrack(0, start_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(left_track, "P_NAME", f"{track_name} L", True)
    # Pan 100% Left (-1.0)
    RPR.RPR_SetMediaTrackInfo_Value(left_track, "D_PAN", -1.0)
    # Normal folder track (Depth = 0)
    RPR.RPR_SetMediaTrackInfo_Value(left_track, "I_FOLDERDEPTH", 0)

    # 2c. Child Track - Right
    RPR.RPR_InsertTrackAtIndex(start_idx + 2, True)
    right_track = RPR.RPR_GetTrack(0, start_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(right_track, "P_NAME", f"{track_name} R", True)
    # Pan 100% Right (1.0)
    RPR.RPR_SetMediaTrackInfo_Value(right_track, "D_PAN", 1.0)
    # End of Folder (Depth = -1)
    RPR.RPR_SetMediaTrackInfo_Value(right_track, "I_FOLDERDEPTH", -1)


    # === Step 3: Add FX Chain to Parent Bus ===
    # Add ReaTune (Cockos) for monitoring tuning
    tune_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaTune", False, -1)
    
    # Add an Amp/Tone placeholder (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    
    # Open the Tuner UI for the user automatically
    if tune_idx >= 0:
        RPR.RPR_TrackFX_SetOpen(bus_track, tune_idx, True)

    return f"Created Double-Tracking Architecture: '{track_name} Bus' containing hard-panned L/R tracks."
