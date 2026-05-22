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
    Creates a 'Scale Guide' MIDI item filled with muted notes across all octaves.
    When opened in the MIDI Editor alongside the 'Hide unused note rows' action, 
    it visually collapses the piano roll to only show notes in the target scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C', 'F#', 'Bb').
        scale: Scale type ('major', 'minor', 'harmonic_minor', 'whole_tone', etc.).
        bars: Number of bars to generate for the guide item.
        velocity_base: Base MIDI velocity (100).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{key} {scale.capitalize()} Guide", True)
    
    # Set track color to a distinct light blue to identify it as a guide
    color = RPR.RPR_ColorToNative(100, 150, 255) | 0x1000000
    RPR.RPR_SetTrackColor(track, color)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    cursor_pos = RPR.RPR_GetCursorPosition()
    item = RPR.RPR_CreateNewMIDIItemInProj(track, cursor_pos, cursor_pos + item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos + item_length)

    # === Step 4: Calculate & Insert Muted Notes ===
    # Format the key safely (e.g., 'c#' -> 'C#')
    clean_key = key.capitalize() if len(key) == 1 else key[0].upper() + key[1:].lower()
    root_pitch_class = NOTE_MAP.get(clean_key, 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    valid_notes = []
    # MIDI note numbers range roughly from octaves -1 to 9 (0 to 127)
    for octave in range(-1, 10): 
        for interval in scale_intervals:
            note = ((octave + 1) * 12) + root_pitch_class + interval
            if 0 <= note <= 127:
                valid_notes.append(note)

    # Insert notes (muted = True) spanning the entire item length
    for note in valid_notes:
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note, velocity_base, True)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add basic Synth ===
    # Adds a synth so that when the user draws active notes over the guide grid, they can hear them.
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth volume slightly lower to prevent harsh peaks
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.1) 

    return f"Created '{key} {scale.capitalize()} Guide' track with {len(valid_notes)} muted notes over {bars} bars. Open in MIDI Editor and trigger 'View: Hide unused note rows'."
