def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a synth drone with Volume and Filter Cutoff automation in Read mode.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate the swell over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth and Configure Timbre ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Turn down Sine (Param 7), turn up Sawtooth (Param 8) for a rich filter sweep
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.0)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 1.0)

    # === Step 4: Create MIDI Item & Drone Note ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Root note in octave 3
    root_pitch = NOTE_MAP.get(key, 0) + 48 
    
    # 1 Quarter Note = 960 PPQ (Pulses Per Quarter)
    total_ppq = int(beats_per_bar * bars * 960)
    
    RPR.RPR_MIDI_InsertNote(
        take, False, False, 0, total_ppq, 0, root_pitch, velocity_base, False
    )
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate Filter Cutoff (Param 11) ===
    # True flag creates the envelope if it doesn't exist
    cut_env = RPR.RPR_GetFXEnvelope(track, synth_idx, 11, True) 
    
    # Sweep from 10% closed to 90% open over the item duration
    RPR.RPR_InsertEnvelopePoint(cut_env, 0.0, 0.1, 0, 0.0, False, False)
    RPR.RPR_InsertEnvelopePoint(cut_env, item_length_sec, 0.9, 0, 0.0, False, False)
    RPR.RPR_Envelope_Sort(cut_env)

    # === Step 6: Automate Volume (Param 0) ===
    vol_env = RPR.RPR_GetFXEnvelope(track, synth_idx, 0, True)
    
    # Swell volume: Silence -> 70% at midpoint -> Silence at end
    RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 0, 0.0, False, False)
    RPR.RPR_InsertEnvelopePoint(vol_env, item_length_sec * 0.5, 0.7, 0, 0.0, False, False)
    RPR.RPR_InsertEnvelopePoint(vol_env, item_length_sec, 0.0, 0, 0.0, False, False)
    RPR.RPR_Envelope_Sort(vol_env)

    # === Step 7: Set Automation Mode ===
    # 0=Trim/Read, 1=Read, 2=Touch, 3=Write, 4=Latch
    # Sets track to actively read our programmed envelopes.
    RPR.RPR_SetTrackAutomationMode(track, 1)

    return f"Created '{track_name}' drone with Volume & Filter Read Automation over {bars} bars at {bpm} BPM in {key} {scale}."
