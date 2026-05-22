def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Sweep",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Resonant Filter Sweep in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the sweep over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Automated Filter Sweep' with Wah/Filter Sweep over 4 bars at 120 BPM"
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

    # === Step 3: Create MIDI Item & Diatonic 9th Chord ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    item_length = beat_sec * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine diatonic 9th chord (Root, 3rd, 5th, 7th, 9th)
    root_midi = NOTE_MAP.get(key, 0) + 48  # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 6, 8]
    chord_pitches = []
    
    for deg in chord_degrees:
        octave_shift = deg // len(scale_intervals)
        interval = scale_intervals[deg % len(scale_intervals)]
        chord_pitches.append(root_midi + interval + (octave_shift * 12))

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # Insert the sustained chord
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Synth & EQ) ===
    # A) Add ReaSynth (Set to Sawtooth for rich harmonics)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.15) # Volume (attenuated to prevent clipping)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 1.0)  # Sawtooth mix (full)

    # B) Add ReaEQ (Configure Band 3 as a sharp resonant peak)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 7, 18.0) # Param 7 = Band 3 Gain (Set to +18dB)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 8, 4.0)  # Param 8 = Band 3 Q (Tight peak)

    # === Step 5: Automate Plugin Parameter ===
    # Force creation of automation envelope for ReaEQ Band 3 Frequency (Param 6)
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 6, True)

    # Draw the sweep: Start low -> Peak at midpoint -> End low
    shape = 0 # Linear shape
    tension = 0
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, shape, tension, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length / 2, 0.85, shape, tension, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length, 0.1, shape, tension, False, True)
    
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with Wah/Filter Sweep automation over {bars} bars at {bpm} BPM in {key} {scale}"
