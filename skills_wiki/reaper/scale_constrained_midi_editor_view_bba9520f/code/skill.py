import reaper_python as RPR

def create_scale_constrained_midi_view(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    octaves: int = 6, # Number of octaves to cover for the scale guide, starting from C1
    start_octave: int = 1, # The starting octave (e.g., C1 is MIDI note 24)
    duration: float = 0.25, # Duration of each guide note in beats (e.g., 0.25 for a 16th note)
    **kwargs,
) -> str:
    """
    Creates a new track with muted MIDI notes representing a chosen scale across multiple octaves.
    Then, it opens the MIDI editor for this item and executes "Hide unused note rows"
    to provide a visual scale guide in the piano roll.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (used for item length, but guide notes are static).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, pentatonic_major, pentatonic_minor, blues, whole_tone).
        octaves: Number of octaves for the scale guide to span.
        start_octave: The MIDI octave to start generating notes from (e.g., 1 for C1).
        duration: Duration of each guide note in beats.
        **kwargs: Additional overrides (not used in this skill but for composability).

    Returns:
        Status string, e.g., "Created 'Scale Guide - C Major' and set up MIDI editor view."
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Added based on video example
        "chromatic":        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # Full scale for comparison
    }

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Please choose from {list(NOTE_MAP.keys())}."
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Please choose from {list(SCALES.keys())}."

    root_midi_offset = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    
    # === Step 1: Create Track for Scale Guide ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    guide_track_name = f"{track_name} - {key} {scale.replace('_', ' ').title()}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", guide_track_name, True)
    
    # Mute the track completely so guide notes don't play
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.0) # Set track volume to 0.0 (-inf dB)

    # === Step 2: Create MIDI Item for Scale Guide ===
    # Item length doesn't matter much as it's just for holding notes, 1 bar is sufficient.
    item_position = 0.0
    item_length = (60.0 / bpm) * 4 # 4 beats for 1 bar
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Ensure the item is selected and active for MIDI editor operations
    RPR.RPR_SetMediaItemSelected(item, True)
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Insert Muted Scale Notes into MIDI Item ===
    RPR.RPR_MIDI_SetItemExtents(item, item_position, item_length) # Set MIDI item bounds
    RPR.RPR_MIDI_Clear(item) # Clear any existing MIDI in the new take
    
    current_time_pos = 0.0
    note_count = 0
    
    # Generate notes for 0-127 MIDI range or specified octaves
    for octave in range(start_octave, start_octave + octaves):
        for interval in scale_intervals:
            midi_note = (octave * 12) + root_midi_offset + interval
            if 0 <= midi_note <= 127: # Ensure note is within valid MIDI range
                # Insert note at a fixed position, minimal velocity, short duration
                RPR.RPR_MIDI_InsertNote(item, 0, 0, current_time_pos, current_time_pos + duration, 1, 1, midi_note, 1) # pos, start_in_beats, end_in_beats, channel, no_loop, velocity
                note_count += 1
                # Increment time slightly to place notes sequentially if needed, or keep them all at start for simplicity
                # For a visual guide, placing them all at the start is fine.
    
    RPR.RPR_MIDI_Sort(item) # Sort notes for good measure
    RPR.RPR_MIDI_Commit(item) # Commit MIDI changes
    
    # === Step 4: Open MIDI Editor and Hide Unused Note Rows ===
    # Open MIDI editor for the created item (selects it first if not already selected)
    RPR.RPR_Main_OnCommand(40166, 0) # Action: View: Open item in editor
    
    # Execute "Hide unused note rows"
    # This action works on the *currently open* MIDI editor.
    RPR.RPR_Main_OnCommand(40866, 0) # Action: MIDI editor: Hide unused note rows
    
    # Unselect item so it doesn't interfere with future actions
    RPR.RPR_SetMediaItemSelected(item, False)
    
    return f"Created '{guide_track_name}' track with {note_count} guide notes. MIDI editor view set to {key} {scale.replace('_', ' ').title()}."

