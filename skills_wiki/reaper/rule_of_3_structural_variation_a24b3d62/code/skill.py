def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a 12-bar progression demonstrating the "Rule of 3" structural variation.
    Plays a 4-bar idea twice, then varies the chords and melody on the 3rd repetition.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (forced to at least 12 to demonstrate the 3-repetition rule).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup Instrument and FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.4) # Sawtooth
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.4) # Square
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.05) # Attack (snappy)
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.4)  # Sustain
    
    # Add light reverb to glue it together
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.15) # Wet mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.85) # Dry mix

    # === Step 4: Create MIDI Item ===
    # Force at least 12 bars to properly demonstrate the 3-repetition rule
    total_bars = max(12, bars)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * total_bars)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Music Theory Engine ===
    root_pitch = NOTE_MAP.get(key.upper(), 0)
    scale_arr = SCALES.get(scale.lower(), SCALES["major"])

    def get_pitch(deg, octv):
        """Calculates exact MIDI pitch using diatonic scale degrees"""
        octave_offset = deg // len(scale_arr)
        scale_idx = deg % len(scale_arr)
        return root_pitch + (octv * 12) + (octave_offset * 12) + scale_arr[scale_idx]

    note_count = 0
    
    # Generate the pattern bar by bar
    for bar_idx in range(total_bars):
        # Determine where we are in the 12-bar (3 repetition) macro structure
        rep_within_macro = (bar_idx // 4) % 3
        bar_within_rep = bar_idx % 4
        
        # Rule of 3 Logic: Reps 1 & 2 are identical. Rep 3 goes somewhere different.
        if rep_within_macro == 2:
            degrees = [0, 4, 1, 4] # I - V - ii - V (Creates variation)
            is_turnaround = (bar_within_rep == 3) # Apply rhythmic change on the final bar
        else:
            degrees = [0, 4, 5, 3] # I - V - vi - IV (Standard pop progression)
            is_turnaround = False
            
        degree = degrees[bar_within_rep]
        start_qn = bar_idx * 4

        # --- Harmony (Chords) ---
        c_root = get_pitch(degree, 5)   # Octave 5 (approx MIDI note 60 / C4)
        c_third = get_pitch(degree + 2, 5)
        c_fifth = get_pitch(degree + 4, 5)

        for pitch in [c_root, c_third, c_fifth]:
            RPR.RPR_MIDI_InsertNote(take, False, False, int(start_qn * 960), int((start_qn + 4) * 960), 0, pitch, 75, True)
            note_count += 1

        # --- Melody ---
        if not is_turnaround:
            # Standard melodic rhythm: Rest 1 beat, then play three 1/4 notes
            m_notes = [
                get_pitch(degree + 2, 6), # 3rd
                get_pitch(degree + 4, 6), # 5th
                get_pitch(degree + 7, 6)  # Octave
            ]
            for i, m_n in enumerate(m_notes):
                n_start_qn = start_qn + 1 + i
                RPR.RPR_MIDI_InsertNote(take, False, False, int(n_start_qn * 960), int((n_start_qn + 1) * 960), 0, m_n, velocity_base, True)
                note_count += 1
        else:
            # Turnaround rhythm: Dense 1/8th notes building in velocity to create tension
            m_notes = [
                get_pitch(degree, 6),
                get_pitch(degree + 2, 6),
                get_pitch(degree + 4, 6),
                get_pitch(degree + 7, 6),
                get_pitch(degree + 4, 6),
                get_pitch(degree + 2, 6),
                get_pitch(degree, 6),
                get_pitch(degree - 1, 6) # Leading tone
            ]
            for i, m_n in enumerate(m_notes):
                n_start_qn = start_qn + (i * 0.5)
                vel = min(127, velocity_base + (i * 4)) # Increasing intensity
                RPR.RPR_MIDI_InsertNote(take, False, False, int(n_start_qn * 960), int((n_start_qn + 0.5) * 960), 0, m_n, vel, True)
                note_count += 1

    # Apply all note insertions at once
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating the Rule of 3 (12-bar phrase, {note_count} notes) at {bpm} BPM in {key} {scale}."
