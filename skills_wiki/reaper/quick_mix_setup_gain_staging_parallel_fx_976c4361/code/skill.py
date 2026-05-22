def create_pattern(
    project_name: str = "MixSetup",
    track_name: str = "Mix Template",
    bpm: int = 112,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    headroom_db: float = -10.0,
    **kwargs,
) -> str:
    """
    Create a 'Quick Mix Setup' in the current REAPER project.
    Lowers existing track volumes to create headroom, then creates standard
    parallel FX return busses and pre-routes sends from all audio tracks.

    Args:
        project_name: Project identifier (for logging).
        track_name: Unused here (track names are dictated by the FX busses).
        bpm: Tempo in BPM (crucial for delay syncing).
        key: Unused for mixing.
        scale: Unused for mixing.
        bars: Unused for mixing.
        headroom_db: Target volume for existing tracks to create headroom (default -10dB).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the routing and gain staging operations.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    # Important for 1/8 and 1/4 delays to sync to the grid properly
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Gain Stage Existing Tracks ===
    num_existing_tracks = RPR.RPR_CountTracks(0)
    
    # Calculate linear volume from dB ( REAPER API uses linear values for D_VOL )
    vol_linear = 10.0 ** (headroom_db / 20.0)

    audio_tracks = []
    for i in range(num_existing_tracks):
        track = RPR.RPR_GetTrack(0, i)
        audio_tracks.append(track)
        # Pull down faders to create mix headroom
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol_linear)

    # === Step 3: Create FX Return Busses ===
    return_configs = [
        {"name": "VocalVerb", "fx": "ReaVerbate"},
        {"name": "DrumVerb", "fx": "ReaVerbate"},
        {"name": "Echo 1/8 Delay", "fx": "ReaDelay"},
        {"name": "Echo 1/4 Delay", "fx": "ReaDelay"}
    ]

    return_tracks = []
    for config in return_configs:
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        ret_track = RPR.RPR_GetTrack(0, idx)
        
        # Name the track
        RPR.RPR_GetSetMediaTrackInfo_String(ret_track, "P_NAME", config["name"], True)
        
        # Add the effect plugin
        RPR.RPR_TrackFX_AddByName(ret_track, config["fx"], False, -1)
        
        return_tracks.append(ret_track)

    # === Step 4: Batch Create the Routing Matrix ===
    # Route every original audio track to every new FX return track
    for src in audio_tracks:
        for dest in return_tracks:
            # Create Send
            send_idx = RPR.RPR_CreateTrackSend(src, dest)
            
            # Set Send Volume to -inf (0.0 in linear amplitude)
            # This prevents double-summing until the user explicitly pushes the send up
            RPR.RPR_SetTrackSendInfo_Value(src, 0, send_idx, "D_VOL", 0.0)
            
            # Disable MIDI Send (-1 disables the source MIDI routing)
            RPR.RPR_SetTrackSendInfo_Value(src, 0, send_idx, "I_SRCMIDI", -1)
            
            # Ensure Post-Fader routing (Mode 0) so spatial FX follow volume automation
            RPR.RPR_SetTrackSendInfo_Value(src, 0, send_idx, "I_SENDMODE", 0)

    return f"Gain staged {num_existing_tracks} tracks to {headroom_db}dB and established {len(return_configs)} pre-routed parallel FX busses."
