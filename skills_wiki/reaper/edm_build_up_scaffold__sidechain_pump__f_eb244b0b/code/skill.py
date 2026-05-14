def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Intro Pad",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Build-Up Scaffold with Sidechain Pumping and Filter Sweep.
    """
    import reaper_python as RPR

    # === Music Theory & Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }
    
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Create a 7th chord (Root, 3rd, 5th, 7th) anchored at C3 (MIDI 48)
    chord_pitches = [
        48 + root_val + intervals[0],
        48 + root_val + intervals[2],
        48 + root_val + intervals[4],
        48 + root_val + intervals[6 % len(intervals)] + (12 if 6 >= len(intervals) else 0)
    ]

    # === Timing Calculations ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beat_sec = 60.0 / bpm
    total_beats = bars * 4
    
    # THE PRE-DROP GAP: We leave the final beat completely empty
    active_beats = total_beats - 1
    item_length_sec = active_beats * beat_sec

    # === Track 1: Ghost Kick (Sidechain Trigger) ===
    idx_kick = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_kick, True)
    track_kick = RPR.RPR_GetTrack(0, idx_kick)
    RPR.RPR_GetSetMediaTrackInfo_String(track_kick, "P_NAME", "Ghost Kick (SC Trigger)", True)
    
    # Disable master send (it should only trigger the compressor, not be heard)
    RPR.RPR_SetMediaTrackInfo_Value(track_kick, "B_MAINSEND", 0.0)

    item_kick = RPR.RPR_AddMediaItemToTrack(track_kick)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_LENGTH", item_length_sec)
    take_kick = RPR.RPR_AddTakeToMediaItem(item_kick)
    
    # Insert 4-on-the-floor ghost kicks
    for i in range(active_beats):
        start_time = i * beat_sec
        end_time = start_time + (beat_sec * 0.5)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_kick, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_kick, end_time)
        RPR.RPR_MIDI_InsertNote(take_kick, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
    RPR.RPR_MIDI_Sort(take_kick)

    # === Track 2: Intro Pad (The Target) ===
    idx_pad = idx_kick + 1
    RPR.RPR_InsertTrackAtIndex(idx_pad, True)
    track_pad = RPR.RPR_GetTrack(0, idx_pad)
    RPR.RPR_GetSetMediaTrackInfo_String(track_pad, "P_NAME", track_name, True)
    
    # Set to 4 channels to receive sidechain on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(track_pad, "I_NCHAN", 4.0)

    # Route Ghost Kick (1/2) -> Intro Pad (3/4)
    send_idx = RPR.RPR_CreateTrackSend(track_kick, track_pad)
    RPR.RPR_SetTrackSendInfo_Value(track_kick, 0, send_idx, "I_DSTCHAN", 2.0) # 2 = channels 3/4

    item_pad = RPR.RPR_AddMediaItemToTrack(track_pad)
    RPR.RPR_SetMediaItemInfo_Value(item_pad, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_pad, "D_LENGTH", item_length_sec)
    take_pad = RPR.RPR_AddTakeToMediaItem(item_pad)

    # Insert sustained chord
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_pad, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_pad, item_length_sec)
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take_pad, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 10, False)
    RPR.RPR_MIDI_Sort(take_pad)

    # === Sound Design & FX Chain ===
    # 1. Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track_pad, "ReaSynth", False, -1)
    
    # 2. Sidechain Compressor (ReaComp)
    comp_idx = RPR.RPR_TrackFX_AddByName(track_pad, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track_pad, comp_idx, 0, 0.1)  # Threshold (pull down to catch signal)
    RPR.RPR_TrackFX_SetParam(track_pad, comp_idx, 1, 0.5)  # Ratio (high for distinct pump)
    RPR.RPR_TrackFX_SetParam(track_pad, comp_idx, 2, 0.0)  # Attack (fast)
    RPR.RPR_TrackFX_SetParam(track_pad, comp_idx, 3, 0.15) # Release (timed to groove)
    RPR.RPR_TrackFX_SetParam(track_pad, comp_idx, 8, 1.0)  # Detector input -> Aux L+R (channels 3/4)

    # 3. Filter Sweep (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track_pad, "ReaEQ", False, -1)
    # Param 9 is Band 4 Frequency in ReaEQ
    env = RPR.RPR_GetFXEnvelope(track_pad, eq_idx, 9, True)
    
    # Insert envelope points to sweep filter from muffled (low) to open (high)
    # Normalized parameters: 0.1 = ~100Hz, 0.9 = ~15000Hz
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length_sec, 0.9, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created EDM Build-up: Ghost kick triggering sidechain on '{track_name}' (Chord: {key} {scale}), with automated filter sweep and a 1-beat drop gap."
