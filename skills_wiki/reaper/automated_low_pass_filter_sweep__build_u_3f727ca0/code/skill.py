def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Low-Pass Filter Sweep (Build-Up Pad) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the sweep should last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Calculate absolute root note (Octave 3 = 48)
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    base_midi_note = 48 + root_val
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # Determine 1st, 3rd, 5th, and 7th scale degrees for a rich pad chord
    chord_degrees = [0, 2, 4, 6] 
    chord_notes = []
    for degree in chord_degrees:
        # Wrap around octave if degree exceeds scale length
        octave_shift = degree // len(scale_intervals)
        interval_idx = degree % len(scale_intervals)
        note = base_midi_note + scale_intervals[interval_idx] + (octave_shift * 12)
        chord_notes.append(note)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert the sustained chord
    start_qn = 0.0
    end_qn = bars * beats_per_bar
    
    for note in chord_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                start_qn * 960, end_qn * 960, 
                                0, note, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments & FX ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more "sawtooth/square" pad sound
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.8) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.8) # Release

    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # In ReaEQ, Band 4 (defaults to High Shelf) has parameters starting at index 9:
    # Param 9: Freq, Param 10: Gain, Param 11: Q
    # Set Band 4 Gain to minimum (0.0 normalized) to act as a harsh low-pass filter
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0)

    # === Step 5: Automate Filter Sweep ===
    # Get the envelope for ReaEQ Band 4 Frequency (Parameter 9)
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    
    # REAPER parameter values are normalized 0.0 to 1.0.
    # We will sweep from 0.15 (very muffled) to 0.9 (bright/open)
    start_val = 0.15
    end_val = 0.90
    
    # Shape 0 = Linear transition
    RPR.RPR_InsertEnvelopePoint(env, 0.0, start_val, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length, end_val, 0, 0.0, False, True)
    
    # Sort the envelope points to ensure they play back correctly
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with a {bars}-bar automated filter sweep at {bpm} BPM."
