def create_pattern(
    project_name: str = "OldKanyeBeat",
    track_name: str = "Soul",
    bpm: int = 83,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 'Chipmunk Soul' beat foundation with chopped chords, boom-bap drums, and sub bass.
    """
    import reaper_python as RPR

    # === Music Theory & Logic Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }
    
    root_note = NOTE_MAP.get(key.capitalize(), 0)
    scale_notes = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_notes_from_degree(root_degree, num_notes, octave):
        notes = []
        for i in range(num_notes):
            deg = root_degree + i * 2  # Stack 3rds
            octave_shift = deg // len(scale_notes)
            scale_idx = deg % len(scale_notes)
            note = (octave + octave_shift + 1) * 12 + root_note + scale_notes[scale_idx]
            notes.append(note)
        return notes

    # Rhythm Arrays (2-bar loops)
    # Chord indices: 0 = i9, 1 = iv9, 2 = VImaj7, 3 = v7
    chop_bar0 = [
        {"beat": 0.0, "len": 0.5, "chord_idx": 0},
        {"beat": 0.75, "len": 0.25, "chord_idx": 0},
        {"beat": 1.5, "len": 0.5, "chord_idx": 0},
        {"beat": 2.0, "len": 1.0, "chord_idx": 1},
        {"beat": 3.0, "len": 0.4, "chord_idx": 1},
        {"beat": 3.5, "len": 0.4, "chord_idx": 1},
    ]
    chop_bar1 = [
        {"beat": 0.0, "len": 0.5, "chord_idx": 2},
        {"beat": 0.75, "len": 0.25, "chord_idx": 2},
        {"beat": 1.5, "len": 0.5, "chord_idx": 2},
        {"beat": 2.0, "len": 1.0, "chord_idx": 3},
        {"beat": 3.0, "len": 0.4, "chord_idx": 0},
        {"beat": 3.5, "len": 0.4, "chord_idx": 0},
    ]

    kick_bar0 = [0.0, 1.5, 2.5]
    kick_bar1 = [0.0, 1.5, 2.5, 3.0]
    snare_bar = [1.0, 3.0]
    
    bass_bar0 = [
        {"beat": 0.0, "len": 1.25, "root_idx": 0},
        {"beat": 1.5, "len": 0.4, "root_idx": 0},
        {"beat": 2.0, "len": 1.25, "root_idx": 3},
        {"beat": 3.5, "len": 0.4, "root_idx": 3},
    ]
    bass_bar1 = [
        {"beat": 0.0, "len": 1.25, "root_idx": 5},
        {"beat": 1.5, "len": 0.4, "root_idx": 5},
        {"beat": 2.0, "len": 1.25, "root_idx": 4},
        {"beat": 3.5, "len": 0.4, "root_idx": 0},
    ]

    # === Project & Track Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beat_sec = 60.0 / bpm
    item_length = (beat_sec * 4) * bars
    
    track_count = RPR.RPR_CountTracks(0)
    
    # Track 1: Chops (High Pass Filtered)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    chords_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chops", True)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, eq_idx, 0, 0.3) # Shift band 1 right (acts as HPF)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, eq_idx, 1, 0.0) # Gain to -inf to cut lows
    
    item1 = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", item_length)
    take1 = RPR.RPR_AddTakeToMediaItem(item1)

    # Track 2: Drums
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    drums_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_track, "P_NAME", f"{track_name}_Drums", True)
    item2 = RPR.RPR_AddMediaItemToTrack(drums_track)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", item_length)
    take2 = RPR.RPR_AddTakeToMediaItem(item2)

    # Track 3: Sub Bass
    RPR.RPR_InsertTrackAtIndex(track_count + 2, True)
    bass_track = RPR.RPR_GetTrack(0, track_count + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_Bass", True)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1) # Default sine tone acts as pure sub
    item3 = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(item3, "D_LENGTH", item_length)
    take3 = RPR.RPR_AddTakeToMediaItem(item3)

    # === Note Generation Loop ===
    for bar_idx in range(bars):
        p_idx = bar_idx % 2
        bar_start_sec = (bar_idx * 4.0) * beat_sec
        is_last_bar = (bar_idx == bars - 1)
        
        # 1. Chords
        chops = chop_bar0 if p_idx == 0 else chop_bar1
        if is_last_bar:
            # Kanye-style MPC stutter edit on the final beat
            last_chord = chops[-1]["chord_idx"]
            stutters = [{"beat": 3.0 + (i * 0.25), "len": 0.125, "chord_idx": last_chord} for i in range(4)]
            current_chops = [c for c in chops if c["beat"] < 3.0] + stutters
        else:
            current_chops = chops
            
        for chop in current_chops:
            c_idx = chop["chord_idx"]
            notes = get_notes_from_degree(c_idx, 5 if c_idx in [0, 1] else 4, octave=5) # Octave 5 for chipmunk pitch
            s_time = bar_start_sec + (chop["beat"] * beat_sec)
            e_time = s_time + (chop["len"] * beat_sec)
            s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take1, s_time)
            e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take1, e_time)
            for note in notes:
                RPR.RPR_MIDI_InsertNote(take1, False, False, s_ppq, e_ppq, 0, note, velocity_base, False)

        # 2. Drums
        kicks = kick_bar0 if p_idx == 0 else kick_bar1
        snares = snare_bar
        # Generate swung 8th note hi-hats
        hats = []
        for b in range(4):
            hats.append(float(b))               # On-beat
            hats.append(float(b) + 0.5 + 0.08)  # Off-beat (delayed by 8% for classic swing)
            
        if is_last_bar:
            # Drop drums on the 4th beat to highlight the stutter edit
            kicks = [k for k in kicks if k < 3.0]
            snares = [s for s in snares if s < 3.0]
            hats = [h for h in hats if h < 3.0]

        def insert_drum(beat_list, pitch, dynamic_vel=False):
            for b in beat_list:
                s_time = bar_start_sec + (b * beat_sec)
                e_time = s_time + (0.1 * beat_sec)
                s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take2, s_time)
                e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take2, e_time)
                vel = int(velocity_base * 0.75) if dynamic_vel and b % 1.0 != 0.0 else velocity_base
                RPR.RPR_MIDI_InsertNote(take2, False, False, s_ppq, e_ppq, 0, pitch, vel, False)

        insert_drum(kicks, 36)
        insert_drum(snares, 38)
        insert_drum(hats, 42, dynamic_vel=True)

        # 3. Sub Bass
        bass = bass_bar0 if p_idx == 0 else bass_bar1
        if is_last_bar:
            bass = [b for b in bass if b["beat"] < 3.0]
            
        for b in bass:
            note = get_notes_from_degree(b["root_idx"], 1, octave=1)[0] # Octave 1 for sub
            s_time = bar_start_sec + (b["beat"] * beat_sec)
            e_time = s_time + (b["len"] * beat_sec)
            s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take3, s_time)
            e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take3, e_time)
            RPR.RPR_MIDI_InsertNote(take3, False, False, s_ppq, e_ppq, 0, note, velocity_base, False)

    RPR.RPR_MIDI_Sort(take1)
    RPR.RPR_MIDI_Sort(take2)
    RPR.RPR_MIDI_Sort(take3)

    return f"Created Vintage Soul Beat Foundation: '{track_name}_Chops', '_Drums', and '_Bass' over {bars} bars at {bpm} BPM."
