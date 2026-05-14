def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, 
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create the 'Rule of 3' Progression pattern in REAPER.
    Generates a 12-bar sequence (three 4-bar phrases) demonstrating how to 
    deviate on the 3rd repetition to hold listener interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored here; strictly locked to 12 bars to demonstrate the 3x4 phrase rule.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # Safe defaults
    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "major"
    
    root_pitch = NOTE_MAP[key] + 48 # Root at C3
    scale_intervals = SCALES[scale]
    
    # Helper to get diatonic pitches
    def get_scale_pitch(root, intervals, degree):
        octave = degree // len(intervals)
        note_idx = degree % len(intervals)
        return root + (octave * 12) + intervals[note_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    # We strictly use 12 bars to demonstrate the Rule of 3 (4 bars x 3 iterations)
    total_bars = 12
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: The Rule of 3 Logic & Note Insertion ===
    # Phrase structure based on scale degrees (0-indexed). 
    # Example in Major: 3=IV, 4=V, 5=vi, 2=iii, 1=ii, 0=I
    phrases = [
        [3, 4, 5, 2], # Phrase 1: Standard loop (IV - V - vi - iii)
        [3, 4, 5, 2], # Phrase 2: Identical repetition to reinforce idea
        [3, 4, 1, 0]  # Phrase 3: The Deviation (IV - V - ii - I)
    ]

    ppq_per_quarter = 960
    ppq_per_bar = ppq_per_quarter * 4
    note_count = 0

    for phrase_idx, phrase_chords in enumerate(phrases):
        for bar_idx, chord_degree in enumerate(phrase_chords):
            # Calculate timing
            start_ppq = (phrase_idx * 4 + bar_idx) * ppq_per_bar
            end_ppq = start_ppq + ppq_per_bar - 120 # leave a slight gap between chords
            
            # Generate diatonic triad
            pitches = [
                get_scale_pitch(root_pitch, scale_intervals, chord_degree - 7), # Bass octave down
                get_scale_pitch(root_pitch, scale_intervals, chord_degree),     # Root
                get_scale_pitch(root_pitch, scale_intervals, chord_degree + 2), # 3rd
                get_scale_pitch(root_pitch, scale_intervals, chord_degree + 4), # 5th
            ]
            
            # Insert notes
            for pitch in pitches:
                pitch_clamped = max(0, min(127, pitch)) # Safety clamp
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch_clamped, velocity_base, False)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Stock Instrument (ReaSynth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a soft electric piano/pad feel instead of harsh default sine
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)   # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.8)   # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.3)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4)   # Release

    return f"Created '{track_name}' showcasing the 'Rule of 3' (12 bars, 3 phrases). Deviated harmonically on phrase 3. Inserted {note_count} notes at {bpm} BPM in {key} {scale}."
