def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Verse",
    bpm: int = 124,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Verse Arrangement featuring 4-on-the-floor drums, 
    a root-note bassline, and sidechain routing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing generated arrangement.
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
    
    # Fallback to minor if an unsupported scale is provided
    if scale not in SCALES:
        scale = "minor"

    key_clean = key.capitalize() if len(key) == 1 else key[0].capitalize() + key[1:].lower()
    root_midi = 36 + NOTE_MAP.get(key_clean, 0) # Base C2

    # Progression logic
    if scale == "minor":
        prog_degrees = [0, 5, 2, 6] # i, VI, III, VII
    else:
        prog_degrees = [0, 4, 5, 3] # I, V, vi, IV

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    # === Step 2: Create Sidechain Trigger Track ===
    RPR.RPR_InsertTrackAtIndex(0, True)
    trig_track = RPR.RPR_GetTrack(0, 0)
    RPR.RPR_GetSetMediaTrackInfo_String(trig_track, "P_NAME", f"{track_name}_SC_Trigger", True)
    RPR.RPR_SetMediaTrackInfo_Value(trig_track, "B_MAINSEND", 0) # Disconnect from Master

    trig_item = RPR.RPR_AddMediaItemToTrack(trig_track)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_LENGTH", bar_len * bars)
    trig_take = RPR.RPR_AddTakeToMediaItem(trig_item)

    # Insert Trigger Notes
    for i in range(bars):
        for b in range(beats_per_bar):
            pos_time = (i * bar_len) + (b * beat_len)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trig_take, pos_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trig_take, pos_time + 0.1)
            RPR.RPR_MIDI_InsertNote(trig_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
            
    # Add synth to generate trigger pulse
    RPR.RPR_TrackFX_AddByName(trig_track, "ReaSynth", False, -1)

    # === Step 3: Create Verse Bass Track ===
    RPR.RPR_InsertTrackAtIndex(1, True)
    bass_track = RPR.RPR_GetTrack(0, 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_Bass", True)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "I_NCHAN", 4) # Enable 4 channels for sidechain

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", bar_len * bars)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Setup Bass Routing & FX
    send_idx = RPR.RPR_CreateTrackSend(trig_track, bass_track)
    RPR.RPR_SetTrackSendInfo_Value(trig_track, 0, send_idx, "I_DSTCHAN", 2) # Route to Channels 3/4
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    
    # Add Bass Synth
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_fx, 1, 1.0) # Set to Sawtooth wave

    # Insert Bassline Notes
    for i in range(bars):
        degree = prog_degrees[i % len(prog_degrees)]
        note = root_midi + SCALES[scale][degree]
        # Restrict to powerful bass octave (E1 to D#2)
        while note > 39: note -= 12
        while note < 28: note += 12
        
        start_time = i * bar_len
        end_time = start_time + bar_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time - 0.05) # slight gap
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)

    # === Step 4: Create Drums Track ===
    RPR.RPR_InsertTrackAtIndex(2, True)
    drum_track = RPR.RPR_GetTrack(0, 2)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", bar_len * bars)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    for i in range(bars):
        for b in range(beats_per_bar):
            pos_time = (i * bar_len) + (b * beat_len)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_time + 0.1)
            
            # Kick
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
            
            # Hat on off-beat
            hat_time = pos_time + (beat_len / 2.0)
            hat_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, hat_time)
            hat_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, hat_time + 0.1)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, hat_ppq, hat_end_ppq, 0, 42, max(1, velocity_base - 20), False)
            
            # Clap on 2 and 4
            if b % 2 == 1:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 39, velocity_base, False)

    RPR.RPR_MIDI_Sort(trig_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drum_take)
    
    return f"Created EDM Verse Setup with 3 tracks (Trigger, Bass, Drums) over {bars} bars at {bpm} BPM in {key} {scale}."
