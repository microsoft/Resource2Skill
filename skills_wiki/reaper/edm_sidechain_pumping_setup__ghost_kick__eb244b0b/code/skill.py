def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Pumping_Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Sidechain Pumping Setup in the current REAPER project.
    Generates a muted ghost kick track that triggers ReaComp on a synthesized chord pad.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chords track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_pitches = [root_val + interval for interval in scale_intervals]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    track_count = RPR.RPR_CountTracks(0)
    
    # Track 1: Pumping Chords
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    chords_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4) # Enable 4 channels for sidechain

    # Track 2: Ghost Kick (Sidechain Trigger)
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Kick (Sidechain Trigger)", True)
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0) # Mute from master output

    # === Step 3: Create MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    # Chord generator with tight voice-leading (clamps notes between G3 and G4)
    def get_chord(degree, root_octave):
        deg_idx = (degree - 1) % 7
        oct_shift = (degree - 1) // 7
        
        n1 = root_octave * 12 + scale_pitches[deg_idx] + oct_shift * 12
        n3 = root_octave * 12 + scale_pitches[(deg_idx + 2) % 7] + ((deg_idx + 2) // 7) * 12 + oct_shift * 12
        n5 = root_octave * 12 + scale_pitches[(deg_idx + 4) % 7] + ((deg_idx + 4) // 7) * 12 + oct_shift * 12
        
        chord = []
        for n in [n1, n3, n5]:
            while n > 67: # Max height G4
                n -= 12
            while n < 55: # Min height G3
                n += 12
            chord.append(n)
        return sorted(chord)

    # Insert Chords (Progression: i - VI - III - VII)
    for bar in range(bars):
        degree = [1, 6, 3, 7][bar % 4]
        chord_notes = get_chord(degree, 4)
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(chords_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(chords_take, end_qn)
        
        for pitch in chord_notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)

    # Insert Ghost Kick (Quarter notes)
    for i in range(bars * 4):
        start_time = i * (60.0 / bpm)
        end_time = start_time + 0.1 # Short blip
        
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(kick_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(kick_take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 1, 36, 127, False)

    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 4: Sound Design & Sidechain Routing ===
    
    # 4a. Add Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 6, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 7, 1.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 8, 0.0)   # Triangle mix
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 5, 200.0) # Release tail

    # 4b. Add Compressor
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 0, -25.0) # Threshold
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 1, 4.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 2, 5.0)   # Attack ms
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 3, 100.0) # Release ms
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 8, 1.0)   # Detector Input: Aux L+R

    # 4c. Route Trigger to Chords (Channels 3/4)
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chords_track)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2) # 2 = Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "D_VOL", 1.0)   # Unity Gain

    return f"Created pumping synth pad and sidechain trigger over {bars} bars at {bpm} BPM in {key} {scale}."
