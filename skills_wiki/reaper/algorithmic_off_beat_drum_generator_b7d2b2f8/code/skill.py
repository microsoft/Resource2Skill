def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic OffBeat Drums",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an algorithmic, off-beat focused drum pattern natively simulating
    Reason's Beat Map Algorhythmic Drummer behavior.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused for drums, preserved for signature).
        scale: Scale type (unused for drums, preserved for signature).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: 
            density (float): 0.0 to 1.0, controls probability of 16th note algorithmic hits. Default 0.6.

    Returns:
        Status string describing the generated pattern.
    """
    import reaper_python as RPR
    import random

    density = kwargs.get("density", 0.6)

    # === Step 1: Set Tempo ===
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
    
    start_time = 0.0
    end_time = item_length
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # === Step 4: Algorithmic Pattern Generation ===
    ppq = 960  # Pulses per quarter note
    ticks_per_bar = ppq * 4
    total_ticks = ticks_per_bar * bars
    
    # Standard GM Drum Map Pitches
    KICK = 36
    SNARE = 38
    CH = 42
    OH = 46
    PERC1 = 60
    PERC2 = 62
    
    random.seed(42) # Deterministic generation so loops repeat predictably across renders
    note_count = 0
    step_ticks = ppq // 4 # 16th note steps
    
    for tick in range(0, total_ticks, step_ticks):
        is_quarter = (tick % ppq == 0)
        is_eighth_offbeat = (tick % ppq == ppq // 2)
        is_sixteenth_offbeat = not is_quarter and not is_eighth_offbeat
        
        # 1. Solid Foundation: Quarter notes
        if is_quarter:
            # 4-on-the-floor Kick
            RPR.RPR_MIDI_InsertNote(take, False, False, tick, tick + step_ticks - 20, 9, KICK, velocity_base, False)
            note_count += 1
            
            # Snare/Clap on Beats 2 and 4
            if (tick % (ppq * 2)) != 0:
                RPR.RPR_MIDI_InsertNote(take, False, False, tick, tick + step_ticks - 20, 9, SNARE, min(127, velocity_base + 10), False)
                note_count += 1
                
        # 2. Main Syncopation: 8th note off-beats (the "and")
        if is_eighth_offbeat:
            RPR.RPR_MIDI_InsertNote(take, False, False, tick, tick + step_ticks - 40, 9, OH, max(1, velocity_base - 10), False)
            note_count += 1
            
        # 3. Algorithmic Elements: 16th note off-beats (the "e" and "a")
        if is_sixteenth_offbeat:
            # Emulate the density mapping of an algorithmic drummer
            if random.random() < density:
                inst = random.choice([CH, PERC1, PERC2])
                # Lower, varied velocity for ghost notes/percussion
                vel = random.randint(max(1, velocity_base - 40), max(10, velocity_base - 10))
                # Shorter staccato note length
                RPR.RPR_MIDI_InsertNote(take, False, False, tick, tick + (step_ticks // 2), 9, inst, vel, False)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Percussive Synth for Native Audibility ===
    # Since third party drum VSTs aren't guaranteed, we configure ReaSynth as a percussive "click/bloop" generator
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Attack: Instant (percussive)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.05)  # Decay: Fast
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.0)   # Sustain: None
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.05)  # Release: Fast
    
    return f"Created '{track_name}' algorithmic drum pattern with {note_count} notes over {bars} bars at {bpm} BPM."
