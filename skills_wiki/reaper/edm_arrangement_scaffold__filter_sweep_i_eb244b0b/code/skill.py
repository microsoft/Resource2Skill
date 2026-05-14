def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Arrangement",
    bpm: int = 128,
    key: str = "E",
    scale: str = "minor",
    bars: int = 16,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Arrangement Scaffold (Filter Sweep Intro -> Drop) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Total number of bars (split evenly between Intro and Drop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
    """
    import reaper_python as RPR

    # Enforce minimum length to allow for an Intro and a Drop
    if bars < 4:
        bars = 4
        
    intro_bars = bars // 2
    drop_bars = bars - intro_bars

    # Set project tempo
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0.0, -1, -1, bpm, 4, 4, False)
    RPR.RPR_UpdateTimeline()

    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    # Music theory setup
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

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # Determine progression based on scale flavor
    if "minor" in scale.lower() or "dorian" in scale.lower() or "blues" in scale.lower():
        progression = [0, 5, 2, 6]  # i - VI - III - VII
    else:
        progression = [0, 4, 5, 3]  # I - V - vi - IV

    def get_diatonic_note(degree, octave):
        octave_offset = degree // len(scale_intervals)
        scale_degree = degree % len(scale_intervals)
        return root_pitch + ((octave + octave_offset) * 12) + scale_intervals[scale_degree]

    # Syncopated 3+3+2 rhythm grid: (start_beat, duration_beats)
    rhythm_pattern = [(0.0, 0.75), (0.75, 0.75), (1.5, 0.5), 
                      (2.0, 0.75), (2.75, 0.75), (3.5, 0.5)]

    def insert_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        return trk

    # ==========================================
    # 1. CHORDS TRACK (Plays throughout)
    # ==========================================
    chords_track = insert_track(f"{track_name} Chords")
    fx_chords = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    
    # Buzzy supersaw patch
    RPR.RPR_TrackFX_SetParam(chords_track, fx_chords, 2, 0.05) # Attack
    RPR.RPR_TrackFX_SetParam(chords_track, fx_chords, 5, 0.3)  # Release
    RPR.RPR_TrackFX_SetParam(chords_track, fx_chords, 6, 0.5)  # Square mix
    RPR.RPR_TrackFX_SetParam(chords_track, fx_chords, 7, 0.8)  # Saw mix

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", bars * bar_len)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # Filter Cutoff Automation (Sweep up over Intro)
    env_cutoff = RPR.RPR_GetFXEnvelope(chords_track, fx_chords, 11, True)
    if env_cutoff:
        RPR.RPR_InsertEnvelopePoint(env_cutoff, 0.0, 0.15, 2, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_cutoff, intro_bars * bar_len, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env_cutoff)

    for bar_idx in range(bars):
        deg = progression[bar_idx % 4]
        notes = [get_diatonic_note(deg, 4), get_diatonic_note(deg+2, 4), get_diatonic_note(deg+4, 4)]
        
        for start_b, dur_b in rhythm_pattern:
            proj_start = (bar_idx * 4 + start_b) * beat_len
            proj_end = proj_start + (dur_b * beat_len * 0.85) # Slight staccato gap
            s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, proj_start)
            e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, proj_end)
            for pitch in notes:
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, s_ppq, e_ppq, 0, pitch, min(velocity_base, 127), False)
    RPR.RPR_MIDI_Sort(chords_take)

    # ==========================================
    # 2. BASS TRACK (Enters at Drop)
    # ==========================================
    bass_track = insert_track(f"{track_name} Bass")
    fx_bass = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Plucky sub-bass patch
    RPR.RPR_TrackFX_SetParam(bass_track, fx_bass, 2, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(bass_track, fx_bass, 3, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(bass_track, fx_bass, 4, 0.2)  # Sustain
    RPR.RPR_TrackFX_SetParam(bass_track, fx_bass, 6, 0.6)  # Square
    RPR.RPR_TrackFX_SetParam(bass_track, fx_bass, 7, 0.0)  # Saw
    RPR.RPR_TrackFX_SetParam(bass_track, fx_bass, 8, 1.0)  # Triangle (Sub weight)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", intro_bars * bar_len)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", drop_bars * bar_len)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    for bar_idx in range(intro_bars, bars):
        deg = progression[bar_idx % 4]
        bass_note = get_diatonic_note(deg, 2) # Two octaves lower
        
        for start_b, dur_b in rhythm_pattern:
            proj_start = (bar_idx * 4 + start_b) * beat_len
            proj_end = proj_start + (dur_b * beat_len * 0.8)
            s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, proj_start)
            e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, proj_end)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, s_ppq, e_ppq, 0, bass_note, min(velocity_base + 10, 127), False)
    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # 3. DRUMS TRACK (Enters at Drop)
    # ==========================================
    drums_track = insert_track(f"{track_name} Drums (Add VSTi)")
    
    drums_item = RPR.RPR_AddMediaItemToTrack(drums_track)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_POSITION", intro_bars * bar_len)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_LENGTH", drop_bars * bar_len)
    drums_take = RPR.RPR_AddTakeToMediaItem(drums_item)

    for bar_idx in range(intro_bars, bars):
        for beat in range(4):
            # Kick (36)
            proj_start = (bar_idx * 4 + beat) * beat_len
            s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, proj_start)
            e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, proj_start + beat_len * 0.25)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, s_ppq, e_ppq, 0, 36, min(velocity_base + 15, 127), False)
            
            # Clap (39) on off-beats
            if beat % 2 == 1:
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, s_ppq, e_ppq, 0, 39, min(velocity_base, 127), False)
                
            # Hi-hat (42) on eighth-note off-beats
            hat_start = proj_start + beat_len * 0.5
            h_s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, hat_start)
            h_e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, hat_start + beat_len * 0.25)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, h_s_ppq, h_e_ppq, 0, 42, max(velocity_base - 10, 1), False)
            
    RPR.RPR_MIDI_Sort(drums_take)

    return f"Created EDM Arrangement '{track_name}': {intro_bars} bars Intro (Filter Sweep) -> {drop_bars} bars Drop at {bpm} BPM in {key} {scale}."
