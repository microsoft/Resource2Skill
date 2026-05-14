def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bassline",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Groovy Syncopated Slap Bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc. - mostly utilizes root and chromatics here).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

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
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key.upper(), 4) # Default E
    root_pitch = 36 + root_val # Octave 2, solid bass range
    
    # Helper for humanization
    def humanize(val, variance):
        return val + (random.random() - 0.5) * variance

    # === Step 4: Generate Pattern ===
    # A 1-bar looping phrase mimicking the visual piano roll in the tutorial
    for b in range(bars):
        bar_offset = b * 4.0  # 4 beats per bar
        
        # Note structure: (beat_start, length, pitch_offset, velocity)
        pattern = [
            # Downbeat plucked root
            (0.00, 0.35, 0, velocity_base),
            
            # Syncopated pluck (splits the note)
            (0.75, 0.25, 0, velocity_base - 10),
            
            # First octave Slap (very short, max velocity)
            (1.50, 0.15, 12, 127),
            
            # On-beat pluck
            (2.00, 0.35, 0, velocity_base),
            
            # Second octave Slap (syncopated)
            (2.75, 0.15, 12, 127),
            
            # Chromatic walk-up to the next downbeat
            (3.25, 0.25, -2, velocity_base - 15),
            (3.50, 0.25, -1, velocity_base - 5)
        ]
        
        for start, length, p_offset, vel in pattern:
            # Apply micro-timing humanization (+/- 0.03 beats)
            h_start = humanize(start, 0.06)
            h_start = max(0, h_start) # Prevent negative starts
            
            # Apply velocity humanization (+/- 8)
            h_vel = int(humanize(vel, 16))
            h_vel = max(1, min(127, h_vel)) # Clamp 1-127
            
            # Calculate absolute times
            start_time = (bar_offset + h_start) * (60.0 / bpm)
            end_time = (bar_offset + h_start + length) * (60.0 / bpm)
            
            # Convert to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert note
            pitch = root_pitch + p_offset
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, h_vel, True)

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Stock FX) ===
    # Add ReaSynth for a synthetic bass tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a bassy, slightly harmonically rich tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.8) # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.3) # Saw mix

    # Add ReaComp to tame the slaps and glue the dynamics
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -18.0) # Threshold (-18dB)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio (4:1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 5.0)   # Attack (5ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 100.0) # Release (100ms)

    return f"Created '{track_name}' with {bars * 7} humanized notes over {bars} bars at {bpm} BPM."
