def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Floaty Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Lush Diatonic 7th Chord Progression (Imaj7 - IVmaj7 - iii7) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major is intended for this specific progression).
        bars: Number of bars to generate (forces 4 bars to complete the progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
    # Forcing to 4 bars to match the specific progression structure
    actual_bars = 4 
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * actual_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define Harmony & Insert Notes ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Start at octave 3 (MIDI note 48 for C3)
    root_midi = 48 + NOTE_MAP.get(key, 0)
    
    # Intervals for Imaj7, IVmaj7, iii7 relative to the root
    chords = [
        {"name": "Imaj7",  "intervals": [0, 4, 7, 11],   "start_bar": 0, "len_bars": 1},
        {"name": "IVmaj7", "intervals": [5, 9, 12, 16],  "start_bar": 1, "len_bars": 1},
        {"name": "iii7",   "intervals": [4, 7, 11, 14],  "start_bar": 2, "len_bars": 2},
    ]

    item_start_sec = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")
    item_start_qn = RPR.RPR_TimeMap2_timeToQN(0, item_start_sec)
    
    RPR.RPR_MIDI_DisableSort(take)
    
    note_count = 0
    for chord in chords:
        start_qn = item_start_qn + (chord["start_bar"] * beats_per_bar)
        end_qn = item_start_qn + ((chord["start_bar"] + chord["len_bars"]) * beats_per_bar)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        for interval in chord["intervals"]:
            pitch = root_midi + interval
            # Ensure pitch stays within valid MIDI range
            pitch = max(0, min(127, pitch))
            
            # Slightly humanize velocities for realism
            vel = max(1, min(127, int(velocity_base - (interval * 0.5))))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Basic Pad Sound) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Turn down volume slightly to accommodate 4-note chords (Param 0 is Volume)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.5)

    return f"Created '{track_name}' with {note_count} notes over {actual_bars} bars at {bpm} BPM in {key} {scale}"
