def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lead Synth",
    bpm: int = 120,
    key: str = "E",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Lead Synth track and a Dynamic Ducking Delay FX bus using sidechain compression.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "pentatonic_minor": [0, 3, 5, 7, 10]
    }
    
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    root_pitch = NOTE_MAP.get(key, 4) + 60 # Octave 4

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 1: Create Source Track (Lead) ===
    idx_lead = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_lead, True)
    tr_lead = RPR.RPR_GetTrack(0, idx_lead)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_lead, "P_NAME", track_name, True)
    
    # Add an instrument so we have a sound
    RPR.RPR_TrackFX_AddByName(tr_lead, "ReaSynth", False, -1)

    # === Step 2: Create MIDI Data (Phrases with Gaps) ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(tr_lead)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Generate an active phrase in Bar 1, REST in Bar 2, Phrase in Bar 3, REST in Bar 4
    for b in range(bars):
        if b % 2 == 1:
            continue # Leave odd bars (2 and 4) completely empty for the delay to swell
            
        bar_start = b * bar_length_sec
        # Write a syncopated 1/8 note riff
        for i, step in enumerate([0, 1.5, 2.5, 3]): 
            q_note_len = 60.0 / bpm
            start_time = bar_start + (step * q_note_len)
            end_time = start_time + (q_note_len * 0.5) # staccato notes
            
            note_idx = i % len(scale_intervals)
            pitch = root_pitch + scale_intervals[note_idx]
            
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time), 
                                    1, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Create Dynamic Delay FX Bus ===
    idx_fx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_fx, True)
    tr_fx = RPR.RPR_GetTrack(0, idx_fx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_fx, "P_NAME", "Dynamic Delay Bus", True)
    
    # Set FX track to 4 channels to accommodate sidechain input
    RPR.RPR_SetMediaTrackInfo_Value(tr_fx, "I_NCHAN", 4)

    # === Step 4: Routing & Sidechain Setup ===
    # Send 1: Audio to Delay (Lead 1/2 -> FX 1/2)
    send_audio = RPR.RPR_CreateTrackSend(tr_lead, tr_fx)
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_audio, "I_SRCCHAN", 0) # 0 = ch 1/2
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_audio, "I_DSTCHAN", 0) # 0 = ch 1/2
    
    # Send 2: Sidechain Trigger (Lead 1/2 -> FX 3/4)
    send_sc = RPR.RPR_CreateTrackSend(tr_lead, tr_fx)
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_sc, "I_SRCCHAN", 0) # 0 = ch 1/2
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_sc, "I_DSTCHAN", 2) # 2 = ch 3/4
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_sc, "D_VOL", 1.0) # Ensure trigger is strong

    # === Step 5: Add and Configure FX ===
    # 1. Delay
    fx_delay = RPR.RPR_TrackFX_AddByName(tr_fx, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_delay, 0, -120.0) # Dry = -inf (100% wet bus)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_delay, 1, 0.0)    # Wet = 0dB
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_delay, 13, 1.0)   # Length 1 Musical = 1 quarter note
    
    # 2. Compressor (Ducking)
    fx_comp = RPR.RPR_TrackFX_AddByName(tr_fx, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 0, -25.0) # Threshold (clamp down hard)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 1, 8.0)   # Ratio 8:1
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 2, 2.0)   # Attack 2ms (fast duck)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 3, 200.0) # Release 200ms (musical swell)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 15, 1.0)  # Detector Input: 1.0 = Aux L+R (Ch 3/4)
    
    return f"Created '{track_name}' and 'Dynamic Delay Bus' with 4-channel sidechain routing over {bars} bars at {bpm} BPM."
