def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter_Build",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Low-Pass Filter Build-up & Subtractive Drop arrangement.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (first half is build, second half is drop). Must be even.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Safety check for bars
    if bars < 2:
        bars = 8
    build_bars = bars // 2
    drop_bars = bars - build_bars

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }
    
    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # === Step 2: Track 1 - Pad / Chords (Spans entire length) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    pad_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", f"{track_name}_Pad_FilterBuild", True)
    # Lower volume slightly to prevent harshness
    RPR.RPR_SetMediaTrackInfo_Value(pad_track, "D_VOL", 0.5)

    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", bar_length_sec * bars)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)

    # Chord Progression: i - VI - III - VII (classic epic progression)
    progression = [0, 5, 2, 6] 
    octave = 4
    base_pitch = NOTE_MAP[key] + (octave * 12)

    # Insert sustained chords
    for bar in range(bars):
        chord_root_idx = progression[bar % len(progression)]
        start_time = bar * bar_length_sec
        end_time = (bar + 1) * bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, end_time)

        # Build triad
        for voice in [0, 2, 4]:
            deg = chord_root_idx + voice
            pitch = base_pitch + SCALES[scale][deg % len(SCALES[scale])] + (12 * (deg // len(SCALES[scale])))
            # Keep pitch within safe MIDI bounds
            pitch = max(0, min(127, pitch))
            RPR.RPR_MIDI_InsertNote(pad_take, False, False, start_ppq, end_ppq, 1, pitch, int(velocity_base * 0.8), False)

    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(pad_track, synth_idx, 1, 0.4) # Add Sawtooth for harmonics to be filtered
    
    # Add ReaEQ for the Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(pad_track, "ReaEQ", False, -1)
    # Band 4 (High Shelf) Gain -> parameter 10. Set to 0.0 (-inf dB) to mimic Low Pass
    RPR.RPR_TrackFX_SetParamNormalized(pad_track, eq_idx, 10, 0.0)
    
    # Automate Band 4 Freq (parameter 9)
    env = RPR.RPR_GetFXEnvelope(pad_track, eq_idx, 9, True)
    
    # Point 1: Start (Muffled - roughly 200Hz)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.15, 0, 0.0, False, True)
    # Point 2: Just before Drop (Fully Open - roughly 20kHz)
    drop_time = build_bars * bar_length_sec
    RPR.RPR_InsertEnvelopePoint(env, drop_time, 1.0, 0, 0.0, False, True)
    # Point 3: End of arrangement (Stays Open)
    RPR.RPR_InsertEnvelopePoint(env, bars * bar_length_sec, 1.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    # === Step 3: Track 2 - Subtractive Drums (Drop only) ===
    track_idx_drum = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_drum, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx_drum)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums_Drop", True)

    # Item ONLY exists during the drop (Subtractive arrangement)
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", drop_time)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", drop_bars * bar_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Insert 4-on-the-floor Kick to maximize impact
    for bar in range(drop_bars):
        for beat in range(beats_per_bar):
            note_start = drop_time + (bar * bar_length_sec) + (beat * (bar_length_sec / beats_per_bar))
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, note_start)
            end_ppq = start_ppq + 240 # Short punchy length
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 1, 36, velocity_base, False)

    # Add quick decay synth to simulate a drum thump
    drum_synth = RPR.RPR_TrackFX_AddByName(drum_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_synth, 3, 0.0)  # Attack = 0
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_synth, 4, 0.05) # Decay = extremely short
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_synth, 5, 0.0)  # Sustain = 0
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_synth, 6, 0.0)  # Release = 0
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_synth, 0, 0.8)  # Volume slightly boosted

    # Update UI
    RPR.RPR_UpdateArrange()

    return f"Created Filter Build/Drop arrangement: {build_bars}-bar build into {drop_bars}-bar drop at {bpm} BPM in {key} {scale}."
