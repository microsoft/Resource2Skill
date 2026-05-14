def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "R&B Drill Bass",
    bpm: int = 90,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create an R&B/Neo-Soul bassline using the Octaves & 5ths drill.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
    
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

    # Normalize key and get root MIDI pitch (placed in Octave 2 for bass)
    key_norm = key.capitalize()
    if len(key_norm) > 1 and key_norm[1] == 'B':
        key_norm = key_norm[0] + 'b'
        
    base_note = NOTE_MAP.get(key_norm, 24)
    root_midi = base_note + 12 # Shifts range to C2(36) - B2(47)

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Bassline MIDI ===
    # Calculate diatonic passing tones dynamically based on the scale
    if len(scale_intervals) >= 7:
        pass_idx_1 = 6 # 7th degree
        pass_idx_2 = 5 # 6th degree
    else:
        pass_idx_1 = -1
        pass_idx_2 = -2

    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * 4
        
        # Alternating chord progression: i -> v
        if bar % 2 == 0:
            R = root_midi
            # Passing note to walk down to V
            passing = root_midi + scale_intervals[pass_idx_1] - 12
        else:
            # Find closest interval to a Perfect 5th (+7) for the V chord
            fifth_interval = min(scale_intervals, key=lambda x: abs(x - 7))
            R = root_midi + fifth_interval - 12
            # Passing note to walk back up to i
            passing = root_midi + scale_intervals[pass_idx_2] - 12
            
        # The "Drill" Pattern: (beat_offset, duration_beats, pitch)
        pattern = [
            (0.0, 1.0, R),       # Beat 1: Root (Quarter)
            (1.0, 0.5, R + 7),   # Beat 2: Perfect 5th (Eighth)
            (1.5, 0.5, R + 12),  # Beat 2.5: Octave (Eighth)
            (2.0, 0.5, R + 7),   # Beat 3: Perfect 5th (Eighth)
            (2.5, 0.5, R),       # Beat 3.5: Root (Eighth)
            (3.0, 1.0, passing)  # Beat 4: Passing Note (Quarter)
        ]
        
        for offset, dur, p in pattern:
            start_time = (bar_start_beat + offset) * beat_sec
            
            # Articulation: Long notes are legato, short off-beats are staccato
            gap_factor = 0.95 if dur >= 1.0 else 0.80
            end_time = start_time + (dur * beat_sec) * gap_factor
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Humanize velocity: weaker on the off-beats
            vel = velocity_base
            if offset in [1.5, 2.5]: 
                vel = int(velocity_base * 0.85)
                
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(p), vel, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Sub Bass FX Chain ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.6)  # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)  # Square
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.05) # Saw (just a tiny bit for presence)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Triangle (warmth)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0)  # Extra Sine (deep sub)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.02) # Attack (20ms)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.15) # Release

    return f"Created '{track_name}' with {note_count} bass notes (Octaves/5ths Drill) over {bars} bars at {bpm} BPM in {key} {scale}"
