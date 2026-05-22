def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Overridden internally to 12 bars to fit the 3-part structure
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Rule of 3 Arrangement Variation in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored here (hardcoded to 12 to demonstrate the 3x 4-bar concept).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    def get_pitch(degree: int, octave: int) -> int:
        """Converts a 1-based scale degree and octave to a MIDI pitch."""
        deg_idx = (degree - 1) % len(scale_intervals)
        oct_shift = (degree - 1) // len(scale_intervals)
        # MIDI note 60 is C4. (octave + 1) * 12 ensures octave 4 centers around 60.
        pitch = root_pitch + scale_intervals[deg_idx] + (octave + oct_shift + 1) * 12
        return max(0, min(127, pitch))

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Define the Musical Phrases ===
    # Format: (degree, octave, start_beat, duration_in_beats)
    
    # Phrase A: The established idea (I - V - vi - IV)
    phrase_A = [
        # Bar 1 (I)
        (1,3, 0,4), (3,3, 0,4), (5,3, 0,4),             # Block chord
        (1,5, 0,1), (2,5, 1,1), (3,5, 2,1), (2,5, 3,1), # Melody
        # Bar 2 (V)
        (5,2, 4,4), (7,2, 4,4), (9,2, 4,4),             
        (0,5, 4,1), (1,5, 5,1), (2,5, 6,1), (1,5, 7,1), 
        # Bar 3 (vi)
        (6,2, 8,4), (8,2, 8,4), (10,2, 8,4),            
        (6,4, 8,1), (7,4, 9,1), (8,4, 10,1), (7,4, 11,1), 
        # Bar 4 (IV)
        (4,2, 12,4), (6,2, 12,4), (8,2, 12,4),            
        (4,4, 12,1), (6,4, 13,1), (8,4, 14,1), (6,4, 15,1),
    ]

    # Phrase A': The variation for the 3rd iteration (Starts same, ends on ii - V)
    phrase_A_prime = [
        # Bar 1 (I) - Same
        (1,3, 0,4), (3,3, 0,4), (5,3, 0,4),
        (1,5, 0,1), (2,5, 1,1), (3,5, 2,1), (2,5, 3,1),
        # Bar 2 (V) - Same
        (5,2, 4,4), (7,2, 4,4), (9,2, 4,4),
        (0,5, 4,1), (1,5, 5,1), (2,5, 6,1), (1,5, 7,1),
        # Bar 3 (ii) - DIFFERENT
        (2,3, 8,4), (4,3, 8,4), (6,3, 8,4),
        (2,5, 8,1), (4,5, 9,1), (6,5, 10,1), (4,5, 11,1),
        # Bar 4 (V) - DIFFERENT
        (5,3, 12,4), (7,3, 12,4), (9,3, 12,4),
        (5,5, 12,1), (4,5, 13,1), (2,5, 14,1), (0,5, 15,1),
    ]

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12  # We are hardcoding to 12 to showcase the 3x4-bar rule
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Sequence structure: Iteration 1 (A), Iteration 2 (A), Iteration 3 (A')
    sequence = ["A", "A", "A_prime"]
    
    total_notes_inserted = 0
    for phrase_idx, phrase_type in enumerate(sequence):
        beat_offset = phrase_idx * 16  # 4 bars * 4 beats
        active_phrase = phrase_A if phrase_type == "A" else phrase_A_prime
        
        for degree, octave, beat, dur in active_phrase:
            pitch = get_pitch(degree, octave)
            
            abs_beat = beat_offset + beat
            start_time = abs_beat * (60.0 / bpm)
            end_time = (abs_beat + dur) * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Lower velocity slightly for sustained chords, higher for melody
            vel = int(velocity_base * 0.7) if dur > 2 else velocity_base
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape ReaSynth to sound like a plucky piano rather than a harsh sine
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.4)   # Volume (attenuate)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.02)  # Fast Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.3)   # Medium Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.1)   # Low Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.4)   # Medium Release

    return f"Created '{track_name}' applying the 'Rule of 3' with {total_notes_inserted} notes over {total_bars} bars at {bpm} BPM."
