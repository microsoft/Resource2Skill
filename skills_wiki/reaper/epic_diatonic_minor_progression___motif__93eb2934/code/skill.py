def create_pattern(
    project_name: str = "CloudPiano_Project",
    track_name: str = "Cloud Chords & Melody",
    bpm: int = 120,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Epic Diatonic Minor Progression with a Top-Line Melody in REAPER.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    key_midi_base = NOTE_MAP.get(key.capitalize(), 5) # Default F
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Base octave for chords (e.g., Octave 4)
    OCTAVE_OFFSET = 48 
    root_midi = key_midi_base + OCTAVE_OFFSET

    # Helper to calculate diatonic pitch based on scale degree
    def get_pitch(degree):
        octave_shift = degree // 7
        scale_idx = degree % 7
        return root_midi + (octave_shift * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument & FX ===
    # ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower the harsh sawtooth, bring up triangle for a softer piano-like pluck
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) # Saw down
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.8) # Triangle up
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.05) # Quick Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.4) # Medium Decay
    
    # ReaEQ (Lowpass to make it atmospheric)
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 0, 0) # Tab 1
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 11, 4000) # Band 4 Freq
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 12, -12) # Band 4 Gain

    # ReaVerbate (Cloud atmosphere)
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.9) # Wet
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.2) # Dry
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.8) # Room size

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_note(pitch, start_beat, end_beat, velocity):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    # === Step 5: Generate Progression & Melody ===
    # Emotional minor progression: i - VII - VI - iv
    progression_degrees = [0, 6, 5, 3] 

    note_count = 0
    for bar in range(bars):
        # Loop progression if bars > 4
        chord_root_deg = progression_degrees[bar % len(progression_degrees)]
        bar_start_beat = bar * beats_per_bar
        
        # 1. BASS NOTE (Root - 2 Octaves)
        bass_pitch = get_pitch(chord_root_deg - 14)
        insert_note(bass_pitch, bar_start_beat, bar_start_beat + 4, velocity_base + 10)
        note_count += 1

        # 2. CHORD VOICING (Root, 3rd, 5th, Octave Root)
        chord_pitches = [
            get_pitch(chord_root_deg),       # Root
            get_pitch(chord_root_deg + 2),   # 3rd
            get_pitch(chord_root_deg + 4),   # 5th
            get_pitch(chord_root_deg + 7)    # Root + 1 Octave
        ]
        for pitch in chord_pitches:
            insert_note(pitch, bar_start_beat, bar_start_beat + 4, velocity_base - 10)
            note_count += 1

        # 3. QUESTION & ANSWER MELODY (Rhythmic Motif)
        # Melody shifts diatonically with the chord to stay perfectly in harmony
        is_question = (bar % 2 == 0)
        
        if is_question:
            # Rhythmic Motif A (Syncopated drop)
            m_notes = [
                (chord_root_deg + 11, 0.0, 0.5), # 5th (+1 oct)
                (chord_root_deg + 9, 1.5, 2.0),  # 3rd (+1 oct)
                (chord_root_deg + 8, 2.5, 3.0),  # 2nd (+1 oct)
                (chord_root_deg + 7, 3.0, 4.0)   # Root (+1 oct)
            ]
        else:
            # Rhythmic Motif B (Resolution variation)
            m_notes = [
                (chord_root_deg + 11, 0.0, 0.5),
                (chord_root_deg + 9, 1.5, 2.0),
                (chord_root_deg + 8, 2.5, 3.0),
                (chord_root_deg + 6, 3.0, 4.0)   # Drops down to 7th for tension/resolution
            ]

        for deg, b_start, b_end in m_notes:
            insert_note(get_pitch(deg), bar_start_beat + b_start, bar_start_beat + b_end, velocity_base)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
