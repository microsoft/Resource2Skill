def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Filter Sweep Transition in the current REAPER project.

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
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # --- 1. Music Theory & Lookup Tables ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10]
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Build a lush 9th chord stack extending beyond the first octave
    # Degrees: 1st, 3rd, 5th, 7th, 9th (index 0, 2, 4, 6, 8 mapped to scale)
    octave_base = 48 # C3
    chord_pitches = []
    for degree in [0, 2, 4, 6, 8]:
        octave_offset = (degree // 7) * 12
        interval = scale_intervals[degree % 7]
        chord_pitches.append(octave_base + root_val + octave_offset + interval)

    # --- 2. Project Setup & Timing ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    start_time = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    end_time = start_time + item_length_sec

    # --- 3. Track Creation ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- 4. FX Chain (Synth & EQ) ---
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Give it a bit more saw/square character for the filter to chew on
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.4) # Saw shape
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.2) # Square shape
    
    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Configure ReaEQ Band 4 (High Shelf) to act as a cut filter
    # Param 10 is Band 4 Gain. Set to 0.0 (-inf dB)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0)

    # --- 5. MIDI Generation ---
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
    
    for pitch in chord_pitches:
        # Insert sustained notes spanning the entire item
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        
    RPR.RPR_MIDI_Sort(take)

    # --- 6. Automation Envelope (The Sweep) ---
    # Param 9 in ReaEQ is Band 4 Frequency
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    
    if env:
        # Insert point 1: Muffled (Freq normalized ~0.15)
        # 0 = Linear transition to next point
        RPR.RPR_InsertEnvelopePoint(env, start_time, 0.15, 0, 0.0, False, True)
        
        # Insert point 2: Bright/Open (Freq normalized ~0.85)
        RPR.RPR_InsertEnvelopePoint(env, end_time, 0.85, 0, 0.0, False, True)
        
        RPR.RPR_Envelope_SortRqst(env)
        env_status = "and applied Frequency Sweep Automation"
    else:
        env_status = "but failed to create automation envelope"

    return f"Created '{track_name}' with a {bars}-bar {key} {scale} pad {env_status}."
