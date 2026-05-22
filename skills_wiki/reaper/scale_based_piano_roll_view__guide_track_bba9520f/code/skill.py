def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 1, # Scale guide only needs to be 1 bar, user can loop/stretch
    velocity_base: int = 10, # Low velocity for guide notes
    note_length_beats: float = 0.1, # Short length for guide notes
    octave_range_low: int = 0, # Start octave (C0)
    octave_range_high: int = 8, # End octave (C8)
    **kwargs,
) -> str:
    """
    Create a Scale Guide track with MIDI notes for the selected scale.
    This guide can be used with REAPER's "Hide unused note rows" action
    in the MIDI editor to show only notes in the chosen scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track (default "Scale Guide").
        bpm: Tempo in BPM (used for item length calculation).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, mixolydian,
                       pentatonic_major, pentatonic_minor, blues, whole_tone).
        bars: Number of bars for the scale guide MIDI item.
        velocity_base: Base MIDI velocity for guide notes (0-127).
        note_length_beats: Duration of each guide note in beats.
        octave_range_low: The lowest octave for the scale notes (e.g., 0 for C0).
        octave_range_high: The highest octave for the scale notes (e.g., 8 for C8).
        **kwargs: Additional overrides (not used in this skill).

    Returns:
        Status string, e.g., "Created 'Scale Guide' track with C Major scale notes."
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Whole Tone scale
    }

    import reaper_python as RPR

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Choose from {list(NOTE_MAP.keys())}."
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Choose from {list(SCALES.keys())}."

    root_midi = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # === Step 1: Set Tempo (if not already set, it's good practice) ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This command might interfere with user's project, better not to change global BPM

    # === Step 2: Create Track for Scale Guide ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0) # Mute the guide track

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4 # Assuming 4/4 time signature for simplicity
    item_position = 0.0 # Start at the beginning of the project
    item_length = (60.0 / bpm) * beats_per_bar * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Populate MIDI Item with Scale Notes ===
    RPR.RPR_MIDI_SetItemExtents(item, item_position, item_position + item_length)
    RPR.RPR_MIDI_Clear(take) # Clear any existing notes in the take

    midi_event_idx = 0
    for octave in range(octave_range_low, octave_range_high + 1):
        for interval in scale_intervals:
            midi_note = root_midi + interval + (octave * 12)
            if 0 <= midi_note <= 127: # Ensure note is within MIDI range
                # Insert note at the beginning of the item
                RPR.RPR_MIDI_InsertNote(take, False, False, midi_event_idx, item_position,
                                        item_position + note_length_beats, midi_note,
                                        velocity_base, False)
                midi_event_idx += 1
    
    RPR.RPR_MIDI_Sort(take) # Sort notes after insertion
    RPR.RPR_UpdateItemInProject(item)

    # Provide user instructions
    RPR.RPR_ShowConsoleMsg(
        f"\n--- Scale Guide Created ---\n"
        f"A track named '{track_name}' has been created with {key} {scale} notes.\n"
        f"To use it:\n"
        f"1. Create your own MIDI item on a separate track.\n"
        f"2. Select both your MIDI item AND the '{track_name}' MIDI item.\n"
        f"3. Open the MIDI editor (double-click one of the selected items).\n"
        f"4. In the MIDI editor, go to Actions -> Show action list... (or press '?')\n"
        f"5. Search for 'Hide unused note rows' and run it.\n"
        f"   (You might want to assign a hotkey to this action for convenience)\n"
        f"6. The piano roll will now only show the notes of the {key} {scale} scale!\n"
        f"7. To show all notes again, run the action 'Show all note rows'.\n"
        f"---------------------------\n"
    )

    return f"Created '{track_name}' track with {key} {scale} scale notes from C{octave_range_low} to C{octave_range_high}."

