def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Creates a musical block demonstrating the 'Rule of 3' (A-A-B repetition/variation structure).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars to generate (will be divided into 3 phrases).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # Validate inputs
    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "major"
    
    root_midi = 48 + NOTE_MAP[key] # C3 Base
    scale_intervals = SCALES[scale]

    # Helper to calculate correct MIDI pitch based on scale degree
    def get_pitch(degree, octave_offset=0):
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_midi + (octave + octave_offset) * 12 + scale_intervals[idx]

    def get_triad(degree):
        # 1-3-5 chord voicings based on the active scale
        return [get_pitch(degree), get_pitch(degree+2), get_pitch(degree+4)]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth and configure as a plucky keys/piano sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.01) # Fast attack
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Medium decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.2)  # Low sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.4)  # Release

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Apply the "Rule of 3" Composition Logic ===
    # 12-chord macro sequence that executes the Rule of 3
    # Phrase A1 (Pattern Intro), Phrase A2 (Pattern Confirmed), Phrase B (The Subversion)
    macro_progression = [
        0, 4, 5, 3,  # Phrase A1 (e.g. I, V, vi, IV)
        0, 4, 5, 3,  # Phrase A2 (Repeats exact same idea)
        5, 3, 1, 4   # Phrase B  (Rule of 3 subversion: vi, IV, ii, V)
    ]
    
    total_chords = len(macro_progression)
    beats_per_chord = (bars * beats_per_bar) / float(total_chords)
    PPQ = 960  # Default pulses per quarter note in REAPER

    for i, degree in enumerate(macro_progression):
        start_beat = i * beats_per_chord
        # Make chords play for 80% of the duration so it breathes (legato envelope)
        end_beat = start_beat + (beats_per_chord * 0.8)

        start_tick = int(start_beat * PPQ)
        end_tick = int(end_beat * PPQ)

        notes = get_triad(degree)
        bass_pitch = get_pitch(degree, -1) # Add a solid root bass note

        # Insert Bass Note
        RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, bass_pitch, velocity_base + 10, False)
        
        # Insert Triad Notes
        for pitch in notes:
            # Humanize velocity slightly across chord stack
            vel = max(1, min(127, velocity_base - (pitch % 5)))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating Rule of 3 (A-A-B structure) with 12 chords over {bars} bars at {bpm} BPM in {key} {scale}."
