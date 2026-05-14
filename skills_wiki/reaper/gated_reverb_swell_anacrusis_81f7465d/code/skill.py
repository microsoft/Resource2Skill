def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Snare Reverb Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Gated Reverb Swell (Anacrusis) in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused for noise snare, kept for signature).
        scale: Scale type (unused, kept for signature).
        bars: Number of bars. The swell will happen at the end of the final bar.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Synth Snare + Huge Reverb) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape the synth into a snappy noise burst (Snare)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 1.0)  # Noise Mix up
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.1)  # Decay time short
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 10, 0.0) # Sustain level 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 11, 0.1) # Release time short

    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    # Shape the reverb for a massive, bright tail
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.8)  # Wet high
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.5)  # Dry lower
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.95) # Room size huge
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 3, 0.1)  # Dampening low (bright)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar
    item_length = bar_length * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Insert a Snare hit on Beat 3 of every bar
    note_pitch = 48 # Arbitrary C4
    for b in range(bars):
        # Beat 3 (0-indexed: beat 0, beat 1, beat 2)
        start_time = b * bar_length + (2 * beat_length) 
        end_time = start_time + 0.1
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_pitch, velocity_base, False)
    
    # === Step 5: Automate Track Volume for Swell and Cut ===
    # Force Volume Envelope to be active and visible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    # If envelope is somehow hidden, toggle guarantees it exists in chunk
    if not env:
        RPR.RPR_Main_OnCommand(40406, 0)
        env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    if env:
        # Clear any existing points just in case
        RPR.RPR_DeleteEnvelopePointRange(env, 0.0, item_length + 1.0)
        
        # Point Shapes: 0 = Linear, 1 = Square
        # In REAPER Volume Envelope: 0.0 = -inf, 1.0 = 0dB, ~1.9 = +5.5dB
        
        # 1. Start completely muted
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, 1, 0.0, False, True)
        
        for b in range(bars):
            snare_hit_time = b * bar_length + (2 * beat_length)
            
            # 2. Unmute exactly when snare hits (Square shape holds 1.0 flat)
            RPR.RPR_InsertEnvelopePoint(env, snare_hit_time, 1.0, 1, 0.0, False, True)
            
            # 3. Only trigger the swell/cut on the very last measure
            if b == bars - 1:
                swell_start_time = b * bar_length + (3 * beat_length) # Start swell at Beat 4
                peak_time = (b + 1) * bar_length - 0.001              # Peak just before downbeat
                end_time = (b + 1) * bar_length                       # Exact downbeat cut
                
                # Ramp up linearly
                RPR.RPR_InsertEnvelopePoint(env, swell_start_time, 1.0, 0, 0.0, False, True)
                # Peak at approx +5.5dB
                RPR.RPR_InsertEnvelopePoint(env, peak_time, 1.9, 0, 0.0, False, True)
                # Square drop to -inf
                RPR.RPR_InsertEnvelopePoint(env, end_time, 0.0, 1, 0.0, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with gated reverb swell over {bars} bars at {bpm} BPM."
