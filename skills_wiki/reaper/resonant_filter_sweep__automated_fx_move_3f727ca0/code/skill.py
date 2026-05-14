def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an evolving synth pad featuring an automated resonant filter sweep 
    demonstrating the core "Automate Anything" concept from the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the sweep duration.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., sweep_direction="up" or "down").

    Returns:
        Status string describing the generated track and automation.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item for Duration ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Dense Harmonic Chord (9th Chord) ===
    root_val = NOTE_MAP.get(key.capitalize(), 0) + 48 # Start at octave 3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    chord_degrees = [0, 2, 4, 6, 8] # Root, 3rd, 5th, 7th, 9th

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for degree in chord_degrees:
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        note = root_val + scale_intervals[scale_idx] + (octave_shift * 12)
        
        # Insert sustained note covering the whole item
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
        
        # Add a lower octave bass note for weight
        if degree == 0:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note - 12, velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    # 1. Add Sound Source (ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, 1)
    # Blend in some sawtooth for rich harmonics to filter
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5) # Saw character

    # 2. Add Filter (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, 1)
    
    # Configure Band 3 to be a pronounced resonant peak
    BAND3_FREQ_PARAM = 6
    BAND3_GAIN_PARAM = 7
    BAND3_Q_PARAM = 8
    
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, BAND3_GAIN_PARAM, 0.75) # Boost Gain (+12dB)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, BAND3_Q_PARAM, 0.6)    # Narrow Q for resonance

    # === Step 6: Create the Automation Envelope ===
    # Get the envelope for Band 3 Frequency, create it if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, BAND3_FREQ_PARAM, True)
    
    # Define sweep direction
    sweep_dir = kwargs.get("sweep_direction", "up").lower()
    start_val = 0.15 if sweep_dir == "up" else 0.85
    end_val = 0.85 if sweep_dir == "up" else 0.15

    # Insert automation points
    # Shape 0 = Linear transition
    RPR.RPR_InsertEnvelopePoint(env, 0.0, start_val, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length, end_val, 0, 0.0, False, True)
    RPR.RPR_Envelope_Sort(env)

    # Update REAPER UI
    RPR.RPR_TrackList_AdjustWindows(False)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with a {bars}-bar automated filter sweep ({sweep_dir}) at {bpm} BPM in {key} {scale}."
