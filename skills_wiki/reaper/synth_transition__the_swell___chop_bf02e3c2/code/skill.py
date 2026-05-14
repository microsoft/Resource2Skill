def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Swell Chop Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Synth Swell & Chop transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the entire transition duration.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the transition.
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
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Compute Timeline Lengths ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_transition_sec = bar_length_sec * bars

    # Create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_transition_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Note length is shorter than transition to let Reverb tail play & chop
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    # MIDI cuts out half a bar early
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_length_sec * max(0.5, bars - 0.5))

    # === Step 4: Insert Pitch/Harmony Data ===
    root_val = NOTE_MAP.get(key, 0) + 36 # Start around C2
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Build a lush 5-note pad chord (Root, 3rd, 5th, Octave, 9th)
    chord_indices = [0, 2, 4, len(scale_intervals), len(scale_intervals) + 1]
    
    for idx in chord_indices:
        octave_offset = 12 * (idx // len(scale_intervals))
        scale_degree = idx % len(scale_intervals)
        pitch = root_val + scale_intervals[scale_degree] + octave_offset
        # Restrict extreme high pitches
        if pitch <= 100:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Build FX Chain (Order is crucial) ===
    
    # 1. Synthesis
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 0, 0.7) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 1.0) # Sawtooth
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 4, 0.5) # Square (thick mix)

    # 2. Movement (Flanging/Chorus)
    fx_chorus = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_chorus, 3, 0.5) # Mod depth

    # 3. Space (Reverb) - Placed BEFORE the chop
    fx_reverb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_reverb, 0, 0.6) # Wet
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_reverb, 1, 0.8) # Dry
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_reverb, 2, 0.9) # Roomsize (Big)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_reverb, 3, 0.1) # Dampening

    # 4. Rhythm Chop (Tremolo)
    fx_tremolo = RPR.RPR_TrackFX_AddByName(track, "JS: Tremolo", False, -1)
    # 32nd notes = 8 cycles per beat
    freq_hz = (bpm / 60.0) * 8.0 
    RPR.RPR_TrackFX_SetParam(track, fx_tremolo, 0, freq_hz) # Hz
    RPR.RPR_TrackFX_SetParam(track, fx_tremolo, 1, -24.0) # Chop depth in dB

    # 5. Spatial Automation (Mono to Stereo)
    fx_width = RPR.RPR_TrackFX_AddByName(track, "JS: Stereo Width", False, -1)
    env_width = RPR.RPR_GetFXEnvelope(track, fx_width, 0, True) # Param 0 is Width
    # Slow Start/End curve shape = 2
    RPR.RPR_InsertEnvelopePoint(env_width, 0.0, 0.0, 2, 0.0, False, False) # Start Mono
    RPR.RPR_InsertEnvelopePoint(env_width, total_transition_sec, 100.0, 2, 0.0, False, False) # End Wide
    RPR.RPR_Envelope_SortPoints(env_width)

    # 6. Macro Volume Swell (Separated from track fader)
    fx_vol = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    env_vol = RPR.RPR_GetFXEnvelope(track, fx_vol, 0, True) # Param 0 is Adjustment (dB)
    RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, -24.0, 2, 0.0, False, False) # Start quiet
    RPR.RPR_InsertEnvelopePoint(env_vol, total_transition_sec, 0.0, 2, 0.0, False, False) # End at 0dB
    RPR.RPR_Envelope_SortPoints(env_vol)

    return f"Created '{track_name}' swell-and-chop transition over {bars} bars at {bpm} BPM in {key} {scale}."
