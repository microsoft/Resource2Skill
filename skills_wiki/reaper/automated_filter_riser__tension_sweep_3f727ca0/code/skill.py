def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Riser Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Automated Filter Riser by generating a sustained chord and drawing 
    an automation envelope on a ReaEQ filter, replicating the automation concepts in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the riser will sweep across.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Normalize inputs
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Create MIDI Item for Drone ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Timebase conversions
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)
    
    # Generate a wide sustained chord (Root, Fifth, Octave, 10th)
    base_octave = 36 # C2
    chord_degrees = [0, 4, 7, 9] # 1st, 5th, 8ve, 3rd(up an octave)
    
    for degree in chord_degrees:
        # Wrap degree to scale length to allow extensions
        scale_idx = degree % len(scale_intervals)
        octave_shift = degree // len(scale_intervals)
        
        pitch = base_octave + root_val + scale_intervals[scale_idx] + (octave_shift * 12)
        pitch = max(0, min(127, pitch)) # Ensure valid MIDI pitch
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            start_ppq, end_ppq, 
            0, int(pitch), velocity_base, True
        )
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add FX Chain ===
    # Add Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a richer tone (Mix in some square wave)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.5) # Mix param
    
    # Add EQ for the filter sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Find the parameter index for a high frequency band in ReaEQ
    # Standard ReaEQ usually has Band 4 Freq at index 9, but let's be robust
    num_params = RPR.RPR_TrackFX_GetNumParams(track, eq_idx)
    target_param_idx = 0 
    
    for i in range(num_params):
        _, _, _, name, _ = RPR.RPR_TrackFX_GetParamName(track, eq_idx, i, "", 256)
        # Look for the last frequency band (usually High Shelf or Low Pass)
        if "Freq" in name and ("4" in name or "High" in name):
            target_param_idx = i
            break

    # Setup the EQ Band as a Low Pass or pull down the high shelf gain to muffle it
    # Gain for the found band is usually param_idx + 1
    gain_idx = target_param_idx + 1
    if gain_idx < num_params:
        RPR.RPR_TrackFX_SetParam(track, eq_idx, gain_idx, -24.0) # Cut the highs heavily
    
    # === Step 5: Automate the Filter (The Core Tutorial Skill) ===
    # create=True instantiates the envelope
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, target_param_idx, True)
    
    if env:
        # Normalized values (0.0 to 1.0)
        start_val = 0.1 # Very low cutoff frequency
        end_val = 0.9   # High cutoff frequency (fully open)
        
        # Insert point at start (Time 0)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, start_val, 0, 0.0, False, True)
        
        # Insert point at end (Sweep up)
        # Shape 2 is "Slow Start/End" which creates a nice natural sweeping curve
        RPR.RPR_InsertEnvelopePoint(env, item_length_sec, end_val, 2, 0.0, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' Filter Riser over {bars} bars at {bpm} BPM with FX Automation."
