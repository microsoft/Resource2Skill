def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Bass",
    bpm: int = 120,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a Syncopated Step-Sequenced Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
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

    scale_intervals = SCALES.get(scale, SCALES["minor"])
    # Set bass to standard synth bass octave range (MIDI note ~36 is C2)
    base_midi_note = 36 + NOTE_MAP.get(key, 0)
    if base_midi_note > 45: 
        base_midi_note -= 12 # Keep it strictly in the bass register
        
    def get_scale_note(degree, octave_offset=0):
        deg = degree % len(scale_intervals)
        octaves = (degree // len(scale_intervals)) + octave_offset
        return base_midi_note + (octaves * 12) + scale_intervals[deg]

    # Matrix sequence: (16th_step_index, scale_degree, octave_offset, duration_multiplier)
    pattern = [
        (0,  0,  0, 1.0), # Downbeat root
        (3,  0,  1, 0.5), # Syncopated high octave jump
        (6,  2,  0, 1.0), # Minor 3rd emphasis
        (8,  0,  0, 1.5), # Mid-bar root anchor
        (11, 6, -1, 0.5), # Low 7th pickup
        (14, 4,  0, 1.0)  # 5th leading back
    ]

    sixteenth_sec = bar_length_sec / 16.0
    note_count = 0
    
    for bar in range(bars):
        bar_start_pos = bar * bar_length_sec
        for step, degree, oct_off, dur in pattern:
            start_time = bar_start_pos + (step * sixteenth_sec)
            end_time = start_time + (sixteenth_sec * 0.8 * dur) # 80% staccato length
            pitch = get_scale_note(degree, oct_off)
            
            # Convert time to PPQ for exact MIDI placement
            start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            # Alternate velocity slightly for humanization/groove
            vel = velocity_base if step in [0, 8] else velocity_base - 15
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add Sound Design FX Chain ===
    # Plucky, filtered analog-style bass tone
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_synth >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 0, 0.4)  # Volume
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.7)  # Square mix
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.6)  # Saw mix
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 6, 0.0)  # Attack
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 7, 0.15) # Decay
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 8, 0.0)  # Sustain
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 9, 0.15) # Release
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 11, 0.3) # Filter Cutoff
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 12, 0.4) # Filter Resonance
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 13, 0.6) # Filter Env Amount
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 14, 0.0) # Filter Env Attack
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 15, 0.2) # Filter Env Decay

    # Add Saturation to thicken the bass and add harmonics
    fx_sat = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    if fx_sat >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_sat, 0, 0.45) # Drive amount

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"
