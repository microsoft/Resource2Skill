def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Dry Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Parallel FX Return (Send/Return Routing) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the dry source track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the tracks and routing created.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Source (Dry) Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    src_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(src_track, "P_NAME", track_name, True)

    # Add ReaSynth for a dry pluck sound
    synth_idx = RPR.RPR_TrackFX_AddByName(src_track, "ReaSynth", False, -1)
    # Make it a short, staccato sound so the reverb tail stands out
    RPR.RPR_TrackFX_SetParamNormalized(src_track, synth_idx, 3, 0.0) # Attack fast
    RPR.RPR_TrackFX_SetParamNormalized(src_track, synth_idx, 4, 0.1) # Decay fast
    RPR.RPR_TrackFX_SetParamNormalized(src_track, synth_idx, 5, 0.0) # Sustain 0
    RPR.RPR_TrackFX_SetParamNormalized(src_track, synth_idx, 6, 0.1) # Release fast

    # === Step 3: Create FX Return Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    ret_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(ret_track, "P_NAME", f"{track_name} Echo/Verb", True)

    # Add ReaDelay (100% Wet, 0% Dry)
    delay_idx = RPR.RPR_TrackFX_AddByName(ret_track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(ret_track, delay_idx, 1, 0.0) # Dry = -inf
    RPR.RPR_TrackFX_SetParamNormalized(ret_track, delay_idx, 0, 0.8) # Wet = Nominal level

    # Add ReaVerbate AFTER delay (100% Wet, 0% Dry)
    reverb_idx = RPR.RPR_TrackFX_AddByName(ret_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(ret_track, reverb_idx, 1, 0.0) # Dry = -inf
    RPR.RPR_TrackFX_SetParamNormalized(ret_track, reverb_idx, 0, 0.8) # Wet = Nominal level
    RPR.RPR_TrackFX_SetParamNormalized(ret_track, reverb_idx, 2, 0.9) # Roomsize = Large
    RPR.RPR_TrackFX_SetParamNormalized(ret_track, reverb_idx, 4, 0.5) # Stereo Width

    # === Step 4: Route Source to Return (Create Send) ===
    # This establishes the parallel processing flow
    send_idx = RPR.RPR_CreateTrackSend(src_track, ret_track)
    # Category 0 = Send. Set volume to 0.5 (approx -6dB) so the effect sits behind the dry signal
    RPR.RPR_SetTrackSendInfo_Value(src_track, 0, send_idx, "D_VOL", 0.5)

    # === Step 5: Generate Staccato MIDI Item to Demonstrate the Effect ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(src_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root_midi = NOTE_MAP.get(key.upper(), 0) + 60 # Default to C4
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    note_length_qn = 0.25 # 1/16th note in quarter notes
    ticks_per_qn = 960
    note_len_ticks = int(note_length_qn * ticks_per_qn)

    # Simple arpeggio pattern representing scale degrees
    pattern_degrees = [0, 2, 4, 7, 0, 4, 2, -5] 
    
    RPR.RPR_MIDI_CountEvts(take, 0, 0, 0) # Initialize MIDI take
    
    event_count = 0
    for bar in range(bars):
        for beat in range(beats_per_bar):
            degree = pattern_degrees[event_count % len(pattern_degrees)]
            
            # Calculate octave offset (handles negative degrees cleanly)
            octave_offset = (degree // len(scale_intervals)) * 12
            scale_pitch = scale_intervals[degree % len(scale_intervals)]
            pitch = root_midi + octave_offset + scale_pitch
            
            # Position note exactly on the beat
            start_pos_qn = bar * beats_per_bar + beat
            start_pos_ticks = int(start_pos_qn * ticks_per_qn)
            end_pos_ticks = start_pos_ticks + note_len_ticks
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_pos_ticks, end_pos_ticks, 0, pitch, velocity_base, False)
            event_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' and routed it in parallel to '{track_name} Echo/Verb' return track over {bars} bars at {bpm} BPM."
