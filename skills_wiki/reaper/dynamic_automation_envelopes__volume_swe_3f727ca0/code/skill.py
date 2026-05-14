def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Dynamic Automation Envelopes (Volume Swells, Auto-Pan, & Mute Gating) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (minimum 2 recommended).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the automation generation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Add Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth to generate a sustained tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item & Insert Chord ===
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    item_len = bar_len * bars
    
    # Create time selection and insert MIDI item via Action to ensure standard setup
    RPR.RPR_GetSet_LoopTimeRange(True, False, 0.0, item_len, False)
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40214, 0) # Action: Insert new MIDI item...
    
    item = RPR.RPR_GetTrackMediaItem(track, 0)
    take = RPR.RPR_GetActiveTake(item)
    
    # Calculate triad chord pitches
    root_pitch = 48 + NOTE_MAP.get(key, 0) # Octave 3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_pitches = [
        root_pitch + scale_intervals[0], # Root
        root_pitch + scale_intervals[2], # 3rd
        root_pitch + scale_intervals[4]  # 5th
    ]
    
    # Insert sustained chord spanning the entire item length
    start_ppq = 0
    end_ppq = int(960 * beats_per_bar * bars) # Assuming standard 960 PPQ
    
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Toggle Envelopes Visible ===
    # Envelopes must be visible/active to fetch them by name
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40408, 0) # Toggle track pan envelope visible
    RPR.RPR_Main_OnCommand(40410, 0) # Toggle track mute envelope visible

    # === Step 5: Draw Automation Envelopes ===
    
    # 1. Volume Swell (starts at silence, swells to 0dB over 2 bars)
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env_vol:
        # shape: 2 = Slow start/end (S-Curve)
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 2, 0, False, True)
        swell_end = min(bar_len * 2, item_len)
        RPR.RPR_InsertEnvelopePoint(env_vol, swell_end, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_Sort(env_vol)

    # 2. Pan Sweep (Ping-pong Left to Right every bar)
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if env_pan:
        # shape: 0 = Linear
        for b in range(bars + 1):
            time_pos = b * bar_len
            pan_val = -1.0 if b % 2 == 0 else 1.0
            if b == bars: 
                pan_val = 0.0 # Return to center at the very end
            RPR.RPR_InsertEnvelopePoint(env_pan, time_pos, pan_val, 0, 0, False, True)
        RPR.RPR_Envelope_Sort(env_pan)

    # 3. Mute Stutter / Trance Gate (1/8th note gating in the final bar)
    env_mute = RPR.RPR_GetTrackEnvelopeByName(track, "Mute")
    if env_mute and bars >= 1:
        # Initial unmuted state
        RPR.RPR_InsertEnvelopePoint(env_mute, 0.0, 0.0, 1, 0, False, True) 
        
        stutter_start = bar_len * (bars - 1)
        step = bar_len / 8 # 1/8th note lengths
        
        for i in range(8):
            time_pos = stutter_start + i * step
            # Mute = 1.0, Unmute = 0.0. Shape 1 = Square (instant step change)
            val = 1.0 if i % 2 == 1 else 0.0 
            RPR.RPR_InsertEnvelopePoint(env_mute, time_pos, val, 1, 0, False, True)
            
        # Ensure it ends unmuted
        RPR.RPR_InsertEnvelopePoint(env_mute, item_len, 0.0, 1, 0, False, True)
        RPR.RPR_Envelope_Sort(env_mute)

    # Clear time selection
    RPR.RPR_GetSet_LoopTimeRange(True, False, 0.0, 0.0, False)

    return f"Created '{track_name}' with Volume swell, Pan sweeps, and 1/8th Mute stutters over {bars} bars at {bpm} BPM in {key} {scale}."
