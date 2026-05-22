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
    Create an EDM Sidechain Pumping Chord progression using a Ghost Kick trigger.

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
        Status string.
    """
    import reaper_python as RPR

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

    # === Step 2: Create Tracks ===
    base_track_idx = RPR.RPR_CountTracks(0)
    
    # Track A: Chords (Target)
    RPR.RPR_InsertTrackAtIndex(base_track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, base_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    # Set to 4 channels to receive sidechain on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)
    
    # Track B: Ghost Kick (Trigger)
    RPR.RPR_InsertTrackAtIndex(base_track_idx + 1, True)
    kick_track = RPR.RPR_GetTrack(0, base_track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Kick Trigger", True)
    # Disable master send so it operates silently
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0)

    # === Step 3: Routing (Ghost Kick -> Chords 3/4) ===
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chords_track)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_SRCCHAN", 0) # Source audio from 1/2
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2) # Dest audio to 3/4
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "D_VOL", 1.0)

    # === Step 4: Add FX Chains ===
    # Add Synth and Compressor to Chords
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    
    # Configure ReaComp for intense pumping
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 0, 0.4)  # Threshold (-24dB approx)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 1, 0.3)  # Ratio (high)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 2, 0.0)  # Attack (0ms for instant ducking)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 3, 0.06) # Release (~300ms for rhythm swell)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 8, 0.25) # Detector Input: Aux L+R

    # Add Synth to Kick Trigger
    RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)

    # === Step 5: Generate MIDI for Chords ===
    root_val = NOTE_MAP.get(key.upper(), 0) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    prog = [0, 5, 2, 6] if scale.lower() == "minor" else [0, 4, 5, 3] # i-VI-III-VII or I-V-vi-IV
    
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", bar_length_sec * bars)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    for b in range(bars):
        chord_deg = prog[b % len(prog)]
        
        # Calculate triad notes
        notes = []
        for offset in [0, 2, 4]:
            deg = chord_deg + offset
            octave = deg // len(scale_intervals)
            note = root_val + scale_intervals[deg % len(scale_intervals)] + (octave * 12)
            notes.append(note)

        start_pos = b * bar_length_sec
        end_pos = start_pos + bar_length_sec
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_pos)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_pos)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(chords_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(chords_take, end_qn)

        for note in notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(chords_take)

    # === Step 6: Generate MIDI for Ghost Kick ===
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", bar_length_sec * bars)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    # 4/4 Four-on-the-floor trigger
    for b in range(bars):
        for beat in range(4):
            start_pos = b * bar_length_sec + beat * (bar_length_sec / 4)
            end_pos = start_pos + (bar_length_sec / 16) # Sharp 16th note transient

            start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_pos)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_pos)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(kick_take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(kick_take, end_qn)

            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 36, 127, False)
            
    RPR.RPR_MIDI_Sort(kick_take)

    return f"Created sidechain setup: '{track_name}' pumping over {bars} bars triggered by Ghost Kick at {bpm} BPM in {key} {scale}"
