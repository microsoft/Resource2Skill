def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard Stabs",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Syncopated Staccato Keyboard Stabs in the current REAPER project.

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
        Status string describing the creation.
    """
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
    
    # Create MIDI item (qnIn = False means we pass seconds)
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Music Theory & Note Generation ===
    # Rhythm Pattern: 16-step sequence (1/16th notes)
    # Values represent velocity modifier type: 1 = normal, 2 = accented/ghost
    step_pattern = [
        1, 0, 0, 0,  # Beat 1: On the downbeat
        0, 0, 2, 0,  # Beat 2: On the "and"
        0, 1, 0, 0,  # Beat 3: On the "e"
        0, 0, 2, 0,  # Beat 4: On the "and"
    ]
    
    # Progression: scale degrees (i, v, iv, i)
    progression_degrees = [0, 4, 3, 0] 
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)
    root_midi = 48 + NOTE_MAP.get(key, 0) # Octave 3 (C3 = 48)
    
    ppq_per_quarter = 960
    ppq_per_16th = ppq_per_quarter // 4
    notes_added = 0

    def get_chord_pitches(base_midi, intervals, degree, num_notes=4):
        pitches = []
        for i in range(num_notes):
            # Stack in thirds
            idx = degree + (i * 2)
            octave_shift = idx // scale_len
            scale_note = intervals[idx % scale_len]
            pitches.append(base_midi + scale_note + (octave_shift * 12))
        return pitches

    # Generate MIDI Notes
    for bar in range(bars):
        degree = progression_degrees[bar % len(progression_degrees)]
        # Generate a 4-note 7th chord based on the diatonic scale
        chord_pitches = get_chord_pitches(root_midi, scale_intervals, degree, 4)
        
        for step, hit_type in enumerate(step_pattern):
            if hit_type > 0:
                start_ppq = (bar * 16 * ppq_per_16th) + (step * ppq_per_16th)
                # Staccato duration: 1.5 16th notes
                end_ppq = start_ppq + int(ppq_per_16th * 1.5) 
                
                # Humanize velocity based on hit type
                vel = velocity_base if hit_type == 1 else max(10, velocity_base - 15)
                
                for pitch in chord_pitches:
                    # pitch bounds check
                    pitch = max(0, min(127, pitch))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                    notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design / FX Chain ===
    # Add stock synthesizer
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a pluck/keyboard envelope
    # Param 3: Attack (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.01)
    # Param 4: Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1)
    # Param 5: Sustain (lower to emphasize staccato)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.4)
    # Param 6: Release (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.15)
    # Param 0: Volume mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.6)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}."
