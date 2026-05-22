def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "EDM",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an 8-bar EDM "Buildup to Drop" arrangement pattern.
    Bars 1-4: Filtered chords with 4-on-the-floor kick.
    Bars 5-8: Filter opens, syncopated chords, driving bassline, and full drums enter.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    scale_notes = [(root_val + iv) for iv in intervals]
    
    # Simple progression: i - VI - III - VII (using scale degrees 0, 5, 2, 6)
    prog_degrees = [0, 5, 2, 6] 
    
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    
    # Helper to insert a track
    def add_track(name, vol=1.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "D_VOL", vol)
        return trk

    # Helper to create MIDI item
    def create_midi_item(trk, start_time, length):
        item = RPR.RPR_AddMediaItemToTrack(trk)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    # === 1. CHORDS TRACK ===
    chords_trk = add_track(f"{track_name}_Chords", 0.7)
    RPR.RPR_TrackFX_AddByName(chords_trk, "ReaSynth", False, -1)
    # Make ReaSynth sound a bit richer (sawtooth mix)
    RPR.RPR_TrackFX_SetParam(chords_trk, 0, 1, 1.0) # Square mix
    RPR.RPR_TrackFX_SetParam(chords_trk, 0, 2, 1.0) # Saw mix
    
    # Add JS Resonant Lowpass Filter for the sweep
    lp_fx = RPR.RPR_TrackFX_AddByName(chords_trk, "JS: Filters/resonantlowpass", False, -1)
    
    # Add Filter Automation Envelope
    env = RPR.RPR_GetFXEnvelope(chords_trk, lp_fx, 0, True) # Param 0 is Frequency
    # Start closed (Buildup)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 400.0, 0, 0, False, True)
    # Sweep up to end of bar 4
    RPR.RPR_InsertEnvelopePoint(env, bar_len * 4 - 0.1, 20000.0, 0, 0, False, True)
    # Keep open for Drop (Bars 5-8)
    RPR.RPR_InsertEnvelopePoint(env, bar_len * 8, 20000.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    chords_take = create_midi_item(chords_trk, 0.0, bar_len * 8)
    
    octave_base = 4 * 12
    for bar in range(8):
        degree = prog_degrees[bar % 4]
        # Build a triad
        root_note = octave_base + scale_notes[degree % 7] + (12 if degree >= 7 else 0)
        third_note = octave_base + scale_notes[(degree + 2) % 7] + (12 if (degree + 2) >= 7 else 0)
        fifth_note = octave_base + scale_notes[(degree + 4) % 7] + (12 if (degree + 4) >= 7 else 0)
        
        bar_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, bar * bar_len)
        
        if bar < 4:
            # Buildup: Long sustained whole notes
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, (bar + 1) * bar_len)
            for note in [root_note, third_note, fifth_note]:
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, bar_start_ppq, end_ppq, 0, note, velocity_base, False)
        else:
            # Drop: Syncopated stabs (dotted-quarter, eighth, half)
            hit1_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, bar * bar_len + beat_len * 1.5)
            hit2_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, bar * bar_len + beat_len * 1.5)
            hit2_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, bar * bar_len + beat_len * 2.0)
            hit3_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, bar * bar_len + beat_len * 2.5)
            hit3_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, (bar + 1) * bar_len)
            
            for note in [root_note, third_note, fifth_note]:
                # Hit 1
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, bar_start_ppq, hit1_end, 0, note, velocity_base, False)
                # Hit 2
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, hit2_start, hit2_end, 0, note, velocity_base-10, False)
                # Hit 3
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, hit3_start, hit3_end, 0, note, velocity_base+10, False)


    # === 2. DRUMS TRACK ===
    drums_trk = add_track(f"{track_name}_Drums", 0.9)
    RPR.RPR_TrackFX_AddByName(drums_trk, "ReaSynth", False, -1)
    # Tune down for a kick-like thump
    RPR.RPR_TrackFX_SetParam(drums_trk, 0, 3, -24.0) # Extra tuning
    RPR.RPR_TrackFX_SetParam(drums_trk, 0, 4, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(drums_trk, 0, 5, 20.0)  # Short decay
    
    drums_take = create_midi_item(drums_trk, 0.0, bar_len * 8)
    
    kick_note = 36
    snare_note = 38
    
    for bar in range(8):
        for beat in range(4):
            beat_time = (bar * bar_len) + (beat * beat_len)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time + (beat_len * 0.25))
            
            # Kick on every beat (4-on-the-floor)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, kick_note, 110, False)
            
            # Add Snare on 2 and 4 ONLY during the drop (Bars 5-8)
            if bar >= 4 and (beat == 1 or beat == 3):
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, snare_note, 100, False)


    # === 3. BASS TRACK ===
    bass_trk = add_track(f"{track_name}_Bass", 0.85)
    RPR.RPR_TrackFX_AddByName(bass_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_trk, 0, 1, 0.5) # Triangle/Square blend
    
    # Bass ONLY plays during the drop (Bars 5-8)
    bass_take = create_midi_item(bass_trk, bar_len * 4, bar_len * 4)
    
    bass_octave = 2 * 12
    for bar in range(4, 8):
        degree = prog_degrees[bar % 4]
        root_note = bass_octave + scale_notes[degree % 7] + (12 if degree >= 7 else 0)
        
        # Driving 8th notes
        for eighth in range(8):
            eighth_time = (bar * bar_len) + (eighth * (beat_len / 2))
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, eighth_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, eighth_time + (beat_len / 2.2)) # Slight staccato
            
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, root_note, velocity_base, False)

    # Force MIDI evaluation
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(drums_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_UpdateArrange()

    return f"Created EDM Arrangement over 8 bars at {bpm} BPM in {key} {scale}. (Bars 1-4: Filtered Buildup | Bars 5-8: Drop)"
