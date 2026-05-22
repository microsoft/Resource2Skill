def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scaffold",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a basic Generative Drum & Bass scaffold in the current REAPER project.
    Acts as a REAPER-native placeholder for third-party tools like Beat Map and Bass Master.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks (appends '_Bass' and '_Drums').
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the tracks created.
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # ==========================================
    # 1. Create Bass Track (Replacing Bass Master)
    # ==========================================
    track_idx_bass = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_bass, True)
    track_bass = RPR.RPR_GetTrack(0, track_idx_bass)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name}_Bass", True)

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", item_length)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)

    # Calculate Bass Notes
    root_note = 36 + NOTE_MAP.get(key.capitalize(), 0) # Octave 2
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    note_3rd = root_note + scale_intervals[2]
    note_5th = root_note + scale_intervals[4]

    # Insert syncopated Bass line
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Define rhythm: beat positions and corresponding pitches
        bass_hits = [
            (0.0, root_note, velocity_base),
            (0.75, note_3rd, max(1, velocity_base - 15)),
            (1.5, root_note, max(1, velocity_base - 5)),
            (2.5, note_5th, velocity_base),
        ]
        
        for beat_offset, pitch, vel in bass_hits:
            pos_beat = bar_start_beat + beat_offset
            start_time = RPR.RPR_TimeMap2_beatsToTime(0, pos_beat, 0)[0]
            end_time = RPR.RPR_TimeMap2_beatsToTime(0, pos_beat + 0.25, 0)[0]
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, end_time)
            
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    RPR.RPR_MIDI_Sort(take_bass)

    # Add ReaSynth for Bass tone
    fx_idx = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx, 0, 0.5)   # Volume
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx, 2, 0.02)  # Attack
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx, 3, 0.3)   # Decay
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx, 4, 0.2)   # Sustain
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx, 6, 0.8)   # Square mix
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx, 7, 0.4)   # Saw mix

    # ==========================================
    # 2. Create Drum Track (Replacing Beat Map)
    # ==========================================
    track_idx_drums = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_drums, True)
    track_drums = RPR.RPR_GetTrack(0, track_idx_drums)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", f"{track_name}_Drums", True)

    item_drums = RPR.RPR_AddMediaItemToTrack(track_drums)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_LENGTH", item_length)
    take_drums = RPR.RPR_AddTakeToMediaItem(item_drums)

    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Kicks on 1, 2, 3, 4 (MIDI 36)
        for beat in range(4):
            start_time = RPR.RPR_TimeMap2_beatsToTime(0, bar_start_beat + beat, 0)[0]
            end_time = RPR.RPR_TimeMap2_beatsToTime(0, bar_start_beat + beat + 0.25, 0)[0]
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, end_time)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, 36, velocity_base, False)
            
        # Snares on 2, 4 (MIDI 38)
        for beat in [1, 3]:
            start_time = RPR.RPR_TimeMap2_beatsToTime(0, bar_start_beat + beat, 0)[0]
            end_time = RPR.RPR_TimeMap2_beatsToTime(0, bar_start_beat + beat + 0.25, 0)[0]
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, end_time)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, 38, velocity_base, False)

    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created placeholder Bass & Drum tracks over {bars} bars at {bpm} BPM in {key} {scale}."
