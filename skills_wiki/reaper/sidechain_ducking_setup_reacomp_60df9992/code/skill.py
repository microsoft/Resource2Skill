def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain_Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete Sidechain Ducking setup in the current REAPER project.
    Generates a Pad track (Target) and a Kick track (Trigger), routes them 
    appropriately, and configures ReaComp for auxiliary sidechain ducking.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the target ducked track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import reaper_python as RPR

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
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    root = NOTE_MAP.get(key, 0) + 48 # Base C3
    intervals = SCALES.get(scale, SCALES["minor"])
    # Create a simple triad based on the root
    chord_notes = [root, root + intervals[2], root + intervals[4]]

    # === Step 2: Create Target Track (Pad) ===
    track_idx_tgt = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_tgt, True)
    tgt_track = RPR.RPR_GetTrack(0, track_idx_tgt)
    RPR.RPR_GetSetMediaTrackInfo_String(tgt_track, "P_NAME", track_name, True)
    
    # CRITICAL: Increase track channels to 4 so it can receive sidechain audio on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(tgt_track, "I_NCHAN", 4)

    # Add Pad MIDI Item (one long sustained chord)
    item_tgt = RPR.RPR_AddMediaItemToTrack(tgt_track)
    RPR.RPR_SetMediaItemInfo_Value(item_tgt, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_tgt, "D_LENGTH", item_length)
    take_tgt = RPR.RPR_AddTakeToMediaItem(item_tgt)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_tgt, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_tgt, item_length)
    
    for note in chord_notes:
        RPR.RPR_MIDI_InsertNote(take_tgt, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
    RPR.RPR_MIDI_Sort(take_tgt)

    # Add Pad Instrument (ReaSynth)
    fx_synth_tgt = RPR.RPR_TrackFX_AddByName(tgt_track, "ReaSynth", False, -1)
    # Make it pad-like (long release)
    RPR.RPR_TrackFX_SetParam(tgt_track, fx_synth_tgt, 2, 0.8) # Long Release

    # Add Sidechain Compressor (ReaComp)
    fx_comp = RPR.RPR_TrackFX_AddByName(tgt_track, "ReaComp", False, -1)
    
    # Dynamically find and set ReaComp Parameters
    num_params = RPR.RPR_TrackFX_GetNumParams(tgt_track, fx_comp)
    for i in range(num_params):
        name_res = RPR.RPR_TrackFX_GetParamName(tgt_track, fx_comp, i, "", 256)
        param_name = name_res[4].lower()
        if "detector" in param_name:
            # ReaComp Detector: 0=Main, 1=Aux L+R, 2=Aux L, 3=Aux R, 4=Output...
            # 1.0 / 6.0 approx 0.1667 (Index 1 out of 7 choices)
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 1.0/6.0)
        elif "thresh" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.3) # Lower threshold for heavy ducking
        elif "ratio" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.2) # High ratio
        elif "attack" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.0) # Fast attack
        elif "release" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.15) # Smooth release (~150ms) to avoid clicking

    # === Step 3: Create Trigger Track (Kick) ===
    track_idx_trig = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_trig, True)
    trig_track = RPR.RPR_GetTrack(0, track_idx_trig)
    RPR.RPR_GetSetMediaTrackInfo_String(trig_track, "P_NAME", "Trigger_Kick", True)

    # Add Kick MIDI Item (4-on-the-floor pattern)
    item_trig = RPR.RPR_AddMediaItemToTrack(trig_track)
    RPR.RPR_SetMediaItemInfo_Value(item_trig, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_trig, "D_LENGTH", item_length)
    take_trig = RPR.RPR_AddTakeToMediaItem(item_trig)
    
    kick_pitch = 36 # C2
    note_length_sec = 0.2 # Short percussive hits
    
    for b in range(bars * beats_per_bar):
        note_start_sec = b * (60.0 / bpm)
        note_end_sec = note_start_sec + note_length_sec
        n_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_trig, note_start_sec)
        n_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_trig, note_end_sec)
        RPR.RPR_MIDI_InsertNote(take_trig, False, False, n_start_ppq, n_end_ppq, 0, kick_pitch, 120, False)
    RPR.RPR_MIDI_Sort(take_trig)

    # Add Kick Instrument (ReaSynth)
    fx_synth_trig = RPR.RPR_TrackFX_AddByName(trig_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(trig_track, fx_synth_trig, 1, 0.0) # Instant attack
    RPR.RPR_TrackFX_SetParam(trig_track, fx_synth_trig, 2, 0.05) # Super fast release for staccato kick

    # === Step 4: Setup Sidechain Routing (Send Trigger 1/2 -> Target 3/4) ===
    # 0 in CreateTrackSend indicates a standard track-to-track send
    send_idx = RPR.RPR_CreateTrackSend(trig_track, tgt_track)
    # I_SRCCHAN: 0 = Channels 1/2
    RPR.RPR_SetTrackSendInfo_Value(trig_track, 0, send_idx, "I_SRCCHAN", 0)
    # I_DSTCHAN: 2 = Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(trig_track, 0, send_idx, "I_DSTCHAN", 2)

    return f"Created sidechain setup: '{track_name}' (Pad) ducking to 'Trigger_Kick' over {bars} bars at {bpm} BPM in {key} {scale}."
