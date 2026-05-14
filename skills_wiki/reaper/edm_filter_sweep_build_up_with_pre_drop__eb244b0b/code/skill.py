def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "BuildUp_Chords",
    bpm: int = 126,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an EDM Filter Sweep Build-Up with a Pre-Drop Cut in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate for the build-up.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
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

    # === Step 1: Set Tempo & Calculate Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    
    # We create a 1-beat "dropout" at the end of the pattern
    total_length_sec = bar_length_sec * bars
    item_length_sec = total_length_sec - beat_length_sec

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Synth and EQ for Automation ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more "pad" like sound (reduce sustain, increase release slightly)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.2) # Sawtooth mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.4) # Release

    # Add ReaEQ for the Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Set Band 4 (Param 9=Freq, 10=Gain, 11=Q) to act as a Low Pass by dropping High Shelf gain
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0) # Gain to 0.0 (-120dB)
    
    # Automate Band 4 Freq (Parameter 9)
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    if env:
        # Start muffled, sweep up to fully open right before the drop cut
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.2, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, item_length_sec, 0.9, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    # === Step 4: Create MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Chords ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generic progression degrees (i - VI - III - VII style)
    degrees = [0, 5, 2, 4]
    
    notes_added = 0
    octave_base = 4
    
    for i in range(bars):
        degree = degrees[i % len(degrees)]
        
        # Build triad with octave wrapping
        chord_notes = []
        for interval in [0, 2, 4]:
            idx = (degree + interval) % len(scale_intervals)
            octave_shift = (degree + interval) // len(scale_intervals)
            midi_pitch = root_val + scale_intervals[idx] + (octave_base + octave_shift + 1) * 12
            chord_notes.append(midi_pitch)
        
        start_time = i * bar_length_sec
        # If it's the last bar, cut it short by 1 beat for the dropout
        if i == bars - 1:
            end_time = start_time + bar_length_sec - beat_length_sec
        else:
            end_time = start_time + bar_length_sec
            
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for pitch in chord_notes:
            # Add a bit of velocity humanization
            vel = max(1, min(127, velocity_base + (i % 2) * 5))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars (ending with a 1-beat dropout) at {bpm} BPM. Added an automated filter sweep via ReaEQ."
