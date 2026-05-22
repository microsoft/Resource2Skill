def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pulse",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Pulse track featuring precise Volume fade-in and tempo-synced Pan sweeps.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # --- 1. Setup & Music Theory ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_midi = 36 + NOTE_MAP.get(key, 0) # Root note around C2
    
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # --- 2. Track & FX Setup ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Exclusively select the track so automation commands apply correctly
    RPR.RPR_SetOnlyTrackSelected(track)

    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0) # Osc 1 Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 1.0) # Sawtooth mix (bright tone)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0) # Pulse width
    
    # --- 3. Generate MIDI Item (16th note pulse) ---
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    step_sec = (60.0 / bpm) * 0.25 # 1/16th note
    note_len_sec = step_sec * 0.7  # Staccato
    
    current_time = 0.0
    RPR.RPR_MIDI_DisableSort(take)
    
    while current_time < item_length - 0.01:
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, current_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, current_time + note_len_sec)
        
        # Add slight velocity variation for groove
        vel = velocity_base if (current_time % step_sec < 0.01) else int(velocity_base * 0.8)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_midi, vel, False)
        current_time += step_sec
        
    RPR.RPR_MIDI_Sort(take)

    # --- 4. Automate Volume (Tension Fade-in) ---
    # Trigger REAPER Action to reveal and activate the Volume envelope lane
    RPR.RPR_Main_OnCommand(40406, 0) 
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if vol_env:
        # API parameters: RPR_InsertEnvelopePoint(envelope, time, value, shape, tension, selected, noSortIn)
        # Shape 2 = "Slow start/end" (Bezier-like curve)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, True)         # Start at -inf (0.0)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 0, 0.0, False, True) # End at 0dB (1.0)
        RPR.RPR_Envelope_Sort(vol_env)

    # --- 5. Automate Pan (Tempo-synced Auto-panner) ---
    # Trigger REAPER Action to reveal and activate the Pan envelope lane
    RPR.RPR_Main_OnCommand(40456, 0)
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    
    if pan_env:
        # Insert a panning point at the start of every bar, alternating sides
        for b in range(bars + 1):
            t = b * bar_length_sec
            val = -0.8 if b % 2 == 0 else 0.8 # Alternate 80% Left and 80% Right
            # Shape 2 ensures a smooth sinusoidal sweep rather than an abrupt jump
            RPR.RPR_InsertEnvelopePoint(pan_env, t, val, 2, 0.0, False, True)
            
        RPR.RPR_Envelope_Sort(pan_env)

    return f"Created '{track_name}' with rhythmic pulse, Volume fade-in, and Pan sweeps over {bars} bars at {bpm} BPM"
