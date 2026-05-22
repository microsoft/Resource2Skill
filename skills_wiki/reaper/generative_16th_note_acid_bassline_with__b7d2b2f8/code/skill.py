def create_generative_acid_bass(
    project_name: str = "MyProject",
    track_name: str = "Distorted Acid Bass",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a generative 16th-note bassline processed with heavy distortion.
    Approximates the workflow of using a generative sequencer and saturation VSTs.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (minor, pentatonic_minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Generative MIDI Algorithm ===
    base_note = 36 + NOTE_MAP.get(key, 0) # e.g., C2 = 36
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generate a 1-bar looping pattern
    pattern = []
    for step in range(16):
        # 15% chance of a rest
        if random.random() < 0.15: 
            pattern.append(None)
            continue
            
        # Pitch selection logic (weighted towards root and octave)
        rand_val = random.random()
        if rand_val < 0.60:
            pitch_offset = 0 # Root
        elif rand_val < 0.75:
            pitch_offset = 12 # Octave up
        else:
            pitch_offset = random.choice(scale_intervals) # Random scale degree
            
        pitch = base_note + pitch_offset
        
        # Velocity accent logic
        velocity = velocity_base + random.randint(-15, 10)
        if step % 4 == 0: # Downbeats
            velocity += 15 
            
        velocity = min(127, max(1, velocity))
        pattern.append((pitch, velocity))

    # === Step 4: Create MIDI Item and Insert Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    step_len = bar_length_sec / 16.0
    note_count = 0
    
    # Loop the generated 1-bar pattern across requested bars
    for b in range(bars):
        for step, note_data in enumerate(pattern):
            if note_data is None:
                continue
                
            pitch, vel = note_data
            start_time = (b * bar_length_sec) + (step * step_len)
            
            # Make notes slightly staccato (80% of a 16th note)
            end_time = start_time + (step_len * 0.8) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(vel), False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Synth + Distortion FX) ===
    # Add stock synth (mixing Square and Saw for acid character)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.0)  # Vol
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.4)  # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.2)  # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.1)  # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.3)  # Release
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.8)  # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.7)  # Saw mix

    # Add Distortion (mimicking the "BLENDZ" plugin drive)
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    # Pushing the gain up to clip the signal aggressively
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 15.0) # Gain (dB)
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 1, 0.5)  # Hard clip point
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 2, -6.0) # Max output volume to prevent blowing out mix

    return f"Created '{track_name}' with a generative {key} {scale} sequence ({note_count} notes over {bars} bars) routed through heavy distortion."
