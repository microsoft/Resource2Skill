def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Create a Humanized Chord Progression in the current REAPER project.

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
        Status string describing the operation.
    """
    import reaper_python as RPR
    import random

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

    # Helper to clamp velocity
    def clamp_vel(v):
        return int(max(1, min(127, v)))

    # Calculate scale notes starting from C0
    root_val = NOTE_MAP.get(key.upper(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth to hear the chords
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a more piano-like plucky envelope
    # Param 3: Attack (fast), Param 4: Decay (medium), Param 5: Sustain (low)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.2)  # Sustain

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Humanized Chord Progression ===
    # Progression: I - V - vi - IV
    progression_degrees = [0, 4, 5, 3] 
    
    # Base octave for chords (e.g., C3 = MIDI 48)
    base_octave = 3
    notes_created = 0
    
    for bar in range(bars):
        chord_degree = progression_degrees[bar % len(progression_degrees)]
        
        # Calculate chord tones (Root, 3rd, 5th)
        chord_notes = []
        for chord_tone in [0, 2, 4]: 
            scale_idx = chord_degree + chord_tone
            octave_shift = scale_idx // len(intervals)
            rem_idx = scale_idx % len(intervals)
            
            note_pitch = root_val + intervals[rem_idx] + ((base_octave + octave_shift + 1) * 12)
            chord_notes.append(note_pitch)
            
        # Timing for this chord (1 bar length, slight gap at end for articulation)
        start_time = bar * bar_length_sec
        end_time = start_time + (bar_length_sec * 0.95)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Insert humanized notes
        for i, pitch in enumerate(chord_notes):
            # Humanization logic:
            # - Random jitter between -12 and +12
            # - The root note (i==0) gets a slight velocity bump (+5)
            # - Inner voices get slight velocity reduction (-5)
            jitter = random.randint(-12, 12)
            voicing_accent = 5 if i == 0 else -5
            
            human_vel = clamp_vel(velocity_base + voicing_accent + jitter)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, human_vel, True
            )
            notes_created += 1

    # Sort the MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized notes (velocity variation) over {bars} bars at {bpm} BPM."
