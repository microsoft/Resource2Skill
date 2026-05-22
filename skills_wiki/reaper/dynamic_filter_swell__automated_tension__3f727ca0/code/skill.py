def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an automated filter swell using ReaSynth and ReaEQ.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars the sweep will last.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the generated track and automation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define chord extensions based on scale
    if scale.lower() == "minor" or scale.lower() == "aeolian":
        chord_intervals = [0, 3, 7, 10]  # Minor 7th
    elif scale.lower() == "major" or scale.lower() == "ionian":
        chord_intervals = [0, 4, 7, 11]  # Major 7th
    else:
        chord_intervals = [0, 7, 12, 14] # Sus2 / 9th (Neutral/Ambient)

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
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 48 # Base octave C3
    
    # Insert the sustained chord
    for interval in chord_intervals:
        pitch = root_pitch + interval
        # Ensure pitch is in valid MIDI range
        if 0 <= pitch <= 127:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments & Effects ===
    # 1. ReaSynth (Generate harmonically rich raw waves)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.6) # Add Square wave
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.6) # Add Sawtooth wave

    # 2. ReaEQ (Used for the filter sweep)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # ReaEQ Parameter indices for Band 4 (High Shelf)
    # Param 9: Freq, Param 10: Gain
    
    # Turn the high shelf into a low-pass filter by dropping its gain to the minimum (-120dB)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0)

    # === Step 5: Automate Filter Sweep ===
    # Get/Create the automation envelope for Band 4 Frequency (Param 9)
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    
    # Shape 2 = "Slow start/end" (an S-Curve for smoother musical sweeps)
    shape_s_curve = 2 
    
    # Insert start point (Muffled/Dark - low normalized frequency value)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.15, shape_s_curve, 0.0, False, True)
    
    # Insert end point (Open/Bright - high normalized frequency value)
    RPR.RPR_InsertEnvelopePoint(env, item_length, 0.95, shape_s_curve, 0.0, False, True)
    
    # Apply and sort the automation points
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with automated ReaEQ filter swell over {bars} bars at {bpm} BPM in {key} {scale}."
