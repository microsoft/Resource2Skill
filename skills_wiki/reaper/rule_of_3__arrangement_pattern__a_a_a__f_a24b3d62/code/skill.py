def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOfThree",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar 'Rule of 3' arrangement (A-A-A' form) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (minimum 12 recommended to hear the effect).
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Rooted at octave 3

    def get_scale_note(degree, octave_offset=0):
        octave = degree // len(scale_intervals) + octave_offset
        idx = degree % len(scale_intervals)
        return root_midi + (octave * 12) + scale_intervals[idx]

    def clamp_vel(v):
        return max(1, min(127, int(v)))

    # Setup Timing
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar
    total_length_sec = bars * bar_length

    # Create Tracks
    track_idx = RPR.RPR_CountTracks(0)
    
    # 1. Chords Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)
    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", total_length_sec)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)

    # 2. Melody Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_mel = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_mel, "P_NAME", f"{track_name}_Melody", True)
    item_mel = RPR.RPR_AddMediaItemToTrack(track_mel)
    RPR.RPR_SetMediaItemInfo_Value(item_mel, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_mel, "D_LENGTH", total_length_sec)
    take_mel = RPR.RPR_AddTakeToMediaItem(item_mel)
    RPR.RPR_TrackFX_AddByName(track_mel, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_mel, "ReaDelay", False, -1)

    # Progression Degrees (0-indexed)
    A_chords = [0, 4, 5, 3]        # I, V, vi, IV
    A_prime_chords = [0, 4, 1, 4]  # I, V, ii, V (The "Bait and Switch")

    chord_notes_list = []
    mel_notes_list = []

    # Generate Arrangement
    for bar in range(bars):
        phrase_idx = bar // 4
        bar_in_phrase = bar % 4

        # Rule of 3 Logic: On every 3rd phrase, vary the second half of the progression
        is_variation = (phrase_idx % 3 == 2) and (bar_in_phrase >= 2)
        chord_degree = A_prime_chords[bar_in_phrase] if is_variation else A_chords[bar_in_phrase]
        bar_start_time = bar * bar_length

        # Create Chords (Whole Notes)
        c_root = get_scale_note(chord_degree, 0)
        c_third = get_scale_note(chord_degree + 2, 0)
        c_fifth = get_scale_note(chord_degree + 4, 0)
        c_vel = clamp_vel(velocity_base - 20)
        
        chord_notes_list.extend([
            (bar_start_time, bar_start_time + bar_length, c_root, c_vel),
            (bar_start_time, bar_start_time + bar_length, c_third, c_vel),
            (bar_start_time, bar_start_time + bar_length, c_fifth, c_vel)
        ])

        # Create Melody
        if is_variation:
            # A' Melody: Straight descending quarter notes to signal a change
            m_data = [
                (0.0, 1.0, get_scale_note(chord_degree + 7, 1), clamp_vel(velocity_base)),
                (1.0, 2.0, get_scale_note(chord_degree + 4, 1), clamp_vel(velocity_base)),
                (2.0, 3.0, get_scale_note(chord_degree + 2, 1), clamp_vel(velocity_base)),
                (3.0, 4.0, get_scale_note(chord_degree, 1),     clamp_vel(velocity_base))
            ]
        else:
            # A Melody: Syncopated 8th note bounce motif
            m_data = [
                (0.0, 1.0, get_scale_note(chord_degree, 1),     clamp_vel(velocity_base)),
                (1.0, 1.5, get_scale_note(chord_degree + 2, 1), clamp_vel(velocity_base - 15)),
                (1.5, 2.0, get_scale_note(chord_degree + 4, 1), clamp_vel(velocity_base - 15)),
                (2.0, 3.0, get_scale_note(chord_degree + 7, 1), clamp_vel(velocity_base)),
                (3.0, 4.0, get_scale_note(chord_degree + 4, 1), clamp_vel(velocity_base - 10))
            ]

        for b_start, b_end, pitch, vel in m_data:
            start_sec = bar_start_time + (b_start * beat_length)
            end_sec = bar_start_time + (b_end * beat_length)
            mel_notes_list.append((start_sec, end_sec, pitch, vel))

    # Insert notes into REAPER items
    for start_sec, end_sec, pitch, vel in chord_notes_list:
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, end_sec)
        RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    for start_sec, end_sec, pitch, vel in mel_notes_list:
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, end_sec)
        RPR.RPR_MIDI_InsertNote(take_mel, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_mel)

    return f"Created 'Rule of 3' arrangement across {bars} bars on tracks '{track_name}_Chords' and '{track_name}_Melody' in {key} {scale} at {bpm} BPM."
