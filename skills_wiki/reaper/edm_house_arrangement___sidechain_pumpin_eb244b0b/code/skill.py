def create_pattern(
    project_name: str = "EDM_House_Arrangement",
    track_name: str = "House",
    bpm: int = 125,
    key: str = "G",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM House arrangement featuring an Intro and a Drop with a sidechain pumping effect.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    if scale not in SCALES:
        scale = "minor"
    
    # Structural math
    intro_bars = bars // 2
    drop_bars = bars - intro_bars
    beats_per_bar = 4
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Helper: Build chords
    def get_chord_notes(degree, octave, num_notes=4):
        scale_idx = degree - 1
        notes = []
        for i in range(num_notes):
            curr_idx = scale_idx + (i * 2)
            oct_shift = curr_idx // 7
            note_in_scale = curr_idx % 7
            pitch = (octave + oct_shift) * 12 + SCALES[scale][note_in_scale] + NOTE_MAP[key]
            notes.append(min(127, max(0, pitch)))
        return notes

    # Helper: Create MIDI item
    def create_midi_item(track, start_qn, len_qn):
        t_start = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        t_end = RPR.RPR_TimeMap2_QNToTime(0, start_qn + len_qn)
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", t_start)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", t_end - t_start)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take, start_qn

    # Helper: Insert note by QN
    def insert_note_qn(take, item_start_qn, qn_pos, qn_len, pitch, vel):
        t_start = RPR.RPR_TimeMap2_QNToTime(0, item_start_qn + qn_pos)
        t_end = RPR.RPR_TimeMap2_QNToTime(0, item_start_qn + qn_pos + qn_len)
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_end)
        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, pitch, vel, False)

    # === TRACK 1: CHORDS ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_trk = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_trk, "P_NAME", f"{track_name}_Chords", True)
    
    fx_idx = RPR.RPR_TrackFX_AddByName(chords_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_trk, fx_idx, 1, 0.8) # Sawtooth
    RPR.RPR_TrackFX_SetParam(chords_trk, fx_idx, 4, 0.1) # Attack
    RPR.RPR_TrackFX_SetParam(chords_trk, fx_idx, 7, 0.5) # Release

    # === TRACK 2: BASS ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_trk = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_trk, "P_NAME", f"{track_name}_Bass", True)
    
    fx_idx2 = RPR.RPR_TrackFX_AddByName(bass_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_trk, fx_idx2, 1, 0.0) # Sawtooth down
    RPR.RPR_TrackFX_SetParam(bass_trk, fx_idx2, 2, 1.0) # Square up (Plucky bass)
    RPR.RPR_TrackFX_SetParam(bass_trk, fx_idx2, 5, 0.1) # Fast Decay
    RPR.RPR_TrackFX_SetParam(bass_trk, fx_idx2, 6, 0.1) # Low Sustain

    # === TRACK 3: DRUMS ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    drums_trk = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_trk, "P_NAME", f"{track_name}_Drums", True)

    # Rhythm pattern: start pos, length
    house_rhythm = [(0, 1.25), (1.5, 0.5), (2.5, 0.5), (3.5, 0.5)]
    progression = [1, 5, 6, 7] # i - v - VI - VII
    
    # 1. INTRO SECTION (Chords only, quiet)
    chords_intro_take, c_i_start = create_midi_item(chords_trk, 0, intro_bars * beats_per_bar)
    for bar in range(intro_bars):
        degree = progression[bar % len(progression)]
        notes = get_chord_notes(degree, octave=4, num_notes=4)
        for r_pos, r_len in house_rhythm:
            for n in notes:
                insert_note_qn(chords_intro_take, c_i_start, (bar * beats_per_bar) + r_pos, r_len, n, int(velocity_base * 0.7))

    # 2. DROP SECTION (Chords, Bass, Drums)
    drop_start_qn = intro_bars * beats_per_bar
    chords_drop_take, c_d_start = create_midi_item(chords_trk, drop_start_qn, drop_bars * beats_per_bar)
    bass_drop_take, b_d_start = create_midi_item(bass_trk, drop_start_qn, drop_bars * beats_per_bar)
    drums_drop_take, d_d_start = create_midi_item(drums_trk, drop_start_qn, drop_bars * beats_per_bar)

    for bar in range(drop_bars):
        qn_offset = bar * beats_per_bar
        degree = progression[bar % len(progression)]
        
        # Chords & Bass
        chord_notes = get_chord_notes(degree, octave=4, num_notes=4)
        bass_note = get_chord_notes(degree, octave=2, num_notes=1)[0]
        
        for r_pos, r_len in house_rhythm:
            # Drop chords are full velocity
            for n in chord_notes:
                insert_note_qn(chords_drop_take, c_d_start, qn_offset + r_pos, r_len, n, velocity_base)
            # Bass plays the root on the same syncopated rhythm
            insert_note_qn(bass_drop_take, b_d_start, qn_offset + r_pos, r_len, bass_note, velocity_base)

        # Drums (4 on the floor + offbeat hats)
        for beat in range(beats_per_bar):
            insert_note_qn(drums_drop_take, d_d_start, qn_offset + beat, 0.25, 36, 110) # Kick
            insert_note_qn(drums_drop_take, d_d_start, qn_offset + beat + 0.5, 0.25, 42, 90) # Hat

    # === VOLUME ENVELOPE (SIDECHAIN PUMPING EFFECT) ===
    # We automate the volume of the chords track during the drop to simulate sidechain
    RPR.RPR_SetOnlyTrackSelected(chords_trk)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env = RPR.RPR_GetTrackEnvelopeByName(chords_trk, "Volume")
    
    if env:
        # Pre-drop normal volume
        t_pre = RPR.RPR_TimeMap2_QNToTime(0, drop_start_qn - 0.1)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, t_pre, 1.0, 0, 0, False, True)
        
        # Pump on every quarter note during the drop
        for qn in range(drop_start_qn, drop_start_qn + (drop_bars * beats_per_bar)):
            t_beat = RPR.RPR_TimeMap2_QNToTime(0, qn)
            t_rise = RPR.RPR_TimeMap2_QNToTime(0, qn + 0.3) 
            t_end = RPR.RPR_TimeMap2_QNToTime(0, qn + 0.95)
            
            # Value 0.15 simulates a deep -16dB duck, 1.0 is unity (0dB)
            RPR.RPR_InsertEnvelopePoint(env, t_beat, 0.15, 5, 0.5, False, True) # Drop fast, Bezier curve up
            RPR.RPR_InsertEnvelopePoint(env, t_rise, 1.0, 0, 0, False, True)    # Recovered
            RPR.RPR_InsertEnvelopePoint(env, t_end, 1.0, 0, 0, False, True)     # Hold until next kick
            
        RPR.RPR_Envelope_Sort(env)

    return f"Created House arrangement: {intro_bars} bars Intro, {drop_bars} bars Drop at {bpm} BPM with sidechain volume pumping."
