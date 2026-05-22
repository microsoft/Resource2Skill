def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Bassline",
    bpm: int = 125,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates a generative, syncopated 16th-note bassline through a plucky native synth chain.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    if scale not in SCALES:
        scale = "minor"
        
    scale_degrees = SCALES[scale]
    # Place root note in the bass register (Octave 1 = MIDI ~24)
    root_midi = NOTE_MAP.get(key, 4) + 24 

    # === Step 1: Initialize Project Temp ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

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

    # === Step 4: Generative Rhythm Logic ===
    # Format: (16th_step_index, scale_degree, octave_offset, velocity_multiplier, length_multiplier)
    base_pattern = [
        (0,  0, 0, 1.1, 0.8), # Downbeat root
        (2,  0, 1, 0.8, 0.5), # Offbeat high octave
        (3,  0, 0, 0.7, 0.5), # Syncopated pickup
        (5,  2, 0, 1.0, 0.8), # 3rd degree
        (7,  0, 0, 0.9, 0.5), 
        (8,  0, 0, 1.1, 0.8), # Beat 3 root
        (10, 4, 0, 1.0, 0.5), # 5th degree
        (11, 6, 0, 1.0, 0.8), # 7th degree
        (14, 0, 1, 1.1, 0.8), # Anticipation for next bar
    ]

    item_start_time = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")
    item_start_qn = RPR.RPR_TimeMap2_timeToQN(0, item_start_time)
    step_length_qn = 0.25 # 1/16th note in QN

    for b in range(bars):
        # Add a slight variation on the final bar for turnaround
        current_pattern = base_pattern
        if b == bars - 1:
            current_pattern = base_pattern + [(15, 4, 1, 1.0, 0.5)] 

        for p in current_pattern:
            step, degree, oct_offset, vel_mod, len_mod = p
            
            # Map scale degree to exact MIDI pitch, allowing wrapping for scales of any length
            octave = degree // len(scale_degrees) + oct_offset
            idx = degree % len(scale_degrees)
            pitch = root_midi + (octave * 12) + scale_degrees[idx]
            pitch = max(0, min(127, pitch))

            vel = int(velocity_base * vel_mod)
            vel = max(1, min(127, vel))

            # Calculate exact project quarters and convert to MIDI ticks (PPQ)
            abs_start_qn = item_start_qn + (b * 4.0) + (step * step_length_qn)
            abs_end_qn = abs_start_qn + (step_length_qn * len_mod)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, abs_start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, abs_end_qn)

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (FX Chain) ===
    
    # 1. ReaSynth (Analog-style saw/square blend with pluck envelope)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.4)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.01) # Attack (sharp)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.15) # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)  # Sustain (0 for pluck)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.1)  # Release
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.7)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.5)  # Saw mix

    # 2. JS: Distortion (Adds analog warmth/drive)
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    if dist_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 3.0) # Gain
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 1, 1.5) # Hard clip / Mode

    # 3. JS: Moog 24dB Filter (Classic resonant low-pass to tame the highs)
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Moog 24dB Filter", False, -1)
    if filter_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, filter_idx, 0, 0.35) # Cutoff frequency
        RPR.RPR_TrackFX_SetParam(track, filter_idx, 1, 0.60) # Resonance bump

    return f"Created '{track_name}' featuring a generative syncopated 16th-note pattern over {bars} bars in {key} {scale} at {bpm} BPM."
