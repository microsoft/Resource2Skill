def create_pattern(
    project_name: str = "ParallelReverbDemo",
    source_track_name: str = "Dry Lead",
    track_name: str = "Reverb Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Parallel Reverb Send setup in the current REAPER project.
    If the source track doesn't exist, it creates a dummy staccato synth track 
    so the reverb tail can be clearly heard.

    Args:
        project_name: Project identifier (for logging).
        source_track_name: The track to send TO the reverb bus.
        track_name: Name for the created Reverb track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, pentatonic_minor, etc.).
        bars: Number of bars to generate for the test audio.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., send_volume, room_size).

    Returns:
        Status string describing the routing created.
    """
    import reaper_python as RPR

    # Optional kwargs for mixing
    send_vol_linear = kwargs.get("send_volume", 0.5) # 0.5 is approx -6dB
    room_size = kwargs.get("room_size", 0.8) # 0.0 to 1.0

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 1: Find or Create Source Track ===
    num_tracks = RPR.RPR_CountTracks(0)
    source_track = None
    
    # Check if target source track already exists
    for i in range(num_tracks):
        t = RPR.RPR_GetTrack(0, i)
        _, _, name, _ = RPR.RPR_GetSetMediaTrackInfo_String(t, "P_NAME", "", False)
        if name == source_track_name:
            source_track = t
            break

    # If it doesn't exist, create it and add staccato MIDI so we can hear the reverb
    if not source_track:
        RPR.RPR_InsertTrackAtIndex(num_tracks, True)
        source_track = RPR.RPR_GetTrack(0, num_tracks)
        RPR.RPR_GetSetMediaTrackInfo_String(source_track, "P_NAME", source_track_name, True)
        RPR.RPR_TrackFX_AddByName(source_track, "ReaSynth", False, -1)
        
        # Make ReaSynth plucky
        fx_idx = RPR.RPR_TrackFX_AddByName(source_track, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_SetParamNormalized(source_track, fx_idx, 3, 0.0) # Sustain 0
        RPR.RPR_TrackFX_SetParamNormalized(source_track, fx_idx, 4, 0.2) # Release short

        # Create MIDI Item
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_length_sec * bars
        
        item = RPR.RPR_AddMediaItemToTrack(source_track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        root_midi = 60 + NOTE_MAP.get(key, 0)
        scale_intervals = SCALES.get(scale, SCALES["minor"])
        
        # Insert a staccato note every quarter note
        ticks_per_quarter = 960
        for b in range(bars * beats_per_bar):
            start_pos = b * ticks_per_quarter
            end_pos = start_pos + int(ticks_per_quarter * 0.25) # Very short note
            pitch = root_midi + scale_intervals[b % len(scale_intervals)]
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_pos, end_pos, 0, pitch, velocity_base, False)
        
        RPR.RPR_MIDI_Sort(take)
        num_tracks += 1 # Update track count since we added one

    # === Step 2: Create Reverb Send Track ===
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    reverb_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(reverb_track, "P_NAME", track_name, True)

    # === Step 3: Add Reverb & Set to 100% Wet ===
    rev_fx_idx = RPR.RPR_TrackFX_AddByName(reverb_track, "ReaVerbate", False, -1)
    
    # ReaVerbate Param 0 is Wet, Param 1 is Dry, Param 2 is Room Size
    # 1.0 Normalized Wet is roughly +6dB. 0.5 is roughly 0dB.
    RPR.RPR_TrackFX_SetParamNormalized(reverb_track, rev_fx_idx, 0, 0.5) # Wet to 0dB
    RPR.RPR_TrackFX_SetParamNormalized(reverb_track, rev_fx_idx, 1, 0.0) # Dry to -inf (100% Wet!)
    RPR.RPR_TrackFX_SetParamNormalized(reverb_track, rev_fx_idx, 2, room_size) # Room size
    RPR.RPR_TrackFX_SetParamNormalized(reverb_track, rev_fx_idx, 4, 0.7) # Highpass to prevent mud

    # === Step 4: Route Source Track to Reverb Track ===
    # 0 = Post-Fader send
    send_idx = RPR.RPR_CreateTrackSend(source_track, reverb_track)
    RPR.RPR_SetTrackSendInfo_Value(source_track, 0, send_idx, "D_VOL", send_vol_linear)

    return f"Created Parallel Reverb: '{source_track_name}' now sends to '{track_name}' (100% Wet) at {send_vol_linear} volume."
