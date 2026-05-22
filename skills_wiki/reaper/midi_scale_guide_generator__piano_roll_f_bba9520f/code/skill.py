def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a muted MIDI Scale Guide track to filter the Piano Roll.
    
    After running this, open the item in the MIDI Editor and use the action:
    'View: Hide unused note rows' (Command ID 40452) to collapse the piano roll.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate the guide for.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated item.
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
        "melodic_minor":    [0, 2, 3, 5, 7, 9, 11],
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

    # Input validation
    if key not in NOTE_MAP:
        key = "C"
    if scale not in SCALES:
        scale = "minor"

    root_pitch = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Dedicated Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} - {key} {scale}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Configure Item Length ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # === Step 4: Create and Mute MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Mute the item so it doesn't play sound, acting purely as a visual guide
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Insert Scale Notes Across Entire MIDI Spectrum ===
    start_time = 0.0
    end_time = item_length
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

    note_count = 0
    # Iterate through all 128 possible MIDI notes
    for pitch in range(128):
        # Calculate distance from the root note and apply modulo 12
        # to determine its interval regardless of octave
        interval = (pitch - root_pitch) % 12
        
        if interval in scale_intervals:
            # Note parameters: take, selected, muted, start_ppq, end_ppq, channel, pitch, velocity, noSort
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)
            note_count += 1

    # Finalize MIDI
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{full_track_name}' guide track with {note_count} muted notes. (Tip: Open in MIDI Editor and run 'Hide unused note rows')"
