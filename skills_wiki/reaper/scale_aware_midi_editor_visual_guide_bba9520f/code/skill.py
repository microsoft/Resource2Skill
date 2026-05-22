def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 1,
    start_octave: int = 2, # C2, MIDI 36
    num_octaves: int = 7, # Spans multiple octaves
    guide_velocity: int = 1, # Visible, barely audible
    **kwargs,
) -> str:
    """
    Creates a MIDI item with all notes of a specified scale across multiple octaves.
    This item serves as a visual guide in the REAPER MIDI editor.
    To visually hide non-scale notes (showing only the scale notes) when composing:
    1. Double-click the newly created MIDI item to open its MIDI editor.
    2. In the MIDI editor, run the action "MIDI: Hide unused note rows" (ID 40867).
       (You can assign a hotkey or add this action to your MIDI toolbar for quick access).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (will set project tempo).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, whole_tone, etc.).
        bars: Length of the MIDI item in bars.
        start_octave: The lowest octave for the scale notes (e.g., 2 for C2).
        num_octaves: The number of octaves to span for the scale notes.
        guide_velocity: MIDI velocity for the guide notes (0-127).
                        Set to 0 for truly silent guides, 1 for barely audible.
        **kwargs: Additional overrides (not used in this simple example but good for future expansion).

    Returns:
        Status string describing what was created and next steps.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10], # Natural minor
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "locrian": [0, 1, 3, 5, 6, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
        "whole_tone": [0, 2, 4, 6, 8, 10],
    }

    RPR.Undo_BeginBlock2(0) # Begin undo block for this operation

    # --- Input Validation ---
    if key.upper() not in NOTE_MAP:
        RPR.ShowConsoleMsg(f"Error: Invalid key '{key}'. Please use C, C#, D, etc. (case-insensitive).\n")
        RPR.Undo_EndBlock2(0, "Create Scale Visual Guide (Error)", 0)
        return f"Error: Invalid key '{key}'."
    if scale.lower() not in SCALES:
        RPR.ShowConsoleMsg(f"Error: Invalid scale '{scale}'. Please use major, minor, whole_tone, etc. (case-insensitive).\n")
        RPR.Undo_EndBlock2(0, "Create Scale Visual Guide (Error)", 0)
        return f"Error: Invalid scale '{scale}'."
    if not (0 <= guide_velocity <= 127):
        RPR.ShowConsoleMsg(f"Error: Invalid velocity '{guide_velocity}'. Must be between 0 and 127.\n")
        RPR.Undo_EndBlock2(0, "Create Scale Visual Guide (Error)", 0)
        return f"Error: Invalid guide_velocity '{guide_velocity}'."

    # --- Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Create MIDI Item ---
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    bar_length_seconds = seconds_per_beat * beats_per_bar
    item_length_seconds = bar_length_seconds * bars

    # Create a new, empty MIDI item at the current edit cursor position
    RPR.RPR_CreateNewMIDIItemInProj(
        track,
        RPR.TimeMap2_GetCurLevelInc(0, 0), # Start at current cursor position
        RPR.TimeMap2_GetCurLevelInc(0, 0) + item_length_seconds, # End after specified bars
        False # Do not automatically select item
    )
    # Get the newly created item (assuming it's the last one on the track)
    item = RPR.RPR_GetMediaItem(0, track_idx, 0)
    take = RPR.RPR_GetActiveTake(item)

    # --- Insert Scale Notes ---
    root_midi_base = NOTE_MAP[key.upper()]
    scale_intervals = SCALES[scale.lower()]
    inserted_notes_count = 0

    midi_take_ptr = RPR.RPR_MIDI_GetTake(take)
    if not midi_take_ptr:
        RPR.ShowConsoleMsg("Error: Failed to get MIDI take pointer for note insertion.\n")
        RPR.Undo_EndBlock2(0, "Create Scale Visual Guide (Error)", 0)
        return "Error: Could not access MIDI take for note insertion."

    RPR.RPR_MIDI_DisableUpdate(midi_take_ptr) # Optimize MIDI editing for faster insertion

    for octave_num in range(num_octaves):
        # Calculate MIDI offset for the current octave (e.g., C2 is 2*12=24, C3 is 3*12=36)
        current_octave_midi_offset = (start_octave + octave_num) * 12
        for interval in scale_intervals:
            midi_note = current_octave_midi_offset + root_midi_base + interval
            if 0 <= midi_note <= 127: # Ensure note is within valid MIDI range
                # Insert note at the beginning of the item, spanning its full length
                RPR.RPR_MIDI_InsertNote(midi_take_ptr, False, False, 0.0, item_length_seconds, 0, midi_note, guide_velocity, False)
                inserted_notes_count += 1

    RPR.RPR_MIDI_EnableUpdate(midi_take_ptr) # Re-enable MIDI updates after insertions

    # --- Add ReaSynth to the track ---
    # Adding ReaSynth to make the guide notes audible if velocity > 0
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # --- Instructions for user ---
    instruction_msg = (
        f"\n--- Skill: Scale-Aware MIDI Editor Visual Guide ---\n"
        f"Scale guide for {key.upper()} {scale.capitalize()} created on track '{track_name}'.\n"
        "To visually hide non-scale notes (showing only the scale notes) in the MIDI editor:\n"
        "1. Double-click the newly created MIDI item on track '{track_name}' to open its MIDI editor.\n"
        "2. In the MIDI editor, run the action 'MIDI: Hide unused note rows' (Action ID 40867).\n"
        "   (Tip: Consider assigning a hotkey or adding this action to your MIDI toolbar for quick access).\n"
        f"The guide notes have velocity {guide_velocity}. You can mute this track if you don't want to hear them."
    )
    RPR.ShowConsoleMsg(instruction_msg + "\n")

    RPR.Undo_EndBlock2(0, "Create Scale Visual Guide", 1) # End undo block (successful)

    return (
        f"Created '{track_name}' with {inserted_notes_count} guide notes for {key.upper()} {scale.capitalize()} "
        f"over {num_octaves} octaves."
    )

