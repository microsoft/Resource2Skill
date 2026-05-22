def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic Pluck",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Algorithmic Syncopated Pluck Sequence in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    # Set up tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create new track additively
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add stock synthesizer
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Pitch logic
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    base_midi_note = 36 + root_val # Start lower (C2) for bass/pluck feel

    def get_note_in_scale(degree_index):
        """Safely fetch a pitch based on scale array length to avoid index errors."""
        idx = degree_index % len(scale_intervals)
        return base_midi_note + scale_intervals[idx]

    # Rhythm pattern: 3+3+3+3+4 syncopation relative to beats
    # Beats: 0.0 (1), 0.75 (4), 1.5 (7), 2.25 (10), 3.0 (13)
    note_pattern_def = [
        (0.00, get_note_in_scale(0)),           # Downbeat Root
        (0.75, get_note_in_scale(0)),           # Syncopated Root
        (1.50, get_note_in_scale(0) + 12),      # Octave jump
        (2.25, get_note_in_scale(4)),           # Approx 5th degree
        (3.00, get_note_in_scale(2))            # Approx 3rd degree
    ]

    note_count = 0
    note_duration_beats = 0.25 # Staccato 16th note for pluck effect

    # Generate sequence across all bars
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        for beat_pos, pitch in note_pattern_def:
            start_pos_beats = bar_offset_beats + beat_pos
            end_pos_beats = start_pos_beats + note_duration_beats
            
            # Convert beats to time, then to PPQ for the MIDI API
            start_time = start_pos_beats * (60.0 / bpm)
            end_time = end_pos_beats * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Alternate velocity slightly for humanization
            vel = velocity_base if beat_pos == 0.0 else max(10, velocity_base - 15)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} algorithmic pluck notes over {bars} bars at {bpm} BPM in {key} {scale}."
