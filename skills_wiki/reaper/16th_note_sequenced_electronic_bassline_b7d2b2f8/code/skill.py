def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sequenced Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create 16th-Note Sequenced Electronic Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
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

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Calculate Pitches & Pattern ===
    # Start at octave 1 or 2 for a deep bass tone (C1 = 24)
    base_midi = 24 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Safely select the 3rd and 7th scale degrees (accounting for pentatonic lengths)
    idx_3rd = 2 if len(scale_intervals) > 5 else 1
    idx_7th = 6 if len(scale_intervals) > 5 else len(scale_intervals) - 1

    # 16-step sequence based on step sequencer logic
    # Numbers represent semitone intervals from the root. 'None' is a rest.
    seq_pattern = [
        0, 0, 12, None,                                    # 1 2 3 4
        scale_intervals[idx_3rd], None, 0, scale_intervals[idx_7th], # 5 6 7 8
        0, 0, 12, None,                                    # 9 10 11 12
        scale_intervals[idx_3rd], 0, scale_intervals[idx_7th], None  # 13 14 15 16
    ]

    # Length of a 16th note in seconds
    step_len_sec = (60.0 / bpm) / 4.0
    
    # Staccato multiplier (notes play for 75% of the step duration)
    gate_length = step_len_sec * 0.75 

    # Insert MIDI notes
    notes_added = 0
    for b in range(bars):
        for i, step_val in enumerate(seq_pattern):
            if step_val is not None:
                start_time = (b * bar_length_sec) + (i * step_len_sec)
                end_time = start_time + gate_length
                
                # Convert project time to PPQ (ticks) for the MIDI item
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                pitch = base_midi + step_val
                
                # Minor velocity variation for groove
                vel = velocity_base if i % 4 == 0 else int(velocity_base * 0.85)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Synth FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Turn volume down slightly to prevent clipping on the sub frequencies
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.4) 

    return f"Created '{track_name}' with {notes_added} sequenced notes over {bars} bars at {bpm} BPM."
