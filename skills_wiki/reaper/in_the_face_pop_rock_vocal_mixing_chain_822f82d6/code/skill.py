def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lead Vocal - Mix Ready",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Lead Vocal mixing chain with Comp, EQ, Stereo Delay, and Reverb.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused, audio processing).
        scale: Scale type (unused, audio processing).
        bars: Length of dummy item.
        velocity_base: Base MIDI velocity (unused).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created
    """
    import reaper_python as RPR

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a dummy audio item to hold space for the vocal
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)

    # === Step 2: Build FX Chain (Order is Critical) ===
    
    # 1. ReaComp (Dynamics Control First)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    
    # 2. ReaEQ (Tone Shaping Second)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # 3. ReaDelay (Stereo Slapback Third)
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    
    # 4. ReaVerbate (Short Plate Reverb Fourth)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)

    # === Step 3: Configure Key FX Parameters ===
    
    # --- Configure ReaComp ---
    # Param 1: Ratio. 0.0 = 1:1, ~0.08 = 4:1 (normalized curve)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 1, 0.08)
    # Param 2: Attack. 0.0 = 0ms, 1.0 = 500ms. Set to ~2ms.
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 2, 2.0 / 500.0)
    # Param 3: Release. 0.0 = 0ms, 1.0 = 5000ms. Set to ~90ms.
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 3, 90.0 / 5000.0)
    # Param 9: Auto Makeup Gain (1.0 = On)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 9, 1.0)

    # --- Configure ReaDelay (Stereo Slapback) ---
    # Param 4: Length Time Tap 1. 0.0 = 0ms, 1.0 = 10000ms. Set to 150ms.
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 4, 150.0 / 10000.0)
    # Param 5: Length Musical Tap 1. Set to 0 to force time-based ms.
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 5, 0.0)
    # Param 8: Pan Tap 1. 0.0 = Left, 0.5 = Center, 1.0 = Right. Set to Left.
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 8, 0.0)
    # Param 0: Wet. Lower the delay mix so it sits behind the vocal.
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 0, 0.15)
    
    # --- Configure ReaVerbate (Plate Style) ---
    # Param 0: Wet. Push reverb back in the mix.
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.2)
    # Param 1: Dry. Keep original signal strong.
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 1.0)
    # Param 2: Room Size. Set to ~50% for a medium plate feel.
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 2, 0.5)

    # Select track to help user find it for manual Pre-FX Volume automation
    RPR.RPR_SetOnlyTrackSelected(track)

    return f"Created '{track_name}' with Vocal Mix Chain (Comp->EQ->Delay->Verb). Drop vocal audio here and automate 'Volume (Pre-FX)' for de-essing."
