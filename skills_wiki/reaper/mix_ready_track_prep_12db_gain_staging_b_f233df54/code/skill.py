def create_pattern(
    project_name: str = "GordianKnot_Mixing",
    track_name: str = "MixPrep_SynthBass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Mix-Ready prepped track featuring -12dB gain staging, Gating, and Bracketing EQ.

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
        Status string describing the created track and FX chain.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Apply Gain Staging ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Gain Staging: Target -12.0 dB
    # Conversion: linear_vol = 10^(dB / 20) -> 10^(-12 / 20) ≈ 0.2511886
    target_vol_linear = 0.2511886
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", target_vol_linear)

    # === Step 3: Create Staccato MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine pitch (Octave 2 for Bass/Lower register)
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    base_pitch = 36 + root_val 
    
    # 1/8th note step, but note duration is 1/16th to create gaps for the Gate
    step_qn = 0.5
    note_len_qn = 0.25
    total_qn = bars * beats_per_bar
    current_qn = 0.0
    
    RPR.RPR_MIDI_DisableSort(take)
    step_count = 0
    
    while current_qn < total_qn:
        # Octave jumps on the downbeats
        octave_offset = 12 if (step_count % 4 == 0) else 0
        pitch = base_pitch + octave_offset
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, current_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, current_qn + note_len_qn)
        
        # Add slight velocity humanization
        vel = velocity_base if (step_count % 2 == 0) else max(10, velocity_base - 15)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
        
        current_qn += step_qn
        step_count += 1
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Mix Preparation FX Chain ===
    # Source instrument
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Gating (Controls bleed and ensures total silence between staccato notes)
    RPR.RPR_TrackFX_AddByName(track, "ReaGate", False, -1)
    
    # Bracketing EQ (To be manually swept for High-Pass/Low-Pass as per tutorial)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    return f"Created '{track_name}' with -12dB gain staging, ReaGate, and ReaEQ template over {bars} bars."
