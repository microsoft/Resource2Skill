def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with a 1/4-note "fake sidechain" volume automation pump.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) ===
    # Adding ReaSynth to generate our pad sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a lush saw pad
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.8)  # Saw wave mix
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.0)  # Attack (instant)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.5)  # Release

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 5: Generate Sustained 9th Chord ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define scale intervals
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Build a 9th chord (Root, 3rd, 5th, 7th, 9th)
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 0) # Start in octave 3
    chord_degrees = [0, 2, 4, 6, 8] # 1st, 3rd, 5th, 7th, 9th degree
    
    chord_pitches = []
    for degree in chord_degrees:
        octave_shift = degree // 7
        scale_idx = degree % 7
        pitch = root_midi + (octave_shift * 12) + scale_intervals[scale_idx]
        chord_pitches.append(pitch)
        
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Create "Fake Sidechain" Automation Envelope ===
    # Param 0 in ReaSynth is the Master Volume. 
    # 'True' parameter creates the envelope lane if it doesn't exist, as shown in the tutorial.
    env = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)
    
    if env:
        total_beats = bars * beats_per_bar
        # Loop through every quarter note to create the rhythmic pump
        for b in range(total_beats):
            beat_start_time = b * beat_length_sec
            
            # Point 1: Duck down immediately at the start of the beat (Kick transient)
            # Shape 0 = Linear, 5 = Bezier (smooth curve)
            RPR.RPR_InsertEnvelopePoint(env, beat_start_time, 0.0, 5, 0.5, False, True)
            
            # Point 2: Swell back up by the 8th note offbeat
            offbeat_time = beat_start_time + (beat_length_sec * 0.5)
            RPR.RPR_InsertEnvelopePoint(env, offbeat_time, 0.8, 0, 0.0, False, True)
            
            # Point 3: Hold the volume until slightly before the next beat
            hold_time = beat_start_time + beat_length_sec - 0.01
            if b < total_beats - 1:
                RPR.RPR_InsertEnvelopePoint(env, hold_time, 0.8, 0, 0.0, False, True)
                
        # Sort envelope points so REAPER renders them correctly
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with a {bars}-bar automated fake-sidechain volume pump at {bpm} BPM."
