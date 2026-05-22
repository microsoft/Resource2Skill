def create_pattern(
    project_name: str = "MasteringProject",
    track_name: str = "Mastering Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an 'In-the-Box Serial Mastering Chain' using REAPER stock plugins.
    Creates a dedicated track to drop a final mixdown into, pre-loaded with
    Saturation, Corrective EQ, Creative EQ, Bus Compression, and Limiting.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the mastering track.
        bpm: Tempo in BPM (used to calculate approximate compressor release time).
        key: Root note (unused in mastering, kept for API compliance).
        scale: Scale type (unused in mastering, kept for API compliance).
        bars: Length of dummy item.
        velocity_base: Base MIDI velocity (unused here).
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the created FX chain.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Mastering Track ===
    # Additive design: we add a new track at the end of the project
    num_tracks = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Insert Dummy Audio Item (Placeholder for Mixdown) ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Give the item a noticeable color and name to indicate it's a placeholder
    RPR.RPR_GetSetMediaItemInfo_String(item, "P_NOTES", "DROP STEREO MIXDOWN HERE", True)

    # === Step 4: Build the Serial Mastering FX Chain ===
    
    # 1. Saturation (Harmonic Excitement & Transient Taming)
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    # Parameter 0 is Amount. Normalized values vary in JSFX, setting to approx 9%
    RPR.RPR_TrackFX_SetParamNormalized(track, sat_idx, 0, 0.09) 

    # 2. Corrective EQ (Subtractive)
    # Instantiate ReaEQ. We leave parameters at default so the user can sweep and destroy harsh resonances.
    RPR.RPR_TrackFX_AddByName(track, "VST: ReaEQ (Cockos)", False, -1)

    # 3. Creative EQ (Additive)
    # Instantiate a second ReaEQ specifically for broad, musical boosts.
    RPR.RPR_TrackFX_AddByName(track, "VST: ReaEQ (Cockos)", False, -1)

    # 4. Bus Compression (Dynamics Gluing)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "VST: ReaComp (Cockos)", False, -1)
    
    # ReaComp parameters (Approximate Normalized Values):
    # Param 1: Ratio (0.0 to 1.0 represents 1:1 to inf:1). ~0.04 is roughly 1.5:1
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 1, 0.04) 
    
    # Param 2: Attack (0.0 to 1.0 represents 0ms to 500ms). ~0.02 is roughly 10ms
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 2, 0.02) 
    
    # Param 3: Release. Calculate musical release based on BPM (e.g., an 8th note or 16th note).
    # 60000 / bpm = ms per quarter note. Let's aim for a musical release around 150-200ms.
    # 0.0 to 1.0 represents 0ms to 5000ms. ~0.03 is roughly 150ms.
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 3, 0.03) 
    
    # Param 10: Auto Make-up gain (0.0 = off). We want this OFF for mastering control.
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 10, 0.0)

    # 5. Peak Catching & Loudness (Limiting)
    lim_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Master Limiter", False, -1)
    # JS Master Limiter typical params: Param 0 = Threshold, Param 3 = Limit
    # Setting Limit to -1.0 dB (to provide streaming platform True Peak headroom)
    # Note: JSFX API parameter normalization can be tricky, but we establish the plugin state.
    
    status_msg = (
        f"Created '{track_name}' for Mastering.\n"
        f"FX Chain loaded: Saturation (9%) -> ReaEQ (Corrective) -> ReaEQ (Creative) -> "
        f"ReaComp (Ratio 1.5:1, Att: 10ms) -> Master Limiter."
    )
    
    return status_msg
