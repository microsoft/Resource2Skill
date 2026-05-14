def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Notation Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a chord progression and open it in REAPER's Musical Notation view.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (generates a 4-bar loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation and view change.
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    qn_per_bar = 4 # 4/4 time
    item_length = (60.0 / bpm) * qn_per_bar * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Diatonic Chords ===
    root_val = NOTE_MAP.get(key.capitalize(), 0) + 48 # Start around C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    def get_diatonic_triad(degree):
        """Builds a diatonic triad (root, third, fifth) for a given scale degree (0-indexed)."""
        chord_notes = []
        for offset in [0, 2, 4]: # Triad spacing
            idx = degree + offset
            octave_shift = idx // 7
            interval = scale_intervals[idx % 7]
            chord_notes.append(root_val + interval + (octave_shift * 12))
        return chord_notes

    # Progression: I - IV - V - I
    progression_degrees = [0, 3, 4, 0]

    for i in range(bars):
        # Loop the progression if bars > 4
        degree = progression_degrees[i % len(progression_degrees)]
        chord = get_diatonic_triad(degree)
        
        start_qn = i * qn_per_bar
        end_qn = start_qn + qn_per_bar # Whole notes
        
        start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)

        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        for note in chord:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Open Item in Musical Notation View ===
    # Unselect all, then select our new item
    RPR.RPR_SelectAllMediaItems(0, False)
    RPR.RPR_SetMediaItemSelected(item, True)

    # Open in built-in MIDI editor (Main Action)
    RPR.RPR_Main_OnCommand(40153, 0)

    # Grab the active MIDI editor handle
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # Trigger "View: Mode: musical notation" within the MIDI Editor
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40954)

    return f"Created '{track_name}' with a {key} {scale} I-IV-V-I progression and opened in Notation View."
