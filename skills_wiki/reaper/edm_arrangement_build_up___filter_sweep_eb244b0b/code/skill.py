def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Build",
    bpm: int = 125,
    key: str = "G",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Arrangement Build-Up with an EQ filter sweep in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars (first half is the build, second half is the drop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    # === Step 2: Create Tracks ===
    base_idx = RPR.RPR_CountTracks(0)
    
    # Track 1: Chords (Pad)
    RPR.RPR_InsertTrackAtIndex(base_idx, True)
    track_chords = RPR.RPR_GetTrack(0, base_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)
    
    # Track 2: Kick
    RPR.RPR_InsertTrackAtIndex(base_idx + 1, True)
    track_kick = RPR.RPR_GetTrack(0, base_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_kick, "P_NAME", f"{track_name}_Kick", True)
    
    # Track 3: Bass
    RPR.RPR_InsertTrackAtIndex(base_idx + 2, True)
    track_bass = RPR.RPR_GetTrack(0, base_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name}_Bass", True)

    # === Helper Functions ===
    def insert_midi_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    def get_chord_notes(root_idx, scale_arr):
        n1 = scale_arr[root_idx % len(scale_arr)] + 12 * (root_idx // len(scale_arr))
        n2 = scale_arr[(root_idx + 2) % len(scale_arr)] + 12 * ((root_idx + 2) // len(scale_arr))
        n3 = scale_arr[(root_idx + 4) % len(scale_arr)] + 12 * ((root_idx + 4) // len(scale_arr))
        return [n1, n2, n3]

    root_offset = NOTE_MAP.get(key, 0) + 48 # Base octave 4
    scale_notes = SCALES.get(scale, SCALES["minor"])
    progression = [0, 5, 2, 6] # Diatonic i, VI, III, VII
    drop_start_time = (bars // 2) * bar_len
    drop_bars = bars - (bars // 2)

    # === Step 3: Chords & Filter Automation ===
    # Set up ReaSynth Pad
    synth_chords = RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, synth_chords, 1, 0.6) # Saw Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, synth_chords, 2, 0.4) # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, synth_chords, 4, 0.7) # Release

    # Set up ReaEQ Filter
    eq_idx = RPR.RPR_TrackFX_AddByName(track_chords, "ReaEQ", False, -1)
    # Param 10 is Band 4 Gain. 0.0 effectively makes the High Shelf act as a Low Pass Cut.
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, eq_idx, 10, 0.0) 
    
    # Automate Band 4 Frequency (Param 9)
    env = RPR.RPR_GetFXEnvelope(track_chords, eq_idx, 9, True)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.2, 0, 0, False, True) # Start muffled (~300Hz)
    RPR.RPR_InsertEnvelopePoint(env, drop_start_time, 0.9, 0, 0, False, True) # Open at the drop (~15kHz)
    RPR.RPR_Envelope_SortPoints(env)

    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bar_len * bars)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    for b in range(bars):
        chord_idx = progression[b % len(progression)]
        notes = get_chord_notes(chord_idx, scale_notes)
        start_time = b * bar_len
        end_time = start_time + bar_len * 0.95 # Leave a slight gap for breathing room
        for n in notes:
            insert_midi_note(take_chords, start_time, end_time, root_offset + n, int(velocity_base * 0.8))

    # === Step 4: Kick Drum (Enters at Drop) ===
    synth_kick = RPR.RPR_TrackFX_AddByName(track_kick, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 3, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 4, 0.05) # Release (tight)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 1, 0.0)  # No Saw
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 2, 0.0)  # No Pulse (Pure Sine)

    item_kick = RPR.RPR_AddMediaItemToTrack(track_kick)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_POSITION", drop_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_LENGTH", drop_bars * bar_len)
    take_kick = RPR.RPR_AddTakeToMediaItem(item_kick)

    for b in range(drop_bars):
        for beat in range(4):
            start_time = drop_start_time + b * bar_len + beat * beat_len
            end_time = start_time + beat_len * 0.25
            insert_midi_note(take_kick, start_time, end_time, 36, velocity_base) # C1 Kick

    # === Step 5: Off-beat Bass (Enters at Drop) ===
    synth_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, synth_bass, 1, 0.0) # No Saw
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, synth_bass, 2, 0.7) # Square wave for EDM buzz
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, synth_bass, 4, 0.15) # Plucky release

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", drop_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", drop_bars * bar_len)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)

    for b in range(drop_bars):
        overall_bar = (bars // 2) + b
        chord_idx = progression[overall_bar % len(progression)]
        root_note = scale_notes[chord_idx % len(scale_notes)] + 12 * (chord_idx // len(scale_notes))
        pitch = root_offset + root_note - 24 # Drop 2 octaves into sub range
        
        start_time = drop_start_time + b * bar_len
        
        # Off-beat 8th notes (playing strictly on the 'AND' of each beat)
        for i in range(4):
            note_start = start_time + (i * beat_len) + (beat_len / 2)
            note_end = note_start + (beat_len / 2) * 0.8
            insert_midi_note(take_bass, note_start, note_end, pitch, velocity_base)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_kick)
    RPR.RPR_MIDI_Sort(take_bass)

    return f"Created '{track_name}' EDM arrangement ({bars} bars) at {bpm} BPM in {key} {scale} with an automated filter sweep."
