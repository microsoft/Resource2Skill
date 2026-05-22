def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Progression",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Rule of 3 Arrangement Structure in the current REAPER project.
    Generates an AAB musical structure where the 3rd repetition diverges to maintain interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (defaults to 12 to demonstrate the 3x4 rule).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Note computation logic
    root_midi = NOTE_MAP[key.capitalize()] + 48 # Base octave (e.g., C3 = 48)
    active_scale = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(active_scale)

    def get_pitch(degree: int) -> int:
        """Converts a diatonic scale degree (relative to 0 = root) to an exact MIDI pitch."""
        octave = degree // scale_len
        idx = degree % scale_len
        return root_midi + (octave * 12) + active_scale[idx]

    def insert_note(start_beat: float, end_beat: float, pitch: int, vel: int):
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Determine structural progressions based on tonality
    if "minor" in scale.lower() or "dorian" in scale.lower() or "blues" in scale.lower():
        prog_a = [-2, -1, 0, 0] # VI, VII, i, i
        prog_b = [-2, -1, 3, 4] # VI, VII, iv, v
    else:
        prog_a = [-4, -3, 0, 0] # IV, V, I, I
        prog_b = [-4, -3, 1, 2] # IV, V, ii, iii

    # === Step 4: Generate AAB Structure ===
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        cycle_bar = bar % 12
        
        # Rule of 3 routing: First two times are A, third time is B
        if cycle_bar < 8:
            chord_degree = prog_a[cycle_bar % 4]
            pattern_type = "A"
        else:
            chord_degree = prog_b[cycle_bar % 4]
            pattern_type = "B"
            
        # 1. Bass note (1 octave down)
        insert_note(bar_start_beat, bar_start_beat + 4.0, get_pitch(chord_degree) - 12, velocity_base)
        
        # 2. Chord pad (Triad)
        for offset in [0, 2, 4]:
            insert_note(bar_start_beat, bar_start_beat + 4.0, get_pitch(chord_degree + offset), velocity_base - 15)
            
        # 3. Melody motif (Diverges on the 3rd repetition)
        if pattern_type == "A":
            m_offsets = [0, 2, 4, 2]
            m_beats = [0.0, 1.0, 2.0, 2.5] # Syncopated motif
            m_len = 0.4
        else:
            m_offsets = [4, 2, 0, -1, 0]
            m_beats = [0.0, 0.5, 1.0, 1.5, 2.0] # Denser, descending motif variation
            m_len = 0.4
            
        for m_off, m_beat in zip(m_offsets, m_beats):
            insert_note(
                bar_start_beat + m_beat, 
                bar_start_beat + m_beat + m_len, 
                get_pitch(chord_degree + m_off) + 12, 
                velocity_base + 10
            )

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Ambient Pad FX Chain) ===
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_synth >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.3)   # Volume mix
        RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.4)   # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.6)   # Saw mix
        RPR.RPR_TrackFX_SetParam(track, fx_synth, 6, 0.05)  # Soft Attack
        RPR.RPR_TrackFX_SetParam(track, fx_synth, 9, 0.4)   # Long Release

    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    if fx_verb >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.6)    # Wet
        RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.7)    # Dry
        RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.9)    # Large Roomsize

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' demonstrating the Rule of 3 structure over {bars} bars at {bpm} BPM."
