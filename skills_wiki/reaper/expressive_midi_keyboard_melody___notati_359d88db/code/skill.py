def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a velocity-sensitive keyboard melody and open it in Notation View.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) to anchor the dynamic variations.
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the operation.
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

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a basic synth so the keyboard track makes sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Humanized Melody ===
    base_pitch = 60 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_pitch(degree):
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return base_pitch + (octave * 12) + scale_intervals[idx]

    def insert_note(start_qn, duration_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn + duration_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # A simple, expressive 2-bar phrase mapping: (Scale Degree, Duration in Quarter Notes, Velocity Offset)
    phrase = [
        (0, 1.0, 10),   # Downbeat tonic (Hit slightly harder)
        (2, 0.5, -10),  # Upbeat passing 3rd (Softer)
        (4, 0.5, 5),    # Arp up to 5th
        (5, 1.0, 15),   # Emphasized 6th
        (4, 1.0, 0),    # Resolve to 5th
        (3, 0.5, -5),   # Walk down 4th
        (1, 0.5, -15),  # Walk down 2nd (Ghost note feel)
        (0, 3.0, 20),   # Final held tonic resolution
    ]
    
    current_qn = 0.0
    notes_added = 0
    
    # Loop the phrase to fill the specified number of bars
    while current_qn < bars * beats_per_bar:
        for degree, dur, vel_off in phrase:
            if current_qn >= bars * beats_per_bar:
                break
            
            pitch = int(max(0, min(127, get_pitch(degree))))
            vel = int(max(1, min(127, velocity_base + vel_off)))
            actual_dur = min(dur, (bars * beats_per_bar) - current_qn)
            
            insert_note(current_qn, actual_dur, pitch, vel)
            
            current_qn += dur
            notes_added += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    # === Step 5: Open in Notation View (Core Feature Demonstration) ===
    # Unselect all items, then select our new item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # Action ID 40954: View: Mode: musical notation
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40954)

    return f"Created '{track_name}' with {notes_added} velocity-sensitive notes over {bars} bars at {bpm} BPM, and opened in Notation View."
