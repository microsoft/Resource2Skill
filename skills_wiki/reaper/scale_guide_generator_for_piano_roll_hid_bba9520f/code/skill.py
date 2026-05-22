def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale Guide in the current REAPER project to be used with the 
    'Hide unused note rows' action in the MIDI Editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate for the dummy item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Scale Guide (C major)' with 74 notes over 1 bars at 120 BPM"
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Normalize inputs
    key_upper = key.upper()
    root_pitch = NOTE_MAP.get(key_upper, 0)
    scale_lower = scale.lower()
    scale_intervals = SCALES.get(scale_lower, SCALES["major"])
    
    full_track_name = f"{track_name} ({key_upper} {scale_lower})"

    # === Step 1: Calculate all valid scale pitches from MIDI 0 to 127 ===
    valid_pitches = []
    for octave in range(-1, 10):  # Covers notes 0 to 127
        for interval in scale_intervals:
            pitch = root_pitch + interval + (octave * 12)
            if 0 <= pitch <= 127:
                valid_pitches.append(pitch)

    # === Step 2: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 3: Create Track & Mute it ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    # Mute the track so the dummy notes don't accidentally play
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Insert Dummy Notes ===
    # Notes will stretch across the entire item length
    start_ppq = 0
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    notes_created = 0
    for pitch in valid_pitches:
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        notes_created += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # Note: To use this visually, the user/agent must select this new item alongside 
    # their actual target item, open the MIDI editor, and trigger Action 40453 
    # ("MIDI Editor: Hide unused and unnamed note rows").

    return f"Created '{full_track_name}' (muted) with {notes_created} dummy notes over {bars} bars at {bpm} BPM"
