def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 127,
    **kwargs,
) -> str:
    """
    Create a Kick-Synced Metal Pedal Bass line in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for accents (0-127). Unaccented notes will be scaled down.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated bass line.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_beats = bars * beats_per_bar
    item_length_sec = (item_length_beats / bpm) * 60.0

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine Root Pitch (Low Octave for Metal Bass, C1 = 24)
    root_pitch = NOTE_MAP.get(key, 0) + 24 
    
    # Calculate reduced velocity for "chugs" to reduce harsh attack (approx 86% of max)
    chug_vel = int(velocity_base * 0.86) 

    # Define a syncopated metal rhythm (beat_position, duration_beats, velocity, octave_offset)
    base_pattern = [
        (0.0,  0.15, velocity_base, 0), # Downbeat accent
        (0.5,  0.15, chug_vel,      0), # 8th upbeat
        (0.75, 0.15, chug_vel,      0), # 16th syncopation
        (1.25, 0.15, chug_vel,      0), # 16th syncopation
        (1.5,  0.15, chug_vel,      0), # 8th upbeat
        (2.0,  0.25, velocity_base, 0), # Beat 3 accent (slightly longer)
        (3.0,  0.15, velocity_base, 0), # Beat 4 accent
        (3.5,  0.15, chug_vel,      0)  # 8th upbeat
    ]

    # Variation pattern with octave jumps at the end of the phrase
    fill_pattern = [
        (0.0,  0.15, velocity_base, 0),
        (0.5,  0.15, chug_vel,      0), 
        (0.75, 0.15, chug_vel,      0),
        (1.25, 0.15, chug_vel,      0),
        (1.5,  0.15, chug_vel,      0),
        (2.0,  0.25, velocity_base, 0),
        (3.0,  0.15, velocity_base, 12), # Octave Jump!
        (3.5,  0.15, chug_vel,      12)  # Octave Jump!
    ]

    total_notes = 0

    for b in range(bars):
        bar_start_beat = b * beats_per_bar
        
        # Use the fill pattern with octave jumps on every 2nd bar (e.g., bars 1, 3, 5...)
        current_pattern = fill_pattern if (b % 2 == 1) else base_pattern
        
        for pos, dur, vel, oct_off in current_pattern:
            start_pos_beats = bar_start_beat + pos
            end_pos_beats = start_pos_beats + dur
            
            start_time = (start_pos_beats / bpm) * 60.0
            end_time = (end_pos_beats / bpm) * 60.0
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = root_pitch + oct_off
            
            # Insert Note (noSort=True for performance in loops)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes += 1

    # Sort MIDI events after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Aggressive Tone Placeholder) ===
    # 1. Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, -6.0)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.6)   # Saw mix (bite)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4)   # Square mix (low end weight)
    
    # 2. Distortion
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 12.0)   # Gain/Drive
    
    # 3. Compression (Tighten dynamics)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -18.0)  # Threshold
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)    # Ratio
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 5.0)    # Attack (ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 50.0)   # Release (ms)

    return f"Created '{track_name}' with {total_notes} synced metal bass notes over {bars} bars at {bpm} BPM."
