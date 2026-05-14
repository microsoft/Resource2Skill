def create_pattern(
    project_name: str = "Retro",
    track_name: str = "70s Disco Drums",
    bpm: int = 115,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 70s Vintage Disco Drum Pattern and Analog Mix Bus in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created drum track.
        bpm: Tempo in BPM.
        key: Root note (unused for standard GM drums).
        scale: Scale type (unused for standard GM drums).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Mix Bus Track (Parent) ===
    bus_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(bus_idx, True)
    bus_track = RPR.RPR_GetTrack(0, bus_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", f"{project_name} Mix Bus", True)
    # Set as folder parent
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1)

    # === Step 3: Create Drum Track (Child) ===
    drum_idx = bus_idx + 1
    RPR.RPR_InsertTrackAtIndex(drum_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", track_name, True)
    # Set as last folder child
    RPR.RPR_SetMediaTrackInfo_Value(drum_track, "I_FOLDERDEPTH", -1)

    # === Step 4: Build Analog Mix Bus FX Chain ===
    # 1. ReaComp (Neve 33609 style mix glue: Low ratio, slow auto-release style)
    RPR.RPR_TrackFX_AddByName(bus_track, "ReaComp", False, -1)
    
    # 2. ReaEQ (Avalon Mastering EQ style: low bump, high shelf sweetening)
    RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    
    # 3. JS: Saturation (Emulating printing to analog tape)
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: Saturation", False, -1)

    # === Step 5: Build Drum Track FX Chain ===
    # Add Sampler placeholders for Kick, Snare, Hat
    rs5k_kick = RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_track, rs5k_kick, 3, 36) # Note start
    RPR.RPR_TrackFX_SetParam(drum_track, rs5k_kick, 4, 36) # Note end

    rs5k_snare = RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_track, rs5k_snare, 3, 38)
    RPR.RPR_TrackFX_SetParam(drum_track, rs5k_snare, 4, 38)

    rs5k_hat = RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_track, rs5k_hat, 3, 42)
    RPR.RPR_TrackFX_SetParam(drum_track, rs5k_hat, 4, 42)

    # Add API-style EQ for the drum channel
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaEQ", False, -1)

    # === Step 6: Create MIDI Item & Insert Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    qn_per_bar = 4
    note_count = 0

    # Generate Standard 70s Disco Groove
    for b in range(bars):
        bar_start_qn = b * qn_per_bar
        
        for beat in range(4):
            # 1. Kick (Four-on-the-floor)
            k_start_qn = bar_start_qn + beat
            k_end_qn = k_start_qn + 0.25
            
            k_start_time = RPR.RPR_TimeMap2_QNToTime(0, k_start_qn)
            k_end_time = RPR.RPR_TimeMap2_QNToTime(0, k_end_qn)
            
            k_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, k_start_time)
            k_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, k_end_time)
            
            # Accentuate the downbeat slightly
            vel = velocity_base if beat == 0 else int(velocity_base * 0.9)
            RPR.RPR_MIDI_InsertNote(take, False, False, k_start_ppq, k_end_ppq, 0, 36, vel, True)
            note_count += 1
            
            # 2. Snare (Beats 2 and 4, which is index 1 and 3)
            if beat == 1 or beat == 3:
                RPR.RPR_MIDI_InsertNote(take, False, False, k_start_ppq, k_end_ppq, 0, 38, velocity_base, True)
                note_count += 1
            
            # 3. Off-beat Hi-Hat
            h_start_qn = k_start_qn + 0.5
            h_end_qn = h_start_qn + 0.25
            
            h_start_time = RPR.RPR_TimeMap2_QNToTime(0, h_start_qn)
            h_end_time = RPR.RPR_TimeMap2_QNToTime(0, h_end_qn)
            
            h_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, h_start_time)
            h_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, h_end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, h_start_ppq, h_end_ppq, 0, 42, int(velocity_base * 0.85), True)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created Mix Bus folder and '{track_name}' with {note_count} disco drum notes over {bars} bars at {bpm} BPM."
