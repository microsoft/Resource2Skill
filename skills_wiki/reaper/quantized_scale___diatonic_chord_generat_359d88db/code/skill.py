def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Quantized Scale & Diatonic Chord Generator in the current REAPER project.
    Creates a melodic scale run followed by a diatonic I-IV-V-I progression, ideal for 
    viewing in REAPER's Musical Notation Mode (Alt+4).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, etc.).
        bars: Number of bars to generate (forces to 2 for this exercise).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
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
        "pentatonic_major": [0, 2, 4, 7, 9, 12, 14], # padded to 7 for formula
        "pentatonic_minor": [0, 3, 5, 7, 10, 12, 15], # padded to 7 for formula
    }

    # Normalize inputs
    key_upper = key.upper()
    root_val = NOTE_MAP.get(key_upper, 0)
    base_midi = 60 + root_val # Middle C (C4) adjusted by key
    selected_scale = SCALES.get(scale.lower(), SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth for sound ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    quarter_note_sec = 60.0 / bpm
    eighth_note_sec = quarter_note_sec / 2.0
    bar_length_sec = quarter_note_sec * beats_per_bar
    item_length = bar_length_sec * 2 # Fixed at 2 bars for this exercise
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    note_events = [] # List of (pitch, start_time, end_time)

    # -- Bar 1: Ascending Scale Run (8th notes) --
    scale_run = selected_scale + [12] # Add octave completion
    for i, interval in enumerate(scale_run[:8]): # Take exactly 8 notes
        start_t = i * eighth_note_sec
        end_t = start_t + (eighth_note_sec * 0.9) # 90% length for slight staccato separation
        note_events.append((base_midi + interval, start_t, end_t))

    # -- Bar 2: Diatonic Chords (Quarter notes) --
    # Helper to stack thirds purely diatonically based on the current scale array
    def get_diatonic_triad(degree):
        n1 = selected_scale[degree % 7] + (12 * (degree // 7))
        n2 = selected_scale[(degree + 2) % 7] + (12 * ((degree + 2) // 7))
        n3 = selected_scale[(degree + 4) % 7] + (12 * ((degree + 4) // 7))
        return [n1, n2, n3]

    # Standard progression: I (0), IV (3), V (4), I (0)
    progression_degrees = [0, 3, 4, 0] 
    bar2_start = bar_length_sec

    for i, degree in enumerate(progression_degrees):
        chord_intervals = get_diatonic_triad(degree)
        start_t = bar2_start + (i * quarter_note_sec)
        end_t = start_t + (quarter_note_sec * 0.9) # 90% length
        
        for interval in chord_intervals:
            note_events.append((base_midi + interval, start_t, end_t))

    # === Step 5: Insert Notes into REAPER ===
    for pitch, st, et in note_events:
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, st)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, et)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' track with a diatonic {key} {scale} scale & progression. Open MIDI Editor and hit Alt+4 to view Notation!"
