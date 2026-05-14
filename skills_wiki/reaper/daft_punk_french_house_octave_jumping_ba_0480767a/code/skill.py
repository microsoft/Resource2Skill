def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Octave Funk Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a French House Octave-Jumping Bassline in the current REAPER project.

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
        Status string describing the created track and notes.
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

    # === Step 3: Add FX Chain (Synth & Tone) ===
    # Add native synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tune ReaSynth for a plucky bass tone:
    # Param 2 is Attack (0 = fast), Param 5 is Release (short)
    # Param 6 is Square mix (turn up for hollow funk sound), Param 0 is Vol
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)    # Fast Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.3)    # Plucky Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.1)    # Low Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.8)    # Square wave mix
    
    # Add EQ to beef up low-mids and roll off harsh digital highs
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0.0)       # Band 1 Freq (Low Shelf)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 2.0)       # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, -12.0)    # Band 4 Gain (High-cut)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    qn_length_sec = 60.0 / bpm
    bar_length_sec = qn_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Octave Groove ===
    # 16th note grid positions in a 4/4 bar (0 to 15)
    # Tuple format: (16th_offset, is_octave_jump)
    funk_groove_mask = [
        (0, False),  # 1
        (2, False),  # &
        (3, True),   # a (Octave)
        (5, False),  # e
        (7, True),   # a (Octave)
        (8, False),  # 3
        (10, False), # &
        (11, True),  # a (Octave)
        (13, False), # e
        (14, True),  # a (Octave)
    ]

    base_root_midi = 24 + NOTE_MAP.get(key.upper(), 0) # Octave 1/2 bass range
    selected_scale = SCALES.get(scale.lower(), SCALES["minor"])
    
    # A classic French House progression pattern traversing the scale (e.g., i - v - VI - iv)
    progression_degrees = [0, 4, 5, 3] 

    sixteenth_length_sec = qn_length_sec / 4.0
    staccato_duration = sixteenth_length_sec * 0.75 # 75% of a 16th note for bounce
    
    note_count = 0

    for bar in range(bars):
        # Determine the root note for this specific bar
        scale_degree = progression_degrees[bar % len(progression_degrees)]
        # Map degree safely to the scale array
        semitone_offset = selected_scale[scale_degree % len(selected_scale)]
        current_chord_root = base_root_midi + semitone_offset

        for offset, is_octave in funk_groove_mask:
            start_time = (bar * bar_length_sec) + (offset * sixteenth_length_sec)
            end_time = start_time + staccato_duration

            # Convert to PPQ for exact MIDI placement
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Apply octave leap and dynamic velocity (octaves slightly softer for groove)
            pitch = current_chord_root + 12 if is_octave else current_chord_root
            vel = max(1, velocity_base - 15) if is_octave else velocity_base

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} funk octave bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
