def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Macro_Split",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Demonstrates the 'Split and Move Up' custom action shown in the video.
    Generates a continuous phrase, splits it in half, and moves the second half
    to a track above for layered processing / hocketing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name base for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Calculate Timings ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    split_time_sec = total_length_sec / 2.0  # We will split the phrase exactly in half

    # === Step 3: Create Upper and Lower Tracks ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # Upper Track (Destination)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    upper_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(upper_track, "P_NAME", f"{track_name}_Upper", True)
    
    # Lower Track (Source)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    lower_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(lower_track, "P_NAME", f"{track_name}_Lower", True)

    # === Step 4: Generate Continuous MIDI Item on Lower Track ===
    item = RPR.RPR_CreateNewMIDIItemInProj(lower_track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)
    
    root_note = NOTE_MAP.get(key, 0) + 48  # Start at octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    note_length_sec = bar_length_sec / 8.0  # 1/8th notes
    
    total_notes = bars * 8
    for i in range(total_notes):
        scale_degree = i % len(scale_intervals)
        octave_shift = (i // len(scale_intervals)) * 12
        pitch = root_note + scale_intervals[scale_degree] + octave_shift
        
        # Keep pitch within safe MIDI bounds
        if pitch > 127: pitch = 127
        
        start_time = i * note_length_sec
        end_time = start_time + (note_length_sec * 0.8) # 80% gate length
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Execute the "Split and Move Up" Macro ===
    # Split the continuous phrase in half
    right_half_item = RPR.RPR_SplitMediaItem(item, split_time_sec)
    
    # Move the split portion up one track to demonstrate the macro
    if right_half_item:
        RPR.RPR_MoveMediaItemToTrack(right_half_item, upper_track)
        
    return f"Created workflow demo '{track_name}': generated {bars} bars of {key} {scale} MIDI, split phrase at {split_time_sec}s, and moved the second half to the track above at {bpm} BPM."
