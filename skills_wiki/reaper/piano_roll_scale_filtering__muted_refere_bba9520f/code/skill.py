def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Reference",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a muted reference MIDI item containing all notes of a specified scale across all octaves.
    When opened in the MIDI Editor alongside an active item, running the action 
    'View: Hide unused note rows' will fold the piano roll to this exact scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate the reference block.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string indicating the track and scale generated.
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
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "locrian":          [0, 1, 3, 5, 6, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Normalize inputs
    safe_key = key if key in NOTE_MAP else "C"
    safe_scale = scale if scale in SCALES else "major"
        
    root_pitch = NOTE_MAP[safe_key]
    scale_intervals = SCALES[safe_scale]
    
    # Calculate all valid MIDI pitches (0-127) for the selected scale
    valid_pitches = []
    for octave in range(-1, 10):
        for interval in scale_intervals:
            pitch = (octave + 1) * 12 + root_pitch + interval
            if 0 <= pitch <= 127:
                valid_pitches.append(pitch)
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Muted Reference Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name}: {safe_key} {safe_scale}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Mute the track to prevent the massive note cluster from playing audio
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_time = 0.0
    end_time = item_length
    
    # Convert absolute project time to MIDI PPQ (Pulses Per Quarter Note)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
    
    # Insert a full-length note for every single pitch in the scale
    for pitch in valid_pitches:
        # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        
    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created muted reference track '{full_track_name}' containing {len(valid_pitches)} notes over {bars} bars at {bpm} BPM."
