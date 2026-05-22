def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Velocity-Humanized MIDI Chord Progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (will loop a 4-chord progression).
        velocity_base: Base MIDI velocity (0-127). Will be randomized for humanization.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 0) # Base octave C3 = 48

    # Helper to get the MIDI pitch for a specific scale degree (0-indexed)
    def get_pitch(degree):
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_midi + scale_intervals[scale_idx] + (octave_shift * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Native Instrument (ReaSynth) ===
    # Using ReaSynth as a fallback so the MIDI generates audio out of the box
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth to be slightly softer (lower square mix, add some decay)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.2) # Square mix down
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5) # Release time up

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Enable MIDI for the take
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "I_CUSTOMCOLOR", 0)

    # === Step 5: Generate Humanized Chord Progression ===
    # A standard diatonic progression (I - vi - IV - V) expressed in scale degrees
    progression_degrees = [0, 5, 3, 4] 
    
    notes_created = 0
    
    for bar in range(bars):
        # Loop the progression if bars > 4
        chord_root_degree = progression_degrees[bar % len(progression_degrees)]
        
        # Build a basic triad: Root, 3rd, 5th
        chord_degrees = [chord_root_degree, chord_root_degree + 2, chord_root_degree + 4]
        
        # Calculate timings
        start_time = bar * bar_length_sec
        # Leave a tiny gap at the end of the bar for realism (legato but not overlapping)
        end_time = start_time + (bar_length_sec * 0.95) 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Insert each note of the chord
        for degree in chord_degrees:
            pitch = get_pitch(degree)
            
            # CORE SKILL: Velocity Humanization
            # Instead of a static max velocity, randomize around the base
            # This emulates the tutorial's advice to drag velocities up/down for realism
            humanized_vel = velocity_base + random.randint(-18, 12)
            # Clamp velocity to valid MIDI range
            humanized_vel = max(1, min(127, humanized_vel))
            
            RPR.RPR_MIDI_InsertNote(
                take, 
                False,       # selected
                False,       # muted
                start_ppq, 
                end_ppq, 
                0,           # channel
                pitch, 
                humanized_vel, 
                True         # noSort (we will sort at the end)
            )
            notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} humanized MIDI notes over {bars} bars at {bpm} BPM in {key} {scale}."
