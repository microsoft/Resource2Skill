def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Expressive Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Create Expressive MIDI Chord Humanization in the current REAPER project.

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
        Status string describing the generated chords.
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

    scale_intervals = SCALES.get(scale, SCALES["major"])
    root_midi = NOTE_MAP.get(key, 0) + 48  # Base octave C3

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a softer, more pad/piano-like response
    # Param 2 is Attack, Param 5 is Release
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.05) # Slower, gentle attack
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3)  # Longer, trailing release

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create new MIDI item across the defined duration
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Insert Humanized Chords ===
    # Progression: I, V, vi, IV represented by 0-indexed scale degrees
    chords = [
        (0, 2, 4),      # I chord
        (4, 6, 8),      # V chord (8 wraps to 2nd scale degree, one octave up)
        (5, 7, 9),      # vi chord
        (3, 5, 7)       # IV chord
    ]

    total_chords = bars * 2  # 2 chords per bar (half notes)
    half_note_sec = bar_length_sec / 2.0

    def degree_to_midi(deg):
        """Converts a scale degree integer to an absolute MIDI pitch, handling octave wrapping."""
        octave = deg // len(scale_intervals)
        idx = deg % len(scale_intervals)
        return root_midi + scale_intervals[idx] + (octave * 12)

    notes_created = 0
    for i in range(total_chords):
        chord_deg = chords[i % len(chords)]
        
        # Macro-dynamics: Velocity swells across the phrase 
        # (Simulating the slope drawn in the MIDI editor CC lane)
        curve_offsets = [0, 15, 5, -5] 
        phrase_vel = velocity_base + curve_offsets[i % len(curve_offsets)]
        
        start_sec = i * half_note_sec
        # Slightly detach notes (95% length) for natural piano re-triggering
        end_sec = start_sec + (half_note_sec * 0.95)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        # Micro-dynamics: Velocity variation within the specific chord structure
        vel_root = max(1, min(127, phrase_vel + 10))  # Accented structural root
        vel_third = max(1, min(127, phrase_vel - 10)) # Softer emotional color note
        vel_fifth = max(1, min(127, phrase_vel))      # Neutral fifth
        
        # Insert Root
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, degree_to_midi(chord_deg[0]), int(vel_root), False)
        # Insert Third
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, degree_to_midi(chord_deg[1]), int(vel_third), False)
        # Insert Fifth
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, degree_to_midi(chord_deg[2]), int(vel_fifth), False)
        
        notes_created += 3

    # Important: sort the MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}"
