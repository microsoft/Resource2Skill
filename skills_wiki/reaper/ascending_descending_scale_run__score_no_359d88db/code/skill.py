def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard Score Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an ascending and descending 8th-note scale run in the current REAPER project.
    This pattern is ideal for testing instruments and demonstrating REAPER's Musical Notation view.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored for this specific structural skill (hardcoded to 2 bars for the run).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
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

    # Format key and get base pitch (Middle C / C4 = 60)
    key_formatted = key.capitalize()
    if key_formatted not in NOTE_MAP:
        key_formatted = "C"
    
    root_pitch = 60 + NOTE_MAP[key_formatted]
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # Construct the sequence of pitches (Ascending + Octave + Descending)
    pitches = []
    # Ascending
    for iv in scale_intervals:
        pitches.append(root_pitch + iv)
    # The Octave
    pitches.append(root_pitch + 12)
    # Descending
    for iv in reversed(scale_intervals):
        pitches.append(root_pitch + iv)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_GetNumTracks()
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a basic synth instrument to monitor the playback
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qn_length = 60.0 / bpm
    
    item_position = 0.0
    item_length_sec = qn_length * beats_per_bar * 2  # Exactly 2 bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, item_position, item_position + item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Insert notes
    current_beat = 0.0
    for i, pitch in enumerate(pitches):
        # 8th notes (0.5 beats) for everything except the last note
        # The final root note is held for a 1/4 note (1.0 beats) to elegantly conclude Bar 2
        note_length_beats = 1.0 if i == len(pitches) - 1 else 0.5
        
        start_time = item_position + (current_beat * qn_length)
        end_time = start_time + (note_length_beats * qn_length)
        
        # Convert times to MIDI ticks (PPQ)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Insert the note
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
        current_beat += note_length_beats
        
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {len(pitches)} notes (Ascending/Descending {key_formatted} {scale} run) over 2 bars at {bpm} BPM."
