def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Sweeping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a lush synthesized pad featuring Volume, Pan, and EQ Filter automation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # --- Music Theory Lookup Tables ---
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

    # --- Step 1: Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Step 2: Create MIDI Item & Insert Sustained Chord ---
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate Chord Pitches (Root, 3rd, 5th, 7th from scale)
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    base_octave = 48  # C3
    
    # Safe index wrapping for extended chords
    def get_scale_pitch(degree):
        octave_shift = degree // len(scale_intervals)
        interval = scale_intervals[degree % len(scale_intervals)]
        return base_octave + root_val + interval + (octave_shift * 12)

    # Build a lush 7th chord (1st, 3rd, 5th, 7th degrees of the scale)
    chord_degrees = [0, 2, 4, 6] 
    
    # Insert notes into the MIDI item
    for degree in chord_degrees:
        pitch = get_scale_pitch(degree)
        # Add note: take, selected, muted, startppq, endppq, chan, pitch, vel
        # PPQ calculation: 1 beat = 960 PPQ
        start_ppq = 0
        end_ppq = int(beats_per_bar * bars * 960)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # --- Step 3: Sound Design (ReaSynth & ReaEQ) ---
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Blend Saw and Square to get a thicker analog-style pad
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.4) # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.6) # Saw Mix

    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # --- Step 4: Write Automation Envelopes ---
    # 4a. FX Parameter Automation (Filter Sweep)
    # Param 0 in ReaEQ is Band 1 Frequency. True flag creates the envelope if it doesn't exist.
    eq_env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)
    if eq_env:
        # shape=0 is linear transition
        RPR.RPR_InsertEnvelopePoint(eq_env, 0.0, 0.15, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length / 2, 0.85, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length, 0.15, 0, 0.0, False, True)
        RPR.RPR_Envelope_Sort(eq_env)

    # 4b. Track Volume Automation (Dynamic Swell)
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        # Volume scale: 0.0 = -inf, 1.0 = 0dB
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length / 2, 1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 0.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_Sort(vol_env)

    # 4c. Track Pan Automation (Spatial Movement)
    RPR.RPR_Main_OnCommand(40456, 0) # Toggle track pan envelope visible
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        # Pan scale: -1.0 = 100% L, 1.0 = 100% R
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, -0.75, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.75, 0, 0.0, False, True)
        RPR.RPR_Envelope_Sort(pan_env)

    return f"Created '{track_name}' pad with Volume, Pan, and Filter automation spanning {bars} bars at {bpm} BPM."
