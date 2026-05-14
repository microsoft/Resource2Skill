def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Bass",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    progression: list = [4, 1], # Default scale degrees (iv -> i)
    **kwargs,
) -> str:
    """
    Create a 'Viral R&B/Neo-Soul Bassline Formula' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        progression: List of scale degrees to outline per bar (1-indexed).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Calculate Timing & Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    base_note = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    ppq_per_qn = 960

    # === Step 5: Insert MIDI Notes ===
    for bar in range(bars):
        bar_start_ppq = bar * ppq_per_qn * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Calculate root pitch (Octave 2 for bass)
        deg_idx = (chord_degree - 1) % len(scale_intervals)
        octave_shift = (chord_degree - 1) // len(scale_intervals)
        semitones = scale_intervals[deg_idx]
        root_pitch = (2 + octave_shift + 1) * 12 + base_note + semitones

        # Formula Pattern: (start_qn, end_qn, pitch_offset, vel_offset)
        notes = [
            (0.0, 1.0, 0, 0),       # Beat 1: Root downbeat
            (1.5, 2.0, 12, -10),    # Beat 2.5: Octave jump syncopation
            (2.5, 3.0, 0, -5),      # Beat 3.5: Root syncopation
            (3.0, 3.5, 7, -15),     # Beat 4.0: Perfect 5th passing
            (3.5, 4.0, 10, -10),    # Beat 4.5: Minor 7th passing
        ]

        for start_qn, end_qn, pitch_offset, vel_offset in notes:
            start_ppq = int(bar_start_ppq + start_qn * ppq_per_qn)
            end_ppq = int(bar_start_ppq + end_qn * ppq_per_qn)
            pitch = max(0, min(127, root_pitch + pitch_offset))
            vel = max(1, min(127, velocity_base + vel_offset))
            
            # Insert note, deferring sort for performance
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add Instrument FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a bouncy Neo-Soul Sub Bass
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.4)   # Volume (to prevent clipping)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.25)  # Square Mix (adds mid harmonics)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5)   # Triangle Mix (warmth)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.05)  # Quick Release (tightness)

    return f"Created '{track_name}' bassline over {bars} bars at {bpm} BPM in {key} {scale}"
