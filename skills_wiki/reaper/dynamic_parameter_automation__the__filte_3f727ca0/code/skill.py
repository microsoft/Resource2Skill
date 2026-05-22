def create_pattern(
    project_name: str = "Automated Pad",
    track_name: str = "Sweeping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with an automated ReaEQ Low-Pass filter sweep.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars for the swell/sweep.
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    if scale not in SCALES:
        scale = "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup FX Chain (Synth + EQ) ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak synth for a pad feel (slower attack/release, mix of saw/square)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.4) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.6) # Release

    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # In ReaEQ, Band 1 Type is parameter 3. Value ~0.8 maps to Low Pass.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 3, 0.88)
    
    # === Step 4: Create Automation Envelope ===
    # Parameter 0 in ReaEQ is Band 1 Frequency. We want to automate this.
    # The 'True' flag creates the envelope if it doesn't exist.
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)

    # Calculate timings
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_time_sec = bar_length_sec * bars

    # Insert automation points to create a "V" shape filter sweep
    # RPR_InsertEnvelopePoint(env, time, value, shape, tension, selected, noSortIn)
    # Shape 0 = Linear, Shape 1 = Square, Shape 2 = Slow start/end
    
    # Start bright (normalized frequency near 1.0)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.9, 2, 0.0, False, True)
    # Muffle in the middle of the pattern (normalized frequency low)
    RPR.RPR_InsertEnvelopePoint(env, total_time_sec / 2.0, 0.15, 2, 0.0, False, True)
    # Open back up at the end
    RPR.RPR_InsertEnvelopePoint(env, total_time_sec, 0.9, 0, 0.0, False, True)
    
    # Apply points
    RPR.RPR_Envelope_SortPoints(env)

    # === Step 5: Create MIDI Item & Notes ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_time_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Build a lush chord: Root, 5th, Octave, 3rd (an octave up)
    root_pitch = SCALES[scale][0] + NOTE_MAP[key] + 48 # Octave 4
    chord_pitches = [
        root_pitch, 
        root_pitch + SCALES[scale][4],      # 5th
        root_pitch + 12,                    # Octave
        root_pitch + 12 + SCALES[scale][2]  # 10th (3rd octave up)
    ]

    ticks_per_quarter = 960
    total_ticks = int(bars * beats_per_bar * ticks_per_quarter)

    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            0, total_ticks, # Start to End
            0, pitch, velocity_base, False
        )

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with automated EQ filter sweep over {bars} bars at {bpm} BPM."
