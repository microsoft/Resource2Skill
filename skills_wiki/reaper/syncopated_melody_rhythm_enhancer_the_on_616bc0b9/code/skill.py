def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Syncopated Melody",
    bpm: int = 95,
    key: str = "A",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Syncopated Melody' demonstrating the One-Note Test fix.
    It shifts notes from strong beats to off-beats to add groove.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (tutorial uses 95).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
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

    # === Step 2: Create Track (Additive) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4.0
    beat_sec = 60.0 / bpm
    item_length_sec = beat_sec * beats_per_bar * bars
    
    # Create MIDI item using the proper REAPER API function
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Syncopated Rhythm & Pitch ===
    root_midi = NOTE_MAP.get(key, 9) + 60 # Default to octave 4 (Middle C area)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # The Syncopated Pattern (Start Beat, Length in Beats, Scale Degree, Velocity Offset)
    # Notice the shift to the "and" of beat 1 (1.5) and the "and" of beat 2 (2.5)
    rhythm_pattern = [
        (0.0, 0.5, 0, 0),    # Downbeat (Root)
        (0.5, 0.5, 2, 10),   # Off-beat, accented (3rd)
        (1.5, 0.5, 4, 15),   # Off-beat syncopation, heavily accented (5th)
        (2.5, 0.5, 3, 5),    # Off-beat syncopation (4th)
        (3.0, 1.0, 0, -5)    # Resolution back on the strong beat (Root)
    ]
    
    note_count = 0
    for b in range(bars):
        bar_offset_beats = b * beats_per_bar
        
        for start_b, len_b, degree, vel_offset in rhythm_pattern:
            # Calculate absolute beat positions
            abs_start_b = bar_offset_beats + start_b
            abs_end_b = abs_start_b + len_b
            
            # Convert beats to seconds
            start_sec = abs_start_b * beat_sec
            end_sec = abs_end_b * beat_sec
            
            # Convert seconds to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Calculate Pitch
            octave_shift = (degree // len(scale_intervals)) * 12
            pitch = root_midi + scale_intervals[degree % len(scale_intervals)] + octave_shift
            
            # Clamp Velocity
            velocity = max(1, min(127, velocity_base + vel_offset))
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, False)
            note_count += 1

    # Sort MIDI events to ensure valid playback
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX ===
    # Add a stock synth so the melody is audible immediately
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Adjust ReaSynth to be a bit "pluckier" to emphasize the rhythm
    # Param 1 is Attack, Param 2 is Decay, Param 3 is Sustain, Param 4 is Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.1)  # Short decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.2)  # Low sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)  # Short release

    return f"Created '{track_name}' with {note_count} syncopated notes over {bars} bars at {bpm} BPM in {key} {scale}."
