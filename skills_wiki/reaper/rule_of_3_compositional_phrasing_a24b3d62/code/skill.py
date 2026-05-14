def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a multi-track composition demonstrating the "Rule of 3" phrasing structure.
    Generates an Idea (A), a Reinforcement (A), and a Departure (B) sequence.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks (Chords and Melody).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Total number of bars for the entire structure (defaults to 12).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Music Theory Lookup Tables ===
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

    # === Step 2: Pitch & Time Math Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    def get_midi_note(degree, octave):
        """Converts a 0-indexed scale degree into an absolute MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_degree = degree % len(scale_intervals)
        return root_val + scale_intervals[scale_degree] + (octave + octave_shift) * 12

    def get_triad(degree, octave):
        """Builds a root-position diatonic triad."""
        return [
            get_midi_note(degree, octave),
            get_midi_note(degree + 2, octave),
            get_midi_note(degree + 4, octave)
        ]

    # Calculate precise time scalings to stretch the pattern to the requested 'bars'
    total_bars = float(bars)
    phrase_bars = total_bars / 3.0       # Divide total bars into 3 equal phrases
    time_scale = phrase_bars / 4.0       # Scale factor relative to a standard 4-bar phrase template
    
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length_sec = beat_length * beats_per_bar
    item_length_sec = total_bars * bar_length_sec

    # === Step 3: Define Rule of 3 Musical Sequence ===
    # Phrase A: I - IV - vi - V
    phrase_a_chords = [0, 3, 5, 4] 
    phrase_a_melody = [
        # (relative_start_bar, relative_end_bar, scale_degree, octave)
        (0.0, 0.5, 2, 5), (0.5, 1.0, 2, 5),  # Bar 1 (over I)
        (1.0, 1.5, 5, 4), (1.5, 2.0, 5, 4),  # Bar 2 (over IV)
        (2.0, 2.5, 0, 5), (2.5, 3.0, 0, 5),  # Bar 3 (over vi)
        (3.0, 4.0, 6, 4),                    # Bar 4 (over V)
    ]
    
    # Phrase B (Departure): Starts identical to A, changes at Bar 3 to ii - V
    phrase_b_chords = [0, 3, 1, 4]
    phrase_b_melody = [
        (0.0, 0.5, 2, 5), (0.5, 1.0, 2, 5),  # Bar 1 (over I - Identical)
        (1.0, 1.5, 5, 4), (1.5, 2.0, 5, 4),  # Bar 2 (over IV - Identical)
        (2.0, 2.5, 3, 5), (2.5, 3.0, 3, 5),  # Bar 3 (over ii - DEPARTURE)
        (3.0, 4.0, 1, 5),                    # Bar 4 (over V - DEPARTURE)
    ]
    
    # The Tri-Partite Structure
    phrases = [
        (phrase_a_chords, phrase_a_melody), # 1: Idea
        (phrase_a_chords, phrase_a_melody), # 2: Reinforcement
        (phrase_b_chords, phrase_b_melody), # 3: Departure
    ]

    # === Step 4: Create Tracks and Synths ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Chords Track (Soft Triangle Pad)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)
    
    idx_chord = RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 8, 0.8) # Triangle mix
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 2, 0.1) # Attack
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 5, 0.3) # Release
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 0, 0.3) # Volume

    item_chords = RPR.RPR_CreateNewMIDIItemInProj(track_chords, 0.0, item_length_sec, False)
    take_chords = RPR.RPR_GetActiveTake(item_chords)

    # Melody Track (Sharp Saw Lead)
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_mel = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_mel, "P_NAME", f"{track_name}_Melody", True)
    
    idx_mel = RPR.RPR_TrackFX_AddByName(track_mel, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 7, 0.7) # Saw mix
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 2, 0.02) # Attack
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 5, 0.1) # Release
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 0, 0.5) # Volume

    item_mel = RPR.RPR_CreateNewMIDIItemInProj(track_mel, 0.0, item_length_sec, False)
    take_mel = RPR.RPR_GetActiveTake(item_mel)

    # === Step 5: Inject MIDI Sequence ===
    for phrase_idx, (chords, melody) in enumerate(phrases):
        phrase_start_sec = phrase_idx * phrase_bars * bar_length_sec
        
        # Inject Chords
        for chord_idx, chord_deg in enumerate(chords):
            # Base template assumes 1 chord per bar
            rel_start_bar = chord_idx * 1.0
            rel_end_bar = (chord_idx + 1) * 1.0
            
            chord_start_sec = phrase_start_sec + (rel_start_bar * time_scale * bar_length_sec)
            chord_end_sec = phrase_start_sec + (rel_end_bar * time_scale * bar_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, chord_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, chord_end_sec)
            
            for pitch in get_triad(chord_deg, 4):  # Base Octave 4
                RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base * 0.75), True)
                
        # Inject Melody
        for (rel_start_bar, rel_end_bar, degree, octave) in melody:
            note_start_sec = phrase_start_sec + (rel_start_bar * time_scale * bar_length_sec)
            note_end_sec = phrase_start_sec + (rel_end_bar * time_scale * bar_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, note_end_sec)
            
            pitch = get_midi_note(degree, octave)
            RPR.RPR_MIDI_InsertNote(take_mel, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), True)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_mel)

    return f"Created Rule of 3 Structural Arrangement ('{track_name}_Chords' & '{track_name}_Melody') over {bars} bars at {bpm} BPM in {key} {scale}."
