import reaper_python as RPR

def create_scale_guide_midi_item(
    project_name: str = "MyProject",
    key: str = "C",
    scale_type: str = "major",
    num_octaves: int = 4,
    bars: int = 1, # A single bar is enough for a static scale guide
    base_midi_note: int = 36, # C2, a common low starting point for instruments
    guide_track_name: str = "Scale Guide",
    guide_note_velocity: int = 1, # Very low velocity to ensure notes are muted/inaudible but exist
    open_midi_editor: bool = True,
    apply_hide_unused: bool = True,
    item_color: int = 12 # A distinct color, like pink from the video tutorial
) -> str:
    """
    Creates a MIDI item with all notes of a specified scale across several octaves,
    mutes them, and then opens the MIDI editor for this item with "MIDI Editor: Hide unused note rows" applied.
    This serves as a visual guide in the Piano Roll, effectively 'hiding' non-scale notes
    by making them absent in the guide item itself.

    Args:
        project_name: Project identifier (for logging).
        key: Root note (C, C#, D, ..., B).
        scale_type: Type of scale (major, minor, harmonic_minor, dorian, mixolydian,
                    pentatonic_major, pentatonic_minor, blues, whole_tone, etc.).
        num_octaves: Number of octaves to span for the scale notes (e.g., 4-5 octaves).
        bars: Length of the guide MIDI item in bars (usually 1 is sufficient for a static guide).
        base_midi_note: The lowest MIDI note number to start generating scale notes from.
                        This will be adjusted to the nearest `key` for the actual scale root.
        guide_track_name: Name for the created guide track.
        guide_note_velocity: MIDI velocity for the guide notes (0-127).
                             Set to 1 to effectively mute them but keep them present for visual filtering.
        open_midi_editor: If True, opens the MIDI editor for the created guide item.
        apply_hide_unused: If True, applies "MIDI Editor: Hide unused note rows" after opening editor.
        item_color: Integer representing the REAPER item color (0-127 usually).

    Returns:
        Status string, e.g., "Created 'Scale Guide - C Major' with N notes over 1 bar.
        Open this MIDI item in the editor for the scale guide."
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10], # Natural minor
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10],
        # Add more scales here if desired
    }

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Please use C, C#, D, etc."
    if scale_type not in SCALES:
        return f"Error: Invalid scale type '{scale_type}'. Please choose from {list(SCALES.keys())}."

    root_midi_offset = NOTE_MAP[key]
    scale_intervals = SCALES[scale_type]

    RPR.Undo_BeginBlock2(0) # Start undo block

    # === Step 1: Create Track for Scale Guide ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    full_track_name = f"{guide_track_name} - {key} {scale_type.replace('_', ' ').title()}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_RECMODE", 0) # Set to input off

    # === Step 2: Create MIDI Item ===
    # Assuming 4/4 time signature for simplicity as it's a guide item
    current_bpm = RPR.RPR_GetProjectBPM(0, False) # Get current project BPM
    beats_per_bar = 4
    bar_length_sec = (60.0 / current_bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Set item color
    RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", item_color)
    RPR.RPR_SetMediaItemInfo_Value(item, "I_LASTSEL", 1) # Select the item
    RPR.RPR_SetMediaItemInfo_Value(item, "I_SEL", 1) # Select item for color application
    # RPR.RPR_UpdateItemInProject(item) # Not strictly necessary after setting I_SEL

    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)
        if not take:
            RPR.RPR_DeleteTrack(track)
            RPR.Undo_EndBlock2(0, "Create Scale Guide MIDI Item (Failed)", -1)
            return "Error: Could not create take for MIDI item."

    RPR.RPR_MIDI_Clear(take) # Clear any default notes

    # === Step 3: Insert MIDI Notes for the Scale Guide ===
    notes_inserted = 0
    note_duration = 0.5 # Half beat for visibility in piano roll

    # Adjust actual_base_root to be the closest 'key' below or at base_midi_note
    # E.g., if base_midi_note=36 (C2) and key="G", actual_base_root becomes 36+7=43 (G2)
    actual_base_root = (base_midi_note // 12) * 12 + root_midi_offset
    if actual_base_root > base_midi_note:
        actual_base_root -= 12 # Adjust to start from a lower octave if the root is above base_midi_note

    for octave in range(num_octaves):
        for interval in scale_intervals:
            midi_note = actual_base_root + interval + (octave * 12)
            if midi_note < 0 or midi_note > 127: # Ensure notes are within MIDI range
                continue
            
            # Insert note at the beginning of the item
            RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, note_duration, guide_note_velocity, 127, midi_note, True)
            notes_inserted += 1

    RPR.RPR_MIDI_Sort(take) # Sort notes after insertion for consistency
    RPR.RPR_MIDI_SetAllNotesVelocities(take, guide_note_velocity, True) # Ensure all notes have the specified velocity

    # === Step 4: Open MIDI Editor and Apply Hide Unused ===
    if open_midi_editor:
        # Open MIDI editor for the selected item
        RPR.RPR_Main_OnCommand(40003, 0) # MIDI Editor: Open selected MIDI items (This uses the selected item)

        if apply_hide_unused:
            midi_editor = RPR.RPR_MIDIEditor_GetActive()
            if midi_editor:
                # Apply "MIDI Editor: Hide unused note rows" action
                RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40131, 0)
            else:
                RPR.ShowConsoleMsg("Warning: MIDI editor not active, could not apply 'Hide unused note rows'.\n")

        # Deselect the item so it doesn't interfere with future user selections
        RPR.RPR_SetMediaItemInfo_Value(item, "I_LASTSEL", 0)
        RPR.RPR_SetMediaItemInfo_Value(item, "I_SEL", 0)

    RPR.Undo_EndBlock2(0, f"Created Scale Guide MIDI Item - {key} {scale_type.replace('_', ' ').title()}", -1)

    return f"Created '{full_track_name}' with {notes_inserted} guide notes over {bars} bar(s). " \
           f"Open this MIDI item in the editor for the scale guide. For general visual guidance, " \
           f"also consider REAPER's built-in 'Key Snap' feature (bottom bar of MIDI editor)."

