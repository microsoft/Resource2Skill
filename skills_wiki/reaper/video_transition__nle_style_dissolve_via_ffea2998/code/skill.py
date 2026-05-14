def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Video Edit",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create [Video Transition: NLE-Style Dissolve via Item Fades] in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused here, kept for signature consistency).
        scale: Scale type (unused here, kept for signature consistency).
        bars: Total duration context.
        velocity_base: Base MIDI velocity (unused).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created video transition layout.
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
    # Adds the native Video Processor and assigns the preset that links fades to opacity
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "Video Processor", False, -1)
    RPR.RPR_TrackFX_SetPreset(track, fx_idx, "Item fades affect video")

    # === Step 4: Create Overlapping Items for the Dissolve ===
    # Calculate musical timing for the video clips
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    
    # Clip A will last 2 bars. Clip B will last 2 bars.
    # They will crossfade over exactly 2 beats.
    clip_a_length = (sec_per_beat * beats_per_bar) * 2
    clip_b_length = (sec_per_beat * beats_per_bar) * 2
    crossfade_duration = sec_per_beat * 2 

    # --- Item 1 (Video Clip A) ---
    item1 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", clip_a_length)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_FADEOUTLEN", crossfade_duration)
    # 0 = linear fade, 1 = exponential, etc. Linear works best for video opacity.
    RPR.RPR_SetMediaItemInfo_Value(item1, "C_FADEOUTSHAPE", 0) 
    
    take1 = RPR.RPR_AddTakeToMediaItem(item1)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take1, "P_NAME", "[DROP VIDEO HERE] Clip A", True)

    # --- Item 2 (Video Clip B) ---
    # Position Clip B so it starts precisely as Clip A begins its fade-out
    clip_b_start = clip_a_length - crossfade_duration
    
    item2 = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_POSITION", clip_b_start)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", clip_b_length)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_FADEINLEN", crossfade_duration)
    RPR.RPR_SetMediaItemInfo_Value(item2, "C_FADEINSHAPE", 0)
    
    take2 = RPR.RPR_AddTakeToMediaItem(item2)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take2, "P_NAME", "[DROP VIDEO HERE] Clip B", True)

    return f"Created Video Track '{track_name}' with Video Processor. Generated a {crossfade_duration:.2f}s crossfade/dissolve between two placeholder items at {bpm} BPM."
