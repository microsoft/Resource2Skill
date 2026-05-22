def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Expressive Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 60,
    **kwargs,
) -> str:
    """
    Create a snapped MIDI chord progression with a humanized velocity swell.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). The swell peaks at +50 from this.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR
    import math

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track and add Synth ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth as a native stand-in for the Piano VST
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Music Theory Data ===
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

    root_val = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale, SCALES["major"])

    def get_pitch(degree, root, scale_intervals, octave=4):
        # Calculate pitch spanning across octaves if the degree > 7
        octave_shift = degree // 7
        scale_idx = degree % 7
        return (octave + octave_shift + 1) * 12 + root + scale_intervals[scale_idx]

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Chords and Swell Velocities ===
    progression = [0, 5, 3, 4]  # Classic I, vi, IV, V progression
    num_notes = bars * 8        # 8th note rhythm
    eighth_len_sec = (60.0 / bpm) / 2.0

    notes_created = 0
    for i in range(num_notes):
        # Change chord every bar
        bar_idx = (i // 8) % len(progression)
        degree = progression[bar_idx]

        # Automate Velocity Swell: Sine curve creates an organic arch/crescendo
        curve = math.sin(i * math.pi / (num_notes - 1)) if num_notes > 1 else 1.0
        vel = int(velocity_base + 50 * curve)
        vel = max(1, min(127, vel)) # Clamp between 1-127

        start_time = i * eighth_len_sec
        # Small gap (90% duration) to represent clear keystrokes
        end_time = start_time + eighth_len_sec * 0.9

        # Convert project time to PPQ for MIDI insertion
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        # Build triad (Root, 3rd, 5th)
        for inv in [0, 2, 4]:  
            pitch = get_pitch(degree + inv, root_val, intervals, octave=4)
            # Insert the MIDI Note into the buffer (noSort = True for performance)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            notes_created += 1

    # Sort the MIDI buffer once all notes are inserted
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM featuring an automated velocity swell."
