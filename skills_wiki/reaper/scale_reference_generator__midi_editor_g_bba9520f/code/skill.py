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
    Create a muted multi-octave Scale Reference Generator in the current REAPER project.
    Use this alongside REAPER's "View: Hide unused and unnamed note rows" MIDI editor action.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, Db, D, ..., B).
        scale: Scale type (major, minor, whole_tone, dorian, etc.).
        bars: Number of bars the visual guide should span.
        velocity_base: Base MIDI velocity (0-127) (irrelevant here as notes are muted).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created guide track.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Highlighted in the tutorial
    }

    # Normalize inputs
    key_norm = key.capitalize()
    if key_norm not in NOTE_MAP:
        key_norm = "C"
        
    scale_norm = scale.lower()
    if scale_norm not in SCALES:
        scale_norm = "major"
        
    base_pitch = NOTE_MAP[key_norm]
    intervals = SCALES[scale_norm]
    
    # Generate dynamic track name based on scale
    final_track_name = f"{key_norm} {scale_norm.replace('_', ' ').title()} Guide"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", final_track_name, True)
    
    # Mute the track to ensure it acts only as a visual guide
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Get PPQ positions for the full item length
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Populate Scale Notes Across Octaves ===
    note_count = 0
    # Loop through octaves 1 to 7 (MIDI notes 12 to roughly 107)
    for octave in range(1, 8):
        octave_base = base_pitch + (octave * 12)
        
        for interval in intervals:
            note_pitch = octave_base + interval
            
            # Keep within valid MIDI range
            if note_pitch < 128:
                # Insert the note (muted = True) spanning the whole item
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    True,           # muted (purely visual)
                    start_ppq,      # start time
                    end_ppq,        # end time
                    0,              # channel
                    note_pitch,     # pitch
                    velocity_base,  # velocity
                    True            # noSort (we will sort after the loop)
                )
                note_count += 1

    # Sort the MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    # Update timeline UI
    RPR.RPR_UpdateArrange()

    return f"Created visual guide '{final_track_name}' with {note_count} muted notes over {bars} bars."
