def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Arrangement Scaffold (Intro, Build, Drop) in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Length of EACH arrangement section (Intro, Build, Drop). Total length = bars * 3.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    scale_degrees = SCALES.get(scale, SCALES["minor"])
    base_pitch = 48 + NOTE_MAP.get(key, 0) # Start around C3
    
    # Diatonic progression setup
    progression = [3, 5, 4, 0] if scale == "major" else [0, 5, 2, 6]
    
    def get_triad(degrees, root_index):
        n1 = degrees[root_index % 7] + 12 * (root_index // 7)
        n2 = degrees[(root_index + 2) % 7] + 12 * ((root_index + 2) // 7)
        n3 = degrees[(root_index + 4) % 7] + 12 * ((root_index + 4) // 7)
        return [n1, n2, n3]

    # === Step 1: Initialization & Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_duration = 60.0 / bpm
    bar_duration = beat_duration * 4
    section_bars = bars
    
    intro_start = 0.0
    build_start = section_bars * bar_duration
    drop_start = build_start * 2
    outro_end = drop_start + section_bars * bar_duration

    # Track creation helper
    def create_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        return tr

    kick_track = create_track(f"{track_name} Kick")
    snare_track = create_track(f"{track_name} Build Snare")
    chords_track = create_track(f"{track_name} Chords")
    bass_track = create_track(f"{track_name} Bass")

    # MIDI item helper
    def create_midi_item_and_take(tr, start_time, duration):
        item = RPR.RPR_AddMediaItemToTrack(tr)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration)
        tk = RPR.RPR_AddTakeToMediaItem(item)
        return item, tk

    def insert_midi_note(tk, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(tk, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(tk, end_sec)
        RPR.RPR_MIDI_InsertNote(tk, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 2: Kick Track (Drop Only) ===
    kick_fx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, kick_fx, 7, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParamNormalized(kick_track, kick_fx, 8, 0.2)  # Decay
    
    kick_item, kick_take = create_midi_item_and_take(kick_track, drop_start, section_bars * bar_duration)
    for beat in range(section_bars * 4):
        b_time = drop_start + beat * beat_duration
        insert_midi_note(kick_take, b_time, b_time + beat_duration * 0.5, 36, velocity_base + 10)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 3: Snare Track (Build Only) ===
    snare_fx = RPR.RPR_TrackFX_AddByName(snare_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(snare_track, snare_fx, 2, 1.0) # Square wave
    RPR.RPR_TrackFX_SetParamNormalized(snare_track, snare_fx, 8, 0.1) # Short decay
    
    snare_item, snare_take = create_midi_item_and_take(snare_track, build_start, section_bars * bar_duration)
    for beat in range(section_bars * 4):
        bars_from_end = section_bars - (beat // 4)
        b_time = build_start + beat * beat_duration
        
        if bars_from_end >= 3:
            insert_midi_note(snare_take, b_time, b_time + 0.1, 60, velocity_base - 10)
        elif bars_from_end == 2:
            insert_midi_note(snare_take, b_time, b_time + 0.1, 60, velocity_base)
            insert_midi_note(snare_take, b_time + 0.5 * beat_duration, b_time + 0.5 * beat_duration + 0.1, 60, velocity_base)
        else:
            for i in range(4):
                frac = i * 0.25
                v = velocity_base + (i * 5) if bars_from_end == 1 else velocity_base # Crescendo
                insert_midi_note(snare_take, b_time + frac * beat_duration, b_time + frac * beat_duration + 0.05, 60 + (i if bars_from_end==1 else 0), min(127, v))
    RPR.RPR_MIDI_Sort(snare_take)

    # === Step 4: Chords Track (All Sections) ===
    chords_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, chords_fx, 3, 1.0) # Saw wave
    
    # EQ Filter Sweep setup (Automating High Shelf Gain to act as a Low Pass)
    eq_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    env_eq = RPR.RPR_GetFXEnvelope(chords_track, eq_fx, 10, True) # Param 10 = Band 4 Gain
    RPR.RPR_InsertEnvelopePoint(env_eq, intro_start, 0.0, 0, 0, False, True) # Muffled intro
    RPR.RPR_InsertEnvelopePoint(env_eq, build_start, 0.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_eq, drop_start, 0.5, 0, 0, False, True)  # Open drop (0.5 is 0dB)
    RPR.RPR_Envelope_SortPoints(env_eq)

    def generate_chords_for_take(tk, offset, num_bars):
        for bar in range(num_bars):
            root_idx = progression[bar % len(progression)]
            pitches = get_triad(scale_degrees, root_idx)
            # Syncopated rhythm offsets in beats
            rhythm = [ (0.0, 1.0), (1.5, 1.0), (3.0, 1.0) ]
            for r_start, r_len in rhythm:
                n_start = offset + bar * bar_duration + r_start * beat_duration
                n_end = n_start + r_len * beat_duration
                for p in pitches:
                    insert_midi_note(tk, n_start, n_end, p + base_pitch, velocity_base)

    for offset in [intro_start, build_start, drop_start]:
        item, tk = create_midi_item_and_take(chords_track, offset, section_bars * bar_duration)
        generate_chords_for_take(tk, offset, section_bars)
        RPR.RPR_MIDI_Sort(tk)

    # === Step 5: Bass Track (Drop Only) ===
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, bass_fx, 2, 0.5) # Square
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, bass_fx, 3, 0.5) # Saw
    
    bass_item, bass_take = create_midi_item_and_take(bass_track, drop_start, section_bars * bar_duration)
    for bar in range(section_bars):
        root_idx = progression[bar % len(progression)]
        root_pitch = scale_degrees[root_idx % 7] + 12 * (root_idx // 7) + base_pitch - 24 # 2 octaves down
        
        rhythm = [ (0.0, 1.0), (1.5, 1.0), (3.0, 1.0) ]
        for r_start, r_len in rhythm:
            n_start = drop_start + bar * bar_duration + r_start * beat_duration
            insert_midi_note(bass_take, n_start, n_start + r_len * beat_duration, root_pitch, velocity_base + 10)
    RPR.RPR_MIDI_Sort(bass_take)

    # === Step 6: Volume Sidechain Pumping Automation (Drop Only) ===
    def add_sidechain_pump(tr, start_time, duration):
        env = RPR.RPR_GetTrackEnvelopeByName(tr, "Volume")
        if not env:
            RPR.RPR_SetOnlyTrackSelected(tr)
            RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
            env = RPR.RPR_GetTrackEnvelopeByName(tr, "Volume")
            
        if env:
            RPR.RPR_InsertEnvelopePoint(env, start_time - 0.1, 1.0, 0, 0, False, True)
            beats = int(duration / beat_duration)
            for i in range(beats):
                b_time = start_time + i * beat_duration
                RPR.RPR_InsertEnvelopePoint(env, b_time, 0.2, 0, 0, False, True) # Duck
                RPR.RPR_InsertEnvelopePoint(env, b_time + (beat_duration * 0.35), 1.0, 0, 0, False, True) # Recover
                RPR.RPR_InsertEnvelopePoint(env, b_time + beat_duration - 0.01, 1.0, 0, 0, False, True) # Hold
            RPR.RPR_Envelope_SortPoints(env)

    add_sidechain_pump(chords_track, drop_start, section_bars * bar_duration)
    add_sidechain_pump(bass_track, drop_start, section_bars * bar_duration)

    return f"Created EDM Arrangement Scaffold: {bars*3} total bars at {bpm} BPM with Filter Sweep and Sidechain Pumping."
