import reaper_python as RPR

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
    "whole_tone":       [0, 2, 4, 6, 8, 10]
}

def get_midi_pitch(key_name: str, octave: int = 3) -> int:
    """Converts a note name and octave to a MIDI pitch number (C0=0, C3=36, C5=60 etc.)."""
    if key_name not in NOTE_MAP:
        raise ValueError(f"Invalid key name: {key_name}")
    return NOTE_MAP[key_name] + (octave * 12)

def get_scale_notes(root_key: str, scale_type: str, start_octave: int, num_octaves: int) -> list[int]:
    """
    Generates a list of MIDI pitch numbers for a given scale across specified octaves.
    """
    if root_key not in NOTE_MAP:
        raise ValueError(f"Invalid root key: {root_key}. Choose from {list(NOTE_MAP.keys())}")
    if scale_type not in SCALES:
        raise ValueError(f"Invalid scale type: {scale_type}. Choose from {list(SCALES.keys())}")

    root_midi_chromatic = NOTE_MAP[root_key]
    scale_intervals = SCALES[scale_type]
    all_scale_notes = []

    for octave_offset in range(num_octaves):
        # Calculate the base MIDI note for the current root and starting octave
        # MIDI C0 is 0. C3 is 36, C4 is 48.
        current_octave_base_midi = (start_octave + octave_offset) * 12 + root_midi_chromatic
        
        for interval in scale_intervals:
            note = current_octave_base_midi + interval
            if 0 <= note <= 127: # Ensure notes are within MIDI range
                all_scale_notes.append(note)
    return sorted(list(set(all_scale_notes))) # Remove duplicates and sort

def create_scale_guide(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    num_octaves: int = 4, # Number of octaves to generate the scale notes for.
    start_octave: int = 3, # The MIDI octave to start generating notes from (e.g., 3 for C3).
    note_duration: float = 0.5, # Duration of each scale guide note in beats.
    note_velocity: int = 80,
    **kwargs,
) -> str:
    """
    Creates a MIDI item containing notes of a specified scale across multiple octaves
    and applies the "Hide unused note rows" action in the MIDI editor when opened.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate the MIDI item.
        num_octaves: Number of octaves to generate the scale notes for.
        start_octave: The MIDI octave to start generating notes from (e.g., 3 for C3).
        note_duration: Duration of each scale guide note in beats.
        note_velocity: MIDI velocity for the guide notes (0-127).
        **kwargs: Additional overrides (not used in this specific skill but kept for consistency).

    Returns:
        Status string describing what was created.
    """
    RPR.Undo_BeginBlock2(0) # Begin undo block for undo/redo

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item with Scale Notes ===
    # Assuming 4/4 time signature for calculating bar length
    beats_per_bar = 4 
    
    # Calculate item length in seconds based on project BPM
    # RPR.TimeMap_GetMeasuresAndBeat(0, 0, 0, None, None, None, None, None, None) # To get project time signature
    # For simplicity, we assume 4 beats per bar.
    
    # Get current project BPM to calculate item length
    actual_bpm = RPR.RPR_GetProjectTimeSignature2(0, None, None, None) # Use current project BPM
    if actual_bpm == 0: # Fallback if project BPM not set or retrieved
        actual_bpm = bpm
    
    bar_length_sec = (60.0 / actual_bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Add a blank MIDI item to the new track
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)
        
    # Get the active MIDI Take
    midi_take = RPR.RPR_MIDI_SetItemExtents(take, -1.0, -1.0) # Ensure it's a MIDI take, use default extents
    
    # Generate scale notes
    try:
        scale_midi_pitches = get_scale_notes(key, scale, start_octave, num_octaves)
    except ValueError as e:
        RPR.ShowConsoleMsg(f"Error generating scale notes: {e}\n")
        RPR.Undo_EndBlock2(0, "Create Scale Guide (Error)", -1)
        RPR.RPR_DeleteTrack(track) # Clean up track if scale generation fails
        return f"Error: {e}"

    # Insert each scale note at the start of the MIDI item
    # The exact position/length of these guide notes doesn't matter much for 'hide unused note rows',
    # but they must exist in the item to be considered "used".
    note_pos_beats = 0.0 # All guide notes start at the beginning of the MIDI item
    
    RPR.MIDI_SetItemExtents(take, 0.0, item_length, True) # Set correct MIDI item length
    RPR.MIDI_TakeNew(midi_take) # Clear any default notes in a new take

    # Begin editing MIDI take
    RPR.MIDI_SetItemExtents(take, 0.0, item_length) # Set MIDI item bounds
    RPR.MIDI_ClearEvts(midi_take, True) # Clear existing events to ensure only scale notes are present

    for pitch in scale_midi_pitches:
        # RPR.MIDI_InsertNote expects position and end time in MIDI ticks or beats depending on context.
        # It's usually easier to work with beats for initial placement.
        # The arguments are MIDI_SetNote(take, notelookup_idx, selected, muted, start_beat, end_beat, channel, pitch, velocity)
        # We're using MIDI_AddNote for creation, which is RPR.MIDI_InsertNote.
        # Using MIDI_AddNote(take, selected, muted, start_beat, end_beat, channel, pitch, velocity, no_sort_or_update)
        # no_sort_or_update = False for immediate update
        RPR.MIDI_AddNote(midi_take, False, False, note_pos_beats, note_pos_beats + note_duration, 0, pitch, note_velocity, False)
    
    # Update MIDI events
    RPR.MIDI_Sort(midi_take)
    RPR.MIDI_RefreshAndEdits(midi_take, False) # Refresh and update editor if open

    # === Step 3: Open MIDI Editor and Apply "Hide unused note rows" ===
    # Select the newly created MIDI item
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open MIDI editor for selected item(s)
    # Action ID for "MIDI: Open item in editor" (from REAPER's Action List)
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Action ID for "MIDI: Hide unused note rows"
    # This action works on the active MIDI editor, which should now be open for our item.
    RPR.RPR_Main_OnCommand(40889, 0)
    
    # Deselect the item for cleanliness, assuming MIDI editor can remain open.
    RPR.RPR_SetMediaItemSelected(item, False)

    RPR.Undo_EndBlock2(0, "Create Scale Guide", 1) # End undo block

    return f"Created '{track_name}' track with {len(scale_midi_pitches)} scale guide notes in {key} {scale} over {num_octaves} octaves at {actual_bpm} BPM. MIDI editor opened with unused note rows hidden."

