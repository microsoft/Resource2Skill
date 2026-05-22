def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat Bass",
    bpm: int = 124,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Electronic Offbeat Bass Rhythm in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (120-130 recommended for Dance).
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Note map lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root pitch in the bass register (Octave 1 where C1 = 36)
    root_pitch = 36 + NOTE_MAP.get(key.capitalize(), 4) # Defaults to E1 (40) if invalid key

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument ===
    # Using stock ReaSynth as a stand-in for the third-party synth
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Basic EQ to tame highs and boost lows
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)
    
    note_count = 0
    note_duration_qn = 0.25 # 1/16th note duration for tight, staccato bass 

    # === Step 5: Generate Offbeat Pattern ===
    for bar in range(bars):
        bar_start_qn = bar * 4.0
        for beat in range(4):
            # Upbeat position (the "and" of the beat, offset by 0.5 QN)
            start_qn = bar_start_qn + beat + 0.5
            end_qn = start_qn + note_duration_qn
            
            # Convert Quarter Notes to Absolute Project Time
            start_time = start_qn * (60.0 / bpm)
            end_time = end_qn * (60.0 / bpm)
            
            # Convert Absolute Project Time to MIDI PPQ (Ticks)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the MIDI Note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, root_pitch, velocity_base, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} offbeat notes over {bars} bars at {bpm} BPM in key {key}."
