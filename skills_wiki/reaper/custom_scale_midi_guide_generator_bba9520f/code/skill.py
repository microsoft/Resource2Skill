def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 4,
    velocity_base: int = 100,
    octave_start: int = 2,
    octave_end: int = 5,
    **kwargs,
) -> str:
    """
    Create Custom Scale MIDI Guide Generator in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, whole_tone, dorian, etc.).
        bars: Number of bars the guide item should span.
        velocity_base: Base MIDI velocity (0-127).
        octave_start: The lowest octave to generate guide notes for.
        octave_end: The highest octave to generate guide notes for.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated scale guide track.
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
        "melodic_minor":    [0, 2, 3, 5, 7, 9, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "locrian":          [0, 1, 3, 5, 6, 8, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    full_track_name = f"{track_name} ({key} {scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Use specialized ReaScript function to create a ready-to-use MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    
    # Mute the item so it doesn't output sound, fulfilling its purpose as a silent UI guide
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0) 
    
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Scale Notes ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    note_count = 0
    for oct in range(octave_start, octave_end + 1):
        for interval in scale_intervals:
            # Calculate standard MIDI pitch (octave 4 usually equates to middle C / note 60)
            pitch = (oct + 1) * 12 + root_pitch + interval
            
            if 0 <= pitch <= 127:
                # Insert sustained notes that span the entire item
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)

    return f"Created guide track '{full_track_name}' with {note_count} muted notes over {bars} bars at {bpm} BPM."
