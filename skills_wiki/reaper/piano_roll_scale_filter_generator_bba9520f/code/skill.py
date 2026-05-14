def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Piano Roll Scale Filter Generator in the current REAPER project.
    Generates explicitly muted notes for a specific scale across all octaves,
    allowing the user to use 'Hide unused note rows' in the MIDI Editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars the guide item should last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created guide track.
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
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "locrian":          [0, 1, 3, 5, 6, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Resolve scale and root
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key} {scale})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Convert time to PPQ (ticks)
    start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    end_qn = RPR.RPR_TimeMap2_timeToQN(0, item_length)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # === Step 4: Generate Muted Scale Scaffold ===
    note_count = 0
    
    # Loop through 11 octaves to cover the entire MIDI spectrum (0-127)
    for octave in range(11):
        for interval in intervals:
            note_pitch = (octave * 12) + root_val + interval
            
            if 0 <= note_pitch <= 127:
                # Insert note. Parameter 3 is 'muted'. We set it to True.
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note_pitch, velocity_base, True)
                note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{full_track_name}' with {note_count} muted notes over {bars} bars. Open in MIDI editor and trigger 'Hide unused note rows'."
