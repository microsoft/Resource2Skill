def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "Build Chords",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM arrangement scaffold with an automated filter sweep and a ghost sidechain pump.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # 4-bar progression: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6] 

    # === Step 1: Initialize Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    num_tracks = RPR.RPR_CountTracks(0)

    # === Step 2: Create Ghost Kick Track (The Sidechain Trigger) ===
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    ghost_trk = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_trk, "P_NAME", "Ghost Kick (Sidechain)", True)
    
    # Disable Master/Parent send so the kick is purely a control signal
    RPR.RPR_SetMediaTrackInfo_Value(ghost_trk, "B_MAINSEND", 0.0)

    # Create MIDI Item for Ghost Kick
    ghost_item = RPR.RPR_AddMediaItemToTrack(ghost_trk)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_LENGTH", total_length_sec)
    ghost_take = RPR.RPR_AddTakeToMediaItem(ghost_item)
    
    # Add ReaSynth for a basic percussive thump
    RPR.RPR_TrackFX_AddByName(ghost_trk, "ReaSynth", False, -1)

    # Populate 4/4 Kick Pattern
    for b in range(bars * beats_per_bar):
        start_time = b * (60.0 / bpm)
        end_time = start_time + 0.1 # short percussive hit
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, end_time)
        # Note 36 is C2 (standard kick range)
        RPR.RPR_MIDI_InsertNote(ghost_take, False, False, start_ppq, end_ppq, 1, 36, 127, False)

    RPR.RPR_MIDI_Sort(ghost_take)

    # === Step 3: Create Chords Track ===
    chords_trk_idx = num_tracks + 1
    RPR.RPR_InsertTrackAtIndex(chords_trk_idx, True)
    chords_trk = RPR.RPR_GetTrack(0, chords_trk_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_trk, "P_NAME", track_name, True)
    
    # Set to 4 channels to receive the sidechain signal
    RPR.RPR_SetMediaTrackInfo_Value(chords_trk, "I_NCHAN", 4)

    # Create MIDI Item for Chords
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_trk)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # Populate Sustained Chords
    octave_base = 48 # C3
    for bar in range(bars):
        degree = progression_degrees[bar % len(progression_degrees)]
        
        # Build triad (root, 3rd, 5th)
        chord_notes = [
            scale_intervals[degree % len(scale_intervals)] + (12 * (degree // len(scale_intervals))),
            scale_intervals[(degree + 2) % len(scale_intervals)] + (12 * ((degree + 2) // len(scale_intervals))),
            scale_intervals[(degree + 4) % len(scale_intervals)] + (12 * ((degree + 4) // len(scale_intervals)))
        ]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        for note_offset in chord_notes:
            pitch = octave_base + root_val + note_offset
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 1, int(pitch), velocity_base, False)

    RPR.RPR_MIDI_Sort(chords_take)

    # === Step 4: Routing & Effects ===
    
    # Add basic synth
    RPR.RPR_TrackFX_AddByName(chords_trk, "ReaSynth", False, -1)
    
    # Add JS Lowpass Filter for the sweep
    filter_fx_idx = RPR.RPR_TrackFX_AddByName(chords_trk, "JS: Filters/resonantlowpass", False, -1)
    
    # Automate the Filter Cutoff (Parameter 0 in this JS plugin)
    filter_env = RPR.RPR_GetFXEnvelope(chords_trk, filter_fx_idx, 0, True)
    if filter_env:
        # Start at 300Hz, Sweep to 20000Hz
        RPR.RPR_InsertEnvelopePoint(filter_env, 0.0, 300.0, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(filter_env, total_length_sec, 20000.0, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(filter_env)

    # Add ReaComp for Sidechain Pumping
    comp_fx_idx = RPR.RPR_TrackFX_AddByName(chords_trk, "ReaComp", False, -1)
    # Set ReaComp to Auxiliary L+R Detector (Parameter 10 -> value around 1.0)
    RPR.RPR_TrackFX_SetParam(chords_trk, comp_fx_idx, 10, 1.0)
    # Set low threshold to guarantee obvious ducking
    RPR.RPR_TrackFX_SetParam(chords_trk, comp_fx_idx, 0, 0.1) # Threshold
    RPR.RPR_TrackFX_SetParam(chords_trk, comp_fx_idx, 1, 0.5) # Ratio

    # Route Ghost Kick Audio (Channels 1/2) to Chords Audio (Channels 3/4)
    send_id = RPR.RPR_CreateTrackSend(ghost_trk, chords_trk)
    # "I_DSTCHAN" = 2 means Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(ghost_trk, 0, send_id, "I_DSTCHAN", 2)
    # Ensure source is 1/2
    RPR.RPR_SetTrackSendInfo_Value(ghost_trk, 0, send_id, "I_SRCCHAN", 0)

    return f"Created EDM Build-Up: '{track_name}' and 'Ghost Kick' over {bars} bars at {bpm} BPM with Sidechain Routing and automated Filter Sweep."
