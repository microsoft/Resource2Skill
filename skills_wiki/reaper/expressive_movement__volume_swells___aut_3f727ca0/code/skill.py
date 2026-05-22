def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a sustained synth pad with automated volume swells and auto-pan in REAPER.

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
        Status string describing the created track and automation points.
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

    # Extract base MIDI note (default to C3 = 48)
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 48 
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Build a dense chord (Root, 3rd, 5th, 7th) depending on scale availability
    chord_degrees = [0, 2, 4, 6] 
    chord_pitches = []
    for deg in chord_degrees:
        if deg < len(scale_intervals):
            chord_pitches.append(root_pitch + scale_intervals[deg])
            
    # Add a low octave root for bass
    chord_pitches.append(root_pitch - 12)

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
    total_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Get PPQ length for the MIDI notes
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, total_length_sec)
    
    # Insert the sustained chord
    for pitch in chord_pitches:
        # Notes span the entire item length
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, pitch, velocity_base, True)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design (ReaSynth) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a pad sound: Mix saw (param 3) and square (param 2)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.8) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.2) # Extra attack time

    # === Step 5: Automate Pan (Auto-Pan Effect) ===
    # Force track selection to use Action commands safely
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Command 40407: Track: Toggle track pan envelope visible
    RPR.RPR_Main_OnCommand(40407, 0)
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    
    if env_pan:
        # Create an LFO-like pan envelope: sweep left to right every bar
        for b in range(bars):
            t_start = b * bar_length_sec
            t_mid = t_start + (bar_length_sec / 2.0)
            t_end = t_start + bar_length_sec
            
            # shape=0 is linear, shape=1 is square, shape=2 is slow start/end
            RPR.RPR_InsertEnvelopePoint(env_pan, t_start, -0.75, 2, 0, False, True)
            RPR.RPR_InsertEnvelopePoint(env_pan, t_mid, 0.75, 2, 0, False, True)
            if b == bars - 1:
                RPR.RPR_InsertEnvelopePoint(env_pan, t_end, -0.75, 2, 0, False, True)
                
        RPR.RPR_Envelope_Sort(env_pan)

    # === Step 6: Automate Volume (Swell Effect) ===
    # Command 40406: Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40406, 0)
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env_vol:
        # Volume values in ReaScript: 0.0 is -inf, 1.0 is 0dB, 2.0 is +6dB
        # We start at -inf, swell to 0dB at the halfway point, then back to -inf
        mid_point_sec = total_length_sec / 2.0
        
        # Insert Envelope Point: env, time, value, shape(0=linear), tension, selected, noSort
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, mid_point_sec, 1.0, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, total_length_sec, 0.0, 0, 0, False, True)
        
        RPR.RPR_Envelope_Sort(env_vol)

    return f"Created '{track_name}' pad with {len(chord_pitches)} voices over {bars} bars at {bpm} BPM, featuring Volume Swell and Pan automation."
