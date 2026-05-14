def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Smooth S-Curve Fade",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a sustained pad that fades out smoothly using an S-Curve (Slow Start/End) automation envelope.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars for the item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., fade_bars to control fade length).

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Configuration overrides
    fade_bars = kwargs.get("fade_bars", 1.0) # Length of the fade at the end
    
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

    # === Step 2: Create Track & Add Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth to provide an audible signal
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Generate Chord (1st, 3rd, 5th degrees of the scale)
    base_midi = 60 # C4
    root_offset = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    root_midi = base_midi + root_offset
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    chord_intervals = [scale_intervals[0], scale_intervals[2], scale_intervals[4]]

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)

    for interval in chord_intervals:
        RPR.RPR_MIDI_InsertNote(
            take,
            False,            # selected
            False,            # muted
            start_ppq,        # startppqpos
            end_ppq,          # endppqpos
            0,                # chan
            root_midi + interval, # pitch
            velocity_base,    # vol
            False             # noSort
        )
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Smooth S-Curve Fade Automation ===
    # Attempt to get the Volume envelope
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    # If the envelope isn't active/visible yet, toggle it on
    if not env:
        RPR.RPR_SetOnlyTrackSelected(track)
        RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
        env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
        
    if env:
        fade_start_sec = (bars - fade_bars) * bar_length_sec
        fade_end_sec = item_length_sec
        
        # REAPER Envelope Shapes: 
        # 0=Linear, 1=Square, 2=Slow start/end, 3=Fast start, 4=Fast end, 5=Bezier
        
        # 1. Anchor point at 0.0s (Hold at 1.0 amplitude / 0dB)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0.0, False, True)
        
        # 2. Fade Start Point (Shape 2 triggers the "Slow start/end" S-Curve moving forward)
        RPR.RPR_InsertEnvelopePoint(env, fade_start_sec, 1.0, 2, 0.0, False, True)
        
        # 3. Fade End Point (Reaches 0.0 amplitude / -inf dB, shape 0 for subsequent flatline)
        RPR.RPR_InsertEnvelopePoint(env, fade_end_sec, 0.0, 0, 0.0, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with smooth S-Curve fade over the last {fade_bars} bars at {bpm} BPM"
