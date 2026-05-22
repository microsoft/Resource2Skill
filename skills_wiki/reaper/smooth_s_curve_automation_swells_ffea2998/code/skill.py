def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "S-Curve Pad Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an S-Curve Automation Swell in the current REAPER project.
    Generates a sustained 7th chord pad and applies a 'Slow start/end' volume envelope.

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
        Status string describing the generated element.
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

    # === Step 3: Add FX Chain (ReaSynth) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Dial back the harsh saw wave for a softer pad tone
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) # Saw shape 

    # === Step 4: Create MIDI Item & Insert Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Calculate exact PPQ positions for note timing
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    # Determine MIDI pitches (7th chord based on key/scale)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    base_note = NOTE_MAP.get(key, 0) + 48 # Octave 3
    
    chord_degrees = [0, 2, 4, 6] # Root, 3rd, 5th, 7th
    note_count = 0
    
    for degree in chord_degrees:
        oct_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        note = base_note + scale_intervals[scale_idx] + (oct_shift * 12)
        
        # Insert sustained note for the entire duration
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
        note_count += 1
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automation Envelope (Slow Start/End) ===
    # Select track and invoke action 40406 to guarantee the volume envelope is active/visible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) 
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    # Define swell duration (1 bar, capped at half the total length)
    swell_time = bar_length_sec
    if swell_time > item_length / 2:
        swell_time = item_length / 2
        
    # Shape 2 corresponds to "Slow start/end" non-linear curve
    SHAPE_SLOW_START_END = 2
    
    # Point 1: Start at absolute silence (0.0 linear amplitude)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, SHAPE_SLOW_START_END, 0.0, False, True)
    
    # Point 2: S-curve swell up to 0dB (1.0 linear amplitude)
    RPR.RPR_InsertEnvelopePoint(env, swell_time, 1.0, SHAPE_SLOW_START_END, 0.0, False, True)
    
    # Point 3: Hold 0dB until the fade-out begins
    RPR.RPR_InsertEnvelopePoint(env, item_length - swell_time, 1.0, SHAPE_SLOW_START_END, 0.0, False, True)
    
    # Point 4: S-curve fade back to silence at the item's end
    RPR.RPR_InsertEnvelopePoint(env, item_length, 0.0, SHAPE_SLOW_START_END, 0.0, False, True)
    
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}': {note_count}-note chord over {bars} bars at {bpm} BPM with an organic S-Curve volume swell."
