def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Build-Up Swell in the current REAPER project.
    Generates a sustained chord with algorithmic Volume and Pan automation.

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
        Status string describing the creation of the track, MIDI, and envelopes.
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

    # Extract scale intervals and root note
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    base_octave = 48  # C3

    # Resolve chord tones (1st, 3rd, 5th, 7th of the scale)
    chord_degrees = [0, 2, 4, 6] 
    chord_pitches = []
    for degree in chord_degrees:
        if degree < len(intervals):
            chord_pitches.append(base_octave + root_val + intervals[degree])
        else:
            # Wrap to next octave if degree exceeds scale length
            chord_pitches.append(base_octave + root_val + intervals[degree % len(intervals)] + 12)

    # === Step 1: Set Tempo & Calculate Timings ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Insert Sustained Chord ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # 25600 ticks per quarter note is standard in REAPER API without explicit PPQ conversion
    # But using standard normalized positions requires dealing with PPQ.
    # A simpler native way is utilizing RPR_MIDI_InsertNote with actual PPQ:
    ppq = 960  # Standard internal PPQ
    end_ppq = ppq * beats_per_bar * bars

    for pitch in chord_pitches:
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, pitch, velocity_base, True)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instrument FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 5: Generate Automation Envelopes ===
    # Select ONLY this track to safely toggle envelope visibility commands
    RPR.RPR_SetOnlyTrackSelected(track)

    # 5a. Volume Automation (Smooth Swell from 0.0 to 1.0)
    RPR.RPR_Main_OnCommand(40406, 0) # Command: "Track: Toggle track volume envelope visible"
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        # shape 2 = "Slow start/end" (Smooth curve)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, total_length_sec, 1.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_Sort(vol_env)

    # 5b. Pan Automation (Ping-Pong every beat)
    RPR.RPR_Main_OnCommand(40456, 0) # Command: "Track: Toggle track pan envelope visible"
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        num_beats = bars * beats_per_bar
        for i in range(num_beats + 1):
            time_pos = i * beat_length_sec
            # Alternate between -0.8 (Left) and 0.8 (Right)
            pan_val = -0.8 if i % 2 == 0 else 0.8
            # shape 2 = Smooth transition to the next point
            RPR.RPR_InsertEnvelopePoint(pan_env, time_pos, pan_val, 2, 0.0, False, True)
        RPR.RPR_Envelope_Sort(pan_env)

    return f"Created '{track_name}' with automated Volume Swell and Auto-Pan over {bars} bars at {bpm} BPM in {key} {scale}."
