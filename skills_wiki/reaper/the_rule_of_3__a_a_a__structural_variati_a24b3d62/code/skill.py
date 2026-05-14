def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Overridden internally to 12 to satisfy the 3-iteration rule
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create the 'Rule of 3' Compositional Structure in the current REAPER project.
    Generates a 12-bar progression (A - A - A') separated into Chords and Melody tracks.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # === Setup Tempo and Root Pitch ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    root_midi = 60 + NOTE_MAP.get(key, 0)
    if root_midi > 65: # Keep root near middle C
        root_midi -= 12

    # === Helper Functions ===
    def get_diatonic_note(degree, base_midi, scale_name):
        scale_intervals = SCALES.get(scale_name, SCALES["major"])
        degree_idx = degree - 1
        octave = degree_idx // len(scale_intervals)
        s_idx = degree_idx % len(scale_intervals)
        return int(base_midi + scale_intervals[s_idx] + (12 * octave))

    def get_diatonic_chord(degree, base_midi, scale_name):
        # Build a standard triad using scale degrees
        return [get_diatonic_note(degree + i * 2, base_midi, scale_name) for i in range(3)]

    def insert_midi_note(take, start_qn, duration_qn, pitch, velocity):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn + duration_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, False)

    # We enforce exactly 12 bars (3 iterations of 4 bars) to illustrate the rule.
    beats_per_bar = 4
    total_qn = 12 * beats_per_bar
    item_length_sec = RPR.RPR_TimeMap2_QNToTime(0, total_qn)

    # ==========================================
    # TRACK 1: CHORDS (The Foundation)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name} - Chords", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_chords, "D_VOL", 0.4) # Push chords to background

    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", item_length_sec)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    # I - V - vi - IV
    phrase_A_chords = [1, 5, 6, 4]
    # I - V - ii - V (The turnaround variation)
    phrase_A_prime_chords = [1, 5, 2, 5]

    for iter_idx in range(3):
        start_bar = iter_idx * 4
        # Apply the Rule of 3: Change the structure on the 3rd iteration
        chords = phrase_A_chords if iter_idx < 2 else phrase_A_prime_chords
        for i, degree in enumerate(chords):
            start_qn = (start_bar + i) * beats_per_bar
            # Drop octave for foundational chords
            chord_notes = get_diatonic_chord(degree, root_midi - 12, scale) 
            for note in chord_notes:
                insert_midi_note(take_chords, start_qn, beats_per_bar, note, int(velocity_base * 0.7))

    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaVerbate", False, -1)

    # ==========================================
    # TRACK 2: MELODY (The Lead Variation)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_mel = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_mel, "P_NAME", f"{track_name} - Melody", True)

    item_mel = RPR.RPR_AddMediaItemToTrack(track_mel)
    RPR.RPR_SetMediaItemInfo_Value(item_mel, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_mel, "D_LENGTH", item_length_sec)
    take_mel = RPR.RPR_AddTakeToMediaItem(item_mel)

    # Format: (bar_offset, beat_offset, scale_degree, duration_in_beats)
    phrase_A_melody = [
        (0, 0, 3, 1), (0, 1.5, 5, 0.5), (0, 2, 8, 2),
        (1, 0, 2, 1), (1, 1.5, 5, 0.5), (1, 2, 7, 2),
        (2, 0, 1, 1), (2, 1.5, 3, 0.5), (2, 2, 6, 2),
        (3, 0, 1, 1), (3, 1.5, 4, 0.5), (3, 2, 6, 2)
    ]

    # Starts identically, but pivots on bars 3 and 4 to build upward tension
    phrase_A_prime_melody = [
        (0, 0, 3, 1), (0, 1.5, 5, 0.5), (0, 2, 8, 2),
        (1, 0, 2, 1), (1, 1.5, 5, 0.5), (1, 2, 7, 2),
        (2, 0, 4, 1), (2, 1.5, 6, 0.5), (2, 2, 9, 2),   # Traces ii chord
        (3, 0, 5, 1), (3, 1.5, 7, 0.5), (3, 2, 10, 2)   # Traces V chord, climbing up
    ]

    for iter_idx in range(3):
        start_bar = iter_idx * 4
        # Apply the Rule of 3: Change the melody on the 3rd iteration
        melody = phrase_A_melody if iter_idx < 2 else phrase_A_prime_melody
        for m in melody:
            bar_offset, beat_offset, degree, duration_beats = m
            start_qn = (start_bar + bar_offset) * beats_per_bar + beat_offset
            # Raise octave for lead line
            note = get_diatonic_note(degree, root_midi + 12, scale) 
            insert_midi_note(take_mel, start_qn, duration_beats, note, velocity_base)

    RPR.RPR_MIDI_Sort(take_mel)
    
    RPR.RPR_TrackFX_AddByName(track_mel, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_mel, "ReaDelay", False, -1)

    return f"Created 12-bar 'Rule of 3' Arrangement (A-A-A') across 2 tracks in {key} {scale} at {bpm} BPM."
