def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Deep House Groove",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Generative Deep House Groove (Drums + Sub Bass) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for primary hits (0-127).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    note_count = 0
    track_count = RPR.RPR_CountTracks(0)

    # === Step 2: Create Drum Track & FX ===
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    drum_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    # Add Big Hall Reverb Simulation
    drum_fx = RPR.RPR_TrackFX_AddByName(drum_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_fx, 0, 0.35) # Wet slightly elevated
    RPR.RPR_TrackFX_SetParamNormalized(drum_track, drum_fx, 2, 0.85) # Large Room Size
    
    # === Step 3: Insert Drum Notes (16th Note Grid) ===
    DRUM_MAP = {"Kick": 36, "Snare": 38, "Clap": 39, "ClosedHat": 42, "OpenHat": 46}
    drum_pattern = [
        {"name": "Kick", "pos": 0.0, "dur": 0.25, "vel": velocity_base},
        {"name": "Kick", "pos": 1.0, "dur": 0.25, "vel": velocity_base},
        {"name": "Kick", "pos": 2.0, "dur": 0.25, "vel": velocity_base},
        {"name": "Kick", "pos": 3.0, "dur": 0.25, "vel": velocity_base},
        {"name": "Clap", "pos": 1.0, "dur": 0.25, "vel": int(velocity_base * 0.9)},
        {"name": "Clap", "pos": 3.0, "dur": 0.25, "vel": int(velocity_base * 0.9)},
        {"name": "OpenHat", "pos": 0.5, "dur": 0.25, "vel": int(velocity_base * 0.85)},
        {"name": "OpenHat", "pos": 1.5, "dur": 0.25, "vel": int(velocity_base * 0.85)},
        {"name": "OpenHat", "pos": 2.5, "dur": 0.25, "vel": int(velocity_base * 0.85)},
        {"name": "OpenHat", "pos": 3.5, "dur": 0.25, "vel": int(velocity_base * 0.85)},
        # Syncopated ghost notes
        {"name": "ClosedHat", "pos": 0.75, "dur": 0.125, "vel": int(velocity_base * 0.6)},
        {"name": "ClosedHat", "pos": 1.75, "dur": 0.125, "vel": int(velocity_base * 0.6)},
        {"name": "ClosedHat", "pos": 2.25, "dur": 0.125, "vel": int(velocity_base * 0.5)},
        {"name": "ClosedHat", "pos": 3.75, "dur": 0.125, "vel": int(velocity_base * 0.6)},
    ]
    
    for bar in range(bars):
        bar_offset_qn = bar * beats_per_bar
        for note in drum_pattern:
            start_qn = bar_offset_qn + note["pos"]
            end_qn = start_qn + note["dur"]
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(drum_take, end_qn)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, DRUM_MAP[note["name"]], note["vel"], False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(drum_take)
    
    # === Step 4: Create Sub Bass Track & FX ===
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Sub Bass", True)
    
    # Add ReaSynth configured as a pure Sine Sub Bass
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, bass_fx, 6, 0.0) # Square Mix: 0%
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, bass_fx, 7, 0.0) # Saw Mix: 0%
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, bass_fx, 8, 0.0) # Triangle Mix: 0%
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, bass_fx, 9, 1.0) # Extra Sine Mix: 100%
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # === Step 5: Insert Syncopated Bass Notes ===
    # Using scale degrees (0 = root)
    bass_pattern = [
        {"deg": 0, "pos": 0.5, "dur": 0.25},   # off-beat 1
        {"deg": 2, "pos": 1.75, "dur": 0.25},  # syncopated 16th before beat 3
        {"deg": 0, "pos": 2.5, "dur": 0.25},   # off-beat 3
        {"deg": -1, "pos": 3.5, "dur": 0.25},  # drop to 7th on off-beat 4
    ]
    
    def get_pitch(degree, octave=2):
        root_midi = NOTE_MAP.get(key, 0) + (octave * 12)
        intervals = SCALES.get(scale, SCALES["minor"])
        octave_shift = degree // len(intervals)
        idx = degree % len(intervals)
        return root_midi + (octave_shift * 12) + intervals[idx]
        
    for bar in range(bars):
        bar_offset_qn = bar * beats_per_bar
        for note in bass_pattern:
            start_qn = bar_offset_qn + note["pos"]
            end_qn = start_qn + note["dur"]
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(bass_take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(bass_take, end_qn)
            pitch = get_pitch(note["deg"], octave=2)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base * 0.95), False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_UpdateArrange()

    return f"Created {track_name} (Drums & Bass) with {note_count} total notes over {bars} bars at {bpm} BPM in {key} {scale}."
