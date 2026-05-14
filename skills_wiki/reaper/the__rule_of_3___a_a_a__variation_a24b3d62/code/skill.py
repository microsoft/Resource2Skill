def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' A-A-A' chord progression in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Length of the base phrase (default 4). Total length will be bars * 3.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Override default if unchanged to provide context
    if track_name == "Drums":
        track_name = "Rule of 3 Keys"

    # === Music Theory Setup ===
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

    # Generate a massive array of scale notes across 8 octaves to prevent bounds errors
    base_midi = NOTE_MAP.get(key, 0) + 24 # Start at C1 / Octave 1
    scale_intervals = SCALES.get(scale, SCALES["major"])
    all_scale_notes = []
    for oct in range(8):
        for interval in scale_intervals:
            all_scale_notes.append(base_midi + (oct * 12) + interval)

    def get_diatonic_chord(degree: int, num_notes: int = 3, offset_octave: int = 2) -> list:
        """Returns a list of MIDI pitches for a diatonic chord built on 'degree' (1-indexed)."""
        base_idx = (offset_octave * len(scale_intervals)) + (degree - 1)
        return [all_scale_notes[base_idx + i * 2] for i in range(num_notes)]

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: FX Chain (ReaSynth) ===
    # Using ReaSynth to mock up a plucky electric piano sound to demonstrate the chords
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.2)  # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.01) # Fast attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5)  # Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.3)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.7)  # Saw mix

    # === Step 3: Rule of 3 Logic & MIDI Generation ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_iterations = 3
    total_bars = bars * total_iterations
    item_length = bar_length_sec * total_bars

    # Create MIDI Item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # Rhythmic syncopation: Beat 1, Beat 2.5 ("and" of 2), Beat 4
    rhythm_offsets = [0.0, 1.5, 3.0] 
    rhythm_durations = [1.0, 1.0, 0.5]

    for bar in range(total_bars):
        iteration = bar // bars
        bar_in_phrase = bar % bars

        # The Rule of 3 Concept: 
        # First 2 loops are identical. The 3rd loop deviates halfway.
        if iteration < 2:
            progression = [4, 1, 5, 6] # Familiar Theme A
        else:
            progression = [4, 1, 2, 5] # Theme A' (Diverges on the 3rd chord)

        # Map to the progression based on where we are in the phrase
        degree = progression[bar_in_phrase % len(progression)]
        chord_pitches = get_diatonic_chord(degree, num_notes=4, offset_octave=2)

        for off, dur in zip(rhythm_offsets, rhythm_durations):
            qn_start = (bar * beats_per_bar) + off
            qn_end = qn_start + dur
            
            start_time = qn_start * (60.0 / bpm)
            end_time = qn_end * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Insert chord notes
            for pitch in chord_pitches:
                # Add a tiny bit of humanization to velocities
                vel = min(127, max(1, int(velocity_base + (off * 5))))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating the Rule of 3 (A-A-A') over {total_bars} bars at {bpm} BPM."
