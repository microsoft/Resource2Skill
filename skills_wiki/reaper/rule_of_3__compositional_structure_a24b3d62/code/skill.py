def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a "Rule of 3" Compositional Structure in the current REAPER project.
    Generates an A - A - A' phrase structure where the 3rd repetition diverges 
    halfway through to keep the listener engaged.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars (will be divided into 3 phrases).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = 60 + NOTE_MAP.get(key, 0)
    if root_midi > 67: 
        root_midi -= 12 # Keep chords anchored around C3-G3

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Math for Time and Rhythm ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    item_length = beat_sec * beats_per_bar * bars
    
    # Divide the total bars exactly into 3 phrases to demonstrate the rule
    phrase_bars = bars / 3.0
    beats_per_phrase = phrase_bars * beats_per_bar
    chord_beats = beats_per_phrase / 4.0 # 4 chords per phrase
    time_scale = chord_beats / 4.0       # scalar for melody timing

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    notes_to_add = []
    
    def add_midi_note(pitch, start_beat, dur_beats, vel=velocity_base):
        notes_to_add.append((int(pitch), start_beat, dur_beats, int(vel)))

    def get_chord(degree, variation=""):
        # degree is 0-indexed scale degree
        l = len(scale_intervals)
        root = scale_intervals[degree % l] + (degree // l) * 12
        third = scale_intervals[(degree + 2) % l] + ((degree + 2) // l) * 12
        fifth = scale_intervals[(degree + 4) % l] + ((degree + 4) // l) * 12
        
        # Turn a minor V chord into a major V for stronger resolution in the variation
        if variation == "major_V" and degree == 4:
            third = root + 4
            
        return [root_midi - 12 + root, root_midi - 12 + third, root_midi - 12 + fifth]

    def get_mel_note(degree, variation=""):
        l = len(scale_intervals)
        oct_shift = degree // l
        idx = degree % l
        pitch = scale_intervals[idx] + (oct_shift * 12)
        
        # Add a raised leading tone on the V chord if needed
        if variation == "leading_tone" and degree == 6:
            if scale_intervals[6] == 10: # If it's a minor 7th, raise it to major 7th
                pitch += 1
                
        return root_midi + 12 + pitch # Melody sits an octave above chords

    # === Step 4: Generate the "Rule of 3" Composition ===
    for phrase_idx in range(3):
        phrase_start_beat = phrase_idx * beats_per_phrase
        is_variation = (phrase_idx == 2) # The crucial 3rd repetition subversion
        
        # Determine chords for this phrase
        ch_1 = get_chord(0) # Tonic
        ch_2 = get_chord(5) # Submediant
        ch_3 = get_chord(3) if is_variation else get_chord(2) # Subdominant vs Mediant
        ch_4 = get_chord(4, "major_V") if is_variation else get_chord(6) # Dominant vs Subtonic
        
        # Inject Chords
        for p in ch_1: add_midi_note(p, phrase_start_beat + chord_beats * 0, chord_beats, velocity_base * 0.7)
        for p in ch_2: add_midi_note(p, phrase_start_beat + chord_beats * 1, chord_beats, velocity_base * 0.7)
        for p in ch_3: add_midi_note(p, phrase_start_beat + chord_beats * 2, chord_beats, velocity_base * 0.7)
        for p in ch_4: add_midi_note(p, phrase_start_beat + chord_beats * 3, chord_beats, velocity_base * 0.7)
        
        # Inject Melody
        # First half of the melody is ALWAYS identical (The rule)
        add_midi_note(get_mel_note(0), phrase_start_beat + 0, 2.0 * time_scale)
        add_midi_note(get_mel_note(2), phrase_start_beat + 2.0 * time_scale, 1.0 * time_scale)
        add_midi_note(get_mel_note(1), phrase_start_beat + 3.0 * time_scale, 1.0 * time_scale)
        
        add_midi_note(get_mel_note(0), phrase_start_beat + chord_beats + 0, 2.0 * time_scale)
        add_midi_note(get_mel_note(-1), phrase_start_beat + chord_beats + 2.0 * time_scale, 2.0 * time_scale)
        
        # Second half of the melody varies ONLY on the 3rd repetition (The subversion)
        if not is_variation:
            add_midi_note(get_mel_note(-1), phrase_start_beat + chord_beats * 2 + 0, 2.0 * time_scale)
            add_midi_note(get_mel_note(4), phrase_start_beat + chord_beats * 2 + 2.0 * time_scale, 1.0 * time_scale)
            add_midi_note(get_mel_note(3), phrase_start_beat + chord_beats * 2 + 3.0 * time_scale, 1.0 * time_scale)
            
            add_midi_note(get_mel_note(2), phrase_start_beat + chord_beats * 3 + 0, 2.0 * time_scale)
            add_midi_note(get_mel_note(1), phrase_start_beat + chord_beats * 3 + 2.0 * time_scale, 2.0 * time_scale)
        else:
            add_midi_note(get_mel_note(3), phrase_start_beat + chord_beats * 2 + 0, 2.0 * time_scale)
            add_midi_note(get_mel_note(1), phrase_start_beat + chord_beats * 2 + 2.0 * time_scale, 2.0 * time_scale)
            
            add_midi_note(get_mel_note(4), phrase_start_beat + chord_beats * 3 + 0, 2.0 * time_scale)
            add_midi_note(get_mel_note(6, "leading_tone"), phrase_start_beat + chord_beats * 3 + 2.0 * time_scale, 2.0 * time_scale)

    # === Step 5: Write MIDI and FX ===
    RPR.RPR_MIDI_DisableSort(take)
    for pitch, start_beat, dur_beats, vel in notes_to_add:
        # Prevent any possible out of bounds velocities
        vel = max(1, min(127, vel))
        start_pos = start_beat * beat_sec
        end_pos = (start_beat + dur_beats) * beat_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
        
    RPR.RPR_MIDI_Sort(take)

    # Configure ReaSynth to make the arrangement clear and plucky
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.3)  # Add sawtooth bite
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.0)  # Remove pulse width
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.02) # Snappy Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.3)  # Short Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 8, 0.4)  # Lower Sustain level

    return f"Created '{track_name}' using {len(notes_to_add)} notes over {bars} bars at {bpm} BPM, subverting the pattern on phrase 3."
