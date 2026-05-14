def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Liquid DnB Drums",
    bpm: int = 174,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a classic Liquid Drum & Bass Groove in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created drum track.
        bpm: Tempo in BPM (defaults to 174 for DnB).
        key: Root note (unused for standard GM drums, kept for signature).
        scale: Scale type (unused for standard GM drums, kept for signature).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created element.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    # Attempt to set project tempo natively (fallback avoids API version issues)
    try:
        RPR.RPR_SetCurrentBPM(0, False, bpm)
    except:
        RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, bpm, 0, 0, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # GM Drum Mapping
    KICK = 36
    SNARE = 38
    HIHAT_CLOSED = 42
    TAMBOURINE = 54
    GHOST_SNARE = 37  # Side stick / Rimshot
    
    note_count = 0

    # Helper function to insert drum hits using exact project time to PPQ conversion
    def add_drum(beat_offset, pitch, velocity, duration_beats=0.25, time_shift_sec=0.0):
        nonlocal note_count
        pos_sec = bar_start_sec + (beat_offset * beat_length_sec) + time_shift_sec
        
        # Prevent negative absolute time if shifting early on the very first beat
        if pos_sec < 0: pos_sec = 0.0
            
        end_sec = pos_sec + (duration_beats * beat_length_sec)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        vel = max(1, min(127, int(velocity)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 9, pitch, vel, False)
        note_count += 1

    # === Generate the Groove ===
    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        
        # 1. Kicks
        add_drum(0.0, KICK, velocity_base + 10)  # Strong downbeat Kick (Beat 1)
        add_drum(1.5, KICK, velocity_base)       # Syncopated Kick (Beat 2.5 / 'and' of 2)
        
        # Add a rolling ghost kick right before beat 3 on alternating bars
        if bar % 2 == 1:
            add_drum(1.75, KICK, velocity_base - 30) # Ghost Kick (Beat 2.75)
            
        # 2. Snares
        # The tutorial specifically highlights pulling the snare ~10ms early to create a 'rushed' feel
        snare_rush_sec = -0.010 
        add_drum(1.0, SNARE, velocity_base + 10, time_shift_sec=snare_rush_sec) # Backbeat 1 (Beat 2)
        add_drum(3.0, SNARE, velocity_base + 10, time_shift_sec=snare_rush_sec) # Backbeat 2 (Beat 4)
        
        # Add an occasional ghost snare/rimshot right before beat 4 for momentum
        if bar % 4 == 3:
            add_drum(2.75, GHOST_SNARE, velocity_base - 40) # Beat 3.75
            
        # 3. Hi-Hats
        # Continuous 8th notes mimicking a drummer's pendulum hand motion (loud/soft/loud/soft)
        for i in range(8):
            hh_beat = i * 0.5
            hh_vel = velocity_base - 10 if i % 2 == 0 else velocity_base - 50
            add_drum(hh_beat, HIHAT_CLOSED, hh_vel)
            
        # 4. Tambourine / Percussion Top Loop
        # Fills out the high frequencies on the quarter note margins
        add_drum(0.0, TAMBOURINE, velocity_base - 20)
        add_drum(2.0, TAMBOURINE, velocity_base - 20)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add a subtle room reverb to glue the disparate drum elements together
    reverb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    if reverb_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, reverb_idx, 0, 0.15) # Wet Mix (low)
        RPR.RPR_TrackFX_SetParam(track, reverb_idx, 1, 0.85) # Dry Mix (high)
        RPR.RPR_TrackFX_SetParam(track, reverb_idx, 2, 0.60) # Room Size

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"
