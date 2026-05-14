def create_pattern(
    project_name: str = "Vocal Mix Setup",
    track_name: str = "Lead Vocal",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a professional Lead Vocal mixing chain, a Reverb Aux, and a Backing 
    Instrument track with sidechain ducking (frequency masking) in REAPER.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Scale definition for our mock audio generation
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    NOTE_MAP = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 60 # C4
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Helper function to build MIDI items ===
    def create_midi_item(target_track, is_vocal):
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item = RPR.RPR_AddMediaItemToTrack(target_track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Quarter notes per beat
        ppq = 960  
        if is_vocal:
            # Create a simple "vocal" melody line (staccato to hear delay/reverb)
            for b in range(bars * beats_per_bar):
                if b % 2 == 0:  # Only sing on strong beats to leave gaps for the sidechain test
                    start_pos = b * ppq
                    end_pos = start_pos + int(ppq * 0.8)
                    pitch = root_pitch + scale_intervals[(b // 2) % len(scale_intervals)]
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_pos, end_pos, 0, pitch, velocity_base, False)
        else:
            # Create a sustained "acoustic guitar" chord progression
            for b in range(bars):
                start_pos = b * beats_per_bar * ppq
                end_pos = start_pos + (beats_per_bar * ppq)
                chord_root = root_pitch - 12 + scale_intervals[b % len(scale_intervals)]
                for offset in [0, 4, 7]: # Simple triad
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_pos, end_pos, 0, chord_root + offset, 80, False)
        
        RPR.RPR_MIDI_Sort(take)
        return item

    # === Step 2: Create Tracks ===
    base_idx = RPR.RPR_CountTracks(0)
    
    # Track 1: Backing Track (Acoustic Guitar)
    RPR.RPR_InsertTrackAtIndex(base_idx, True)
    tr_acoustic = RPR.RPR_GetTrack(0, base_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_acoustic, "P_NAME", "Acoustic Backing", True)
    # Enable 4 channels for sidechaining
    RPR.RPR_SetMediaTrackInfo_Value(tr_acoustic, "I_NCHAN", 4)
    RPR.RPR_TrackFX_AddByName(tr_acoustic, "ReaSynth", False, -1)
    create_midi_item(tr_acoustic, False)

    # Track 2: Lead Vocal
    RPR.RPR_InsertTrackAtIndex(base_idx + 1, True)
    tr_vocal = RPR.RPR_GetTrack(0, base_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_vocal, "P_NAME", track_name, True)
    fx_synth = RPR.RPR_TrackFX_AddByName(tr_vocal, "ReaSynth", False, -1)
    create_midi_item(tr_vocal, True)

    # Track 3: Vocal Reverb Aux
    RPR.RPR_InsertTrackAtIndex(base_idx + 2, True)
    tr_verb = RPR.RPR_GetTrack(0, base_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_verb, "P_NAME", "Vocal Plate Reverb", True)

    # === Step 3: Vocal FX Chain (The Core Pattern) ===
    
    # A. Corrective & Additive EQ (ReaEQ)
    fx_eq = RPR.RPR_TrackFX_AddByName(tr_vocal, "ReaEQ", False, -1)
    # Band 1: High Pass at 90Hz
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_eq, 0, 90.0) # Freq
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_eq, 3, 4.0)  # Type (High Pass)
    # Band 4: High Shelf at 10kHz, +4dB
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_eq, 12, 10000.0) # Freq
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_eq, 13, 4.0)     # Gain
    
    # B. Leveling Compression (ReaComp mimicking LA-2A)
    fx_comp = RPR.RPR_TrackFX_AddByName(tr_vocal, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_comp, 0, -15.0) # Threshold
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_comp, 1, 3.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_comp, 2, 10.0)  # Attack (ms)
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_comp, 3, 250.0) # Release (ms)

    # C. Tape Saturation (JS Saturation)
    fx_sat = RPR.RPR_TrackFX_AddByName(tr_vocal, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_vocal, fx_sat, 0, 0.4) # Drive amount

    # D. Slapback Delay (ReaDelay)
    fx_delay = RPR.RPR_TrackFX_AddByName(tr_vocal, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_delay, 13, 0.0)  # Dry mix 0dB
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_delay, 14, -12.0) # Wet mix -12dB
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_delay, 4, 120.0) # Length (120ms slapback)
    RPR.RPR_TrackFX_SetParam(tr_vocal, fx_delay, 7, -120.0) # No feedback

    # === Step 4: Reverb Aux Setup ===
    fx_verb = RPR.RPR_TrackFX_AddByName(tr_verb, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_verb, fx_verb, 0, 1.0) # Wet
    RPR.RPR_TrackFX_SetParam(tr_verb, fx_verb, 1, 0.0) # Dry (kill dry on Aux)
    RPR.RPR_TrackFX_SetParam(tr_verb, fx_verb, 2, 0.8) # Room Size (Fat Plate style)
    RPR.RPR_TrackFX_SetParam(tr_verb, fx_verb, 3, 0.5) # Dampening

    # Route Vocal to Reverb Aux
    send_verb = RPR.RPR_CreateTrackSend(tr_vocal, tr_verb)
    RPR.RPR_SetTrackSendInfo_Value(tr_vocal, 0, send_verb, "D_VOL", 0.3) # Send level

    # === Step 5: Sidechain Carving (Vocal masking Acoustic Guitar) ===
    # Route Vocal to Acoustic Track on channels 3/4
    send_sc = RPR.RPR_CreateTrackSend(tr_vocal, tr_acoustic)
    RPR.RPR_SetTrackSendInfo_Value(tr_vocal, 0, send_sc, "I_DSTCHAN", 2) # 2 = Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(tr_vocal, 0, send_sc, "D_VOL", 1.0)

    # Add Sidechain Compressor to Acoustic Track
    fx_sc = RPR.RPR_TrackFX_AddByName(tr_acoustic, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_acoustic, fx_sc, 11, 1.0) # Detector input = Aux L+R (sidechain)
    RPR.RPR_TrackFX_SetParam(tr_acoustic, fx_sc, 0, -20.0) # Threshold (aggressive ducking)
    RPR.RPR_TrackFX_SetParam(tr_acoustic, fx_sc, 1, 4.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(tr_acoustic, fx_sc, 2, 2.0)   # Fast Attack
    RPR.RPR_TrackFX_SetParam(tr_acoustic, fx_sc, 3, 100.0) # Fast Release

    return f"Created full Vocal Mix Chain (EQ, Comp, Saturation, Slapback), Reverb Aux, and Sidechain Routing over {bars} bars at {bpm} BPM."
