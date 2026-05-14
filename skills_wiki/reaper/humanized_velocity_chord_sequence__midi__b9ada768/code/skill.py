def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 40,
    **kwargs,
) -> str:
    """
    Create a 'Humanized Velocity Chord Sequence' in the current REAPER project.
    Generates a pulsing 1/8th note chord progression featuring a velocity crescendo
    and per-note velocity weighting to replicate human expression.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Starting MIDI velocity (0-127) for the crescendo.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth so we can hear the MIDI
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate MIDI Notes with Velocity Automaton ===
    notes_per_beat = 2 # 1/8th notes
    total_chords = bars * beats_per_bar * notes_per_beat
    note_len_qn = 1.0 / (notes_per_beat / 2.0) if notes_per_beat == 4 else 0.5 # 0.5 QN = 1/8th note
    
    # Resolve root note (Octave 3) and scale
    root_val = NOTE_MAP.get(key, 0) + 48 
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Build a basic triad
    chord_pitches = [
        root_val + scale_intervals[0], # Root
        root_val + scale_intervals[2], # 3rd
        root_val + scale_intervals[4]  # 5th
    ]
    
    end_velocity = 115 # Peak velocity at the end of the crescendo
    note_count = 0
    
    for i in range(total_chords):
        # Calculate timing
        start_qn = i * note_len_qn
        # Articulation: Make notes slightly shorter than the grid to detach them
        end_qn = start_qn + (note_len_qn * 0.85) 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        # Calculate macro-dynamics: Velocity ramp (Crescendo)
        progress = i / max(1, (total_chords - 1))
        base_chord_vel = int(velocity_base + (end_velocity - velocity_base) * progress)
        
        # Calculate micro-dynamics: Per-note weighting
        for j, pitch in enumerate(chord_pitches):
            note_vel = base_chord_vel
            
            # Bass note hits slightly harder, top note slightly softer
            if j == 0: 
                note_vel += 6
            elif j == 2: 
                note_vel -= 4
                
            # Clamp velocity to valid MIDI range
            note_vel = max(1, min(127, note_vel))
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, note_vel, True)
            note_count += 1

    # Apply sorting to finalize the MIDI item
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM. Generated a 1/8th note chord sequence with a velocity crescendo from {velocity_base} to {end_velocity}."
