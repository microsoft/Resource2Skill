def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat Bass",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create an Offbeat Bassline Groove in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (120-135 recommended for dance genres).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    # Base MIDI pitch for bass (Octave 2 is standard for mid-bass)
    formatted_key = key.capitalize() if len(key) == 1 else key[0].upper() + key[1:].lower()
    root_pitch = NOTE_MAP.get(formatted_key, 0) + 36 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

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
    
    # Generate Offbeat Rhythm
    # We place notes strictly on the 'and' of each beat (beats 0.5, 1.5, 2.5, 3.5)
    note_count = 0
    note_duration_qn = 0.25  # 16th note duration for a tight, staccato bass
    
    for bar in range(bars):
        for beat in range(beats_per_bar):
            # Calculate start time in quarter notes (QN)
            start_qn = (bar * beats_per_bar) + beat + 0.5
            end_qn = start_qn + note_duration_qn
            
            # Convert Quarter Notes to Seconds, then to MIDI PPQ
            start_sec = (start_qn / (bpm / 60.0))
            end_sec = (end_qn / (bpm / 60.0))
            
            start_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec))
            end_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec))
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Using stock ReaSynth to emulate the sequenced bass sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth parameters for a plucky electronic bass
    # Param 0: Volume (normalized lower to prevent master clipping)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.4)
    # Param 2: Square Mix (Add harmonics/body)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.6)
    # Param 3: Saw Mix (Add grit)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.4)
    # Param 5: Attack (Fastest)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.0)
    # Param 6: Decay (Short ~0.15)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.15)
    # Param 7: Sustain (Zero)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 7, 0.0)
    # Param 8: Release (Fast)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 8, 0.1)

    return f"Created '{track_name}' with {note_count} offbeat notes over {bars} bars at {bpm} BPM"
