def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Wash-Out Build Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Wash-Out Filter Build Pad in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the riser will sustain.
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
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain ===
    # 1. Synthesizer
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.4) # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5) # Attack (slow swell)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.8) # Release (smooth fade)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.8) # Saw mix

    # 2. Filter (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Target Band 4 (High Shelf) and drop Gain to -inf to act as a steep Low Pass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 0.0) 
    # Add slight resonance/Q
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, 0.6)

    # 3. Massive Reverb Tail
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.7) # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.5) # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.9) # Roomsize (Huge)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # Process key string to match dictionary safely
    lookup_key = key.capitalize() if len(key) > 1 else key.upper()
    root_pitch = NOTE_MAP.get(lookup_key, 0) + 48 # Base Octave 3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Construct a lush pad chord voicing (Root, 3rd, 5th, Octave)
    if len(scale_intervals) >= 5:
        chord_intervals = [scale_intervals[0], scale_intervals[2], scale_intervals[4], 12]
    else:
        chord_intervals = [scale_intervals[0], scale_intervals[1], scale_intervals[2], 12]

    # Insert notes
    for interval in chord_intervals:
        pitch = root_pitch + interval
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate Filter Sweep ===
    # Param 9 is the Frequency for Band 4 in ReaEQ
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    if env:
        # Plot 1: Start heavily muffled (~200Hz)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.3, 0, 0.0, False, True)
        
        # Plot 2: Ramp up exponentially, opening just before the drop (~75% through)
        RPR.RPR_InsertEnvelopePoint(env, item_length * 0.75, 0.6, 0, 0.0, False, True)
        
        # Plot 3: Fully open at the absolute end to release the tension
        RPR.RPR_InsertEnvelopePoint(env, item_length, 0.95, 0, 0.0, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' Wash-Out Build using a {key} {scale} pad over {bars} bars at {bpm} BPM."
