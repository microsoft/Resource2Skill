def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Ghost Kick Sidechain Pumping pattern with a pre-drop gap in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the destination chord track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    def get_diatonic_chord(degree_0_idx, base_octave, root_pitch, scale_intervals):
        notes = []
        # Build 1-3-5 triad
        for i in [0, 2, 4]:
            idx = degree_0_idx + i
            octave_shift = idx // len(scale_intervals)
            scale_idx = idx % len(scale_intervals)
            note_pitch = root_pitch + (base_octave + octave_shift) * 12 + scale_intervals[scale_idx]
            notes.append(note_pitch)
        return notes

    # Protect boundaries
    bars = max(1, int(bars))
    root_val = NOTE_MAP.get(str(key).upper(), 0)
    scale_type = str(scale).lower()
    if scale_type not in SCALES:
        scale_type = "minor"
    
    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # 2. Track Setup
    track_cnt = RPR.RPR_CountTracks(0)
    
    # --- Create Pumping Chords Track ---
    RPR.RPR_InsertTrackAtIndex(track_cnt, True)
    pump_tr = RPR.RPR_GetTrack(0, track_cnt)
    RPR.RPR_GetSetMediaTrackInfo_String(pump_tr, "P_NAME", track_name, True)
    # Set to 4 channels to receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(pump_tr, "I_NCHAN", 4)

    # --- Create Ghost Kick Trigger Track ---
    RPR.RPR_InsertTrackAtIndex(track_cnt + 1, True)
    trig_tr = RPR.RPR_GetTrack(0, track_cnt + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(trig_tr, "P_NAME", "Ghost Kick Trigger", True)
    # Disable master send (inaudible)
    RPR.RPR_SetMediaTrackInfo_Value(trig_tr, "B_MAINSEND", 0)

    # 3. Routing (Send Trigger -> Pumping Chords on channels 3/4)
    send_idx = RPR.RPR_CreateTrackSend(trig_tr, pump_tr)
    # I_DSTCHAN: 2 maps to destination channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(trig_tr, 0, send_idx, "I_DSTCHAN", 2)
    RPR.RPR_SetTrackSendInfo_Value(trig_tr, 0, send_idx, "D_VOL", 1.0)

    # 4. MIDI Generation
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar
    item_length = bar_length * bars

    # --- Trigger MIDI ---
    trig_item = RPR.RPR_AddMediaItemToTrack(trig_tr)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_LENGTH", item_length)
    trig_take = RPR.RPR_AddTakeToMediaItem(trig_item)

    kick_pitch = 36 # C2
    for b in range(bars * 4): # 4-on-the-floor
        pos = b * beat_length
        end_pos = pos + 0.1 # short 100ms trigger
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trig_take, pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trig_take, end_pos)
        RPR.RPR_MIDI_InsertNote(trig_take, False, False, start_ppq, end_ppq, 0, kick_pitch, 127, False)
    RPR.RPR_MIDI_Sort(trig_take)

    # --- Chords MIDI ---
    pump_item = RPR.RPR_AddMediaItemToTrack(pump_tr)
    RPR.RPR_SetMediaItemInfo_Value(pump_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pump_item, "D_LENGTH", item_length)
    pump_take = RPR.RPR_AddTakeToMediaItem(pump_item)

    # Classic progression selection
    progression = [0, 5, 2, 4] if scale_type == "minor" else [0, 4, 5, 3]

    for b in range(bars):
        deg = progression[b % len(progression)]
        chord_notes = get_diatonic_chord(deg, 4, root_val, SCALES[scale_type])

        start_time = b * bar_length
        end_time = start_time + bar_length
        
        # Arrangement Cut: Leave a 1-beat gap at the very end of the total sequence
        if b == bars - 1:
            end_time -= beat_length
        else:
            end_time -= 0.05 # standard slight legato separation

        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pump_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pump_take, end_time)

        for pitch in chord_notes:
            RPR.RPR_MIDI_InsertNote(pump_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(pump_take)

    # 5. FX Setup
    # --- Trigger Sound Design ---
    trig_synth_idx = RPR.RPR_TrackFX_AddByName(trig_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(trig_tr, trig_synth_idx, 5, 0.05) # Very short release

    # --- Pumping Chords Sound Design ---
    pump_synth_idx = RPR.RPR_TrackFX_AddByName(pump_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_synth_idx, 0, 0.3)  # Vol down
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_synth_idx, 1, 0.5)  # Add Saw wave
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_synth_idx, 5, 0.5)  # Longer release

    pump_comp_idx = RPR.RPR_TrackFX_AddByName(pump_tr, "ReaComp", False, -1)
    # Configure Sidechain
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_comp_idx, 0, -25.0) # Thresh (-25 dB)
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_comp_idx, 1, 8.0)   # Ratio (8:1)
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_comp_idx, 2, 2.0)   # Attack (2 ms)
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_comp_idx, 3, 100.0) # Release (100 ms)
    RPR.RPR_TrackFX_SetParam(pump_tr, pump_comp_idx, 8, 1.0)   # Detector Input: Aux L+R (1.0)

    return f"Created Ghost Sidechain routing over {bars} bars: Inaudible trigger ducking '{track_name}' at {bpm} BPM in {key} {scale_type}."
