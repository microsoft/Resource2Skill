def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Cinematic Sub Boom",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Tuned Cinematic Sub Boom in the current REAPER project.
    Mimics the "Sub Generator" layering technique.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Sub Generator & Drive) ===
    # 1. ReaSynth (The Sub Generator)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 1.0)     # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 10.0)    # Attack ms (smooth transient)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 3000.0)  # Decay ms (The "Fall" parameter)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 5, 0.0)     # Sustain level (0 = natural exponential decay)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 6, 100.0)   # Release ms
    
    # Ensure pure sine (set other shapes to 0)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 7, 0.0)     # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 8, 0.0)     # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 9, 0.0)     # Triangle mix

    # 2. Saturation (The "Drive" parameter)
    fx_sat = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_sat, 0, 30.0)      # Amount %

    # === Step 4: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate sub pitch (Octave 1 for deep sub, MIDI notes 24 to 35)
    formatted_key = key.upper() if len(key) == 1 else key.capitalize()
    base_note = NOTE_MAP.get(formatted_key, 0)
    sub_note = 24 + base_note
    
    # Insert a sub boom trigger every 4 bars
    notes_added = 0
    for bar in range(0, bars, 4):
        # Trigger note on the downbeat, length 1/4 note.
        # The Decay parameter in ReaSynth handles the actual 3-second audio tail.
        start_qn = bar * beats_per_bar
        end_qn = start_qn + 1.0 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, sub_note, velocity_base, False)
        notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} tuned sub impacts over {bars} bars at {bpm} BPM."
