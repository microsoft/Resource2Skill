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
    Create an Automated Filter Sweep & Volume Swell pattern.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo and Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

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
    
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generate a diatonic 7th chord
    chord_degrees = [0, 2, 4, 6]
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for degree in chord_degrees:
        octave_shift = degree // 7
        interval = scale_intervals[degree % len(scale_intervals)]
        pitch = root_pitch + interval + (octave_shift * 12)
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False,
            start_ppq, end_ppq,
            1, pitch, velocity_base, False
        )

    # === Step 3: Add Instruments & FX ===
    # Add ReaSynth (analog pad sound)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5) # Sawtooth mix up
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4) # Pulse mix up

    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 4: Automate Plugin Parameter (Filter Sweep) ===
    # Get/Create Envelope for ReaEQ Band 1 Freq (Param 0)
    env_eq = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)
    
    # Insert sweeping automation points (Normalized values 0.0 to 1.0)
    sweep_points = [
        (0.0, 0.1),                           # Low start
        (item_length * 0.25, 0.55),           # Build up
        (item_length * 0.5, 0.85),            # Peak bright
        (item_length * 0.75, 0.4),            # Come down
        (item_length, 0.1)                    # Back to low
    ]
    
    for time, val in sweep_points:
        # shape=2 gives a smooth slow-start/slow-end curve exactly like drawn automation
        RPR.RPR_InsertEnvelopePoint(env_eq, time, val, 2, 0.0, False, True)
    RPR.RPR_Envelope_SortOrder(env_eq)

    # === Step 5: Automate Track Volume (Rhythmic Swell/Pump) ===
    # Force volume envelope visible so we can grab it
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env_vol:
        num_beats = int(bars * beats_per_bar)
        beat_length = 60.0 / bpm
        
        for i in range(num_beats + 1):
            t_beat = i * beat_length
            val_high = 0.8  # ~ 0dB
            val_low = 0.35  # ~ -12dB
            
            # Swell peaks on the beat
            RPR.RPR_InsertEnvelopePoint(env_vol, t_beat, val_high, 2, 0.0, False, True)
            
            # Swell drops on the off-beat (if not the very end)
            if i < num_beats:
                t_offbeat = t_beat + (beat_length / 2.0)
                RPR.RPR_InsertEnvelopePoint(env_vol, t_offbeat, val_low, 2, 0.0, False, True)
                
        RPR.RPR_Envelope_SortOrder(env_vol)

    return f"Created '{track_name}' with a sustained {key} {scale} pad, automated Volume pumping, and ReaEQ Filter Sweep over {bars} bars at {bpm} BPM."
