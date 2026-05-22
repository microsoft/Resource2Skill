def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Overridden to 12 internally to demonstrate the 3x4-bar rule
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' (A-A-A' form) compositional block in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Target length (Forces 12 bars to properly demonstrate the 3x4 phrase rule).
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    target_bars = 12 # Force 12 bars (3 blocks of 4 bars) to manifest the Rule of 3
    item_length = bar_length_sec * target_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Music Theory Math ===
    root_midi = 48 + NOTE_MAP.get(key, 0) # Octave 3 (Chords)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    def get_degree_pitch(degree, octave_offset=0):
        """Convert a 0-indexed scale degree into an exact MIDI pitch."""
        octaves = degree // 7
        rem = degree % 7
        return root_midi + ((octaves + octave_offset) * 12) + scale_intervals[rem]

    # Progression definitions (0-indexed scale degrees)
    # Phrase A: I - V - vi - IV
    progression_A = [0, 4, 5, 3] 
    # Phrase A' (Pivot): I - V - ii - V 
    progression_B = [0, 4, 1, 4]

    ppq_per_quarter = 960
    ppq_per_bar = ppq_per_quarter * 4
    note_count = 0

    # === Step 5: Generate "Rule of 3" MIDI Structure ===
    for block in range(3):
        # The 3rd block (index 2) pivots to progression_B
        current_prog = progression_A if block < 2 else progression_B

        for bar_in_block, degree in enumerate(current_prog):
            current_bar = (block * 4) + bar_in_block
            start_ppq = current_bar * ppq_per_bar
            end_ppq = start_ppq + ppq_per_bar

            # 1. Insert Chords (Whole notes holding the foundation)
            chord_offsets = [0, 2, 4] # Triad (Root, 3rd, 5th)
            for offset in chord_offsets:
                pitch = get_degree_pitch(degree + offset, octave_offset=0)
                # Slightly lower velocity for backing chords
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, max(10, velocity_base - 20), False)
                note_count += 1

            # 2. Insert Melody & Structural Variations
            if block < 2 or bar_in_block < 2:
                # Phrase A (and the identical start of Phrase A')
                # Simple melodic motif: 2 half notes
                mel_pitch1 = get_degree_pitch(degree, octave_offset=1)
                mel_pitch2 = get_degree_pitch(degree + 2, octave_offset=1)
                
                mid_ppq = start_ppq + (ppq_per_bar // 2)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, mid_ppq, 0, mel_pitch1, velocity_base, False)
                RPR.RPR_MIDI_InsertNote(take, False, False, mid_ppq, end_ppq, 0, mel_pitch2, velocity_base, False)
                note_count += 2
            else:
                # Phrase A' Pivot (The back-half of the 3rd repetition)
                # The "Rule of 3" variation: Rhythm shifts to quarter notes, melody ascends, velocity builds
                for q in range(4):
                    q_start = start_ppq + (q * ppq_per_quarter)
                    q_end = q_start + ppq_per_quarter
                    
                    # Arpeggiating upward to build tension
                    m_pitch = get_degree_pitch(degree + q, octave_offset=1) 
                    
                    # Velocity ramps up to emphasize the turnaround
                    build_velocity = min(127, velocity_base + (q * 6))
                    RPR.RPR_MIDI_InsertNote(take, False, False, q_start, q_end, 0, m_pitch, build_velocity, False)
                    note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add Basic FX ===
    # Add a stock synth so the chords and melody are audible
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the stock ReaSynth so it sounds like a pleasant keys/pad patch
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)  # Volume (avoid clipping)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5)  # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3)  # Pulse mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.4)  # Release time longer

    return f"Created '{track_name}' applying the 'Rule of 3' (A-A-A' form) with {note_count} notes over {target_bars} bars at {bpm} BPM."
