def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Stock Bass Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a placeholder stock bass synthesizer track with an 8th-note pulse sequence.
    (Fallback generated due to source video lacking explicit musical data and relying on proprietary VSTs).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root note in a bass register (Octave 2)
    root_offset = NOTE_MAP.get(key.capitalize(), 0)
    root_midi = 24 + root_offset # C1 is 24, C2 is 36

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Native Instrument FX (ReaSynth) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item & Sequence ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Generate continuous 8th note sequence
    note_duration_beats = 0.5 # 1/8th note
    note_duration_sec = (60.0 / bpm) * note_duration_beats
    
    note_count = 0
    for bar in range(bars):
        for beat in range(8): # 8 eighth-notes per bar
            start_time = (bar * bar_length_sec) + (beat * note_duration_sec)
            end_time = start_time + (note_duration_sec * 0.8) # Slightly staccato for definition
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert root pitch
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_midi, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} bass notes over {bars} bars at {bpm} BPM using stock ReaSynth."
