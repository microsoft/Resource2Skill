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
    Create a Scale Snap Guide Generator in the current REAPER project.
    This creates a muted track with a MIDI item containing all notes of the 
    specified scale. Open it in the MIDI editor and use "Hide unused note rows".

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate for the guide.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created guide track.
    """
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Mentioned explicitly in the video
    }

    import reaper_python as RPR

    # Input validation and formatting
    key_upper = key.capitalize() if len(key) > 1 else key.upper()
    if key_upper not in NOTE_MAP:
        key_upper = "C"
        
    scale_lower = scale.lower()
    if scale_lower not in SCALES:
        scale_lower = "major"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track explicitly as a guide
    guide_track_name = f"{key_upper} {scale_lower.capitalize()} Guide"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", guide_track_name, True)
    
    # Mute the track for safety (it acts purely as a visual template)
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate PPQ (Pulses Per Quarter Note) for note timing
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Insert Guide Notes ===
    root_note = NOTE_MAP[key_upper]
    
    # Calculate the allowed pitch classes (0-11) for the requested scale
    allowed_pitch_classes = [(root_note + interval) % 12 for interval in SCALES[scale_lower]]
    
    note_count = 0
    # Iterate through all possible MIDI notes (0 to 127)
    for note_num in range(128):
        pitch_class = note_num % 12
        
        # If the note belongs to the scale, insert it
        if pitch_class in allowed_pitch_classes:
            # RPR_MIDI_InsertNote args: take, selected, muted, start_ppq, end_ppq, channel, pitch, velocity, noSort
            # We set muted=True so the individual notes are muted, allowing "Hide unused note rows" to work silently
            RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note_num, velocity_base, True)
            note_count += 1
            
    # Sort the MIDI event list after batch insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created muted guide track '{guide_track_name}' with {note_count} scale notes over {bars} bars."
