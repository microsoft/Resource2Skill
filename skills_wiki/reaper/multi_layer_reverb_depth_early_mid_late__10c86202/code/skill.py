def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Layered Reverb Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Layer Reverb (Early/Mid/Late) on a track in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 60 + NOTE_MAP.get(key.upper(), 0) # Start at C4

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Create a sparse melody so the reverb tails can be heard clearly
    # We will play 3 quick notes, then wait for the rest of the bar
    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Note 1 (Beat 1)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                bar_start_beat * 960, 
                                (bar_start_beat + 0.25) * 960, 
                                0, root_midi, velocity_base, False)
        # Note 2 (Beat 1.5)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                (bar_start_beat + 0.5) * 960, 
                                (bar_start_beat + 0.75) * 960, 
                                0, root_midi + scale_intervals[1], velocity_base - 10, False)
        # Note 3 (Beat 2)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                (bar_start_beat + 1.0) * 960, 
                                (bar_start_beat + 1.5) * 960, 
                                0, root_midi + scale_intervals[2], velocity_base + 10, False)
        note_count += 3

    # === Step 4: Add FX Chain ===
    
    # 4a. Sound Source (ReaSynth)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Make it slightly plucky
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 1, 0.2) # Attack short
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.4) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.1) # Sustain low

    # 4b. Layer 1: Short Reverb (Early Reflections)
    fx_verb1 = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 2, 0.33)  # Room size: Small
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 3, 0.50)  # Dampening: High (Darker)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 5, 0.00)  # Initial delay: 0ms
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 0, 0.25)  # Wet level
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 1, 0.70)  # Dry level (Unity-ish)

    # 4c. Layer 2: Mid Reverb (Body & Width)
    fx_verb2 = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 2, 0.68)  # Room size: Medium
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 3, 0.25)  # Dampening: Medium
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 5, 0.20)  # Initial delay: ~50ms
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 0, 0.15)  # Wet level (Quieter)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 1, 0.70)  # Dry level

    # 4d. Layer 3: Long Reverb (Epic Tail)
    fx_verb3 = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 2, 0.95)  # Room size: Large
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 3, 0.08)  # Dampening: Low (Bright)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 5, 0.32)  # Initial delay: ~80ms
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 0, 0.10)  # Wet level (Quietest, long decay)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 1, 0.70)  # Dry level

    return f"Created '{track_name}' with a 3-layer depth reverb (Short/Mid/Long) and {note_count} notes over {bars} bars."
