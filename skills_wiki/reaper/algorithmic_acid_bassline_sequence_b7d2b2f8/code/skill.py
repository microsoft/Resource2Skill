def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Acid Bass Sequence",
    bpm: int = 125,
    key: str = "G",
    scale: str = "pentatonic_minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a syncopated 16th-note acid bassline sequence natively in REAPER.
    Mimics the algorithmic output of a step sequencer driving a resonant synth.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Sound Design (ReaSynth + Resonant Filter) ===
    # 3a. Add ReaSynth for the core Sawtooth tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.4) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.0) # Attack (Fast)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.2) # Decay (Short)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.1) # Sustain (Low)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.1) # Release (Fast)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.0) # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 1.0) # Saw Mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.0) # Triangle Mix

    # 3b. Add JS: 4-Pole Resonant Filter (standard REAPER acid filter)
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "sstillwell/4pole", False, -1)
    if filter_idx == -1:
        # Fallback if 4pole is named differently in user's install
        filter_idx = RPR.RPR_TrackFX_AddByName(track, "Liteon/moog24db", False, -1)
    
    if filter_idx != -1:
        # Set high resonance (Param 1 is resonance 0-1 on both JS filters)
        RPR.RPR_TrackFX_SetParamNormalized(track, filter_idx, 1, 0.8) 

    # === Step 4: MIDI Sequence Generation ===
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar
    total_length = bar_length * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Generative Sequence Blueprint: (16th note step index, scale degree, octave offset, velocity)
    # This creates a classic syncopated acid groove
    pattern = [
        (0, 0, 0, 110),   # Root
        (2, 0, 0, 90),    # Root
        (3, 0, 1, 120),   # Root (Octave up accent)
        (5, 1, 0, 100),   # Minor 3rd
        (7, 0, 0, 110),   # Root
        (8, 0, 1, 120),   # Root (Octave up accent)
        (10, 4, 0, 100),  # Minor 7th
        (11, 0, 0, 90),   # Root
        (13, 0, 1, 110),  # Root (Octave up accent)
        (15, 1, 1, 120)   # Minor 3rd (Octave up accent)
    ]

    root_midi = NOTE_MAP.get(key, 7) + 36 # Start around C2 register for bass
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    note_count = 0

    for b in range(bars):
        bar_offset = b * bar_length
        for step, scale_deg, oct_offset, vel in pattern:
            # Pitch calculation
            octave_shift = scale_deg // len(scale_intervals)
            scale_idx = scale_deg % len(scale_intervals)
            pitch = root_midi + scale_intervals[scale_idx] + (octave_shift * 12) + (oct_offset * 12)

            # Timing calculation (16th note = 0.25 beats, duration = 0.15 beats for staccato)
            start_beat = step * 0.25
            start_time_sec = bar_offset + (start_beat * beat_length)
            end_time_sec = start_time_sec + (0.15 * beat_length)

            # Convert to PPQ for REAPER MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Filter Automation Sweep ===
    if filter_idx != -1:
        # Get parameter 0 (Cutoff/Frequency)
        env = RPR.RPR_GetFXEnvelope(track, filter_idx, 0, True)
        if env != 0:
            # Create a smooth macro sweep: Low -> High -> Low over the generated bars
            # Shape 2 is 'Slow start/end' for smooth curves
            RPR.RPR_InsertEnvelopePoint(env, 0.0, 300.0, 2, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(env, total_length * 0.5, 2500.0, 2, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(env, total_length, 300.0, 2, 0.0, False, True)
            RPR.RPR_Envelope_SortPoints(env)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} sequenced notes and automated filter sweep over {bars} bars at {bpm} BPM"
