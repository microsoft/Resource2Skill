def create_pattern(
    project_name: str = "AndyWallaceBass",
    track_name: str = "Wallace Push-Pull Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create an Andy Wallace style extreme low-end push-pull bass chain.
    Generates a driving 8th-note bassline and applies the massive sub-boost -> HPF -> Comp chain.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Create MIDI Item & Driving 8th Note Bassline ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate Root Note (Drop down to Octave 1 for Bass, e.g., E1 = MIDI 28)
    root_pitch = NOTE_MAP.get(key.upper(), 4) + 24 
    
    # Insert 8th notes
    total_eighth_notes = bars * 8
    eighth_note_duration_sec = (60.0 / bpm) / 2.0
    
    for i in range(total_eighth_notes):
        start_time = i * eighth_note_duration_sec
        end_time = start_time + (eighth_note_duration_sec * 0.85) # Slight staccato for compressor attack
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Add slight velocity variation to test the compressor
        vel = velocity_base if i % 2 == 0 else velocity_base - 15
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, vel, False)
        
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add FX Chain ===
    
    # 1. Sound Source: ReaSynth (Approximating a DI Bass)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, 1)
    # Set ReaSynth: Mix of Saw and Sine for fundamental + harmonics
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 0, 0.0) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 1, 0.0) # Tuning
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.5) # Saw mix
    
    # 2. The "Neve" Pre-EQ: Extreme Low Shelf Boost
    fx_eq_boost = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, 1)
    # Band 1 is Low Shelf by default in ReaEQ
    # Freq ~ 35Hz (Normalized approx 0.05 on the 20-24k log scale)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq_boost, 0, 0.05) 
    # Gain +15dB (Normalized: 0.5 is 0dB, +15dB is approx 0.8125)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq_boost, 1, 0.8125) 
    
    # 3. The "SSL" Channel EQ: High Pass + Low Mid Cut
    fx_eq_cut = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, 1)
    # Convert Band 1 to High Pass (Type 5 in ReaEQ) and set to ~40Hz
    # Since ReaScript can't easily change ReaEQ band types directly via normalized params,
    # we simulate the HPF by severely cutting a low shelf at 40Hz
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq_cut, 0, 0.06) # ~40Hz
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq_cut, 1, 0.0)  # -24dB cut (HPF simulation)
    # Band 2 (Bell): Cut at ~240Hz (Normalized approx 0.25), -1.6dB (Normalized approx 0.46)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq_cut, 3, 0.25)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq_cut, 4, 0.46)
    
    # 4. The "SSL" Channel Compressor
    fx_comp = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, 1)
    # Threshold: Set low enough to catch the massive EQ boost (approx -20dB -> norm 0.55)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 0, 0.55)
    # Ratio: 4:1 (Normalized approx 0.15)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 1, 0.15)
    # Attack: Fast (~3ms -> norm 0.03)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 3, 0.03)
    # Release: Fast (~100ms -> norm 0.1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 4, 0.1)

    return f"Created '{track_name}' with driving bass, +15dB 35Hz Neve boost, 40Hz HPF, and SSL-style 4:1 compression."
