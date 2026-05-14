def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Canvas",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale-Locked MIDI Canvas in the current REAPER project.
    Inserts muted guide notes for every pitch in the scale and hides unused rows.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (not really used here as notes are muted).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the scale canvas.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Normalize inputs
    safe_key = key.capitalize() if len(key) == 1 else key[0].upper() + key[1:].lower()
    root_pitch = NOTE_MAP.get(safe_key, 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    final_track_name = f"{safe_key} {scale.replace('_', ' ').title()} Canvas"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", final_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate position for guide notes (short 1/8th note at the very beginning)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (60.0 / bpm) * 0.5)

    # === Step 4: Insert Muted Guide Notes ===
    note_count = 0
    for octave in range(11):  # 0 to 10 to cover 0-127 MIDI range
        for interval in intervals:
            pitch = root_pitch + (octave * 12) + interval
            if 0 <= pitch <= 127:
                # InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, 1, False)
                note_count += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate UI to Hide Unused Rows ===
    # Unselect all items to ensure we only open the one we just created
    RPR.RPR_Main_OnCommand(40289, 0)
    
    # Select our new canvas item
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "View: Hide unused and unnamed note rows" in the active MIDI Editor
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)

    return f"Created '{final_track_name}' with {note_count} muted guide notes over {bars} bars. Unused piano roll rows have been collapsed to match the scale."
