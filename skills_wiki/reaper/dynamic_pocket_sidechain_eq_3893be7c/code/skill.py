def create_pattern(
    project_name: str = "CleanLowEnd",
    track_name: str = "Sub Bass (Dynamic EQ)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Kick track and a Sub Bass track, utilizing Envelope Automation 
    on ReaEQ to simulate the Dynamic "Sidechain EQ" technique for a clean low end.
    """
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm

    # === Step 2: Create Kick Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    kick_tr = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_tr, "P_NAME", "Kick Trigger", True)

    kick_item = RPR.RPR_AddMediaItemToTrack(kick_tr)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", beat_length_sec * beats_per_bar * bars)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    # Setup ReaSynth to sound like a punchy kick (No sustain, short decay)
    RPR.RPR_TrackFX_AddByName(kick_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(kick_tr, 0, 7, 0.0) # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(kick_tr, 0, 6, 0.05) # Decay

    # Insert 4-on-the-floor kick pattern
    kick_hits = []
    for b in range(bars):
        for beat in [0, 1, 2, 3]:
            start_sec = (b * beats_per_bar + beat) * beat_length_sec
            end_sec = start_sec + 0.1
            kick_hits.append(start_sec) # Store for our envelope ducking later
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_sec)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 110, 36, False)

    # === Step 3: Create Sub Bass Track ===
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_tr = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_tr, "P_NAME", track_name, True)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_tr)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", beat_length_sec * beats_per_bar * bars)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Setup ReaSynth to sound like a Sub Bass (Triangle wave, full sustain)
    RPR.RPR_TrackFX_AddByName(bass_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bass_tr, 0, 2, 0.0) # Square
    RPR.RPR_TrackFX_SetParamNormalized(bass_tr, 0, 3, 0.0) # Saw
    RPR.RPR_TrackFX_SetParamNormalized(bass_tr, 0, 4, 1.0) # Triangle
    RPR.RPR_TrackFX_SetParamNormalized(bass_tr, 0, 7, 1.0) # Sustain

    # Create a 4-bar Bass Drone/Progression
    root_midi = NOTE_MAP.get(key, 0) + 24 # Deep sub (C1)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    progression = [0, 2, 4, 0] # Example: I - III - V - I

    for b in range(bars):
        scale_idx = progression[b % len(progression)] % len(scale_intervals)
        pitch = root_midi + scale_intervals[scale_idx]
        
        start_sec = b * beats_per_bar * beat_length_sec
        end_sec = start_sec + (beats_per_bar * beat_length_sec)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_sec)
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, 90, pitch, False)

    # === Step 4: The Dynamic EQ Ducking Setup ===
    eq_idx = RPR.RPR_TrackFX_AddByName(bass_tr, "ReaEQ", False, -1)
    
    # In ReaEQ, parameter index 4 is the Gain for Band 2 (usually a Bell filter in the low-mid range)
    # We will fetch its envelope and draw "ducking" points every time the kick hits.
    env = RPR.RPR_GetFXEnvelope(bass_tr, eq_idx, 4, True)

    for hit_sec in kick_hits:
        # Gain mapping for ReaEQ: 0.5 roughly equals 0 dB. 
        # Lowering to ~0.35 equates to a substantial dB dip (ducking)
        
        # 1 ms before the kick: Baseline (0 dB)
        RPR.RPR_InsertEnvelopePoint(env, hit_sec - 0.001, 0.5, 0, 0, False, True)
        
        # Exactly on the kick: Duck the frequency band (Fast Attack)
        # Shape 2 represents a slow start/end curve to smooth the ducking
        RPR.RPR_InsertEnvelopePoint(env, hit_sec, 0.35, 2, 0, False, True) 
        
        # ~150 ms after the kick: Recover to Baseline (Release)
        RPR.RPR_InsertEnvelopePoint(env, hit_sec + 0.150, 0.5, 0, 0, False, True)

    # Apply changes to the envelope
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created Kick and '{track_name}' using Dynamic EQ Envelopes on ReaEQ over {bars} bars at {bpm} BPM."
