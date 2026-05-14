def create_pattern(
    project_name: str = "EDM_House",
    track_name: str = "Arrangement",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,  # Length of one section (Total generated = 2 * bars)
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Intro-to-Drop arrangement scaffold with filter sweeps and sidechain pumping.
    """
    import reaper_python as RPR
    import math

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Base octave 4
    
    # Target a classic 1-6-3-7 progression
    prog_degrees = [0, 5, 2, 6] 
    
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    intro_length = bar_sec * bars
    drop_length = bar_sec * bars
    
    start_idx = RPR.RPR_CountTracks(0)

    # === Helper function to insert MIDI notes ===
    def add_midi_note(take, start_time, end_time, pitch, vel):
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                start_time * RPR.RPR_MIDI_GetProjTimeFromPPQPos(take, 1000), 
                                end_time * RPR.RPR_MIDI_GetProjTimeFromPPQPos(take, 1000), 
                                0, pitch, vel, False)

    # ==========================================
    # 1. SETUP CHORDS TRACK (Plays throughout)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    tr_chords = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_chords, "P_NAME", f"{track_name}_Chords", True)
    # Give track 4 channels for sidechaining
    RPR.RPR_SetMediaTrackInfo_Value(tr_chords, "I_NCHAN", 4)
    
    # Add Synth
    fx_synth = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_synth, 0, 1.0) # Sawtooth mix
    
    # Create MIDI item for Chords (Intro + Drop)
    item_chords = RPR.RPR_AddMediaItemToTrack(tr_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", intro_length + drop_length)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)
    
    for i in range(bars * 2):
        degree = prog_degrees[i % len(prog_degrees)]
        
        # Build triad
        root_note = root_midi + scale_intervals[degree]
        third_deg = (degree + 2) % 7
        fifth_deg = (degree + 4) % 7
        
        # Adjust octaves for wrapping
        third_note = root_midi + scale_intervals[third_deg] + (12 if third_deg < degree else 0)
        fifth_note = root_midi + scale_intervals[fifth_deg] + (12 if fifth_deg < degree else 0)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, i * bar_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, (i + 1) * bar_sec)
        
        RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, root_note, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, third_note, velocity_base - 10, False)
        RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, fifth_note, velocity_base - 10, False)

    RPR.RPR_MIDI_Sort(take_chords)

    # ==========================================
    # 2. SETUP DUMMY KICK (Plays during intro, muted)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(start_idx + 1, True)
    tr_dummy = RPR.RPR_GetTrack(0, start_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_dummy, "P_NAME", f"{track_name}_Dummy_SC", True)
    RPR.RPR_SetMediaTrackInfo_Value(tr_dummy, "B_MAINSEND", 0) # Silence the track
    
    # Create Sidechain Send (Track 2 -> Track 1, Dest Chan 3/4)
    send_idx = RPR.RPR_CreateTrackSend(tr_dummy, tr_chords)
    RPR.RPR_SetTrackSendInfo_Value(tr_dummy, 0, send_idx, "I_DSTCHAN", 2) # 2 = channels 3/4
    
    # Dummy Kick Audio Synth
    RPR.RPR_TrackFX_AddByName(tr_dummy, "ReaSynth", False, -1)
    
    item_dummy = RPR.RPR_AddMediaItemToTrack(tr_dummy)
    RPR.RPR_SetMediaItemInfo_Value(item_dummy, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_dummy, "D_LENGTH", intro_length) # Only in intro!
    take_dummy = RPR.RPR_AddTakeToMediaItem(item_dummy)
    
    # 4 on the floor dummy kick
    for b in range(bars * 4):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_dummy, b * beat_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_dummy, b * beat_sec + (beat_sec * 0.2))
        RPR.RPR_MIDI_InsertNote(take_dummy, False, False, start_ppq, end_ppq, 0, 36, 127, False)
    RPR.RPR_MIDI_Sort(take_dummy)

    # Add ReaComp to Chords for Pumping
    fx_comp = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_comp, 0, 0.1)  # Thresh (pull down)
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_comp, 1, 0.25) # Ratio (~4:1)
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_comp, 4, 0.0)  # Fast attack
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_comp, 5, 100)  # 100ms release for standard pump
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_comp, 13, 1)   # Detector: Auxiliary Input L+R

    # ==========================================
    # 3. AUTOMATE FILTER ON CHORDS
    # ==========================================
    fx_eq = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, fx_eq, 11, 3) # Set Band 4 to High Cut (Low Pass)
    
    # Param 9 is Band 4 Frequency in ReaEQ
    env_freq = RPR.RPR_GetFXEnvelope(tr_chords, fx_eq, 9, True)
    
    # Linear sweep from ~300Hz to 20kHz over the intro
    val_start = 0.2 # low pos in ReaEQ curve
    val_end = 0.95  # fully open
    RPR.RPR_InsertEnvelopePoint(env_freq, 0.0, val_start, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_freq, intro_length, val_end, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env_freq)

    # ==========================================
    # 4. SETUP BASS (Plays only during Drop)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(start_idx + 2, True)
    tr_bass = RPR.RPR_GetTrack(0, start_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_bass, "P_NAME", f"{track_name}_Bass", True)
    
    fx_bass = RPR.RPR_TrackFX_AddByName(tr_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_bass, fx_bass, 1, 1.0) # Square wave
    
    item_bass = RPR.RPR_AddMediaItemToTrack(tr_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", intro_length) # Starts at drop
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", drop_length)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)
    
    for i in range(bars):
        degree = prog_degrees[i % len(prog_degrees)]
        bass_note = root_midi + scale_intervals[degree] - 24 # 2 octaves down
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, intro_length + (i * bar_sec))
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, intro_length + ((i + 1) * bar_sec))
        RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, bass_note, velocity_base + 10, False)
    RPR.RPR_MIDI_Sort(take_bass)

    # ==========================================
    # 5. SETUP REAL DRUMS (Plays only during Drop)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(start_idx + 3, True)
    tr_drums = RPR.RPR_GetTrack(0, start_idx + 3)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_drums, "P_NAME", f"{track_name}_Main_Drums", True)
    
    item_drums = RPR.RPR_AddMediaItemToTrack(tr_drums)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_POSITION", intro_length)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_LENGTH", drop_length)
    take_drums = RPR.RPR_AddTakeToMediaItem(item_drums)
    
    # Standard house beat: Kick on downbeats, Hats on offbeats
    for i in range(bars * 4): # Every beat
        time_pos = intro_length + (i * beat_sec)
        time_offbeat = time_pos + (beat_sec / 2.0)
        
        k_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, time_pos)
        k_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, time_pos + (beat_sec * 0.2))
        
        h_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, time_offbeat)
        h_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, time_offbeat + (beat_sec * 0.2))
        
        # Kick (36)
        RPR.RPR_MIDI_InsertNote(take_drums, False, False, k_start, k_end, 0, 36, 120, False)
        # Open Hat (46)
        RPR.RPR_MIDI_InsertNote(take_drums, False, False, h_start, h_end, 0, 46, 100, False)
        
    RPR.RPR_MIDI_Sort(take_drums)

    RPR.RPR_UpdateArrange()

    return f"Created EDM Arrangement Scaffold: {bars}-bar Intro (Filtered & Pumping) -> {bars}-bar Drop in {key} {scale} at {bpm} BPM."
