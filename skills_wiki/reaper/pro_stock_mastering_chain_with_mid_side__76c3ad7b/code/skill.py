def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Mastering Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pro Stock Mastering Chain with Mid/Side Processing in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created mastering track.
        bpm: Tempo in BPM.
        key: Root note (unused for FX chain).
        scale: Scale type (unused for FX chain).
        bars: Number of bars (unused).
        velocity_base: Base velocity (unused).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the constructed mastering chain.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Mastering Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Build the Mastering FX Chain ===

    # 1. ReaEQ - Cleaning extreme lows and highs
    hpf_lpf_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: High-Pass Filter @ 30Hz
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 0, 30.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 3, 4.0)  # Type 4 = HighPass
    # Band 4: Low-Pass Filter @ 18kHz
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 12, 18000.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 15, 3.0)     # Type 3 = LowPass

    # 2. Event Horizon Clipper - Catching stray peaks before compression
    clipper_idx = RPR.RPR_TrackFX_AddByName(track, "Event Horizon Clipper", False, -1)
    RPR.RPR_TrackFX_SetParam(track, clipper_idx, 0, -7.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, clipper_idx, 1, -1.0) # Ceiling
    RPR.RPR_TrackFX_SetParam(track, clipper_idx, 2, 2.0)  # Soft Clip amount

    # 3. Mid/Side Encoder (Translates L/R to M/S on channels 1 & 2)
    enc_idx = RPR.RPR_TrackFX_AddByName(track, "Mid/Side Encoder", False, -1)

    # 4. ReaComp (Mid Compressor)
    mid_comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Pin Routing: Force ReaComp to process ONLY Channel 1 (Mid)
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 0, 0, 0, 1) # Input L <- Ch 1
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 0, 1, 0, 0) # Input R <- None
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 1, 0, 0, 1) # Output L -> Ch 1
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 1, 1, 0, 0) # Output R -> None
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 0, -12.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 1, 2.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 3, 15.0)  # Attack ms
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 4, 100.0) # Release ms

    # 5. ReaComp (Side Compressor)
    side_comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Pin Routing: Force ReaComp to process ONLY Channel 2 (Side)
    # We route Ch 2 into the plugin's Left Input, and output back to Ch 2
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 0, 0, 0, 2) # Input L <- Ch 2
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 0, 1, 0, 0) # Input R <- None
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 1, 0, 0, 2) # Output L -> Ch 2
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 1, 1, 0, 0) # Output R -> None
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 0, -18.0) # Threshold (sides usually quieter)
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 1, 2.5)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 3, 10.0)  # Attack ms
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 4, 50.0)  # Release ms

    # 6. Mid/Side Decoder (Translates M/S back to L/R)
    dec_idx = RPR.RPR_TrackFX_AddByName(track, "Mid/Side Decoder", False, -1)

    # 7. ReaComp (Stereo Bus Glue)
    glue_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 0, -8.0)  # Threshold
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 1, 1.5)   # Ratio (gentle)
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 3, 30.0)  # Attack (slow, lets punch through)
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 4, 200.0) # Release (smooth)

    # 8. ReaLimit (Final Brickwall Limiter)
    limit_idx = RPR.RPR_TrackFX_AddByName(track, "ReaLimit", False, -1)
    RPR.RPR_TrackFX_SetParam(track, limit_idx, 0, -0.5) # Threshold (pushing into limit)
    RPR.RPR_TrackFX_SetParam(track, limit_idx, 1, -0.7) # Ceiling (safe headroom for MP3 conversion)

    return f"Created mastering track '{track_name}' featuring Subtractive EQ, Peak Clipping, discrete M/S Compression, Bus Glue, and Brickwall Limiting."
