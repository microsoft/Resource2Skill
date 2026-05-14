def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Shimmering Generative Bass",
    bpm: int = 120,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a syncopated 16th-note bassline processed with atmospheric delay and reverb,
    approximating the generative bass and shimmer effects from the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # Setup Octaves
    root_val = NOTE_MAP.get(key.upper(), 2) # Default to D if invalid
    base_note = 36 + root_val # Base octave (e.g., D2)
    octave_note = base_note + 12 # Higher octave (e.g., D3)

    # Hardcoded 16-step "Detroit Bounce" style pattern 
    # 1 = low root, 2 = high octave, 0 = rest
    rhythm_pattern = [1, 0, 0, 2,  0, 0, 1, 0,  1, 0, 2, 0,  0, 1, 0, 0]

    qn_length = RPR.RPR_TimeMap2_beatsToTime(0, 1.0, 0) - RPR.RPR_TimeMap2_beatsToTime(0, 0.0, 0)
    sixteenth_length = qn_length / 4.0

    note_count = 0
    # Generate notes across specified bars
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        for step, val in enumerate(rhythm_pattern):
            if val != 0:
                pitch = base_note if val == 1 else octave_note
                start_time = bar_start_time + (step * sixteenth_length)
                # Staccato lengths (80% of a 16th note) to let the reverb breathe
                end_time = start_time + (sixteenth_length * 0.8) 

                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

                RPR.RPR_MIDI_InsertNote(
                    take, False, False,
                    start_ppq, end_ppq,
                    0, pitch, velocity_base, False
                )
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain Approximation ===
    # A. Tone Generator (ReaSynth)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # B. EQ to tame highs and create a "filtered patch" feel
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # C. Delay for rhythmic ping-pong texture
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    
    # D. Long Reverb Wash to emulate the "Shimmer" tail
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    # Give the reverb a very large room size to simulate the ethereal space
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb, 2, 0.9) # Room Size parameter

    return f"Created '{track_name}' with {note_count} rhythmic MIDI notes over {bars} bars at {bpm} BPM (Stock plugins substitute original VSTs)"
