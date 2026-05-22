def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Automated Filter Sweep & Volume Swell buildup.
    Generates a sustained 9th chord, adds ReaSynth and ReaEQ, and
    draws automation envelopes for track volume and EQ frequency.
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

    # 1. Setup Tempo & Calculations
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    duration = bar_length_sec * bars

    # 2. Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 3. Add FX (ReaSynth for tone, ReaEQ for filter sweep)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set synth to a mix of sawtooth and square for rich harmonics
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5) # Saw shape
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Square shape
    
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # 4. Create MIDI Item & Sustained Chord
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration)
    take = RPR.RPR_AddTakeToMediaItem(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, duration)

    # Build a lush 5-note chord (Root, 3rd, 5th, 7th, 9th) over 2 octaves
    octave_base = 48 # Start at C3
    chord_degrees = [0, 2, 4, 6, 8] # 1st, 3rd, 5th, 7th, 9th
    
    for degree in chord_degrees:
        octave_offset = (degree // len(scale_intervals)) * 12
        note_index = degree % len(scale_intervals)
        pitch = octave_base + root_val + scale_intervals[note_index] + octave_offset
        # Ensure pitch is in valid MIDI range
        pitch = max(0, min(127, pitch))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # 5. Automate the Filter (ReaEQ Band 1 Frequency)
    # Param 0 in ReaEQ is Band 1 Frequency. Normalized 0.0 is 20Hz, 1.0 is 24kHz.
    env_eq = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)
    if env_eq:
        # Shape 2 is "Slow start/end" for an organic ramp
        RPR.RPR_InsertEnvelopePoint(env_eq, 0.0, 0.15, 2, 0.0, True, False)      # Start muffled (~150Hz)
        RPR.RPR_InsertEnvelopePoint(env_eq, duration, 0.85, 2, 0.0, True, False) # Sweep open (~10kHz)
        RPR.RPR_Envelope_Sort(env_eq)

    # 6. Automate Track Volume
    # Command 40406: "Track: Toggle track volume envelope visible" ensures the envelope exists
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) 
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env_vol:
        # Volume values: 0.0 is -inf, 1.0 is 0dB, 2.0 is +12dB
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 2, 0.0, True, False)      # Start at -infinity dB
        RPR.RPR_InsertEnvelopePoint(env_vol, duration, 1.0, 2, 0.0, True, False) # Swell up to 0 dB
        RPR.RPR_Envelope_Sort(env_vol)

    return f"Created '{track_name}' with automated Volume and Filter sweeps over {bars} bars at {bpm} BPM in {key} {scale}."
