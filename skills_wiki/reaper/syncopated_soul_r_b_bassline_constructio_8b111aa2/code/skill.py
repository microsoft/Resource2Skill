def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "R&B Groove Bass",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Syncopated Soul/R&B Bassline using roots, 5ths, octaves, and passing notes.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Make sure scale exists, fallback to minor
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Progression: iv - i - iv - i (Degrees 3 and 0 in 0-indexed scale)
    # Adapts safely to smaller scales like pentatonic by using modulo length
    progression = [3 % len(scale_intervals), 0, 3 % len(scale_intervals), 0] 
    
    notes = []
    
    for bar in range(bars):
        chord_degree = progression[bar % 4]
        
        # Calculate root note for this chord (Octave 2 base = MIDI 36)
        chord_root = NOTE_MAP[key] + 36 + scale_intervals[chord_degree]
        
        bar_offset = bar * 4.0
        pattern_bar = bar % 4
        
        if pattern_bar == 0 or pattern_bar == 1:
            # Standard groove: Root -> Octave -> b7 -> 5th
            notes.append((bar_offset + 0.0, bar_offset + 1.0, chord_root, velocity_base + 10))
            notes.append((bar_offset + 1.5, bar_offset + 2.0, chord_root + 12, velocity_base - 10))
            notes.append((bar_offset + 2.5, bar_offset + 3.0, chord_root + 10, velocity_base - 15))
            notes.append((bar_offset + 3.5, bar_offset + 4.0, chord_root + 7, velocity_base - 5))
            
        elif pattern_bar == 2:
            # Variation groove: Root -> 5th -> b7 -> Octave
            notes.append((bar_offset + 0.0, bar_offset + 1.0, chord_root, velocity_base + 10))
            notes.append((bar_offset + 1.5, bar_offset + 2.0, chord_root + 7, velocity_base - 10))
            notes.append((bar_offset + 2.5, bar_offset + 3.0, chord_root + 10, velocity_base - 5))
            notes.append((bar_offset + 3.0, bar_offset + 3.5, chord_root + 12, velocity_base))
            
        elif pattern_bar == 3:
            # Turnaround walkup: Root -> Major 2nd -> Minor 3rd -> 5th drop
            notes.append((bar_offset + 0.0, bar_offset + 1.0, chord_root, velocity_base + 10))
            notes.append((bar_offset + 1.5, bar_offset + 2.0, chord_root + 2, velocity_base - 15))
            notes.append((bar_offset + 2.0, bar_offset + 2.5, chord_root + 3, velocity_base - 10))
            notes.append((bar_offset + 3.0, bar_offset + 4.0, chord_root + 7, velocity_base + 5))

    # Insert computed notes into the MIDI take
    for note in notes:
        start_qn = note[0]
        end_qn = note[1]
        pitch = max(0, min(127, int(note[2])))
        vel = max(1, min(127, int(note[3])))
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add native synth to act as a solid fundamental bass generator
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' containing syncopated bassline with {len(notes)} notes over {bars} bars at {bpm} BPM."
