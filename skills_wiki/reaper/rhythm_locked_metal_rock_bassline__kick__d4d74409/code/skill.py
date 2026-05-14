def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass (Kick-Locked)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a rhythmically locked metal/rock bassline mirroring a kick drum pattern, 
    with velocity reduction for realistic pick attack and octave jumps for fills.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (will loop a 2-bar phrase).
        velocity_base: Base MIDI velocity (lowered to ~110 to reduce VST harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    
    # 1. Look up base MIDI pitch for the root note (octave 1 for bass)
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 24) # Default to low C1

    # Define a 2-bar syncopated metal/djent kick pattern
    # Format: (start_16th, duration_16ths, pitch_offset, velocity_offset)
    pattern_sequence = [
        # Bar 1: Stuttering chugs
        (0,  1.5, 0, 0),  # Beat 1
        (2,  1.0, 0, 0),  # Beat 1 &
        (4,  1.5, 0, 0),  # Beat 2
        (7,  1.0, 0, 0),  # Beat 2 ah
        (8,  1.5, 0, 0),  # Beat 3
        (10, 1.0, 0, 0),  # Beat 3 &
        (12, 1.5, 0, 0),  # Beat 4
        
        # Bar 2: Chugs leading into octave jump fill
        (16, 1.5, 0, 0),  # Beat 1
        (18, 1.0, 0, 0),  # Beat 1 &
        (20, 1.5, 0, 0),  # Beat 2
        (22, 1.0, 0, 0),  # Beat 2 ah
        (24, 1.5, 12, 5), # Beat 3 (OCTAVE JUMP + slightly harder velocity)
        (28, 1.5, 12, 5), # Beat 4 (OCTAVE JUMP)
    ]

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
    
    # 16th note in PPQ (Pulses Per Quarter Note, usually 960 per quarter -> 240 per 16th)
    ppq_per_16th = 240 
    
    note_count = 0
    # Loop the 2-bar pattern across the requested number of bars
    for bar_pair in range(bars // 2):
        bar_offset_16ths = bar_pair * 32
        
        for start_16, dur_16, p_offset, v_offset in pattern_sequence:
            start_ppq = int((bar_offset_16ths + start_16) * ppq_per_16th)
            end_ppq = start_ppq + int(dur_16 * ppq_per_16th)
            
            # Reduce velocity to avoid harsh VST pick attack, as instructed in tutorial
            vel = max(1, min(127, velocity_base + v_offset))
            pitch = max(0, min(127, root_pitch + p_offset))
            
            # Insert note: take, selected, muted, startppq, endppq, chan, pitch, vel, custom
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Native FX Chain Placeholder ===
    # Using ReaSynth to synthesize a tight, plucky bass tone in lieu of external VSTs
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for bass
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.7)  # Vol
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.8)  # Square mix (for grit)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.2)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0)  # Attack (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4)  # Decay (tight)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.1)  # Sustain (low, matching palm mutes)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.1)  # Release (short)

    return f"Created '{track_name}' with {note_count} rhythm-locked bass notes over {bars} bars at {bpm} BPM (Velocity lowered to {velocity_base})."

