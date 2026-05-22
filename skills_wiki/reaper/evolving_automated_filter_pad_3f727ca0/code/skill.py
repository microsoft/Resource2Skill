def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Evolving Automated Filter Pad in the current REAPER project.
    
    Demonstrates Track Volume, Track Pan, and FX Parameter (ReaEQ) envelope automation.

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
        Status string describing the creation of the automated track.
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

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Time and Item Calculation ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Insert Sustained MIDI Chord ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    root_midi = NOTE_MAP[key] + 48 # Octave 3
    chord_degrees = [0, 2, 4] # Root, 3rd, 5th triad
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    for degree in chord_degrees:
        octave_offset = (degree // len(scale_intervals)) * 12
        scale_idx = degree % len(scale_intervals)
        pitch = root_midi + scale_intervals[scale_idx] + octave_offset
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments and FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 5: Automate Track Volume and Pan ===
    # Select track and trigger actions to show default envelopes so we can grab them safely
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40407, 0) # Toggle track pan envelope visible

    # Volume Swell (0.0 = -inf dB, 1.0 = 0 dB)
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 0, 0, False, False)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 0, 0, False, False)
        RPR.RPR_Envelope_Sort(vol_env)

    # Pan Sweep (-0.5 = 50% L, 0.5 = 50% R)
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, -0.5, 0, 0, False, False)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.5, 0, 0, False, False)
        RPR.RPR_Envelope_Sort(pan_env)

    # === Step 6: Automate FX Parameter (ReaEQ Frequency) ===
    # Param 0 in ReaEQ is Band 1 Frequency. get/create=True ensures we can automate it.
    eq_env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)
    if eq_env:
        # VST parameters are normalized 0.0 to 1.0 in REAPER
        RPR.RPR_InsertEnvelopePoint(eq_env, 0.0, 0.1, 0, 0, False, False)
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length, 0.8, 0, 0, False, False)
        RPR.RPR_Envelope_Sort(eq_env)

    return f"Created '{track_name}' (Automated Swell) with a {key} {scale} triad over {bars} bars at {bpm} BPM"
