def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    variation_type: int = 1, # 1 for Complete Change (A-A-B), 2 for Half Change (A-A-A')
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' arrangement structure in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major or minor).
        bars: Total bars (ignored here, strictly mapped to 12 bars to fulfill the 3x4-bar rule).
        velocity_base: Base MIDI velocity (0-127).
        variation_type: 1 for completely different 3rd iteration, 2 for half-changed 3rd iteration.
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    if scale not in SCALES:
        scale = "major"

    # Define the chord progressions based on scale
    if scale == "major":
        prog_A = [1, 5, 6, 4]              # I - V - vi - IV
        prog_B_complete = [6, 4, 1, 5]     # vi - IV - I - V
        prog_B_half = [1, 5, 2, 5]         # I - V - ii - V
    else:
        prog_A = [1, 6, 3, 7]              # i - VI - III - VII
        prog_B_complete = [4, 1, 5, 1]     # iv - i - v - i
        prog_B_half = [1, 6, 2, 5]         # i - VI - ii° - v

    def get_chord_notes(degree, octave=4):
        scale_intervals = SCALES[scale]
        root_midi = NOTE_MAP.get(key, 0)
        notes = []
        
        # 3-note triad in root position
        for i in [0, 2, 4]:
            idx = (degree - 1) + i
            octave_shift = idx // 7
            scale_idx = idx % 7
            note = root_midi + (octave + 1 + octave_shift) * 12 + scale_intervals[scale_idx]
            notes.append(note)
            
        # Bass note (down one octave)
        bass_idx = (degree - 1)
        bass_octave_shift = bass_idx // 7
        bass_scale_idx = bass_idx % 7
        bass_note = root_midi + (octave + bass_octave_shift) * 12 + scale_intervals[bass_scale_idx]
        notes.append(bass_note)
        
        return notes

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # 3 iterations of 4 bars
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    RPR.RPR_MIDI_DisableSort(take)
    
    qn_per_bar = 4
    
    for iteration in range(3):
        # Iteration 0 and 1 are the same (A - A)
        if iteration < 2:
            current_prog = prog_A
        # Iteration 2 is the variation (B or A')
        else:
            current_prog = prog_B_complete if variation_type == 1 else prog_B_half
            
        for i, degree in enumerate(current_prog):
            start_bar = (iteration * 4) + i
            start_qn = start_bar * qn_per_bar
            end_qn = start_qn + qn_per_bar
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            # Get the generated diatonic chord
            notes = get_chord_notes(degree, octave=4)
            for note in notes:
                # Keep notes within safe 0-127 MIDI range
                safe_note = max(0, min(127, note))
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, safe_note, velocity_base, False
                )
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Audition Instrument) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        # Tweak ReaSynth for a soft chord-pad sound
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, -6.0)  # Vol
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)   # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.5)   # Saw mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.5)   # Triangle mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.05)  # Attack (soften transient)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.3)   # Release (fade out gently)

    var_str = "Complete Change" if variation_type == 1 else "Half Change"
    return f"Created '{track_name}' Rule of 3 structure ({total_bars} bars) in {key} {scale} at {bpm} BPM (Variation: {var_str})"

