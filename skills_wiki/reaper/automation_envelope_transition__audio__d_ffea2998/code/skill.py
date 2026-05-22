def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Transition Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automation Envelope Transition (Audio Dip) in the current REAPER project.

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
    # Using ReaSynth as a sound generator so we have continuous audio to fade
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the synth to act as a pad
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.4) # Sawtooth mix down
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5) # Attack longer
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.5) # Release longer

    # === Step 4: Create Sustained MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    root = NOTE_MAP.get(key, 0) + 48 # Base octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4] # Root, Third, Fifth
    
    # Insert a single continuous triad chord spanning the entire item length
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for degree in chord_degrees:
        pitch = root + scale_intervals[degree]
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Translate Video Workflow to Audio Automation ===
    # Toggle the track volume envelope to make it active and accessible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env:
        # Define the 4 points of the transition "dip"
        dip_start_time = bar_length_sec * 1.5   # Midpoint of bar 2
        dip_bottom_time = bar_length_sec * 2.0  # Start of bar 3
        rise_start_time = bar_length_sec * 2.5  # Midpoint of bar 3
        rise_end_time = bar_length_sec * 3.0    # Start of bar 4
        
        # Envelope Shape mapping in REAPER: 0 = Linear, 2 = Slow start/end (S-Curve)
        # Value mapping: 1.0 = 0dB (Unity), 0.0 = -inf dB (Silence)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, dip_start_time, 1.0, 2, 0.0, False, True)  # Start of Dip (Slow fall)
        RPR.RPR_InsertEnvelopePoint(env, dip_bottom_time, 0.0, 0, 0.0, False, True) # Hits Silence
        RPR.RPR_InsertEnvelopePoint(env, rise_start_time, 0.0, 2, 0.0, False, True) # Starts Rise (Slow rise)
        RPR.RPR_InsertEnvelopePoint(env, rise_end_time, 1.0, 0, 0.0, False, True)   # Back to full volume
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' demonstrating a mapped 4-point smooth Envelope Dip Transition over {bars} bars at {bpm} BPM."
