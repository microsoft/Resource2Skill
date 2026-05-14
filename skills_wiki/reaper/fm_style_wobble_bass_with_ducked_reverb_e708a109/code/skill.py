def create_pattern(
    project_name: str = "WobbleProject",
    track_name: str = "Wobble Bass",
    bpm: int = 140,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create an FM-style Wobble Bass with inverted reverb in REAPER.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root MIDI pitch (Octave 1 for heavy bass)
    root_val = NOTE_MAP.get(key, 4)
    bass_pitch = root_val + 24 # e.g., E1
    fm_pitch = bass_pitch + 24 # +2 Octaves to simulate FM modulator

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain ===
    # 1. ReaSynth (Generates the tone)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4) # Square Mix (for weight)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.2) # Saw Mix (for grit)
    
    # 2. JS Distortion (Tube style grit)
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 3.0)  # Gain
    
    # 3. ReaVerbate (For the ducked reverb tail)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.8)  # Room size
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.1)  # Dampening

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert sustained MIDI notes (the "LFO" envelopes will create the rhythm)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, total_length_sec)
    
    # Bass fundamental
    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, True)
    # +2 Octave layer simulating the FM harmonic modulation
    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, fm_pitch, int(velocity_base * 0.8), True)
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate Envelopes (The "Wobble" & Inverted Reverb) ===
    # Get envelopes
    vol_env = RPR.RPR_GetFXEnvelope(track, synth_idx, 0, True) # ReaSynth Volume
    verb_env = RPR.RPR_GetFXEnvelope(track, verb_idx, 0, True) # ReaVerbate Wet
    
    current_time = 0.0
    
    while current_time < total_length_sec - 0.01:
        # Rhythmic variation: 1/16th notes on the last bar, 1/8th notes otherwise
        if current_time >= bar_length_sec * (bars - 1):
            wobble_duration = beat_sec / 4.0 # 1/16 note
        else:
            wobble_duration = beat_sec / 2.0 # 1/8 note
            
        mid_time = current_time + (wobble_duration / 2.0)
        end_time = current_time + wobble_duration

        # --- Synth Volume Wobble (Triangle shape) ---
        # 0 is linear interpolation
        RPR.RPR_InsertEnvelopePoint(vol_env, current_time, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, mid_time, 0.8, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, end_time, 0.0, 0, 0.0, False, True)

        # --- Inverted Reverb Ducking ---
        # Reverb blooms when volume is down, disappears when volume is up
        RPR.RPR_InsertEnvelopePoint(verb_env, current_time, 0.4, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(verb_env, mid_time, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(verb_env, end_time, 0.4, 0, 0.0, False, True)

        current_time = end_time

    # Sort envelope points
    RPR.RPR_Envelope_Sort(vol_env)
    RPR.RPR_Envelope_Sort(verb_env)

    return f"Created '{track_name}' with automated FM wobble + ducked reverb over {bars} bars at {bpm} BPM"
