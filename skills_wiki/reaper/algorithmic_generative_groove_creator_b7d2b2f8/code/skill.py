def create_generative_groove(
    project_name: str = "MyProject",
    track_name: str = "Generative",
    bpm: int = 115,
    key: str = "G",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    bass_density: float = 0.65,
    **kwargs,
) -> str:
    """
    Creates an algorithmic generative drum and bass groove.
    Simulates VST MIDI players by using probability to generate scale-locked MIDI patterns.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        bass_density: Probability (0.0 to 1.0) of a bass note occurring on any given 16th note.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated tracks.
    """
    import reaper_python as RPR
    import random
    
    # Randomize seed so every run generates a unique groove
    random.seed()

    # Music theory lookup tables
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

    if scale not in SCALES:
        scale = "pentatonic_minor"

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    step_length = (60.0 / bpm) * 0.25  # 1/16th note step
    total_steps = bars * 16
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES[scale]

    # ==========================================
    # TRACK 1: Algorithmic Bassline
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)
    
    # Setup placeholder synth (ReaSynth) as a staccato sawtooth pluck
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, 0, 7, 0.8) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, 0, 4, 0.1) # Sustain

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    bass_octave_base = 36 # Start at C2
    notes_generated = 0
    
    for i in range(total_steps):
        if random.random() < bass_density:
            pitch_class = random.choice(scale_intervals)
            # 25% chance to jump up an octave for variation
            octave_shift = random.choice([0, 0, 0, 12]) 
            note_val = bass_octave_base + root_val + pitch_class + octave_shift
            note_val = max(24, min(84, note_val)) # Clamp to safe MIDI bounds
            
            vel = random.randint(80, 120)
            gate = random.uniform(0.4, 0.9) # Randomize note length (staccato to legato)
            
            start_time = i * step_length
            end_time = start_time + (step_length * gate)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, note_val, vel, False)
            notes_generated += 1
            
    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # TRACK 2: Algorithmic Drums (GM MIDI)
    # ==========================================
    drum_idx = track_idx + 1
    RPR.RPR_InsertTrackAtIndex(drum_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums (GM)", True)
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    # Standard GM Drum Mappings
    KICK = 36
    SNARE = 38
    CHH = 42
    OHH = 46
    
    for i in range(total_steps):
        start_time = i * step_length
        end_time = start_time + (step_length * 0.5)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_time)
        
        # Kick generator
        if i % 4 == 0:
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, KICK, 110, False)
        elif random.random() < 0.15: # Syncopated ghost kick
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, KICK, random.randint(60, 90), False)
            
        # Snare generator
        if i % 8 == 4: # Backbeat 
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, SNARE, 110, False)
        elif random.random() < 0.08 and (i % 4 != 0): # Ghost snare offbeat
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, SNARE, random.randint(50, 80), False)
            
        # Hihat generator
        is_open = False
        if i % 4 == 2 and random.random() < 0.4: # Upbeats have a chance to be open
            is_open = True
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, OHH, random.randint(90, 110), False)
            
        if not is_open:
            if i % 2 == 0: # Solid 8th notes
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, CHH, random.randint(80, 105), False)
            elif random.random() < 0.6: # Groovy 16th note offbeats
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, CHH, random.randint(50, 85), False)

    RPR.RPR_MIDI_Sort(drum_take)

    return f"Created Generative Groove: 2 tracks ('{track_name} Bass' and '{track_name} Drums') over {bars} bars at {bpm} BPM. Generated {notes_generated} Bass notes."
