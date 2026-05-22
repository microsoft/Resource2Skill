def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Filter Sweep (Tension Build-Up) in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the sweep lasts.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the created track and automation.
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
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item_length_ppq = bars * beats_per_bar * 960  # 960 PPQ per beat

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Dense Chord ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate chord pitches: 1st, 3rd, 5th, 7th, 9th (if scale permits) to create a rich pad
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 48 # Start at octave 4
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Safe chord degrees (0-indexed: 0=root, 2=3rd, 4=5th, 6=7th, 1=9th but one octave up)
    chord_degrees = [0, 2, 4] 
    if len(scale_intervals) >= 7:
        chord_degrees.extend([6]) # Add 7th for richness
        chord_degrees.extend([1]) # Add 9th

    for degree in chord_degrees:
        octave_shift = 12 if degree == 1 else 0 # Bump 9th up an octave
        pitch = root_pitch + scale_intervals[degree % len(scale_intervals)] + octave_shift
        
        # Insert sustained note covering the whole item
        RPR.RPR_MIDI_InsertNote(
            take, False, False,
            0.0, item_length_ppq,
            0, int(pitch), int(velocity_base), True
        )
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # 4a. Add ReaSynth for a raw, rich oscillator sound
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a pad sound (increase release, mix in some saw wave)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.7) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.8) # Release

    # 4b. Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # ReaEQ Parameter map logic: 
    # Band 4 (Default High Shelf): Freq is param 12, Gain is param 13.
    # We drop Band 4 gain to 0.0 (-inf dB) so it acts as a drastic low-pass cut.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 13, 0.0) 

    # === Step 5: Automate Filter Sweep ===
    # Get the envelope for ReaEQ Band 4 Frequency (Param 12)
    # The 'True' flag creates the envelope if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 12, True)
    
    if env:
        # Sweep from 10% (muffled/dark) to 90% (bright/open) over the item length
        # Shape 2 is 'Slow Start/End', creating a smooth, musical curve
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, item_length, 0.9, 0, 0.0, False, True)
        RPR.RPR_Envelope_Sort(env)

    return f"Created '{track_name}' with a {bars}-bar automated EQ filter sweep at {bpm} BPM."
