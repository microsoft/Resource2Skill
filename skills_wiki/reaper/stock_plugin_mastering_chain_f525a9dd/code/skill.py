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
    Create Stock Plugin Mastering Chain in the current REAPER project.
    
    This applies a standard mastering FX chain (ReaComp, ReaEQ, ReaXcomp, Master Limiter)
    to the Master Track, applying the subtle EQ sweetening and limiting demonstrated
    in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Ignored (applies to Master Track).
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the mastering chain creation.
    """
    import reaper_python as RPR

    # === Step 1: Target the Master Track ===
    master_track = RPR.RPR_GetMasterTrack(0)

    # === Step 2: Add Bus Compressor (ReaComp) ===
    reacomp_idx = RPR.RPR_TrackFX_AddByName(master_track, "ReaComp (Cockos)", False, -1)
    if reacomp_idx >= 0:
        # Subtle "Glue" settings
        RPR.RPR_TrackFX_SetParam(master_track, reacomp_idx, 0, -12.0) # Threshold
        RPR.RPR_TrackFX_SetParam(master_track, reacomp_idx, 1, 2.0)   # Ratio
        RPR.RPR_TrackFX_SetParam(master_track, reacomp_idx, 4, 30.0)  # Attack (ms)
        RPR.RPR_TrackFX_SetParam(master_track, reacomp_idx, 5, 150.0) # Release (ms)

    # === Step 3: Add Mastering EQ (ReaEQ) ===
    # Applying the tutorial's EQ curves: +2dB @ 100Hz, -1dB @ 350Hz, +1dB @ 3500Hz
    reaeq_idx = RPR.RPR_TrackFX_AddByName(master_track, "ReaEQ (Cockos)", False, -1)
    if reaeq_idx >= 0:
        # Band 1 (Low Shelf)
        RPR.RPR_TrackFX_SetParam(master_track, reaeq_idx, 0, 100.0) # Freq
        RPR.RPR_TrackFX_SetParam(master_track, reaeq_idx, 1, 2.0)   # Gain (dB)
        
        # Band 2 (Bell - removing boxiness)
        RPR.RPR_TrackFX_SetParam(master_track, reaeq_idx, 3, 350.0) # Freq
        RPR.RPR_TrackFX_SetParam(master_track, reaeq_idx, 4, -1.0)  # Gain (dB)
        
        # Band 3 (Bell - adding clarity)
        RPR.RPR_TrackFX_SetParam(master_track, reaeq_idx, 6, 3500.0) # Freq
        RPR.RPR_TrackFX_SetParam(master_track, reaeq_idx, 7, 1.0)    # Gain (dB)
        
        # Note: ReaEQ doesn't expose Master Output Gain easily via standard params,
        # but the EQ curve itself is the core of the tonal sweetening.

    # === Step 4: Add Multiband Compressor (ReaXcomp) ===
    # Added to the chain as a placeholder for multiband control
    reaxcomp_idx = RPR.RPR_TrackFX_AddByName(master_track, "ReaXcomp (Cockos)", False, -1)

    # === Step 5: Add Master Limiter ===
    # JS: Master Limiter is a stock REAPER plugin perfect for final loudness
    limiter_idx = RPR.RPR_TrackFX_AddByName(master_track, "JS: Master Limiter", False, -1)
    if limiter_idx >= 0:
        # Param 0: Threshold (Lowering to increase loudness, as shown in tutorial)
        RPR.RPR_TrackFX_SetParam(master_track, limiter_idx, 0, -6.0)
        # Param 1: Limit/Ceiling (Set just below 0 to prevent inter-sample peaking)
        RPR.RPR_TrackFX_SetParam(master_track, limiter_idx, 1, -0.1)

    return "Successfully added Mastering Chain (ReaComp, ReaEQ, ReaXcomp, Limiter) to the Master Track."
