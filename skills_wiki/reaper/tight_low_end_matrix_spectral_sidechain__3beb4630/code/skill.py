def create_pattern(
    project_name: str = "Tight_Low_End",
    track_name: str = "Bass_Sidechain_Matrix",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Kick and Bass sidechain matrix demonstrating low-end spectral separation.
    Uses ReaSynth, ReaEQ, ReaComp, and ReaXcomp to recreate the tutorial's workflow.
    """
    import reaper_python as RPR
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Octaves
    kick_note = root_val + 36  # C1 - standard kick punch area
    bass_note = root_val + 24  # C0 - deep sub bass

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    # === 1. Create Kick Track ===
    idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx, True)
    kick_track = RPR.RPR_GetTrack(0, idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Kick", True)
    
    # Kick Synth Setup
    RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a kick-like punch (fast decay)
    RPR.RPR_TrackFX_SetParam(kick_track, 0, 3, 0.1)  # Release fast
    
    # Kick MIDI
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # 4-on-the-floor kick pattern
    ppq = 960 
    for bar in range(bars):
        for beat in range(4):
            start_pos = (bar * beats_per_bar + beat) * (60.0 / bpm)
            end_pos = start_pos + 0.1 # short punch
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, 
                                    start_pos, end_pos, 
                                    0, kick_note, velocity_base, False)
            
    # === 2. Create Bass Track ===
    idx += 1
    RPR.RPR_InsertTrackAtIndex(idx, True)
    bass_track = RPR.RPR_GetTrack(0, idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", "Bass", True)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "I_NCHAN", 4) # Enable channels 3/4 for sidechain
    
    # Bass Synth Setup
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a heavy bass (Sawtooth)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 1.0) # Mix Saw
    
    # Bass MIDI
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # Sustained bass notes filling the bar (forces masking to demonstrate sidechain utility)
    for bar in range(bars):
        start_pos = bar * bar_length_sec
        end_pos = start_pos + bar_length_sec
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, 
                                start_pos, end_pos, 
                                0, bass_note, int(velocity_base * 0.8), False)
                                
    # === 3. Sidechain Routing (Kick -> Bass 3/4) ===
    send_idx = RPR.RPR_CreateTrackSend(kick_track, bass_track)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_SRCCHAN", 0) # Source 1/2
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2) # Dest 3/4
    
    # === 4. Spectral EQ & Ducking on Bass ===
    # Add ReaEQ (Low shelf at 300Hz) to represent the frequency domain we care about
    eq_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    
    # Add ReaComp for Sidechain Ducking
    comp_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, comp_idx, 0, 0.4)   # Threshold
    RPR.RPR_TrackFX_SetParam(bass_track, comp_idx, 1, 0.3)   # Ratio ~ 4:1
    RPR.RPR_TrackFX_SetParam(bass_track, comp_idx, 2, 0.003) # Fast Attack (3ms)
    RPR.RPR_TrackFX_SetParam(bass_track, comp_idx, 3, 0.050) # Fast/Medium Release (50ms)
    RPR.RPR_TrackFX_SetParam(bass_track, comp_idx, 8, 0.12)  # Detector: Aux L+R (Channels 3/4)
    
    # === 5. Multiband Glue on Master Bus ===
    master_track = RPR.RPR_GetMasterTrack(0)
    xcomp_idx = RPR.RPR_TrackFX_AddByName(master_track, "ReaXcomp", False, -1)
    
    return f"Created Kick and Bass matrix over {bars} bars at {bpm} BPM with proper Sidechain Audio Routing and EQ/Comp setup."
