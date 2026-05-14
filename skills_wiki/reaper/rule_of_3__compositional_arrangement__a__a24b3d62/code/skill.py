def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a 12-bar chord progression demonstrating the "Rule of 3" structural arrangement.
    Plays a 4-bar phrase twice to establish a pattern, then diverges on the third play
    to maintain listener interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Overridden internally to 12 to mathematically satisfy the Rule of 3 structure.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    # Enforce 12 bars for the Rule of 3 structure (3 phrases of 4 bars)
    total_bars = 12 
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Add MIDI Notes ===
    root_val = NOTE_MAP.get(key, 0)
    root_midi = 60 + root_val # Center around C4
    scale_intervals = SCALES.get(scale, SCALES["major"])

    def get_degree_pitch(root, scale_arr, degree, octave_shift=0):
        """Computes the exact MIDI pitch for a given diatonic scale degree."""
        idx = degree - 1
        octaves = idx // len(scale_arr)
        rem = idx % len(scale_arr)
        return root + scale_arr[rem] + ((octaves + octave_shift) * 12)

    def insert_note_qn(take_ptr, start_qn, end_qn, pitch, vel):
        """Safely inserts a MIDI note using Project Quarter Notes."""
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_ptr, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_ptr, end_qn)
        RPR.RPR_MIDI_InsertNote(take_ptr, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    def add_rhythmic_chord(start_qn, degree, octave_shift=0):
        """Builds a diatonic triad and sequences it with a syncopated rhythm."""
        # Rhythm: Dotted quarter (1.5), Eighth (0.5), Half (2.0)
        rhythm_qns = [
            (0.0, 1.5),
            (1.5, 2.0),
            (2.0, 4.0)
        ]
        
        root_pitch = get_degree_pitch(root_midi, scale_intervals, degree, octave_shift)
        third_pitch = get_degree_pitch(root_midi, scale_intervals, degree + 2, octave_shift)
        fifth_pitch = get_degree_pitch(root_midi, scale_intervals, degree + 4, octave_shift)
        
        for r_start, r_end in rhythm_qns:
            s_pos = start_qn + r_start
            e_pos = start_qn + r_end
            
            # Root note is slightly louder for stability
            insert_note_qn(take, s_pos, e_pos, root_pitch, velocity_base)
            insert_note_qn(take, s_pos, e_pos, third_pitch, velocity_base - 15)
            insert_note_qn(take, s_pos, e_pos, fifth_pitch, velocity_base - 15)

    # ---------------------------------------------------------
    # The "Rule of 3" Arrangement Matrix
    # Format: (Scale Degree, Octave Shift, Duration in Bars)
    # ---------------------------------------------------------
    
    # Progression A: The establishing phrase (I - V - vi - IV)
    progression_A = [
        (1, 0, 1),   # I chord
        (5, -1, 1),  # V chord (Voiced downwards for smooth voice leading)
        (6, -1, 1),  # vi chord
        (4, -1, 1),  # IV chord
    ]

    # Progression B: The divergence (I - V - ii - V)
    progression_B = [
        (1, 0, 1),   # Starts identical to A (re-establishes pattern)
        (5, -1, 1),  # Still identical (tricks the listener)
        (2, 0, 1),   # Diverges to the ii chord! (Creates new tension)
        (5, 0, 1),   # Lifts up to a higher V chord to setup the next song section
    ]

    current_qn = 0.0
    
    # 1st Time: Introduce the idea
    for degree, oct_shift, duration in progression_A:
        add_rhythmic_chord(current_qn, degree, oct_shift)
        current_qn += duration * beats_per_bar

    # 2nd Time: Reinforce the idea
    for degree, oct_shift, duration in progression_A:
        add_rhythmic_chord(current_qn, degree, oct_shift)
        current_qn += duration * beats_per_bar

    # 3rd Time: Break the idea (The Rule of 3 in action)
    for degree, oct_shift, duration in progression_B:
        add_rhythmic_chord(current_qn, degree, oct_shift)
        current_qn += duration * beats_per_bar

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a soft electric piano / pad sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume Drop
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)   # Remove harsh Square
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Remove harsh Saw
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.8)   # Primary: Triangle wave
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.4)   # Sub/Body: Sine wave
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.02)  # Soft Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4)   # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.5)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.6)   # Long Release

    return f"Created '{track_name}' showcasing the Rule of 3 Arrangement over {total_bars} bars in {key} {scale} at {bpm} BPM."
