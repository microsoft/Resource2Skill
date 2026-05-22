def create_pattern(
    project_name: str = "NotationDemo",
    track_name: str = "Piano Notation",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a I-vi-IV-V progression and open it in REAPER's Musical Notation view.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (loops the 4-bar progression).
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Lower volume to avoid clipping with chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Add FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    item_length = beat_len * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Define 4-Bar Musical Pattern ===
    # Format: [(start_beat, end_beat, scale_degree, velocity), ...]
    chords_pattern = [
        # Bar 0 (I)
        [(0.0, 4.0, 7, velocity_base - 20), (0.0, 4.0, 9, velocity_base - 20), (0.0, 4.0, 11, velocity_base - 20)],
        # Bar 1 (vi)
        [(0.0, 4.0, 5, velocity_base - 20), (0.0, 4.0, 7, velocity_base - 20), (0.0, 4.0, 9, velocity_base - 20)],
        # Bar 2 (IV)
        [(0.0, 4.0, 3, velocity_base - 20), (0.0, 4.0, 5, velocity_base - 20), (0.0, 4.0, 7, velocity_base - 20)],
        # Bar 3 (V)
        [(0.0, 4.0, 4, velocity_base - 20), (0.0, 4.0, 6, velocity_base - 20), (0.0, 4.0, 8, velocity_base - 20)]
    ]
    
    melody_pattern = [
        # Bar 0
        [(0.0, 2.0, 14, velocity_base), (2.0, 3.0, 12, velocity_base), (3.0, 4.0, 11, velocity_base)],
        # Bar 1
        [(0.0, 4.0, 14, velocity_base)],
        # Bar 2
        [(0.0, 2.0, 10, velocity_base), (2.0, 4.0, 12, velocity_base)],
        # Bar 3
        [(0.0, 2.0, 11, velocity_base), (2.0, 4.0, 13, velocity_base)]
    ]

    # === Step 6: Generate MIDI Notes ===
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.upper(), 0)
    root_midi = 48 + root_val # Base octave around C3
    
    def get_midi_pitch(degree):
        octave = degree // len(scale_intervals)
        scale_degree = degree % len(scale_intervals)
        return root_midi + (octave * 12) + scale_intervals[scale_degree]

    note_count = 0
    for b in range(bars):
        bar_idx = b % 4
        offset_beats = b * beats_per_bar
        
        # Combine chords and melody for the current bar
        bar_notes = chords_pattern[bar_idx] + melody_pattern[bar_idx]
        
        for start_b, end_b, deg, vel in bar_notes:
            proj_time_start = (start_b + offset_beats) * beat_len
            proj_time_end = (end_b + offset_beats) * beat_len
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time_end)
            
            pitch = get_midi_pitch(deg)
            pitch = max(0, min(127, int(pitch)))
            vel = max(1, min(127, int(vel)))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 7: Open in Notation View ===
    # Unselect all items, then select ours
    RPR.RPR_Main_OnCommand(40289, 0) 
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "View: Mode: musical notation" in the active MIDI editor
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        RPR.RPR_MIDIEditor_OnCommand(editor, 40458)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM, and opened in Notation View."
