def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Gain_Staged_Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a correctly Gain-Staged track demonstrating the "Trim + Unity Fader" method.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created gain-staged setup.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # CRITICAL: Keep track fader exactly at Unity (0 dB) to maximize fader throw resolution
    # 1.0 represents 0 dB in REAPER's linear volume scale
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 1.0)

    # === Step 3: Create MIDI Signal Source ===
    # We create a simple repeating root note pulse to generate an audio signal
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # Octave 3 root
    
    # Insert 1/4 notes for the duration of the item
    notes_to_create = bars * 4
    quarter_note_len = 1.0  # 1 beat
    for i in range(notes_to_create):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, i * quarter_note_len * (60.0/bpm))
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (i + 0.8) * quarter_note_len * (60.0/bpm))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_midi, velocity_base, False)

    # === Step 4: Add FX Chain (Source -> Trim -> Processing) ===
    
    # 1. Sound Source (Defaults to very loud, close to 0 dBFS)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. GAIN STAGING TRIM PLUGIN (The core skill)
    # Placed immediately after the instrument (or at the top of an audio track)
    trim_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    
    # We attenuate the signal by -12.0 dB right at the top of the chain.
    # This simulates targeting the -12 dBFS digital sweet spot mentioned in the tutorial.
    # Parameter 0 in "JS: Volume Adjustment" is "Adjustment (dB)"
    RPR.RPR_TrackFX_SetParam(track, trim_idx, 0, -12.0)
    
    # 3. Subsequent Processing (Now receiving signal at proper analog sweet spot)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    
    # Lower compressor threshold to match the newly gain-staged -12dBFS signal
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 0, 0.4) # Threshold roughly adapted

    return f"Created gain-staged track '{track_name}'. Fader is locked at 0dB (Unity). Source trimmed by -12dB using JS Volume before hitting ReaComp."
