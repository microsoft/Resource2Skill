def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a sustained pad with dynamic Mix Automation (Filter Sweep & Delay Throw)
    in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track and automation.
    """
    import reaper_python as RPR

    # === Music Theory & Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Let's voice a nice rich 9th chord to demonstrate the filter sweep
    octave_base = 48 # C3
    chord_degrees = [0, 2, 4, 6] # 1st, 3rd, 5th, 7th in scale (gives 7th chord)
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Insert a single sustained chord for the full duration
    # PQN (Pulses Per Quarter Note) standard is 960
    for degree in chord_degrees:
        # Wrap around octave if degree exceeds scale length
        octave_offset = (degree // len(scale_intervals)) * 12
        note_val = root_val + scale_intervals[degree % len(scale_intervals)] + octave_base + octave_offset
        
        RPR.RPR_MIDI_InsertNote(
            take, 
            False, 
            False, 
            0, # Start PPQ
            int(item_length * (bpm / 60.0) * 960), # End PPQ
            0, # Channel
            note_val, 
            velocity_base, 
            False
        )
    
    # === Step 4: Add FX Chain ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    
    # Make ReaSynth sound more like a pad (longer release, sawtooth)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 1.0) # Sawtooth
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 1.0) # Release
    
    # === Step 5: Automate ReaEQ (Filter Sweep) ===
    # ReaEQ Band 4 Frequency is typically parameter index 9.
    # To be safe, we iterate to find the parameter with "Freq" for Band 4
    num_eq_params = RPR.RPR_TrackFX_GetNumParams(track, eq_idx)
    freq_param_idx = 9 # fallback
    for i in range(num_eq_params):
        _, _, _, name, _ = RPR.RPR_TrackFX_GetParamName(track, eq_idx, i, "", 256)
        if "Freq-Band 4" in name or ("Freq" in name and "4" in name):
            freq_param_idx = i
            break
            
    # Get/Create the envelope for this parameter
    eq_env = RPR.RPR_GetFXEnvelope(track, eq_idx, freq_param_idx, True)
    if eq_env:
        # Create a slow, rising filter sweep over the course of the item
        # Normalized values: 0.0 is low freq, 1.0 is high freq
        RPR.RPR_InsertEnvelopePoint(eq_env, 0.0, 0.2, 2, 0, False, True) # Shape 2 = Slow start/end
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length * 0.8, 0.9, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_Sort(eq_env)
        
    # === Step 6: Automate ReaDelay (Delay Throw) ===
    # We want to automate the 'Wet' parameter. 
    num_dly_params = RPR.RPR_TrackFX_GetNumParams(track, delay_idx)
    wet_param_idx = -1
    for i in range(num_dly_params):
        _, _, _, name, _ = RPR.RPR_TrackFX_GetParamName(track, delay_idx, i, "", 256)
        if "Wet" in name:
            wet_param_idx = i
            break
            
    if wet_param_idx != -1:
        dly_env = RPR.RPR_GetFXEnvelope(track, delay_idx, wet_param_idx, True)
        if dly_env:
            # Keep dry mostly, throw on the 4th beat of alternating bars
            beat_sec = 60.0 / bpm
            
            # Start totally dry
            RPR.RPR_InsertEnvelopePoint(dly_env, 0.0, 0.0, 0, 0, False, True)
            
            for b in range(bars):
                # Throw on beat 4 (index 3) of every 2nd bar
                if b % 2 != 0:
                    throw_start = (b * bar_length_sec) + (2.5 * beat_sec)
                    throw_peak = (b * bar_length_sec) + (3.0 * beat_sec)
                    throw_end = (b * bar_length_sec) + (3.5 * beat_sec)
                    
                    # Ramp up
                    RPR.RPR_InsertEnvelopePoint(dly_env, throw_start, 0.0, 0, 0, False, True)
                    # Peak Wet
                    RPR.RPR_InsertEnvelopePoint(dly_env, throw_peak, 0.8, 0, 0, False, True)
                    # Ramp down
                    RPR.RPR_InsertEnvelopePoint(dly_env, throw_end, 0.0, 0, 0, False, True)
                    
            RPR.RPR_Envelope_Sort(dly_env)
            
    # Set track to Read automation mode (1)
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_AUTOMODE", 1)

    return f"Created '{track_name}' with {bars} bars at {bpm} BPM, featuring an automated filter sweep and rhythmic delay throws."
