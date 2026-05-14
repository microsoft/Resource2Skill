def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Cinematic Swell & Pan Sweep in the current REAPER project.

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
        Status string describing the created automated track.
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

    scale_degrees = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.title(), 0) + 48 # Base octave 4

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Setup ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Exclusively select this track so action commands target it reliably
    RPR.RPR_SetOnlyTrackSelected(track)

    # === Step 3: Add FX Chain ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth for a rich pad tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Square Mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.7) # Saw Mix
    
    # Add Chorus for stereo width before we pan it
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)

    # === Step 4: Create MIDI Content ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Build a lush 4-note chord + sub bass
    chord_indices = [0, 2, 4, 6] 
    pitches = [root_pitch - 12] # Sub octave
    for i in chord_indices:
        octave_shift = i // len(scale_degrees)
        deg = scale_degrees[i % len(scale_degrees)]
        pitches.append(root_pitch + deg + (octave_shift * 12))

    start_qn = 0.0
    end_qn = bars * beats_per_bar

    for pitch in pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_qn * 960, end_qn * 960, 1, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Program Automation Envelopes ===
    
    # Reveal Volume Envelope via Action (requires track selected)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    # Reveal Pan Envelope via Action
    RPR.RPR_Main_OnCommand(40456, 0) # Track: Toggle track pan envelope visible
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")

    shape_slow_start_end = 2

    if vol_env:
        # Clear any existing points in the timeline
        RPR.RPR_DeleteEnvelopePointRange(vol_env, -1.0, item_length + 1.0)
        
        # Swell Volume from 0.0 (-inf) to 1.0 (0dB)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(vol_env)

    if pan_env:
        RPR.RPR_DeleteEnvelopePointRange(pan_env, -1.0, item_length + 1.0)
        
        # Sweep Pan: Center -> Left -> Right -> Center
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, 0.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.25, -0.7, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.75, 0.7, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(pan_env)

    # Set Track Automation Mode to 'Read' (1) so faders move visually during playback
    RPR.RPR_SetTrackAutomationMode(track, 1)

    return f"Created '{track_name}' with {len(pitches)}-note chord, automated Volume swell and Pan sweep over {bars} bars at {bpm} BPM."
