def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "Pumping_Chords",
    bpm: int = 125,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Sidechain Pumping Chord progression with a hidden Ghost Kick trigger
    and a rising EQ filter sweep.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chords track.
        bpm: Tempo in BPM (EDM House standard is 120-128).
        key: Root note (e.g., 'A').
        scale: Scale type (e.g., 'minor').
        bars: Number of bars to generate (4 recommended).
        velocity_base: Base MIDI velocity.
    
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
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Timing calculations
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Step 2: Create Ghost Kick Track (The Trigger)
    idx_ghost = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_ghost, True)
    track_ghost = RPR.RPR_GetTrack(0, idx_ghost)
    RPR.RPR_GetSetMediaTrackInfo_String(track_ghost, "P_NAME", "Ghost Kick (Trigger)", True)
    
    # Disable Master Send so the ghost kick is inaudible
    RPR.RPR_SetMediaTrackInfo_Value(track_ghost, "B_MAINSEND", 0.0)
    
    # Add simple synth to generate the trigger click
    RPR.RPR_TrackFX_AddByName(track_ghost, "ReaSynth", False, -1)
    
    # Create MIDI Item for Ghost Kick (4-on-the-floor)
    item_ghost = RPR.RPR_AddMediaItemToTrack(track_ghost)
    RPR.RPR_SetMediaItemInfo_Value(item_ghost, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_ghost, "D_LENGTH", total_length_sec)
    take_ghost = RPR.RPR_AddTakeToMediaItem(item_ghost)
    
    for b in range(bars * 4): # Every quarter note
        start_time = b * (60.0 / bpm)
        end_time = start_time + 0.1 # Short 100ms trigger
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_ghost, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_ghost, end_time)
        RPR.RPR_MIDI_InsertNote(take_ghost, False, False, start_ppq, end_ppq, 0, 36, 127, False)

    # Step 3: Create Chords Track
    idx_chord = idx_ghost + 1
    RPR.RPR_InsertTrackAtIndex(idx_chord, True)
    track_chord = RPR.RPR_GetTrack(0, idx_chord)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chord, "P_NAME", track_name, True)
    
    # Enable 4 channels on chord track to receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(track_chord, "I_NCHAN", 4)
    
    # Create MIDI Item for Chords
    item_chord = RPR.RPR_AddMediaItemToTrack(track_chord)
    RPR.RPR_SetMediaItemInfo_Value(item_chord, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chord, "D_LENGTH", total_length_sec)
    take_chord = RPR.RPR_AddTakeToMediaItem(item_chord)

    # Standard EDM i - VII - VI progression
    root_val = NOTE_MAP.get(key.capitalize(), 9) + 48 # Default A3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Progression degrees: i (0), VII (-2 in natural minor), VI (-4)
    progression_degrees = [0, -2, -4, -4]
    
    for bar in range(bars):
        degree = progression_degrees[bar % len(progression_degrees)]
        
        # Build triad
        chord_notes = [
            root_val + degree,                  # Root
            root_val + degree + 3 + (0 if degree==0 else 1), # Third (simplified dictation)
            root_val + degree + 7               # Fifth
        ]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec - 0.05 # slight gap
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chord, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chord, end_time)
        
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(take_chord, False, False, start_ppq, end_ppq, 0, int(note), velocity_base, False)

    # Add Instrument and Effects to Chord Track
    fx_synth = RPR.RPR_TrackFX_AddByName(track_chord, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_synth, 0, 0.5) # Saw/Square mix for rich chords
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_synth, 2, 0.4) # Slightly longer release
    
    fx_eq = RPR.RPR_TrackFX_AddByName(track_chord, "ReaEQ", False, -1)
    fx_comp = RPR.RPR_TrackFX_AddByName(track_chord, "ReaComp", False, -1)

    # Configure ReaComp for Sidechain Pumping
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_comp, 0, 0.1)  # Threshold low (-40dB)
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_comp, 1, 0.8)  # Ratio high (approx 10:1)
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_comp, 2, 0.0)  # Attack 0ms
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_comp, 3, 0.12) # Release ~120ms (pumping groove)
    RPR.RPR_TrackFX_SetParamNormalized(track_chord, fx_comp, 13, 0.15)# Detector Input -> Aux L+R (Channels 3/4)

    # Step 4: Route Ghost Kick to Chord Compressor (Channels 1/2 -> 3/4)
    send_idx = RPR.RPR_CreateTrackSend(track_ghost, track_chord)
    RPR.RPR_SetTrackSendInfo_Value(track_ghost, 0, send_idx, "I_DSTCHAN", 2) # 2 = Destination channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(track_ghost, 0, send_idx, "D_VOL", 1.0)

    # Step 5: Automate ReaEQ Filter Sweep (Intro Build-up)
    # Param 11 in ReaEQ is typically Band 4 Frequency (High Shelf/Cut)
    env_eq = RPR.RPR_GetFXEnvelope(track_chord, fx_eq, 11, True)
    if env_eq:
        # Start low (muffled)
        RPR.RPR_InsertEnvelopePoint(env_eq, 0.0, 0.3, 0, 0.0, False, True)
        # End high (open and bright) right before the end of the section
        RPR.RPR_InsertEnvelopePoint(env_eq, total_length_sec - 0.1, 0.9, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_eq)

    return f"Created '{track_name}' pumping sidechain structure with Ghost Kick over {bars} bars at {bpm} BPM."
