def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Gain Staged Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    pre_trim_db: float = -8.0,
    post_trim_db: float = -12.0,
    **kwargs,
) -> str:
    """
    Create a Gain Staged track with Pre/Post trim brackets in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        pre_trim_db: Gain reduction before analog plugins (to hit -18dBFS).
        post_trim_db: Gain reduction after plugins (to optimize fader position).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track and FX chain.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Optimize Fader ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Set Track Fader strictly to 0.0 dB (Unity) for maximum fader resolution 
    # (represented internally as 1.0)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 1.0)

    # === Step 3: Add FX Chain (The Gain Staging Bracket) ===
    
    # 1. Sound Source (ReaSynth) to generate a signal
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Pre-Trim (Simulates turning down hot audio to hit plugins at -18dBFS / 0 VU)
    pre_trim_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    if pre_trim_idx >= 0:
        # Param 0 in "JS: Volume Adjustment" is "Adjustment (dB)"
        RPR.RPR_TrackFX_SetParam(track, pre_trim_idx, 0, pre_trim_db)
        
    # 3. "Analog" Processing Plugin (Receives the optimized signal)
    # We use ReaComp as a placeholder for any analog-modeled compressor/EQ
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    if comp_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -15.0) # Threshold
        RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio
        
    # 4. Post-Trim (Pulls the level down so the track fader can sit nicely at 0 dB)
    post_trim_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    if post_trim_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, post_trim_idx, 0, post_trim_db)

    # === Step 4: Create dummy MIDI to pass audio through the chain ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Build a simple triad chord based on the scale
    chord_notes = [
        root_midi,
        root_midi + scale_intervals[2],
        root_midi + scale_intervals[4]
    ]

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Insert long sustained pad notes to demonstrate the volume bracket
    start_ppq = 0.0
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for note in chord_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with Pre-Trim ({pre_trim_db}dB) and Post-Trim ({post_trim_db}dB). Track fader zeroed for optimal mixing resolution."
