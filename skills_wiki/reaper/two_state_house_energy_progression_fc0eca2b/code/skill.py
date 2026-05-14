def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "House_Energy_Prog",
    bpm: int = 124,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Generates 4 bars Low Energy, 4 bars High Energy
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a two-state House music progression demonstrating energy modulation.
    Bars 1-4: Low Energy (Deep sustained pads).
    Bars 5-8: High Energy (Syncopated plucks, drums, and bass).
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
    }

    if scale not in SCALES:
        scale = "minor"
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # Start around C3
    scale_intervals = SCALES[scale]
    
    # Generate 3 octaves of the diatonic scale for safe lookup
    expanded_scale = []
    for oct in range(3):
        for step in scale_intervals:
            expanded_scale.append(root_midi + (oct * 12) + step)

    # 4-bar standard house progression (Scale degrees: i, VI, iv, v or similar)
    progression_degrees = [0, 5, 3, 4] 

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def add_track_with_synth(name, attack, decay, sustain, release, is_drum=False):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        if not is_drum:
            # Add ReaSynth
            fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Param mapping for ReaSynth (approximate index): 2=Attack, 3=Decay, 4=Sustain, 5=Release
            RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, attack)
            RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, decay)
            RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, sustain)
            RPR.RPR_TrackFX_SetParam(track, fx_synth, 5, release)
            
            # Add ReaVerbate
            fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
            RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.5) # Wet
            RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.5) # Dry

        return track

    # Track 1: Low Energy Pads (Bars 1-4)
    pad_track = add_track_with_synth("Low_Energy_Pads", attack=0.3, decay=0.8, sustain=0.8, release=0.6)
    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", (60.0/bpm)*16) # 4 bars
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)

    # Track 2: High Energy Plucks (Bars 5-8)
    pluck_track = add_track_with_synth("High_Energy_Plucks", attack=0.0, decay=0.1, sustain=0.0, release=0.1)
    pluck_item = RPR.RPR_AddMediaItemToTrack(pluck_track)
    RPR.RPR_SetMediaItemInfo_Value(pluck_item, "D_POSITION", (60.0/bpm)*16) # Starts at bar 5
    RPR.RPR_SetMediaItemInfo_Value(pluck_item, "D_LENGTH", (60.0/bpm)*16)
    pluck_take = RPR.RPR_AddTakeToMediaItem(pluck_item)

    # Track 3: House Drums (Bars 5-8)
    drum_track = add_track_with_synth("High_Energy_Drums", 0, 0, 0, 0, is_drum=True)
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", (60.0/bpm)*16)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", (60.0/bpm)*16)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    notes_created = 0

    # Generate the Chords
    for bar in range(4):
        degree = progression_degrees[bar]
        
        # Diatonic interval math (Root + 3rd)
        root_note = expanded_scale[degree]
        third_note = expanded_scale[degree + 2] # Diatonic third
        
        # --- LOW ENERGY: Sustained Whole Notes ---
        start_qn = bar * 4.0
        end_qn = start_qn + 4.0
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(pad_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(pad_take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(pad_take, False, False, start_ppq, end_ppq, 0, root_note, velocity_base - 20, False)
        RPR.RPR_MIDI_InsertNote(pad_take, False, False, start_ppq, end_ppq, 0, third_note, velocity_base - 20, False)
        notes_created += 2

        # --- HIGH ENERGY: Syncopated Plucks (+1 Octave) ---
        base_qn = 16.0 + (bar * 4.0) # Start at bar 5
        # Syncopated rhythm offsets (dotted 8ths and passing 16ths)
        rhythm_qn_offsets = [0.0, 0.75, 1.5, 2.0, 2.75, 3.5]
        
        for offset in rhythm_qn_offsets:
            p_start_qn = base_qn + offset
            p_end_qn = p_start_qn + 0.25 # Staccato
            p_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(pluck_take, p_start_qn)
            p_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(pluck_take, p_end_qn)
            
            # +12 for higher octave energy
            RPR.RPR_MIDI_InsertNote(pluck_take, False, False, p_start_ppq, p_end_ppq, 0, root_note + 12, velocity_base, False)
            RPR.RPR_MIDI_InsertNote(pluck_take, False, False, p_start_ppq, p_end_ppq, 0, third_note + 12, velocity_base, False)
            notes_created += 2

        # --- DRUMS: 4 on the floor ---
        for beat in range(4):
            # Kick (36)
            k_start_qn = base_qn + beat
            k_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, k_start_qn)
            k_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, k_start_qn + 0.25)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, k_start_ppq, k_end_ppq, 9, 36, 110, False)
            
            # Off-beat Open Hat (46)
            h_start_qn = base_qn + beat + 0.5
            h_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, h_start_qn)
            h_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, h_start_qn + 0.25)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, h_start_ppq, h_end_ppq, 9, 46, 90, False)
            
            # Clap on 2 and 4 (beats 1 and 3 in 0-index)
            if beat % 2 == 1:
                c_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, k_start_qn)
                c_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, k_start_qn + 0.25)
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, c_start_ppq, c_end_ppq, 9, 39, 100, False)

    RPR.RPR_MIDI_Sort(pad_take)
    RPR.RPR_MIDI_Sort(pluck_take)
    RPR.RPR_MIDI_Sort(drum_take)

    return f"Created Two-State House Progression ({notes_created} total chord notes) transitioning at Bar 5. Tempo: {bpm} BPM, Key: {key} {scale}."
