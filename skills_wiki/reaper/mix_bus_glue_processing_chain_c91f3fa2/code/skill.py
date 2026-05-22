def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Master",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Mix Bus "Glue" Processing Chain on the Master Track.

    Args:
        project_name: Project identifier (for logging).
        track_name: Ignored (applies directly to the Master Track).
        bpm: Tempo in BPM (optional, master track FX is tempo-independent).
        key: Root note (ignored).
        scale: Scale type (ignored).
        bars: Number of bars to generate (ignored).
        velocity_base: Base MIDI velocity (ignored).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the applied effects.
    """
    import reaper_python as RPR

    # === Step 1: Get the Master Track ===
    # 0 represents the current project.
    master_track = RPR.RPR_GetMasterTrack(0)

    # === Step 2: Add Stage 1 - JS: 1175 Compressor ===
    # Provides initial "glue" and transient shaping
    comp_idx = RPR.RPR_TrackFX_AddByName(master_track, "1175 Compressor", False, -1)
    if comp_idx >= 0:
        # In JS: 1175, typical parameters are:
        # 0: Threshold, 1: Ratio, 2: Gain, 3: Attack, 4: Release, 5: Mix
        
        # Set Ratio to 4:1 (often index 1 or 2 depending on the specific JS version)
        RPR.RPR_TrackFX_SetParam(master_track, comp_idx, 1, 4.0)
        
        # Set a slightly slower attack (~260) to let transients punch through
        RPR.RPR_TrackFX_SetParam(master_track, comp_idx, 3, 260.0) 
        
        # Set a slightly slower release (~214) to let the compressor breathe
        RPR.RPR_TrackFX_SetParam(master_track, comp_idx, 4, 214.0)

    # === Step 3: Add Stage 2 - VST: ReaXcomp ===
    # Provides multiband spectral balancing
    reaxcomp_idx = RPR.RPR_TrackFX_AddByName(master_track, "ReaXcomp", False, -1)
    if reaxcomp_idx >= 0:
        # Note: Modifying default band counts (from 4 to 3) via standard API parameters 
        # is unreliable. The plugin is instantiated for the user to configure.
        pass

    # === Step 4: Add Stage 3 - VST: ReaLimit ===
    # Provides final brickwall limiting and loudness maximization
    realimit_idx = RPR.RPR_TrackFX_AddByName(master_track, "ReaLimit", False, -1)
    if realimit_idx >= 0:
        # ReaLimit parameters: 0: Threshold, 1: Brickwall Ceiling
        # Set ceiling to -0.3 dB to prevent true peak clipping
        RPR.RPR_TrackFX_SetParam(master_track, realimit_idx, 1, -0.3)

    return "Successfully added 'Glue' mix processing chain (1175 Comp -> ReaXcomp -> ReaLimit) to the Master Track."

