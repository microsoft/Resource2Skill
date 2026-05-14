def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Ghost Sidechain & Filter Sweep arrangement.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chord track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Chord Track (with 4 channels for sidechaining) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "I_NCHAN", 4) # Enable channels 3/4

    # === Step 3: Create Ghost Kick Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Trigger (Muted)", True)
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0) # Mute from master

    # === Step 4: Route Ghost Track to Chord Track (Channels 3/4) ===
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chord_track)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2) # 2 means channels 3/4

    # === Step 5: Setup Ghost Kick Instrument ===
    ksynth_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    # Fast attack/decay to act as a sharp sidechain transient
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, ksynth_idx, 2, 0.0) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, ksynth_idx, 3, 0.1) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, ksynth_idx, 4, 0.0) # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, ksynth_idx, 5, 0.1) # Release

    # === Step 6: Setup Chord Track FX (Synth -> Filter -> Sidechain Comp) ===
    csynth_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, csynth_idx, 1, 0.4) # Saw shape
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, csynth_idx, 5, 0.5) # Release

    filter_idx = RPR.RPR_TrackFX_AddByName(chord_track, "JS: hpflpf", False, -1)
    
    comp_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, comp_idx, 0, 0.6)  # Threshold (low to catch signal)
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, comp_idx, 1, 0.5)  # Ratio (high for pump)
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, comp_idx, 2, 0.0)  # Attack (fastest)
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, comp_idx, 3, 0.1)  # Release (~100ms)

    # Find and set Detector Input to Aux L+R dynamically
    for p in range(15):
        res = RPR.RPR_TrackFX_GetParamName(chord_track, comp_idx, p, "", 64)
        if res[0] and "detector input" in res[3].lower():
            RPR.RPR_TrackFX_SetParamNormalized(chord_track, comp_idx, p, 0.5) # 0.5 maps to Aux L+R in ReaComp

    # === Step 7: MIDI Generation ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_length_sec)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = NOTE_MAP.get(key, 0) + 60 # Octave 5 for chords
    progression = [0, 5, 3, 6] if scale == "minor" else [0, 3, 5, 4]

    for i in range(bars):
        deg = progression[i % len(progression)]
        # Triad logic
        n1 = root_midi + scale_intervals[deg % len(scale_intervals)] + (12 * (deg // len(scale_intervals)))
        d2 = deg + 2
        n2 = root_midi + scale_intervals[d2 % len(scale_intervals)] + (12 * (d2 // len(scale_intervals)))
        d3 = deg + 4
        n3 = root_midi + scale_intervals[d3 % len(scale_intervals)] + (12 * (d3 // len(scale_intervals)))

        abs_start = i * bar_length_sec
        abs_end = (i + 1) * bar_length_sec
        c_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, abs_start)
        c_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, abs_end)
        
        # Insert Chords
        RPR.RPR_MIDI_InsertNote(chord_take, False, False, c_start_ppq, c_end_ppq, 0, n1, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(chord_take, False, False, c_start_ppq, c_end_ppq, 0, n2, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(chord_take, False, False, c_start_ppq, c_end_ppq, 0, n3, velocity_base, False)

        # Insert 4-on-the-floor Kicks
        for b in range(beats_per_bar):
            k_abs_start = abs_start + (b * (60.0 / bpm))
            k_abs_end = k_abs_start + (60.0 / bpm * 0.25) # 16th note length
            k_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, k_abs_start)
            k_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, k_abs_end)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, k_start_ppq, k_end_ppq, 0, 36, 127, False)

    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 8: Filter Automation ===
    # Find LPF param index on JS hpflpf (usually 1)
    lpf_param_idx = 1 
    for p in range(5):
        res = RPR.RPR_TrackFX_GetParamName(chord_track, filter_idx, p, "", 64)
        if res[0] and "lpf" in res[3].lower():
            lpf_param_idx = p
            break

    # Create envelope and sweep from closed (0.1) to open (1.0)
    env = RPR.RPR_GetFXEnvelope(chord_track, filter_idx, lpf_param_idx, True)
    if env:
        # shape 2 = slow start/end (smooth curve)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, total_length_sec, 1.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' and Ghost Trigger over {bars} bars at {bpm} BPM with sidechain routing and filter sweep."
