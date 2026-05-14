def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 115,
    **kwargs,
) -> str:
    """
    Create a Parallel Rock Bass Mixing Chain in REAPER.
    Generates a driving 8th-note bassline and sets up a dual-track 
    (Main + Parallel Distortion) processing architecture.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root note in the bass register (Octave 1)
    # C1 is MIDI note 24.
    root_note = NOTE_MAP.get(key, 4) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Main Bass Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    main_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(main_track, "P_NAME", f"{track_name} Main", True)

    # === Step 3: Create MIDI Item & Driving 8th Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(main_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Insert straight 8th notes
    total_notes = bars * 8
    beat_len = 60.0 / bpm
    eighth_len = beat_len / 2.0
    
    for i in range(total_notes):
        start_time = i * eighth_len
        # 90% duration for a slight gap between picked notes
        end_time = start_time + (eighth_len * 0.9) 
        
        # Convert seconds to MIDI ticks (Project PPQ is typically 960)
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_note, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Main FX Chain (Synth -> Comp -> EQ) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(main_track, "ReaSynth", False, -1)
    
    # Add Compressor
    comp_idx = RPR.RPR_TrackFX_AddByName(main_track, "ReaComp", False, -1)
    # Set explicit normalized values for demonstration (Threshold down, Ratio 4:1)
    RPR.RPR_TrackFX_SetParam(main_track, comp_idx, 0, 0.6) # Threshold
    RPR.RPR_TrackFX_SetParam(main_track, comp_idx, 1, 0.1) # Ratio
    RPR.RPR_TrackFX_SetParam(main_track, comp_idx, 2, 0.02) # Attack (~20ms)
    
    # Add EQ
    eq_idx = RPR.RPR_TrackFX_AddByName(main_track, "ReaEQ", False, -1)
    # Set explicit normalized values for Low Shelf and Mid Peak
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 0, 0.15) # Freq 1 (~200Hz)
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 1, 0.65) # Gain 1 (+5dB)
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 3, 0.5)  # Freq 2 (~2.5kHz)
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 4, 0.6)  # Gain 2 (+4dB)

    # === Step 5: Create Parallel Distortion Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    dist_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(dist_track, "P_NAME", f"{track_name} Dist", True)
    
    # Set Parallel Track Volume to ~ -12dB (linear 0.25) to tuck it under the main mix
    RPR.RPR_SetMediaTrackInfo_Value(dist_track, "D_VOL", 0.25)
    
    # Add Distortion Plugin
    dist_idx = RPR.RPR_TrackFX_AddByName(dist_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(dist_track, dist_idx, 0, 0.8) # Drive it hard

    # === Step 6: Route Main Track to Parallel Track ===
    # 0 = Post-Fader, 1 = Pre-FX, 3 = Post-FX
    RPR.RPR_CreateTrackSend(main_track, dist_track)

    return f"Created Parallel Bass Architecture: '{track_name} Main' routed to '{track_name} Dist' blending {total_notes} notes over {bars} bars."
