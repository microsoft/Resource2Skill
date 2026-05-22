def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Pumping Drop",
    bpm: int = 128,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create an EDM Four-on-the-Floor Drop with volume-ducking sidechain pump.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # ==========================================
    # TRACK 1: FOUR-ON-THE-FLOOR KICK
    # ==========================================
    kick_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(kick_idx, True)
    kick_track = RPR.RPR_GetTrack(0, kick_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", f"{track_name} - Kick", True)

    # Make Kick sound punchy (ReaSynth)
    kick_fx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 1, 0.0)    # Attack
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 2, 0.05)   # Decay
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 3, 0.0)    # Sustain
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 4, 0.05)   # Release
    
    # Kick MIDI Item
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # Insert Kick notes every quarter note
    kick_pitch = NOTE_MAP.get(key, 0) + 24 # C1 area
    total_beats = bars * beats_per_bar
    for i in range(total_beats):
        start_time = i * beat_length_sec
        end_time = start_time + (beat_length_sec * 0.25) # Short clicky note
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_time)
        
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, kick_pitch, 127, False)

    RPR.RPR_MIDI_Sort(kick_take)

    # ==========================================
    # TRACK 2: SUSTAINED SYNTH & SIDECHAIN PUMP
    # ==========================================
    synth_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(synth_idx, True)
    synth_track = RPR.RPR_GetTrack(0, synth_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", f"{track_name} - Synths", True)

    # Make Synth sound thick (ReaSynth Sawtooth)
    synth_fx = RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx, 1, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx, 2, 0.5)  # Decay
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx, 3, 1.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx, 4, 0.2)  # Release
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx, 5, 1.0)  # Sawtooth mix

    # Synth MIDI Item
    synth_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_LENGTH", total_length_sec)
    synth_take = RPR.RPR_AddTakeToMediaItem(synth_item)

    # Calculate Triad Chord
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Octave 3
    chord_pitches = [
        root_pitch - 12,                  # Sub Bass
        root_pitch,                       # Root
        root_pitch + scale_intervals[2],  # Third
        root_pitch + scale_intervals[4]   # Fifth
    ]

    # Insert sustained chord spanning the entire item
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(synth_take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(synth_take, total_length_sec)
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(synth_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(synth_take)

    # ==========================================
    # AUTOMATION: LFO VOLUME DUCKING (PUMP)
    # ==========================================
    # Force the Volume Envelope to be visible and active so we can manipulate it
    RPR.RPR_SetOnlyTrackSelected(synth_track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    
    vol_env = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")
    
    if vol_env:
        for i in range(total_beats):
            beat_time = i * beat_length_sec
            offbeat_time = beat_time + (beat_length_sec * 0.5) # The "and" of the beat
            
            # Envelope values for Volume are Amplitudes (0.0 = -inf dB, 1.0 = 0 dB)
            # Shape 2 = "Slow start/end" which mimics a smooth sidechain release curve perfectly
            
            # Dip sharply on the kick hit (10% amplitude)
            RPR.RPR_InsertEnvelopePoint(vol_env, beat_time, 0.1, 2, 0.0, False, True)
            
            # Swell back to full volume (100% amplitude) by the offbeat
            RPR.RPR_InsertEnvelopePoint(vol_env, offbeat_time, 1.0, 2, 0.0, False, True)
            
        RPR.RPR_Envelope_SortPoints(vol_env)

    return f"Created Drop '{track_name}' in {key} {scale}: 4-on-the-floor Kick + Pumping Sidechain Chords over {bars} bars at {bpm} BPM."
