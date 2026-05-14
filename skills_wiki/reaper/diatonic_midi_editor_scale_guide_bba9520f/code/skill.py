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
    Creates a muted MIDI item containing all notes of a specified scale across multiple octaves.
    When opened in the MIDI Editor alongside your composition, you can use the action
    'View: Hide unused note rows' to snap the piano roll strictly to this scale.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars the item spans.
        velocity_base: Velocity of the guide notes (does not affect audio since muted).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated scale guide.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Emphasized in the video for dreamy sequences
    }

    # Resolve scale and root
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)
    scale_key = scale.lower()
    scale_intervals = SCALES.get(scale_key, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    full_track_name = f"{track_name} ({key.upper()} {scale_key.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # MUTE THE ITEM: Essential so the guide notes don't accidentally play
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Populate Scale Notes ===
    # Make the notes 1 quarter-note long at the very beginning
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (60.0 / bpm))

    note_count = 0
    # Generate across octaves 2 through 6 (standard composition range)
    for octave in range(2, 7):
        base_midi = (octave + 1) * 12 + root_pitch # +1 mapping (e.g., octave 2 = MIDI 36 for C)
        for interval in scale_intervals:
            pitch = base_midi + interval
            if pitch <= 127:
                # Insert note logic
                # args: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created guide track '{full_track_name}' with {note_count} muted notes. (Tip: Open this in MIDI Editor and trigger 'View: Hide unused note rows')"
