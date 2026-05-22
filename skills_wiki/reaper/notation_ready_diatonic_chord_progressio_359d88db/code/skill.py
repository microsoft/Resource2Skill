def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a notation-ready diatonic chord progression in the current REAPER project.

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
        Status string describing what was created.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    qn_length = 60.0 / bpm
    bar_length = qn_length * 4
    
    start_pos = RPR.RPR_GetCursorPosition()
    end_pos = start_pos + (bar_length * bars)
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_pos, end_pos, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Notation-Ready MIDI ===
    formatted_key = key.capitalize()
    root_val = NOTE_MAP.get(formatted_key, 9) # Default to A
    root_midi = root_val + 48 # Octave 3 for keyboard voicing
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_diatonic_triad(degree):
        chord = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            scale_idx = degree + i
            # Handle negative indices cleanly for octave shifting
            octave_shift = scale_idx // len(scale_intervals)
            rem_idx = scale_idx % len(scale_intervals)
            note = root_midi + scale_intervals[rem_idx] + (octave_shift * 12)
            chord.append(note)
        return chord
        
    # Progression degrees: i - VII - VI - VII
    progression = [0, -1, -2, -1]
    
    notes_created = 0
    for bar_idx in range(bars):
        degree = progression[bar_idx % len(progression)]
        chord = get_diatonic_triad(degree)
        
        bar_start = start_pos + (bar_idx * bar_length)
        
        # Rhythm Grid: Half note (beats 1-3), Quarter note (beat 3), Quarter note (beat 4)
        rhythms = [
            (0, 2),       
            (2, 3),       
            (3, 4)        
        ]
        
        for qn_start, qn_end in rhythms:
            t_start = bar_start + (qn_start * qn_length)
            t_end = bar_start + (qn_end * qn_length)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_end)
            
            for note in chord:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, True)
                notes_created += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Synthesizer FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for an EPiano tone
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.2)  # Square wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5)  # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.01) # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, 0, 10, 0.3) # Release (Moderate)

    return f"Created '{track_name}' with {notes_created} perfectly-quantized notes over {bars} bars at {bpm} BPM (Notation Ready)"
