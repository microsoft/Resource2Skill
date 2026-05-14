def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Synth Bass Setup",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Synth Bass Sequence Setup in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}

    # Normalize key input
    key_upper = key.upper()
    root_midi = NOTE_MAP.get(key_upper, 0) + 36  # Offset roughly to C2

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Stock Alternatives) ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if synth_idx >= 0:
        # Tweak ReaSynth for a plucky saw bass
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.0)  # Square mix 0%
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 1.0)  # Saw mix 100%
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.01) # Attack fast
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.1)  # Decay short
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.2)  # Sustain low
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.1)  # Release fast

    # Add Moog Filter JSFX
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Moog 4-Pole Filter", False, -1)
    if filter_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, filter_idx, 0, 800.0) # Cutoff Hz
        RPR.RPR_TrackFX_SetParam(track, filter_idx, 1, 0.3)   # Resonance

    # === Step 4: Create MIDI Item and Pattern ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    start_time = 0.0
    end_time = start_time + item_length
    
    # Create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
    take = RPR.RPR_GetActiveTake(item)
    
    notes_added = 0
    # Generate an algorithmic-style 16th note bassline
    for b in range(bars):
        for beat in range(beats_per_bar):
            for sixteenth in range(4):
                # Calculate timing
                pos_time = start_time + (b * bar_length_sec) + (beat * 60.0/bpm) + (sixteenth * 15.0/bpm)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_time)
                # 80% gate length for staccato feel
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_time + (15.0/bpm * 0.8))
                
                # Accents and dynamics
                vol = velocity_base if sixteenth == 0 else max(10, velocity_base - 30)
                pitch = root_midi
                
                # Occasional octave jump (algorithmic feel)
                if sixteenth == 3 and beat % 2 == 1:
                    pitch += 12
                
                # Insert note
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vol, False)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM (Stock VSTi Approximation)"
