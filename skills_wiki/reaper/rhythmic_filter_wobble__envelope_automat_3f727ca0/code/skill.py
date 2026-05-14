def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Wobble Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a rhythmic automated filter wobble in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Generate triad chord
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    octave_base = 48 # Octave 3 for a thick mid-low pad
    
    chord_pitches = [
        octave_base + root_val + scale_intervals[0], # Root
        octave_base + root_val + scale_intervals[2], # Third
        octave_base + root_val + scale_intervals[4]  # Fifth
    ]
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    # === Step 4: Add Instruments and FX ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth Sawtooth mix up to make the filter sweep very obvious (Param 3 = saw mix)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 1.0)
    
    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # === Step 5: Draw Envelope Automation ===
    # Get envelope for ReaEQ Band 1 Frequency (Param 0)
    # 'True' as the last parameter creates and arms the envelope if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)
    
    # Iterate through every 1/4 note (beat) to draw the rhythmic LFO shape
    total_beats = bars * beats_per_bar
    for beat in range(total_beats):
        time_start = beat * beat_length_sec
        time_mid = time_start + (beat_length_sec / 2.0)
        time_end = time_start + beat_length_sec
        
        # Insert Envelope Points (Slow Start/End shape = 2 for smooth "sine" curves)
        # Value scale: 0.0 to 1.0 (0.0 = low freq cut, 0.8 = open freq)
        RPR.RPR_InsertEnvelopePoint(env, time_start, 0.1, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, time_mid, 0.8, 2, 0.0, False, True)
        
        # Ensure the last beat ends closed
        if beat == total_beats - 1:
            RPR.RPR_InsertEnvelopePoint(env, time_end, 0.1, 2, 0.0, False, True)

    # Sort the envelope points
    RPR.RPR_Envelope_Sort(env)

    return f"Created '{track_name}' with automated rhythmic filter wobble over {bars} bars at {bpm} BPM."
