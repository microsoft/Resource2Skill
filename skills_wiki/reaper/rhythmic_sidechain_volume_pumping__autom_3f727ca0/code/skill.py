def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a sustained pad with rhythmic 1/4-note volume pumping (fake sidechain automation).

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create Sustained MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine diatonic triad (Root, 3rd, 5th)
    root_base = 48 + NOTE_MAP.get(key, 0) # Start at C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Safe fallback if scale is too short (e.g., pentatonic missing a true 5th)
    third_idx = 2 if len(scale_intervals) > 2 else 1
    fifth_idx = 4 if len(scale_intervals) > 4 else len(scale_intervals) - 1
    
    chord_pitches = [
        root_base,
        root_base + scale_intervals[third_idx],
        root_base + scale_intervals[fifth_idx]
    ]

    # Insert sustained notes
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for pitch in chord_pitches:
        # noSort = False to ensure correct internal MIDI list sorting
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instrument and Automate ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Param 0 in ReaSynth is Volume. We create an envelope for it.
    env = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)
    
    # Draw the Pumping Envelope (4 times per bar)
    total_beats = bars * beats_per_bar
    
    for b in range(total_beats):
        t_start = b * beat_sec
        
        # Point 1: Duck the volume at the start of the beat (0.0 = silence)
        RPR.RPR_InsertEnvelopePoint(env, t_start, 0.0, 0, 0.0, False, True)
        
        # Point 2: Swell up 50% of the way through the beat (1/8th note delay)
        RPR.RPR_InsertEnvelopePoint(env, t_start + (beat_sec * 0.5), 0.7, 0, 0.0, False, True)
        
        # Point 3: Hold the volume high until just before the next kick/beat
        RPR.RPR_InsertEnvelopePoint(env, t_start + (beat_sec * 0.90), 0.7, 0, 0.0, False, True)
        
        # Point 4: Snap back down to prepare for the next downbeat
        RPR.RPR_InsertEnvelopePoint(env, t_start + (beat_sec * 0.99), 0.0, 0, 0.0, False, True)

    # Sort envelope points to apply changes
    RPR.RPR_Envelope_SortR(env)

    return f"Created '{track_name}' with {bars} bars of rhythmic sidechain automation at {bpm} BPM in {key} {scale}."
