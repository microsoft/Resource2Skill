def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Syncopated 5ths Bass",
    bpm: int = 95,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create 'Syncopated 5ths & Octaves Bassline' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    scale_degrees = SCALES.get(scale, SCALES["minor"])
    # Base octave 1 (MIDI note 24 is C1) for deep bass
    root_pitch = NOTE_MAP.get(key, 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    notes_added = 0

    def add_midi_note(pitch: int, start_beat: float, duration_beats: float, vel: int):
        nonlocal notes_added
        # REAPER default PPQ is 960 per quarter note
        start_ppq = start_beat * 960
        end_ppq = (start_beat + duration_beats) * 960
        # Ensure pitch bounds
        pitch = max(0, min(127, pitch))
        vel = max(1, min(127, vel))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                start_ppq, end_ppq, 
                                0, pitch, vel, False)
        notes_added += 1

    # Determine 3rd for passing notes (major or minor)
    is_minor = "minor" in scale or scale == "dorian"
    third_offset = 3 if is_minor else 4

    # === Step 4: Generate Rhythmic 5ths & Octaves ===
    for b in range(bars):
        # Alternate between the I chord and the IV chord (4th scale degree)
        if b % 2 == 0:
            base_pitch = root_pitch
        else:
            base_pitch = root_pitch + scale_degrees[3 % len(scale_degrees)]
            
        start_qn = b * 4.0
        
        # Beat 1.0: Downbeat Root (Long)
        add_midi_note(base_pitch, start_qn + 0.0, 0.75, velocity_base)
        
        # Beat 2.5: Octave jump (Syncopated)
        add_midi_note(base_pitch + 12, start_qn + 1.5, 0.5, int(velocity_base * 0.9))
        
        # Beat 3.0: Perfect 5th (On-beat passing tone)
        add_midi_note(base_pitch + 7, start_qn + 2.0, 0.5, int(velocity_base * 0.85))
        
        # Beat 4.0: Return to Root
        add_midi_note(base_pitch, start_qn + 3.0, 0.5, velocity_base)
        
        # Beat 4.5: 3rd passing tone up to the next downbeat
        add_midi_note(base_pitch + third_offset, start_qn + 3.5, 0.5, int(velocity_base * 0.8))

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Sub Bass FX Chain) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth for a warm sub-bass tone without harsh harmonics
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)  # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)  # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)  # Square mix (0%)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)  # Saw mix (0%)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.8)  # Triangle mix (80% for warmth)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0)  # Extra sine (100% for deep sub)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM"
