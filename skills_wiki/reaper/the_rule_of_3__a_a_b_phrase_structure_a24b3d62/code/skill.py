def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Creates a 12-bar compositional structure demonstrating the 'Rule of 3' (A/A/B structure).
    Bars 1-4: Phrase A
    Bars 5-8: Phrase A (Repetition)
    Bars 9-12: Phrase B (Deviation/Surprise)

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (Forces to 12 to mathematically demonstrate the 4-bar x 3 rule).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
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

    base_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)

    def get_midi_note(degree, octave):
        """Converts a scale degree (0-indexed) and octave to a MIDI pitch."""
        octave_offset = degree // scale_len
        scale_degree = degree % scale_len
        return base_pitch + (octave + octave_offset) * 12 + scale_intervals[scale_degree]

    # === Step 1: Initialize Project & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    # Force 12 bars to properly demonstrate A/A/B form (3 phrases of 4 bars)
    demo_bars = 12 
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * demo_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Generate Notes (Rule of 3 Structure) ===
    notes_to_add = [] # (start_beat, end_beat, degree, octave, velocity)

    # Phrase A block generation (Used for Iteration 1 and 2)
    def generate_phrase_a(start_bar_offset):
        start_beat = start_bar_offset * beats_per_bar
        # Chord Progression: i - ii - iii - V (relative degrees: 0, 1, 2, 4)
        chords = [0, 1, 2, 4]
        for i, chord_root in enumerate(chords):
            bar_start = start_beat + (i * beats_per_bar)
            bar_end = bar_start + beats_per_bar
            # Build triad
            notes_to_add.append((bar_start, bar_end, chord_root, 4, velocity_base - 10))
            notes_to_add.append((bar_start, bar_end, chord_root + 2, 4, velocity_base - 15))
            notes_to_add.append((bar_start, bar_end, chord_root + 4, 4, velocity_base - 15))
            
            # Simple Melody Motif: Quarter notes on beats 1, 2.5, and 4
            notes_to_add.append((bar_start + 0.0, bar_start + 1.0, chord_root, 5, velocity_base))
            notes_to_add.append((bar_start + 1.5, bar_start + 2.5, chord_root + 1, 5, velocity_base))
            notes_to_add.append((bar_start + 3.0, bar_start + 4.0, chord_root + 2, 5, velocity_base))

    # Phrase B block generation (The Rule of 3 Deviation)
    def generate_phrase_b(start_bar_offset):
        start_beat = start_bar_offset * beats_per_bar
        # Contrasting Progression: IV - I - VI - V (relative degrees: 3, 0, 5, 4)
        chords = [3, 0, 5, 4]
        for i, chord_root in enumerate(chords):
            bar_start = start_beat + (i * beats_per_bar)
            bar_end = bar_start + beats_per_bar
            # Build triad
            notes_to_add.append((bar_start, bar_end, chord_root, 4, velocity_base - 5))
            notes_to_add.append((bar_start, bar_end, chord_root + 2, 4, velocity_base - 10))
            notes_to_add.append((bar_start, bar_end, chord_root + 4, 4, velocity_base - 10))
            
            # Contrasting Melody Motif: Faster eighth notes, higher register, ascending tension
            notes_to_add.append((bar_start + 0.0, bar_start + 0.5, chord_root + 2, 5, velocity_base + 15))
            notes_to_add.append((bar_start + 0.5, bar_start + 1.0, chord_root + 3, 5, velocity_base + 15))
            notes_to_add.append((bar_start + 1.0, bar_start + 1.5, chord_root + 4, 5, velocity_base + 15))
            notes_to_add.append((bar_start + 2.0, bar_start + 3.5, chord_root + 5, 5, velocity_base + 15))

    # Apply the Rule of 3
    generate_phrase_a(0)   # 1st Time: Introduction
    generate_phrase_a(4)   # 2nd Time: Reinforcement/Expectation
    generate_phrase_b(8)   # 3rd Time: Deviation/Surprise (The Rule of 3)

    # === Step 4: Insert Notes into REAPER ===
    for start_b, end_b, deg, octv, vel in notes_to_add:
        start_pos = start_b * (60.0 / bpm)
        end_pos = end_b * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        pitch = get_midi_note(deg, octv)
        
        # Keep velocities strictly in bounds
        vel = max(1, min(127, int(vel)))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument & FX ===
    # Add stock ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the synth to make chords sound pleasant (Param 2 = Attack, Param 5 = Release)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.05) 
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.40) 

    # Add ReaEQ to roll off harsh high frequencies
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Set band 4 to Low Pass
    RPR.RPR_TrackFX_SetParam(track, 1, 12, 1.0) # Band 4 type (1 = Low Pass)
    RPR.RPR_TrackFX_SetParam(track, 1, 13, 1500.0) # Band 4 Frequency

    return f"Created '{track_name}' demonstrating Rule of 3 A/A/B form with {len(notes_to_add)} notes over {demo_bars} bars at {bpm} BPM in {key} {scale}."
