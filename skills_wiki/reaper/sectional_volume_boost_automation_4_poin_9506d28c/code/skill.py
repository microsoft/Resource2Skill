def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Lead Solo",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a track with a generative synth line and applies a 4-point Volume 
    Automation plateau to boost the level during the second half of the sequence.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Total number of bars. The boost will occur in the second half.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated automation.
    """
    import math
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add Instrument ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item for Audibility ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar
    item_length = sec_per_bar * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Generate a driving 1/4 note pulse
    root_pitch = 60 + NOTE_MAP.get(key, 0)
    notes_per_bar = 4
    note_len_sec = sec_per_beat
    
    note_count = 0
    for b in range(bars):
        for n in range(notes_per_bar):
            start_t = b * sec_per_bar + n * note_len_sec
            end_t = start_t + (note_len_sec * 0.8) # Staccato feel
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_t)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_t)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Configure Automation Envelope ===
    # Attempt to get the envelope; if it doesn't exist, toggle it active via Action
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not env:
        RPR.RPR_SetOnlyTrackSelected(track)
        RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope active
        env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
        
    if not env:
        return f"Created track '{track_name}', but failed to initialize Volume Envelope."

    # === Step 5: Calculate Plateau Timing & Values ===
    # We will boost the volume for the second half of the clip
    boost_start_sec = (bars / 2.0) * sec_per_bar
    boost_end_sec = item_length
    
    # 1 beat ramp time to ensure smooth transitions (no audio popping)
    ramp_sec = sec_per_beat 
    
    # Helper to convert dB to amplitude multiplier (REAPER envelope domain)
    def db_to_amp(db):
        return 10.0 ** (db / 20.0)

    base_db = 0.0
    boost_db = 4.5 # Provide a highly noticeable +4.5dB boost
    
    val_base = db_to_amp(base_db)
    val_boost = db_to_amp(base_db + boost_db)

    # Insert boundary points (Linear shape = 0)
    # 1. Initial base level
    RPR.RPR_InsertEnvelopePoint(env, 0.0, val_base, 0, 0.0, False, True)
    
    # 2. Ramp Start (Anchor point before boost)
    t_ramp_start = max(0.0, boost_start_sec - ramp_sec)
    RPR.RPR_InsertEnvelopePoint(env, t_ramp_start, val_base, 0, 0.0, False, True)
    
    # 3. Boost Start (Peak level reached)
    RPR.RPR_InsertEnvelopePoint(env, boost_start_sec, val_boost, 0, 0.0, False, True)
    
    # 4. Boost End (Begin ramping down)
    t_boost_end = boost_end_sec - ramp_sec
    RPR.RPR_InsertEnvelopePoint(env, t_boost_end, val_boost, 0, 0.0, False, True)
    
    # 5. Ramp End (Back to base level)
    RPR.RPR_InsertEnvelopePoint(env, boost_end_sec, val_base, 0, 0.0, False, True)
    
    # Finalize envelope calculations
    RPR.RPR_Envelope_SortTrackEnvelopes(env)

    return f"Created '{track_name}' ({note_count} notes). Applied a +{boost_db}dB volume boost plateau starting at bar {int(bars/2)+1}."
