def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groove Bassline",
    bpm: int = 115,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a syncopated, humanized "slap" bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for finger plucks (slaps will be louder).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    import random

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

    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_midi = 24 + NOTE_MAP.get(key.upper(), 4) # Base Octave 1 (e.g., E1 = 28)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

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

    # Groove Pattern Definition (1 Bar Loop)
    # Tuple: (Beat_Position, Scale_Degree_Index, Octave_Offset, Length_In_Beats, Velocity_Modifier)
    groove_pattern = [
        (0.00, 0, 0, 0.40,  0),   # Beat 1: Strong downbeat root (Finger)
        (0.75, 0, 1, 0.15, 35),   # Beat 1.75: Staccato Slap Octave (16th before beat 2)
        (1.50, 0, 0, 0.25, -10),  # Beat 2.5: Offbeat root (Finger)
        (2.00, 4, -1, 0.35, -5),  # Beat 3: Lower 5th (Finger)
        (2.50, 0, 0, 0.25,  0),   # Beat 3.5: Root (Finger)
        (2.75, 0, 1, 0.15, 35),   # Beat 3.75: Staccato Slap Octave
        (3.50, 0, 1, 0.15, 25),   # Beat 4.5: Staccato Slap Octave
    ]

    notes_created = 0
    
    # Generate MIDI Notes
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        for pos, degree_idx, oct_offset, length, vel_mod in groove_pattern:
            # Calculate Pitch
            safe_idx = degree_idx % len(scale_intervals)
            pitch = base_midi + scale_intervals[safe_idx] + (oct_offset * 12)
            
            # "Imitate Reality" - Humanization (Micro-timing & Velocity)
            timing_offset_beats = random.uniform(-0.015, 0.015) 
            vel_fluctuation = random.randint(-4, 4)
            
            final_vel = max(1, min(127, velocity_base + vel_mod + vel_fluctuation))
            
            # Absolute beat positions
            note_start_beat = bar_start_beat + pos + timing_offset_beats
            note_end_beat = note_start_beat + length
            
            # Convert beats to time, then to PPQ (Pulses Per Quarter Note)
            start_time = note_start_beat * (60.0 / bpm)
            end_time = note_end_beat * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, False)
            notes_created += 1

    # Sort MIDI notes after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (ReaSynth + ReaEQ for punch) ===
    # ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Mix some square wave for bite
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.6) # Saw mix

    # ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: Boost Lows (80Hz)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0.0) # Band 1 Type: Low Shelf
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0 + 1, 80.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0 + 2, 4.0) # Gain (dB)
    
    # Band 3: Boost High-Mids for "Slap" Presence (2500Hz)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 6, 1.0) # Band 3 Type: Band
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 6 + 1, 2500.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 6 + 2, 4.5) # Gain (dB)

    return f"Created '{track_name}' with {notes_created} syncopated slap bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
