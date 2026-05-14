def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "S-Curve Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an S-Curve Automation Swell in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell duration.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create Sustained MIDI Item ===
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    # MIDI timing variables (960 PPQ is standard)
    start_ppq = 0.0
    end_ppq = float(total_beats * 960)

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate Chord Pitches
    root_val = NOTE_MAP.get(key, 0) + 60 # Start at C4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4] # Root, 3rd, 5th triad

    for degree in chord_degrees:
        octave_shift = (degree // len(scale_intervals)) * 12
        mapped_degree = degree % len(scale_intervals)
        note_pitch = root_val + scale_intervals[mapped_degree] + octave_shift
        
        # Insert sustained notes
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_pitch, velocity_base, False)

    # === Step 4: Add Instrument and S-Curve Automation ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Param 0 in ReaSynth is 'Volume'
    env = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)
    
    if env:
        # Clear any existing points in the envelope lane
        RPR.RPR_DeleteEnvelopePointRange(env, -1.0, 100000.0)
        
        # Point 1: Time=0.0s, Value=0.0 (Silence), Shape=2 (Slow start/end S-Curve)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, 2, 0.0, False, True)
        
        # Point 2: Time=End of item, Value=0.7 (~Unity Gain), Shape=0 (Linear/Hold)
        RPR.RPR_InsertEnvelopePoint(env, item_length_sec, 0.7, 0, 0.0, False, True)
        
        # Force REAPER to validate the new points
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' featuring a {bars}-bar non-linear volume swell at {bpm} BPM in {key} {scale}."
