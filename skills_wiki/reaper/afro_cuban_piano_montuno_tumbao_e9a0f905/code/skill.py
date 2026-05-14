def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "AfroCuban_Piano",
    bpm: int = 150,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Afro-Cuban Piano Montuno and Tumbao pattern in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type ('major' or 'minor').
        bars: Number of bars to generate (should be even for Clave phrasing).
        velocity_base: Base MIDI velocity (0-127).
    
    Returns:
        Status string detailing the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define generic I-IV-V-I progression based on scale
    if scale.lower() == "minor":
        # offsets in semitones, is_major boolean
        # i (min), iv (min), V (maj - harmonic minor), i (min)
        progression = [(0, False), (5, False), (7, True), (0, False)] 
    else:
        # I (maj), IV (maj), V (maj), I (maj)
        progression = [(0, True), (5, True), (7, True), (0, True)]

    # Setup tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Create MIDI Item
    beats_per_bar = 4.0
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    base_root = 48 + NOTE_MAP.get(key.capitalize(), 0) # e.g., C3
    total_notes_added = 0

    # Generate MIDI for each bar
    for bar in range(bars):
        bar_start_qn = bar * beats_per_bar
        
        current_chord = progression[bar % len(progression)]
        next_chord = progression[(bar + 1) % len(progression)]
        
        c_root = base_root + current_chord[0]
        c_third = c_root + (4 if current_chord[1] else 3)
        c_fifth = c_root + 7
        
        n_root = base_root + next_chord[0]

        # -------------------------------------------------------------
        # RIGHT HAND: MONTUNO (2-Bar Pattern)
        # Emphasizing outer root octaves and inner 3rd/5th notes
        # -------------------------------------------------------------
        outer_notes = [c_root + 12, c_root + 24] # e.g., C4, C5
        inner_notes = [c_third + 12, c_fifth + 12] # e.g., E4, G4
        
        # 2-3 Clave Montuno Rhythm phrasing
        if bar % 2 == 0:
            # Bar 1: Hits on beats 1, 2&, 3&, 4&
            montuno_rhythm = [
                (0.0, outer_notes), 
                (1.5, inner_notes), 
                (2.5, outer_notes), 
                (3.5, inner_notes)
            ]
        else:
            # Bar 2: Hits on beats 1&, 2&, 3&, 4&
            montuno_rhythm = [
                (0.5, outer_notes), 
                (1.5, inner_notes), 
                (2.5, outer_notes), 
                (3.5, inner_notes)
            ]

        for beat, notes in montuno_rhythm:
            start_qn = bar_start_qn + beat
            end_qn = start_qn + 0.4 # Staccato/percussive length
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            for pitch in notes:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
                total_notes_added += 1

        # -------------------------------------------------------------
        # LEFT HAND: TUMBAO
        # Bass plays 1, 2&, and strongly anticipates the next chord on 4
        # -------------------------------------------------------------
        tumbao_rhythm = [
            (0.0, [c_root - 12], 1.0), # Beat 1 (Root)
            (1.5, [c_fifth - 12], 1.0), # Beat 2& (Fifth)
            (3.0, [n_root - 12], 1.0)   # Beat 4 (Anticipated Next Root)
        ]

        for beat, notes, dur in tumbao_rhythm:
            start_qn = bar_start_qn + beat
            end_qn = start_qn + dur
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            for pitch in notes:
                # Add a slight velocity accent to the anticipated beat 4 push
                vel = velocity_base + 12 if beat == 3.0 else velocity_base
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), min(127, vel), False)
                total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # Setup ReaSynth to emulate a plucky Electric Piano / Montuno keys sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    if fx_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)  # Attack (instant)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.3)  # Decay (short)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)  # Sustain (none)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1)  # Release (quick)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)  # Square mix 
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.7)  # Saw mix (bit of bite)

    return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}."
