def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Video Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Dip to Black' Video Transition Automation in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused in video context).
        scale: Scale type (unused in video context).
        bars: Number of bars the video item lasts.
        velocity_base: Base MIDI velocity (unused in video context).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Video Processor FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)

    # === Step 4: Create Automation Envelope for Fades ===
    # Get or create the envelope for Parameter 0 (Primary Param/Opacity)
    env = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    # Set fade duration to half a bar (2 beats)
    fade_duration = (60.0 / bpm) * 2.0 

    # REAPER Envelope Point Shapes: 0=Linear, 1=Square, 2=Slow start/end, 3=Fast start, 4=Fast end, 5=Bezier
    # The tutorial specifically highlights the "Slow start/end" curve for organic transitions.
    
    # 1. Start at 0% (Black)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, 2, 0.0, False, True)
    # 2. Fade in to 100% (Visible)
    RPR.RPR_InsertEnvelopePoint(env, fade_duration, 1.0, 0, 0.0, False, True)
    
    # 3. Hold at 100% until the fade out begins
    RPR.RPR_InsertEnvelopePoint(env, total_length - fade_duration, 1.0, 2, 0.0, False, True)
    # 4. Fade out to 0% (Dip to Black)
    RPR.RPR_InsertEnvelopePoint(env, total_length, 0.0, 0, 0.0, False, True)

    # Sort points to ensure correct evaluation
    RPR.RPR_Envelope_SortPoints(env)

    # === Step 5: Add Placeholder Item ===
    # Add an empty item to visually represent the video clip duration in the timeline
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    RPR.RPR_GetSetMediaItemInfo_String(item, "P_NOTES", "Video/Image Placeholder", True)

    return f"Created '{track_name}' with slow start/end fade automation over {bars} bars at {bpm} BPM"
