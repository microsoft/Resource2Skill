def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Loudness Prep Kick",
    bpm: int = 125,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a loudness-optimized kick drum featuring transient clipping and high-mid saturation.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note for the kick fundamental.
        scale: Scale type (unused here, strictly using root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and FX chain.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item (4-on-the-floor kick) ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate MIDI note (Kick generally C2, MIDI pitch 36)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    root_pitch = 36 + NOTE_MAP.get(key, 0) # Base it around C2

    # Insert 1/4 notes for the specified number of bars
    total_beats = bars * beats_per_bar
    for beat in range(total_beats):
        start_time = beat * (60.0 / bpm)
        end_time = start_time + (60.0 / bpm) * 0.25 # Short staccato 1/16th note length
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, velocity_base, True)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    
    # 1. Generator: ReaSynth (Basic Kick Body & Transient)
    synth_fx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Give it a plucky envelope to create a transient
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_fx, 3, 0.05) # Decay: short
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_fx, 4, 0.0)  # Sustain: 0
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_fx, 5, 0.05) # Release: short
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_fx, 6, 0.4)  # Extra sine to beef it up
    
    # 2. Rule 2 of Mixing Loud: Have enough High-Mids
    # Saturation introduces upper harmonics that make the sound *perceivably* louder
    sat_fx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, sat_fx, 0, 0.6) # Saturation Amount 60%
    
    # 3. Rule 1 of Mixing Loud: Manage Dynamic Range (Shave the spiky transient)
    # Using ReaComp as a hard clipper/limiter
    comp_fx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_fx, 0, 0.4) # Threshold: low enough to catch the spike
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_fx, 1, 1.0) # Ratio: Inf:1 (Hard Limit)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_fx, 2, 0.0) # Attack: 0ms (Catch transient immediately)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_fx, 3, 0.0) # Release: 0ms (Reset instantly)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_fx, 4, 0.0) # Pre-comp: 0ms

    return f"Created '{track_name}' with {total_beats} kick hits over {bars} bars at {bpm} BPM, optimized with transient limiting and high-mid saturation."
