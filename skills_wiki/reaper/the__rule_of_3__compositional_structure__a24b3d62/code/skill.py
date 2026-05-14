def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Arranger",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar 'Rule of 3' structural arrangement in the current REAPER project.
    Generates an A-A-A' chord progression and melody to demonstrate expectation deviation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, etc.).
        bars: Number of bars (default 12 to complete the 3-repetition rule).
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

    # === Step 1: Initialization & Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    root_midi = 48 + NOTE_MAP.get(key, 0) # Center around C3
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Timing calculations
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = bars if bars > 0 else 12 
    item_length = bar_length_sec * total_bars

    # === Step 2: Create Additive Track & Item ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Structural Logic (The Rule of 3) ===
    # A 12-bar sequence (Rep 1, Rep 2, Rep 3 Deviation) mapped 1-indexed to scale degrees
    progression = [
        1, 5, 6, 4, # Rep 1: Idea A
        1, 5, 6, 4, # Rep 2: Reinforce Idea A
        1, 5, 2, 5  # Rep 3: Start same, deviate to ii-V turnaround
    ]
    
    # Motif instructions per bar
    motifs = [
        "A", "A", "A", "A",     # Constant 1/8th ostinato
        "A", "A", "A", "A",
        "A", "A", "B0", "B1"    # Deviation drops to 1/4 note resolution
    ]

    def get_pitch(degree, chord_degree, octave_offset=0):
        deg_idx = degree - 1
        scale_idx = deg_idx + chord_degree
        octave_shift = (scale_idx // len(scale_intervals)) * 12 + (octave_offset * 12)
        rem_idx = scale_idx % len(scale_intervals)
        p = root_midi + scale_intervals[rem_idx] + octave_shift
        # Clamp to reasonable MIDI ranges
        while p < 24: p += 12
        while p > 108: p -= 12
        return int(p)

    def add_note(start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Generate MIDI Notes
    for i in range(total_bars):
        bar_start = i * bar_length_sec
        seq_i = i % 12
        degree = progression[seq_i]
        motif = motifs[seq_i]

        # Element 1: Foundational Chords (Transposed down 1 octave, quieter)
        chord_vel = min(127, int(velocity_base * 0.75))
        for c_deg in [0, 2, 4]:  # Root, 3rd, 5th of the chord
            pitch = get_pitch(degree, c_deg, -1)
            add_note(bar_start, bar_start + bar_length_sec * 0.95, pitch, chord_vel)

        # Element 2: Top Line Melody / Motif (Transposed up 1 octave)
        if motif == "A":
            # 1/8th note arpeggio: 1st, 3rd, 5th, 3rd of the chord
            chord_degrees = [0, 2, 4, 2, 0, 2, 4, 2]
            note_len = bar_length_sec / 8.0
            for j, c_deg in enumerate(chord_degrees):
                start_t = bar_start + j * note_len
                pitch = get_pitch(degree, c_deg, 1)
                add_note(start_t, start_t + note_len * 0.8, pitch, velocity_base)
                
        elif motif == "B0":
            # 1/4 note rising scale run
            chord_degrees = [0, 1, 2, 3]
            note_len = bar_length_sec / 4.0
            for j, c_deg in enumerate(chord_degrees):
                start_t = bar_start + j * note_len
                pitch = get_pitch(degree, c_deg, 1)
                add_note(start_t, start_t + note_len * 0.8, pitch, min(127, velocity_base + 5))
                
        elif motif == "B1":
            # 1/4 note strong dominant landing
            chord_degrees = [4, 4, 0, 0] # 5th, 5th, Root, Root
            note_len = bar_length_sec / 4.0
            for j, c_deg in enumerate(chord_degrees):
                start_t = bar_start + j * note_len
                pitch = get_pitch(degree, c_deg, 1)
                add_note(start_t, start_t + note_len * 0.8, pitch, min(127, velocity_base + 10))

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instrument and Effects ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.20)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.02)  # Attack (fast but clickless)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.30)  # Release (moderate tail)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 7, 0.40)  # Add Saw mix for warmth

    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.25) # Wet Mix
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 0.80) # Dry Mix
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 2, 0.60) # Room Size

    return f"Created '{track_name}' applying the 'Rule of 3' arrangement structure over {total_bars} bars at {bpm} BPM in {key} {scale}"
