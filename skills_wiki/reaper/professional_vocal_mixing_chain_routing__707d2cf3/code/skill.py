def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lead Vocal",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Professional Vocal Mixing Chain & Reverb Bus in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the main vocal track.
        bpm: Tempo in BPM.
        key: Root note (unused for mixing template, but maintained for signature).
        scale: Scale type (unused for mixing template).
        bars: Length of the placeholder vocal region to generate.
        velocity_base: Base MIDI velocity (unused).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Reverb Bus Track ===
    # Best practice is to put the bus AFTER the current tracks or at the end
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    reverb_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(reverb_track, "P_NAME", "Vocal Reverb Bus", True)
    
    # Add ReaVerbate to the Bus
    RPR.RPR_TrackFX_AddByName(reverb_track, "ReaVerbate", False, -1)
    
    # === Step 3: Create Main Lead Vocal Track ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    vocal_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(vocal_track, "P_NAME", track_name, True)

    # Add EQ and Compressor
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaComp", False, -1)

    # === Step 4: Create Parallel Routing (Send) ===
    # Route Lead Vocal to Vocal Reverb Bus
    send_idx = RPR.RPR_CreateTrackSend(vocal_track, reverb_track)
    
    # Set send volume to a conservative starting level (approx -12dB or 0.25 in linear gain)
    # Param names: "D_VOL" is send volume
    RPR.RPR_SetTrackSendInfo_Value(vocal_track, 0, send_idx, "D_VOL", 0.25)

    # === Step 5: Create Placeholder Audio Item ===
    # Creates an empty item as a visual cue for where to drop the vocal comp/takes
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(vocal_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Add a take and name it to instruct the user
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", "[DROP VOCAL AUDIO HERE - AUTOMATE VOL]", True)

    return f"Created '{track_name}' and 'Vocal Reverb Bus' with EQ, Compression, and parallel routing."
