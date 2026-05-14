def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "BuildUp",
    bpm: int = 128,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Build-Up with a Filter Sweep and Ghost Sidechain pump.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars for the build-up.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
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
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    track_count = RPR.RPR_CountTracks(0)

    # === Step 2: Create Chords Track ===
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    chords_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chords", True)
    # Set track channels to 4 to allow for sidechain input on ch 3/4
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)

    # === Step 3: Create Ghost Kick Track ===
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", f"{track_name}_GhostKick", True)
    # Disable master/parent send so the kick is silent in the mix
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0)

    # === Step 4: Populate Ghost Kick MIDI & Synth ===
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # Insert 1/4 note kicks (4-on-the-floor)
    for i in range(bars * beats_per_bar):
        start_time = i * (bar_length_sec / beats_per_bar)
        end_time = start_time + 0.1 # Short percussive trigger
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_time)
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)

    kick_synth = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, kick_synth, 1, 0.0) # Very short release

    # === Step 5: Populate Chords MIDI ===
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    root_note = NOTE_MAP.get(key, 0) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    degrees = [0, 5, 3, 4] # Classic i - VI - iv - v progression
    
    for i in range(bars):
        degree = degrees[i % len(degrees)]
        start_time = i * bar_length_sec
        end_time = start_time + bar_length_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        # Build 3-note triad
        for j in [0, 2, 4]:
            idx = degree + j
            octave = idx // len(scale_intervals)
            note_in_scale = scale_intervals[idx % len(scale_intervals)]
            pitch = root_note + note_in_scale + (octave * 12)
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base * 0.8), False)

    # === Step 6: Chords Sound Design & Sidechain FX ===
    chords_synth = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, chords_synth, 0, 0.0) # Sawtooth wave for rich harmonics
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, chords_synth, 2, 0.8) # Long release
    
    # ReaEQ: Set up a Low-Pass filter using Band 4 (High Shelf)
    eq_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, eq_fx, 10, 0.0) # Band 4 Gain down to minimum (-inf)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, eq_fx, 9, 0.1)  # Band 4 Freq starts low (muffled)
    
    # ReaComp: Set up Sidechain Pump
    comp_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 0, 0.15) # Threshold low
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 1, 0.8)  # Ratio high (10:1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 2, 0.0)  # Attack 0ms
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 3, 0.15) # Release ~100ms
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 12, 0.1667) # Detector input to Aux L+R (1/6th of param range)

    # === Step 7: Signal Routing ===
    # Send Ghost Kick to Chords (Channels 3/4)
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chords_track)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2) # 2 = Dest Chan 3/4

    # === Step 8: Automation (Filter Sweep) ===
    # Automate the ReaEQ Band 4 Frequency (param index 9)
    env = RPR.RPR_GetFXEnvelope(chords_track, eq_fx, 9, True)
    if env:
        # Start muffled (low frequency)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 0, 0, False, True)
        # End completely open (high frequency) right before the drop
        RPR.RPR_InsertEnvelopePoint(env, total_length, 0.9, 0, 0, False, True)
        RPR.RPR_Envelope_SortR(env)

    return f"Created EDM Build-Up: {bars} bars of Chords with an automated filter sweep and ghost sidechain pump at {bpm} BPM."
