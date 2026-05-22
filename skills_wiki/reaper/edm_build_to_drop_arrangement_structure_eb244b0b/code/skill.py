def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Build-to-Drop Arrangement in the current REAPER project.
    Generates 8 bars total: 4 bars of tension building, 4 bars of a full drop.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM (120-130 recommended for EDM).
        key: Root note (e.g., "C").
        scale: Scale type (e.g., "minor").
        bars: Total length (fixed to 8 for this structural pattern).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Setup Tempo & Musical Math ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # C3
    
    # Classic EDM Minor Progression: i - VI - III - VII
    # Defined via absolute semitone offsets from the root to ensure tight voice leading
    chords = [
        [0, 3, 7],      # i   (e.g., C, Eb, G)
        [-4, 0, 3],     # VI  (e.g., Ab, C, Eb - shifted down)
        [3, 7, 10],     # III (e.g., Eb, G, Bb)
        [-2, 2, 5]      # VII (e.g., Bb, D, F - shifted down)
    ]
    roots = [0, -4, 3, -2] # Root notes for the bassline

    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    # === Step 2: TRACK 1 - CHORDS (Plays through Intro and Drop) ===
    idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx, True)
    tr_chords = RPR.RPR_GetTrack(0, idx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_chords, "P_NAME", "Synth Chords", True)
    RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_SetMediaTrackInfo_Value(tr_chords, "D_VOL", 0.6) # Leave headroom

    item_chords = RPR.RPR_AddMediaItemToTrack(tr_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bar_len * 8)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    for bar in range(8):
        chord = chords[bar % 4]
        bar_start = bar * bar_len
        
        # Tension Build logic: accelerate rhythm subdivisions
        if bar < 4:
            if bar == 0: divs = 1     # Whole note
            elif bar == 1: divs = 2   # Half notes
            elif bar == 2: divs = 4   # Quarter notes
            else: divs = 8            # 8th notes
        else:
            divs = 1 # Drop logic: return to sustained chords

        note_len = bar_len / divs
        for d in range(divs):
            start_time = bar_start + (d * note_len)
            end_time = start_time + (note_len * 0.95) # Slight legato
            
            start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_chords, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_chords, end_qn)
            
            # Swell velocity up during the build
            vel = int(velocity_base * (0.6 + 0.4 * (bar/4.0))) if bar < 4 else velocity_base
            
            for semitone in chord:
                pitch = root_midi + semitone
                RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
                
    RPR.RPR_MIDI_Sort(take_chords)

    # === Step 3: TRACK 2 - BASS (Drop only, Bars 5-8) ===
    idx += 1
    RPR.RPR_InsertTrackAtIndex(idx, True)
    tr_bass = RPR.RPR_GetTrack(0, idx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_bass, "P_NAME", "Drop Bass", True)
    
    # Plucky synth settings
    RPR.RPR_TrackFX_AddByName(tr_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_bass, 0, 1, 0.0) # Mix Sawtooth
    RPR.RPR_TrackFX_SetParamNormalized(tr_bass, 0, 2, 0.1) # Pulse width
    
    item_bass = RPR.RPR_AddMediaItemToTrack(tr_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", bar_len * 4) # Starts at Drop
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", bar_len * 4)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)

    # Syncopated off-beat pattern
    for bar in range(4):
        root = roots[bar % 4]
        pitch = root_midi + root - 12 # Drop down an octave
        bar_start = (bar + 4) * bar_len
        
        for beat in range(4):
            # Place note exactly halfway through the beat (8th note off-beat)
            start_time = bar_start + (beat * beat_len) + (beat_len / 2.0)
            end_time = start_time + (beat_len / 2.0) * 0.8
            
            start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_bass, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_bass, end_qn)
            
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take_bass)

    # === Step 4: TRACK 3 - KICK (Drop only, Bars 5-8) ===
    idx += 1
    RPR.RPR_InsertTrackAtIndex(idx, True)
    tr_kick = RPR.RPR_GetTrack(0, idx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_kick, "P_NAME", "Drop Kick", True)
    
    # Synthesize a tight kick drum using ReaSynth
    RPR.RPR_TrackFX_AddByName(tr_kick, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_kick, 0, 0, 0.9) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(tr_kick, 0, 4, 0.0) # Fast Attack
    RPR.RPR_TrackFX_SetParamNormalized(tr_kick, 0, 5, 0.1) # Fast Decay
    RPR.RPR_TrackFX_SetParamNormalized(tr_kick, 0, 6, 0.0) # No Sustain
    
    item_kick = RPR.RPR_AddMediaItemToTrack(tr_kick)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_POSITION", bar_len * 4) # Starts at Drop
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_LENGTH", bar_len * 4)
    take_kick = RPR.RPR_AddTakeToMediaItem(item_kick)

    # 4-on-the-floor pattern
    for bar in range(4):
        bar_start = (bar + 4) * bar_len
        for beat in range(4):
            start_time = bar_start + (beat * beat_len)
            end_time = start_time + 0.15 # Short trigger
            
            start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_kick, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_kick, end_qn)
            
            # Low pitch (C1)
            RPR.RPR_MIDI_InsertNote(take_kick, False, False, start_ppq, end_ppq, 0, 36, 127, False)

    RPR.RPR_MIDI_Sort(take_kick)

    return f"Created EDM Build-to-Drop arrangement ({bars} bars) at {bpm} BPM in {key} {scale}"
