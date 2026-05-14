def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Volume Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Volume Swell in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the swell will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
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

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add and Configure Instrument (ReaSynth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a rich "Pad" sound suitable for a swell
    # Param 2: Attack (soften slightly to avoid clicks)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.1) 
    # Param 5: Release (give it a nice tail)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5) 
    # Param 7: Sawtooth mix (turn up for harmonic richness)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 1.0) 

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Convert project time to PPQ for MIDI note insertion
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 5: Generate Harmonic Triad (Pitch & Harmony) ===
    root_offset = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    octave_base = 48 # Start at C3

    chord_degrees = [0, 2, 4] # 1st, 3rd, and 5th degrees
    note_count = 0

    for degree in chord_degrees:
        if degree < len(scale_intervals):
            pitch = octave_base + root_offset + scale_intervals[degree]
            
            # Insert a sustained note for the entire duration of the block
            RPR.RPR_MIDI_InsertNote(
                take, False, False,
                start_ppq, end_ppq,
                0, pitch, velocity_base, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Create the Automation Envelope ===
    # Select only our new track to ensure the command acts on the right target
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Run Action 40406: "Track: Toggle track volume envelope visible"
    # This guarantees the volume envelope exists and is accessible
    RPR.RPR_Main_OnCommand(40406, 0)

    # Fetch the envelope pointer
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env:
        # Insert Start Point at 0 seconds
        # Value = 0.0 (-inf dB)
        # Shape = 2 (Slow start/end - creates a musical bezier curve swell)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, 2, 0.0, False, True)
        
        # Insert End Point at end of item
        # Value = 1.0 (0 dB / Unity Gain)
        RPR.RPR_InsertEnvelopePoint(env, item_length, 1.0, 0, 0.0, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with a {note_count}-note chord swell spanning {bars} bars at {bpm} BPM."
