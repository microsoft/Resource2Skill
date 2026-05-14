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
    Create an Automated Drone/Pad with Volume Swells and Pan Sweeps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the swell over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the track and automation.
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

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Calculate timing
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth to generate sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a pad-like envelope: Attack (param 4) and Release (param 5)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1) # 100ms attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5) # 500ms release

    # Create MIDI Item and Take
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine Base Pitch (Octave 3 = 48)
    root_pitch = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Voicing: 1 - 5 - 8 (Root, Fifth, Octave) for a stable, wide drone
    chord_pitches = [
        root_pitch, 
        root_pitch + scale_intervals[4 % len(scale_intervals)], # 5th
        root_pitch + 12 # Octave
    ]

    # Insert sustained drone notes
    start_qn = 0.0
    end_qn = bars * beats_per_bar
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                start_qn * 960, end_qn * 960, 
                                0, pitch, velocity_base, False)

    # === AUTOMATION SETUP ===
    # To reliably get envelopes in REAPER, we ensure they are visible first
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40407, 0) # Track: Toggle track pan envelope visible

    # 1. Volume Swell Envelope
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        # shape: 2 = Slow start/end (S-Curve) for smooth swells
        # Insert start point (0.0 amplitude = -inf)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, True)
        # Insert end point (1.0 amplitude = 0dB) at the end of the item
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_Sort(vol_env)

    # 2. Pan Sweep Envelope
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        # shape: 2 = Slow start/end
        # Center -> Left -> Right -> Center
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, 0.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.33, -0.8, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.66, 0.8, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_Sort(pan_env)

    # 3. Change Automation Mode to "Read" (1)
    # Mode 1 forces the UI faders (which will turn green) to physically move and follow the drawn envelopes
    RPR.RPR_SetTrackAutomationMode(track, 1)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' drone with Volume Swell and Pan Sweep automation over {bars} bars in {key} {scale}."
