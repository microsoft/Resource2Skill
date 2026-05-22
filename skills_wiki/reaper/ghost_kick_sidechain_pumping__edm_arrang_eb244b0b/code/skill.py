def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "PumpingChords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Ghost Kick Sidechain Pumping in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created target track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
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

    # === Step 2: Create Tracks ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # 2a. Create Ghost Kick Track
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    ghost_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_track, "P_NAME", f"{track_name} Ghost Trigger", True)
    
    # Disable Master/Parent send so the kick is purely a control signal
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0)
    
    # 2b. Create Target Track
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    target_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(target_track, "P_NAME", f"{track_name} Pad", True)
    
    # Set target track to 4 channels to accept sidechain input on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(target_track, "I_NCHAN", 4)

    # === Step 3: Setup Routing ===
    # Send from Ghost Kick (ch 1/2) to Target (ch 3/4)
    send_idx = RPR.RPR_CreateTrackSend(ghost_track, target_track)
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_DSTCHAN", 2) # 2 corresponds to channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "D_VOL", 1.0)   # Unity gain

    # === Step 4: Add FX Chains ===
    # Add a simple synth to act as the ghost click
    RPR.RPR_TrackFX_AddByName(ghost_track, "ReaSynth", False, -1)
    
    # Add target synth and compressor
    synth_idx = RPR.RPR_TrackFX_AddByName(target_track, "ReaSynth", False, -1)
    
    comp_idx = RPR.RPR_TrackFX_AddByName(target_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 0, -30.0) # Threshold (deep cut)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 1, 10.0)  # Ratio (hard compression)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 2, 5.0)   # Attack (catch transient fast)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 3, 150.0) # Release (rhythmic swell)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 8, 1.0)   # Detector Input: 1.0 maps to Aux L/R (Sidechain)

    # === Step 5: Add MIDI Items ===
    cursor_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars

    # --- 5a. Ghost Kick MIDI ---
    ghost_item = RPR.RPR_AddMediaItemToTrack(ghost_track)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_LENGTH", item_length)
    ghost_take = RPR.RPR_AddTakeToMediaItem(ghost_item)
    
    # Insert 4-on-the-floor trigger notes
    for i in range(bars * beats_per_bar):
        start_t = cursor_pos + i * beat_len_sec
        end_t = start_t + (beat_len_sec * 0.1) # extremely short trigger
        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, start_t)
        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, end_t)
        RPR.RPR_MIDI_InsertNote(ghost_take, False, False, s_ppq, e_ppq, 0, 36, 127, False)
    
    RPR.RPR_MIDI_Sort(ghost_take)

    # --- 5b. Target Track MIDI (Chords) ---
    target_item = RPR.RPR_AddMediaItemToTrack(target_track)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_LENGTH", item_length)
    target_take = RPR.RPR_AddTakeToMediaItem(target_item)

    # Determine robust root MIDI note
    root_midi = 60
    for k, v in NOTE_MAP.items():
        if k.lower() == key.lower():
            root_midi = v + 48 # Start around C3
            break

    # Generate scale degrees across 3 octaves
    scale_steps = SCALES.get(scale.lower(), SCALES["minor"])
    full_scale = []
    for oct in range(3):
        for step in scale_steps:
            full_scale.append(root_midi + step + (12 * oct))

    # Simple chord progression based on scale degrees (e.g., i - iv - v - i)
    prog = [0, 3, 4, 0]

    # Insert sustained chords
    for bar in range(bars):
        deg = prog[bar % len(prog)]
        # Build diatonic triad (root, 3rd, 5th)
        chord_pitches = [full_scale[deg], full_scale[deg+2], full_scale[deg+4]]
        
        start_t = cursor_pos + bar * bar_length_sec
        end_t = start_t + bar_length_sec
        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, start_t)
        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, end_t)
        
        for pitch in chord_pitches:
            RPR.RPR_MIDI_InsertNote(target_take, False, False, s_ppq, e_ppq, 0, pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(target_take)
    RPR.RPR_UpdateArrange()

    return f"Created Sidechain Pumping configuration on '{track_name}' over {bars} bars at {bpm} BPM."
