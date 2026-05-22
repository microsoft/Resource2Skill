def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Sidechain Pumping Pad and Kick Trigger in the current REAPER project.
    This replicates the drag-and-drop sidechain routing technique.

    Args:
        project_name: Project identifier.
        track_name: Name for the target (pad) track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Pad voicing: Root, 3rd, 5th, 7th (Octave 4)
    chord_pitches = [
        48 + root_val + scale_intervals[0], 
        48 + root_val + scale_intervals[2], 
        48 + root_val + scale_intervals[4], 
        48 + root_val + scale_intervals[min(6, len(scale_intervals)-1)]
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    # === Step 1: Create the Target Pad Track ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    pad_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", track_name, True)
    
    # CRITICAL: Set Pad track to 4 channels to receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(pad_track, "I_NCHAN", 4)

    # Pad Generator: Add ReaSynth and ReaComp
    pad_synth = RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    pad_comp = RPR.RPR_TrackFX_AddByName(pad_track, "ReaComp", False, -1)
    
    # Configure ReaComp for sidechain ducking
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 0, -25.0)  # Threshold (dB)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 1, 4.0)    # Ratio
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 2, 3.0)    # Attack (ms)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 3, 150.0)  # Release (ms)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 14, 1.0)   # Detector: Auxiliary Inputs

    # Pad MIDI: Sustained chords
    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", bar_len * bars)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)

    for b in range(bars):
        start_time = b * bar_len
        end_time = start_time + bar_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, end_time)
        
        for pitch in chord_pitches:
            RPR.RPR_MIDI_InsertNote(pad_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

    # === Step 2: Create the Trigger Kick Track ===
    kick_idx = track_count + 1
    RPR.RPR_InsertTrackAtIndex(kick_idx, True)
    kick_track = RPR.RPR_GetTrack(0, kick_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "SC Trigger Kick", True)

    # Kick Generator: Add ReaSynth and pitch it down to simulate a kick pulse
    kick_synth = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 0, 0.0)    # Sine wave
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 3, -12.0)  # Tuning down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 4, 100.0)  # Short decay

    # Kick MIDI: 4-on-the-floor trigger
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", bar_len * bars)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    for b in range(bars):
        for beat in range(beats_per_bar):
            start_time = b * bar_len + (beat * beat_len)
            end_time = start_time + (beat_len * 0.25) # Short pulse
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_time)
            
            # Kick pitch (C1 = 36)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base + 20, False)

    RPR.RPR_MIDI_Sort(pad_take)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 3: Audio Routing (The "Drag and Drop" Emulator) ===
    # Send from Kick Track to Pad Track
    send_idx = RPR.RPR_CreateTrackSend(kick_track, pad_track)
    
    # Configure Send Source: Audio Channels 1/2 (Index 0)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_SRCCHAN", 0)
    
    # Configure Send Destination: Audio Channels 3/4 (Index 2)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2)
    
    # Set Send Volume to unity (0 dB = 1.0)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "D_VOL", 1.0)

    # Force update UI
    RPR.RPR_UpdateArrange()
    
    return f"Created Sidechain configuration: 'SC Trigger Kick' ducking '{track_name}' via Channels 3/4 over {bars} bars at {bpm} BPM."
