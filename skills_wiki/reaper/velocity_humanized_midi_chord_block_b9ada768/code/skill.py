def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a diatonic chord progression with humanized MIDI velocities.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (1 chord per bar).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    import random

    # === Theory / Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
                
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Normalize inputs
    key_upper = key.upper()
    root_val = NOTE_MAP.get(key_upper, 0)
    # Start around C3 (MIDI note 48) for chords
    root_midi = 48 + root_val 
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Common diatonic progression: I - vi - IV - V (0-indexed scale degrees)
    progression = [0, 5, 3, 4] 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup FX (Stock Synth) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower ReaSynth volume slightly to prevent harsh clipping on block chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Using CreateNewMIDIItemInProj ensures proper MIDI take initialization
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    notes_created = 0

    # === Step 5: Generate Chords and Humanize Velocities ===
    for i in range(bars):
        # Loop the progression if bars > length of progression
        degree = progression[i % len(progression)]
        
        # Calculate pitches for a 3-note triad
        chord_pitches = []
        for interval in [0, 2, 4]:
            scale_index = (degree + interval) % len(scale_intervals)
            octave_shift = (degree + interval) // len(scale_intervals)
            pitch = root_midi + scale_intervals[scale_index] + (octave_shift * 12)
            chord_pitches.append(pitch)

        # Timing for this chord
        start_time = i * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        # Insert notes with Humanized Velocity
        for pitch in chord_pitches:
            # Emulate the "click and drag" variance from the tutorial (±18 range)
            velocity_variance = random.randint(-18, 18)
            humanized_vel = max(1, min(127, velocity_base + velocity_variance))
            
            # Slightly offset the start time (strum effect) by 0-10 ticks to add realism
            strum_offset = random.randint(0, 15)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq + strum_offset, end_ppq, 
                0, int(pitch), int(humanized_vel), True
            )
            notes_created += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized MIDI notes across {bars} bars at {bpm} BPM in {key} {scale}."
