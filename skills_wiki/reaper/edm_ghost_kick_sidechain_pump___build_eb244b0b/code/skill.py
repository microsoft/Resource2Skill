def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Pump Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM Ghost Kick Sidechain Pump arrangement in REAPER.
    Generates a 4-on-the-floor kick track and a sustained chord track with perfect rhythmic pumping.

    Args:
        project_name: Project identifier.
        track_name: Name for the main pumping chords track.
        bpm: Tempo in BPM (120-130 recommended).
        key: Root note (e.g., C, F#).
        scale: Scale type (e.g., minor, major).
        bars: Number of bars (standard 4-bar loop).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Music Theory Data
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # EDM Standard Progression (i - VI - III - VII in minor, I - IV - vi - V in major)
    prog_degrees = [0, 5, 2, 6] if scale.lower() == "minor" else [0, 3, 5, 4]
    
    # Timing calculations
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    
    # ==========================================
    # TRACK 1: PUMPING CHORDS
    # ==========================================
    idx_chords = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_chords, True)
    tr_chords = RPR.RPR_GetTrack(0, idx_chords)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_chords, "P_NAME", track_name, True)
    
    # Add Synth for Chords
    synth_chords = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, synth_chords, 0, 0.6) # Volume
    RPR.RPR_TrackFX_SetParam(tr_chords, synth_chords, 2, 1.0) # Saw wave mix
    RPR.RPR_TrackFX_SetParam(tr_chords, synth_chords, 4, 0.4) # Attack
    RPR.RPR_TrackFX_SetParam(tr_chords, synth_chords, 5, 0.5) # Release
    
    # Add JS: Volume/Pan Smoother for the Sidechain Pump effect
    fx_vol = RPR_TrackFX_AddByName(tr_chords, "JS: Volume/Pan Smoother", False, -1)
    # Param 0 is Volume (typically -120 to +12dB. 0.0 is -inf, ~0.7 is 0dB)
    env_vol = RPR.RPR_GetFXEnvelope(tr_chords, fx_vol, 0, True)
    
    # Create MIDI Item for Chords
    item_chords = RPR.RPR_AddMediaItemToTrack(tr_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bar_len * bars)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)
    
    # Generate Chord Notes & Pumping Envelope
    octave_base = 48 # C3
    for b in range(bars):
        deg = prog_degrees[b % len(prog_degrees)]
        start_time = b * bar_len
        end_time = start_time + bar_len
        
        # Build 4-note voicing
        chord_notes = []
        for i in [0, 2, 4]: # Triad
            idx = (deg + i) % 7
            oct_shift = (deg + i) // 7
            note = root_val + scale_intervals[idx] + (12 * oct_shift)
            chord_notes.append(octave_base + note)
        # Add deep root note
        chord_notes.append(octave_base - 12 + root_val + scale_intervals[deg])
        
        # Insert MIDI notes
        for note in chord_notes:
            # Note start in PPQ (960 per quarter note)
            start_ppq = b * 4 * 960
            end_ppq = start_ppq + (4 * 960)
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
            
        # Insert Volume Envelope Points for the 4 beats in this bar
        for beat in range(4):
            t_beat = start_time + (beat * beat_len)
            # Fast duck on downbeat (Shape 2: Fast End)
            RPR.RPR_InsertEnvelopePoint(env_vol, t_beat, 0.0, 2, 0, False, True)
            # Swell back to full volume quickly (Shape 0: Linear)
            RPR.RPR_InsertEnvelopePoint(env_vol, t_beat + (beat_len * 0.3), 0.73, 0, 0, False, True)
            # Hold volume until just before next beat
            RPR.RPR_InsertEnvelopePoint(env_vol, t_beat + (beat_len * 0.98), 0.73, 0, 0, False, True)

    RPR.RPR_Envelope_SortPoints(env_vol)
    
    # ==========================================
    # TRACK 2: KICK DRUM (The "Ghost" Kick)
    # ==========================================
    idx_kick = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_kick, True)
    tr_kick = RPR.RPR_GetTrack(0, idx_kick)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_kick, "P_NAME", "Ghost Kick", True)
    
    # Add Synth for Kick
    synth_kick = RPR.RPR_TrackFX_AddByName(tr_kick, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_kick, synth_kick, 0, 0.8) # Volume
    RPR.RPR_TrackFX_SetParam(tr_kick, synth_kick, 1, -1.0) # Tune down
    RPR.RPR_TrackFX_SetParam(tr_kick, synth_kick, 4, 0.0) # Fast attack
    RPR.RPR_TrackFX_SetParam(tr_kick, synth_kick, 5, 0.1) # Fast release
    RPR.RPR_TrackFX_SetParam(tr_kick, synth_kick, 6, 0.15) # Pitch drop envelope

    # Create MIDI Item for Kick
    item_kick = RPR.RPR_AddMediaItemToTrack(tr_kick)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_LENGTH", bar_len * bars)
    take_kick = RPR.RPR_AddTakeToMediaItem(item_kick)
    
    # 4-on-the-floor pattern
    for beat in range(bars * 4):
        start_ppq = beat * 960
        end_ppq = start_ppq + 240 # 16th note length
        # C2 for a nice low kick punch
        RPR.RPR_MIDI_InsertNote(take_kick, False, False, start_ppq, end_ppq, 0, 36, 120, False)
        
    # Force UI update
    RPR.RPR_UpdateTimeline()
    
    return f"Created '{track_name}' pumping chords and 'Ghost Kick' over {bars} bars at {bpm} BPM in {key} {scale}."
