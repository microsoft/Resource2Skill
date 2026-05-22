def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Sweep",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a sustained synth chord with an automated volume swell and 
    an EQ filter sweep over the specified number of bars.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate the sweep over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

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

    # === Step 3: Create MIDI Item & Drone Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    root_val = NOTE_MAP.get(key, 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # 4-note chord: 1st, 3rd, 5th, 7th degrees
    chord_degrees = [0, 2, 4, 6] 
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for degree in chord_degrees:
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        note_pitch = root_val + scale_intervals[scale_idx] + (octave_shift * 12)
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 0, end_ppq, 0, note_pitch, velocity_base, False
        )
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Synth & EQ) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Beef up the harmonic content (add Saw and Square waves) to make the filter sweep obvious
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Saw
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.5) # Square
    
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 5: Automate EQ Frequency (The Filter Sweep) ===
    # ReaEQ Band 4 Frequency is Parameter 15
    eq_env = RPR.RPR_GetFXEnvelope(track, eq_idx, 15, True) 
    if eq_env:
        # Sweep from High Frequency (1.0) down to Low (0.2)
        # 0 = Linear shape
        RPR.RPR_InsertEnvelopePoint(eq_env, 0.0, 1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length, 0.2, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(eq_env)

    # === Step 6: Automate Track Volume (Swell) ===
    # Ensure volume envelope is visible and accessible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if vol_env:
        # Values are amplitude: 0.0 = -inf dB, 1.0 = 0 dB
        # Fade in, hold, fade out
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, bar_length_sec * 0.5, 0.8, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length - (bar_length_sec * 0.5), 0.8, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 0.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(vol_env)

    return f"Created '{track_name}' with a {bars}-bar automated Volume swell and EQ filter sweep at {bpm} BPM."
