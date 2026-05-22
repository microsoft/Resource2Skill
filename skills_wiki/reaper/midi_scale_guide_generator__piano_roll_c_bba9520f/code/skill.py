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
    Creates a muted Scale Guide track populated with every note in the selected scale 
    across all octaves. This enables the "Hide unused note rows" Piano Roll workflow.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate the guide block for.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the created scale guide.
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

    # Validate inputs
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_key = scale.lower()
    scale_intervals = SCALES.get(scale_key, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Muted Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Format a descriptive name
    full_track_name = f"{track_name} ({key} {scale_key})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Explicitly MUTE the track so the guide block doesn't make sound
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    # Insert new MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Convert project time to MIDI PPQ (Pulses Per Quarter Note) for note insertion
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)

    # === Step 4: Insert All Diatonic Notes ===
    note_count = 0
    # Iterate through all standard MIDI octaves (0 to 10)
    for octave in range(11): 
        for interval in scale_intervals:
            pitch = (octave * 12) + root_val + interval
            
            # Ensure we don't exceed the max MIDI note (127)
            if pitch <= 127:
                # Insert note: take, selected, muted, start_ppq, end_ppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1

    # Sort MIDI events after batch insertion for optimal performance
    RPR.RPR_MIDI_Sort(take)

    return (f"Created muted '{full_track_name}' guide track with {note_count} notes over {bars} bars. "
            f"Select this item, open the MIDI Editor, and trigger action 'View: Hide unused note rows'.")
