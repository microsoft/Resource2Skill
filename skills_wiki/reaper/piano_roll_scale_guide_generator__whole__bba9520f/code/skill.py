def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a muted Piano Roll Scale Guide in the current REAPER project.
    
    After generation, open this item in the MIDI editor alongside your synth item,
    and trigger the REAPER action 'View: Hide unused and unnamed note rows' 
    to lock your piano roll visually to the specified scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate for the guide.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10],  # Highlighted in the tutorial
    }

    # Normalize key input
    key_upper = key.upper()
    if key_upper not in NOTE_MAP:
        key_upper = "C"
    
    root_val = NOTE_MAP[key_upper]
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Format track name (e.g., "C Whole Tone Guide")
    formatted_track_name = f"{key_upper} {scale.replace('_', ' ').title()} {track_name}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", formatted_track_name, True)
    
    # Mute the track entirely so it acts only as a visual reference
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", formatted_track_name, True)

    # === Step 4: Insert Diatonic Notes ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    notes_added = 0
    # Iterate across all standard MIDI octaves (-1 to 9)
    for octave in range(-1, 10):
        for interval in scale_intervals:
            note_num = (octave + 1) * 12 + root_val + interval
            # Ensure we only place notes within the 0-127 MIDI bounds
            if 0 <= note_num <= 127:
                # Parameters: take, selected(False), muted(True), start, end, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note_num, velocity_base, True)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{formatted_track_name}' track with {notes_added} muted guide notes over {bars} bars. Use 'Hide unused note rows' in the MIDI editor."
