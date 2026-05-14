def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Chords",
    bpm: int = 125,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM arrangement build with a Ghost Kick Sidechain Pump and Filter Sweep.
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

    # Retrieve root note and scale intervals
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # Basic root triad formula (1st, 3rd, 5th, plus octave)
    chord_degrees = [0, 2, 4] 
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    num_tracks = RPR.RPR_CountTracks(0)

    # === Step 2: Create Ghost Kick Track ===
    kick_track_idx = num_tracks
    RPR.RPR_InsertTrackAtIndex(kick_track_idx, True)
    kick_track = RPR.RPR_GetTrack(0, kick_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Kick (Trigger)", True)
    
    # Disable Master Send (Makes it a "Ghost" kick)
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0)

    # === Step 3: Create Chords Track ===
    chords_track_idx = num_tracks + 1
    RPR.RPR_InsertTrackAtIndex(chords_track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, chords_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    
    # Set Chords track to 4 Channels for Sidechain receiving
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)

    # === Step 4: Setup Sidechain Routing ===
    # Create send from Ghost Kick to Chords Track
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chords_track)
    # Audio Source: Channel 1/2 (Index 0)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_SRCCHAN", 0)
    # Audio Destination: Channel 3/4 (Index 2)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Step 5: Add MIDI & FX to Ghost Kick ===
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # 4-on-the-floor kick MIDI
    kick_pitch = 36 # C2
    for bar in range(bars):
        for beat in range(beats_per_bar):
            start_sec = bar * bar_length_sec + beat * (60.0 / bpm)
            end_sec = start_sec + (60.0 / bpm) * 0.25 # Short trigger
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_sec)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, kick_pitch, 127, True)
    RPR.RPR_MIDI_Sort(kick_take)

    # Add quick, plucky synth for trigger sound
    kick_fx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, kick_fx, 1, 0.0) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, kick_fx, 2, 0.1) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, kick_fx, 3, 0.0) # Sustain

    # === Step 6: Add MIDI & FX to Chords ===
    chord_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_length_sec)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    # Build a sustained root chord
    base_octave = 48 # C3
    for degree in chord_degrees:
        pitch = base_octave + root_val + intervals[degree]
        # Held for the entire duration (all bars)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, 0.0)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, total_length_sec)
        RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        
        # Add an octave up for brightness
        RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, pitch + 12, velocity_base - 10, True)
    RPR.RPR_MIDI_Sort(chord_take)

    # 6a. Chords Synth
    chord_synth = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, chord_synth, 0, 0.7) # Sawtooth

    # 6b. Filter Sweep (ReaEQ)
    eq_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    # Band 4 (High Shelf -> acts as Low Pass if gain is reduced)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, eq_fx, 10, 0.0) # Gain to -inf
    
    # Automate Band 4 Frequency (Param 9)
    env = RPR.RPR_GetFXEnvelope(chords_track, eq_fx, 9, True)
    # Start dark/muffled (Normalized freq ~0.3)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.3, 0, 0, False, True)
    # Sweep up to bright/open over the course of the bars (Normalized freq ~0.9)
    RPR.RPR_InsertEnvelopePoint(env, total_length_sec, 0.9, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    # 6c. Sidechain Pump (ReaComp)
    comp_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 0, 0.3)  # Threshold
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 1, 0.5)  # Ratio (high)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 2, 0.0)  # Attack (fast)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 3, 0.15) # Release (pumping)
    # Note: Detector Input (param 10). Because float mapping can vary, 
    # routing Ch 1/2 to Ch 3/4 + standard ReaComp usually defaults cleanly 
    # but we force parameter 10 to point to Auxiliary Input (~0.25 on normalized scale)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_fx, 10, 0.25) 

    return f"Created Sidechain & Sweep arrangement: 4-channel routing from 'Ghost Kick' to '{track_name}' over {bars} bars at {bpm} BPM in {key} {scale}."
