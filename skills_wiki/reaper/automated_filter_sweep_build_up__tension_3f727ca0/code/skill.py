def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an Automated Filter Sweep Build-up using ReaSynth and ReaEQ.
    Demonstrates programmatic envelope automation (High-pass wash effect).

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Duration of the sweep build-up.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define 9th chords to ensure a thick frequency spectrum for the filter
    CHORD_INTERVALS = {
        "major": [0, 4, 7, 11, 14], # Maj9
        "minor": [0, 3, 7, 10, 14], # Min9
        "dorian": [0, 3, 7, 10, 14],
        "mixolydian": [0, 4, 7, 10, 14]
    }
    intervals = CHORD_INTERVALS.get(scale.lower(), CHORD_INTERVALS["minor"])

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
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert sustained 9th chord
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 0) # Start around C3
    end_ppq = bars * beats_per_bar * 960 # 960 PPQ per quarter note
    
    for interval in intervals:
        note = root_midi + interval
        # Insert note lasting the entire duration of the item
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, note, velocity_base, True)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design (ReaSynth) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # To make a filter sweep audible, we need harmonics. A pure sine wave cannot be filtered well.
    # Set Sine volume to 0.0 (Param 0) and Sawtooth volume to 1.0 (Param 1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.0)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 1.0)
    # Increase attack slightly to avoid clicks (Param 4)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.1)

    # === Step 5: Add ReaEQ and Setup High-Pass Automation ===
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # By default, ReaEQ Band 1 is a Low Shelf. 
    # If we set its Gain (Param 1) to -inf (Normalized 0.0), it acts like a High-Pass filter.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 1, 0.0)
    
    # Get the envelope for ReaEQ Band 1 Frequency (Param 0)
    # create=True ensures the envelope lane is created if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)

    # Insert automation points for the sweep
    # Param 0 Normalized values: 0.0 is ~20Hz, 0.5 is ~1kHz, 1.0 is ~24kHz
    # We sweep from 0.0 to 0.65 to thin out the sound over time (a classic riser wash-out)
    
    # Start point at time 0.0, value 0.0, shape 5 (bezier curve for natural build)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, 5, 0.2, False, True)
    
    # End point at the end of the item, value 0.65 (~3kHz), shape 0 (linear)
    RPR.RPR_InsertEnvelopePoint(env, item_length_sec, 0.65, 0, 0.0, False, True)
    
    # Sort envelope points to apply changes
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}': {bars}-bar automated High-Pass filter sweep on a {key} {scale} 9th chord at {bpm} BPM."
