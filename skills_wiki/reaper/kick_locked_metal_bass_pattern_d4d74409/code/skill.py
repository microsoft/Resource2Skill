def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Kick-Locked Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a syncopated, kick-locked metal bass pattern with octave accents.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (110 recommended to avoid virtual bass harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a virtual instrument placeholder for the bass tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Metal bass pattern: syncopated 16th notes with an octave jump accent
    # Tuples: (position_in_quarter_notes, duration_in_quarter_notes, is_octave_jump)
    # The durations are strictly 0.25 (16th notes) to create the staccato, choked feel.
    rhythm_pattern = [
        (0.0,  0.25, False),  # beat 1
        (0.5,  0.25, False),  # beat 1 &
        (1.25, 0.25, False),  # beat 2 e
        (1.75, 0.25, False),  # beat 2 a
        (2.0,  0.25, False),  # beat 3
        (2.5,  0.25, True),   # beat 3 & (octave accent jump)
        (3.0,  0.25, False),  # beat 4
        (3.5,  0.25, False)   # beat 4 &
    ]
    
    # Metal heavily utilizes low tunings (Drop C, Drop A). 
    # MIDI note 24 is C1. We calculate the root from this low octave.
    root_pitch = 24 + NOTE_MAP.get(key, 0)
    
    qn_len_sec = 60.0 / float(bpm)
    note_count = 0
    
    for bar in range(bars):
        bar_start_qn = bar * beats_per_bar
        
        for pos_qn, dur_qn, is_oct in rhythm_pattern:
            note_start_qn = bar_start_qn + pos_qn
            note_end_qn = note_start_qn + dur_qn
            
            # Convert Quarter Notes to seconds, then to PPQ for the MIDI API
            start_time = note_start_qn * qn_len_sec
            end_time = note_end_qn * qn_len_sec
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Apply octave jump (+12 semitones) if flagged in the pattern
            pitch = root_pitch + 12 if is_oct else root_pitch
            
            # Insert note with the carefully selected velocity_base (110)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM."
