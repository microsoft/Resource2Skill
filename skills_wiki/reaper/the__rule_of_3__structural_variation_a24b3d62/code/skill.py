def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Concept",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # The Rule of 3 fundamentally requires 12 bars (3 iterations of 4 bars)
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a 12-bar composition demonstrating the 'Rule of 3' in the current REAPER project.
    Plays an idea twice, then breaks the pattern halfway through the third repetition.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Forces 12 bars to properly demonstrate the structural concept.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
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

    root_midi = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)

    def get_pitch(degree, octave):
        """Converts a scale degree into an absolute MIDI pitch."""
        oct_offset = degree // scale_len
        rem_deg = degree % scale_len
        # +1 because octave 3 is MIDI note 48 (C3)
        return root_midi + (octave + oct_offset + 1) * 12 + scale_intervals[rem_deg]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # Hardcoded to 12 to fulfill the 'Rule of 3' iterations
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_note(pitch, start_beat, length_beats, velocity):
        """Helper to insert quantized notes using project time calculation."""
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    # Note generation loop over 3 identical-length blocks
    notes_created = 0
    for block in range(3):
        # The core of the Rule of 3:
        # Blocks 0 and 1 play Progression A. Block 2 plays Progression B.
        # Prog A: generic IV-V-iii-vi. Prog B starts same, but resolves differently.
        prog = [3, 4, 2, 5] if block < 2 else [3, 4, 1, 0]

        for bar, chord_deg in enumerate(prog):
            global_bar = (block * 4) + bar
            start_beat = global_bar * 4

            # --- 1. Generate Underlying Harmony (Chords) ---
            # Root, 3rd, 5th intervals
            for interval in [0, 2, 4]:
                chord_pitch = get_pitch(chord_deg + interval, 3) 
                insert_note(chord_pitch, start_beat, 4.0, max(10, velocity_base - 15))
                notes_created += 1

            # --- 2. Generate Lead Melody ---
            if bar < 2 or block < 2:
                # MOTIF 1: Predictable, establishing pattern
                insert_note(get_pitch(chord_deg + 2, 4), start_beat + 0.0, 1.0, velocity_base)
                insert_note(get_pitch(chord_deg + 4, 4), start_beat + 1.0, 1.0, velocity_base)
                insert_note(get_pitch(chord_deg + 2, 4), start_beat + 2.0, 2.0, velocity_base)
                notes_created += 3
            else:
                # MOTIF 2: The "Rule of 3" deviation / pattern break
                # Speeds up rhythmically to 1/8th notes to emphasize the structural change
                if bar == 2:
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 0.0, 1.0, velocity_base + 10)
                    insert_note(get_pitch(chord_deg + 4, 4), start_beat + 1.0, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 1.5, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 0, 4), start_beat + 2.0, 2.0, velocity_base)
                    notes_created += 4
                elif bar == 3:
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 0.0, 1.0, velocity_base + 10)
                    insert_note(get_pitch(chord_deg + 0, 4), start_beat + 1.0, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 1, 4), start_beat + 1.5, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 2.0, 2.0, max(10, velocity_base - 10))
                    notes_created += 4

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add a stock synth and delay to give the pattern atmosphere
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, 1)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, 1)

    return f"Created '{track_name}' demonstrating Rule of 3 ({notes_created} notes over {total_bars} bars at {bpm} BPM in {key} {scale})"
