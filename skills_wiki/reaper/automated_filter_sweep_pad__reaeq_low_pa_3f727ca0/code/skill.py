def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with an automated ReaEQ low-pass filter sweep.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the sweep and chord will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # --- Music Theory & Pitch Mapping ---
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

    # Set project tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Resolve scale and root
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generate a root position triad (1st, 3rd, and 5th scale degrees)
    octave_base = 48 # Octave 3/4
    chord_pitches = [
        octave_base + root_val + scale_intervals[0], # Root
        octave_base + root_val + scale_intervals[2 % len(scale_intervals)] + (12 if 2 >= len(scale_intervals) else 0), # 3rd
        octave_base + root_val + scale_intervals[4 % len(scale_intervals)] + (12 if 4 >= len(scale_intervals) else 0)  # 5th
    ]

    # --- 1. Track Setup ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- 2. MIDI Item Setup ---
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Convert time to PPQ for MIDI note insertion
    start_qn = RPR.RPR_MIDI_GetProjQNFromTime(0, 0.0)
    end_qn = RPR.RPR_MIDI_GetProjQNFromTime(0, item_length)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # Insert sustained chord
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    RPR.RPR_MIDI_Sort(take)

    # --- 3. FX & Sound Design ---
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set synth to a mix of Saw and Square for rich harmonics to filter
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.8) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Square mix

    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Param 1 is Band 1 Gain. We drop the gain heavily to treat the shelf as a low-pass
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 1, 0.0) 

    # --- 4. Automation Mapping ---
    # Param 0 in ReaEQ is Band 1 Frequency. We fetch/create its automation envelope
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)

    # Insert automation points: Sweep from dark (0.15) to bright (0.85) over the length of the item
    # RPR_InsertEnvelopePoint(env, time, value, shape(0=linear), tension, selected, noSort)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.15, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length, 0.85, 0, 0.0, False, True)
    
    # Sort envelope points to apply changes
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with a {bars}-bar automated filter sweep on a {key} {scale} triad at {bpm} BPM."
