def create_pattern(
    project_name: str = "MusicalNotationDemo",
    track_name: str = "Piano Score",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Creates a syncopated, two-handed piano chord progression and opens it 
    in REAPER's Musical Notation view.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    if scale not in SCALES:
        scale = "major"

    # === Step 1: Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Deselect all existing tracks to ensure our new item is the only one selected later
    for i in range(RPR.RPR_CountTracks(0)):
        t = RPR.RPR_GetTrack(0, i)
        RPR.RPR_SetMediaTrackInfo_Value(t, "I_SELECTED", 0)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_SELECTED", 1)
    
    # Add simple synth to hear the chords
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower volume to avoid clipping with chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_qn = bars * beats_per_bar
    item_length_sec = RPR.RPR_TimeMap2_QNToTime(0, item_length_qn)
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 4: Generate Syncopated Piano MIDI ===
    root_midi = 60 + NOTE_MAP.get(key, 0) # Middle C baseline (C4)
    scale_intervals = SCALES[scale]
    
    # Progression: I - vi - IV - V (diatonic scale degrees, 0-indexed)
    progression = [0, 5, 3, 4] 
    
    # Rhythm: Start QN, End QN (Syncopated pattern)
    rhythm = [
        (0.0, 1.0),   # Beat 1 
        (1.5, 2.5),   # Beat 2 "and"
        (3.0, 4.0)    # Beat 4
    ]

    def get_piano_voicing(degree, root_note, intervals):
        notes = []
        # Bass note (1 octave down from root position)
        bass_oct = (degree // len(intervals)) - 1
        notes.append(root_note + (bass_oct * 12) + intervals[degree % len(intervals)])
        
        # Right hand triad
        for offset in [0, 2, 4]:
            idx = degree + offset
            oct_shift = idx // len(intervals)
            notes.append(root_note + (oct_shift * 12) + intervals[idx % len(intervals)])
        return notes

    for bar in range(bars):
        degree = progression[bar % len(progression)]
        chord_notes = get_piano_voicing(degree, root_midi, scale_intervals)
        
        for start_offset, end_offset in rhythm:
            start_qn = (bar * beats_per_bar) + start_offset
            end_qn = (bar * beats_per_bar) + end_offset
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            for pitch in chord_notes:
                # Ensure pitch is within valid MIDI range
                pitch = max(0, min(127, int(pitch)))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Open in Notation View ===
    # Select only our new item
    RPR.RPR_SelectAllMediaItems(0, False)
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Command 40153: Item: Open in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Get the active MIDI editor window
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        # Command 40956 (in MIDI Editor context): View: Mode: musical notation
        RPR.RPR_MIDIEditor_OnCommand(editor, 40956)

    return f"Created '{track_name}' with {bars} bars of syncopated piano chords at {bpm} BPM and opened in Notation View."
