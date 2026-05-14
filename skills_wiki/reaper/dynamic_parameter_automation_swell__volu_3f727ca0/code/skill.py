def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a sustaining 7th chord pad with automated Volume, Pan, and a resonant EQ sweep.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the sweep over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    # === Step 3: Create MIDI Item & 7th Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 6] # Root, 3rd, 5th, 7th
    octave = 4
    base_midi = octave * 12 + root_val
    
    for degree in chord_degrees:
        octave_offset = degree // 7
        scale_idx = degree % len(scale_intervals)
        midi_pitch = base_midi + (octave_offset * 12) + scale_intervals[scale_idx]
        # Insert sustained note for the entire duration of the item
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments & FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Configure ReaEQ Band 2 (Peak filter) to act as a resonant sweep
    # Param 6: Band 2 Gain (Set to ~0.7 for an audible boost peak)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 6, 0.7)
    # Param 7: Band 2 Q (Set to ~0.6 for narrower, squelchy resonance)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 7, 0.6)

    # === Step 5: Automate Volume, Pan, and FX ===
    # Enable Read mode (1) so faders visibly move during playback as shown in the tutorial
    RPR.RPR_SetTrackAutomationMode(track, 1) 
    RPR.RPR_SetOnlyTrackSelected(track)

    # 1. Volume Envelope Swell
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env_vol:
        # Values represent Amplitude: 0.0 = -inf, 1.0 = 0dB. Shape 0 = Linear.
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length / 2.0, 1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length, 0.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    # 2. Panning Envelope Movement
    RPR.RPR_Main_OnCommand(40456, 0) # Toggle track pan envelope visible
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if env_pan:
        # Sweep Pan back and forth across the bars
        for b in range(bars + 1):
            time_pos = b * bar_length_sec
            pan_val = -0.7 if b % 2 == 0 else 0.7
            RPR.RPR_InsertEnvelopePoint(env_pan, time_pos, pan_val, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_pan)

    # 3. FX Parameter Envelope (ReaEQ Band 2 Frequency)
    # Param 5 is Band 2 Frequency. "True" creates the envelope if hidden.
    env_eq = RPR.RPR_GetFXEnvelope(track, eq_idx, 5, True)
    if env_eq:
        # Normalized values (0.0 to 1.0 representing 20Hz to 24000Hz approx)
        RPR.RPR_InsertEnvelopePoint(env_eq, 0.0, 0.1, 0, 0.0, False, True) 
        RPR.RPR_InsertEnvelopePoint(env_eq, item_length / 2.0, 0.9, 0, 0.0, False, True) 
        RPR.RPR_InsertEnvelopePoint(env_eq, item_length, 0.1, 0, 0.0, False, True) 
        RPR.RPR_Envelope_SortPoints(env_eq)

    return f"Created '{track_name}' with automated Volume, Pan, and EQ sweeps over {bars} bars at {bpm} BPM in key of {key} {scale}."
