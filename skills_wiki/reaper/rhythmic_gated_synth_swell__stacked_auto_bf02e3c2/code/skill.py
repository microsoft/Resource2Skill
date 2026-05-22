def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Gated Swell Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    gate_division: int = 16, # 16 for 16th notes, 32 for 32nd notes
    **kwargs,
) -> str:
    """
    Create a Rhythmic Gated Synth Swell in the current REAPER project.
    Simulates stacked automation items using Track Volume and Pre-FX Volume.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars for the transition swell.
        velocity_base: Base MIDI velocity.
        gate_division: Note division for the square wave gating chop.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7],
    }

    # === Step 1: Initialize Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Dense Chord ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Use a Minor 9th or Major 9th chord equivalent based on scale to make it thick
    root_val = NOTE_MAP.get(key, 0) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Degrees for a lush 5-note pad chord (Root, 3rd, 5th, 7th, 9th)
    chord_degrees = [0, 2, 4, 6, 8] 
    
    # Convert absolute time to PPQ
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for degree in chord_degrees:
        octave_offset = (degree // len(scale_intervals)) * 12
        note = root_val + scale_intervals[degree % len(scale_intervals)] + octave_offset
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments and FX ===
    
    # 1. ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5) # Saw
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Square
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.2) # Attack (slow slightly)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 1.0) # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.4) # Release

    # 2. Chorus (Widening and movement)
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus_idx, 2, 0.7) # Mix

    # 3. Reverb
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.3) # Wet Mix
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 0.8) # Room Size

    # === Step 5: Automate Envelopes (The Swell and The Gate) ===
    
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Generate the MACRO SWELL on the main Volume envelope
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env_vol:
        # Linear shape (0). Value is amplitude: 0.1 is quiet, 1.0 is 0dB
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.1, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    # Generate the MICRO GATE on the Pre-FX Volume envelope
    RPR.RPR_Main_OnCommand(40408, 0) # Toggle track Pre-FX volume envelope visible
    env_gate = RPR.RPR_GetTrackEnvelopeByName(track, "Volume (Pre-FX)")
    if env_gate:
        step_time_sec = (60.0 / bpm) * (4.0 / gate_division)
        num_steps = int(item_length / step_time_sec)

        for i in range(num_steps):
            t_start = i * step_time_sec
            t_mid = t_start + (step_time_sec / 2.0)

            # Square shape (1) creates an instant jump/hold
            # Gate OPEN (Amplitude 1.0 = 0dB)
            RPR.RPR_InsertEnvelopePoint(env_gate, t_start, 1.0, 1, 0, False, True)
            # Gate CLOSED (Amplitude 0.0 = -inf dB)
            RPR.RPR_InsertEnvelopePoint(env_gate, t_mid, 0.0, 1, 0, False, True)
            
        RPR.RPR_Envelope_SortPoints(env_gate)

    # Unselect track to clean up
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_SELECTED", 0)

    return f"Created '{track_name}' with macro swell and {gate_division}th-note gating over {bars} bars at {bpm} BPM"
