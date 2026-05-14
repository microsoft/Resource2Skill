def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Dynamic Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Dynamic MIDI Chord Progression in the current REAPER project.
    Generates a continuous chord progression with an automated velocity crescendo.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (cycles a 4-chord progression).
        velocity_base: Base MIDI velocity (0-127). The progression will slope around this.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Setup Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock instrument to interpret the MIDI
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create the item directly using the QN-safe project function
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Music Theory & Progression Setup ===
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
    
    # Clean up input strings
    clean_key = key.replace('m', '').replace('M', '').strip().capitalize()
    if clean_key not in NOTE_MAP:
        clean_key = "C"
        
    root_offset = NOTE_MAP[clean_key]
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Octave 3 (MIDI Note 48 = C3)
    base_octave = 48 

    # Pop/Standard progression: I - vi - IV - V (represented by scale degrees 0, 5, 3, 4)
    progression = [0, 5, 3, 4]

    # Helper function to get correct diatonic pitch
    def get_diatonic_pitch(degree_index):
        octave_shift = degree_index // len(scale_intervals)
        note_idx = degree_index % len(scale_intervals)
        return base_octave + root_offset + scale_intervals[note_idx] + (12 * octave_shift)

    # === Step 5: Insert Notes with Velocity Crescendo ===
    for b in range(bars):
        degree = progression[b % len(progression)]

        # Calculate Root, 3rd, 5th
        root_pitch = get_diatonic_pitch(degree)
        third_pitch = get_diatonic_pitch(degree + 2)
        fifth_pitch = get_diatonic_pitch(degree + 4)

        # Mathematical implementation of the tutorial's CC Velocity slope (Crescendo)
        # It starts -20 from the base and ends +20 over the duration of the item
        progress_ratio = b / max(1, (bars - 1))
        dynamic_velocity = int((velocity_base - 20) + (40 * progress_ratio))
        # Clamp velocity to standard MIDI bounds
        dynamic_velocity = max(1, min(127, dynamic_velocity))

        # Timing (1 bar = 4 Quarter Notes)
        start_qn = b * 4.0
        end_qn = start_qn + 4.0

        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

        # Insert Chord Notes
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, dynamic_velocity, False)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, third_pitch, dynamic_velocity, False)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, fifth_pitch, dynamic_velocity, False)

    # Re-sort the MIDI events after mass insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with dynamic crescendo chords over {bars} bars at {bpm} BPM."
