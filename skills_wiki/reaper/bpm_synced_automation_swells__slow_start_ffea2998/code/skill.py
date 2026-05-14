def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Cinematic Swell Fade",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a BPM-synced Slow Start/End volume fade (analogous to the tutorial's 
    video dissolve curve) applied to a generated synth pad.
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

    # === Step 2: Pitch & Harmony Generation ===
    root_val = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale, SCALES["minor"])
    base_midi = 48 + root_val  # Octave 4
    
    chord_pitches = []
    # Build a 4-note 7th chord utilizing 0-indexed scale degrees (0, 2, 4, 6)
    for i in [0, 2, 4, 6]:
        octave_shift = i // len(intervals)
        scale_idx = i % len(intervals)
        pitch = base_midi + intervals[scale_idx] + (12 * octave_shift)
        chord_pitches.append(pitch)

    # === Step 3: Create Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth to generate audio
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Time Calculation & Item Creation ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate PPQ (Pulses Per Quarter Note) for MIDI boundaries
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # Insert the chord notes
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Mix & S-Curve Automation ===
    # Select only the new track and toggle the Volume envelope to make it visible/active
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env:
        # Clear any default points
        RPR.RPR_DeleteEnvelopePointRange(env, -1.0, item_length + 1.0)
        
        # Insert Point 1: Time=0.0, Value=1.0 (0dB amplitude), Shape=2 (Slow start/end S-Curve)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 2, 0.0, False, True)
        
        # Insert Point 2: Time=item_length, Value=0.0 (-inf amplitude), Shape=0 (Linear, end shape doesn't matter)
        RPR.RPR_InsertEnvelopePoint(env, item_length, 0.0, 0, 0.0, False, True)
        
        RPR.RPR_Envelope_Sort(env)

    return f"Created '{track_name}' with a Slow Start/End volume fade across {bars} bars at {bpm} BPM."
