def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 4,
    velocity_base: int = 10,
    **kwargs,
) -> str:
    """
    Creates a muted template track containing all notes of a specified scale across all octaves.
    To use the effect shown in the tutorial:
      1. Open the created MIDI item in the MIDI Editor.
      2. Run the action "View: Hide unused note rows" (Action ID 40452).
      3. Your piano roll is now locked to the selected scale!

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Length of the guide item.
        velocity_base: Velocity of the muted guide notes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated scale guide.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {
        "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
        "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
        "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11
    }
    
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Normalize inputs
    key_upper = key.upper()
    base_note = NOTE_MAP.get(key_upper, 0) # Default to C if invalid
    scale_lower = scale.lower()
    scale_intervals = SCALES.get(scale_lower, SCALES["major"])

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track clearly so the user knows what scale is active
    full_track_name = f"{track_name} ({key_upper} {scale_lower.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Mute the track entirely to ensure guide notes never play
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Populate MIDI Notes across ALL octaves (0-127) ===
    start_ppq = 0.0
    end_ppq = 960.0 # Length of 1 quarter note in standard PPQ
    
    notes_added = 0
    for pitch in range(128):
        # Check if the current pitch belongs to the selected scale
        if (pitch - base_note) % 12 in scale_intervals:
            # RPR_MIDI_InsertNote args: (take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            # We set muted=True (the 3rd argument) so individual notes are silently drawn
            RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            notes_added += 1

    # Sort the MIDI data to finalize insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{full_track_name}' with {notes_added} muted guide notes. Open MIDI editor and run 'Hide unused note rows' to lock view to scale."
