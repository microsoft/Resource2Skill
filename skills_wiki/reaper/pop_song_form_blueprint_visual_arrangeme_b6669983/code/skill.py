def create_pattern(
    project_name: str = "SongFormBlueprint",
    track_name: str = "Song Form Chords",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 52,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a full visual and musical Pop Song Form arrangement structure.
    Generates a parent synth track with color-coded child tracks for each section,
    populated with appropriate diatonic chord progressions.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
                "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10]
    }

    def get_chord_notes(degree, scale_intervals, root_midi):
        idx = degree - 1
        notes = []
        # Build a standard triad (root, 3rd, 5th in the chosen scale)
        for i in [0, 2, 4]:
            scale_idx = (idx + i) % len(scale_intervals)
            octave_shift = (idx + i) // len(scale_intervals)
            note = root_midi + scale_intervals[scale_idx] + (octave_shift * 12)
            notes.append(note)
        return notes

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Parent Track (Synth) ===
    parent_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(parent_idx, True)
    parent_track = RPR.RPR_GetTrack(0, parent_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaSynth", False, -1)
    
    # Set parent to act as a folder
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1)

    # === Step 3: Define Sections and Create Child Tracks ===
    section_types = {
        "Intro":  {"color": (70, 130, 180)},  # Steel Blue
        "Verse":  {"color": (60, 179, 113)},  # Sea Green
        "Chorus": {"color": (205, 92, 92)},   # Indian Red
        "Bridge": {"color": (147, 112, 219)}, # Medium Purple
        "Outro":  {"color": (218, 165, 32)}   # Goldenrod
    }
    
    track_refs = {}
    
    for i, (s_name, s_data) in enumerate(section_types.items()):
        child_idx = parent_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(child_idx, True)
        child_track = RPR.RPR_GetTrack(0, child_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(child_track, "P_NAME", s_name, True)
        
        # Apply color mapping (REAPER format: R + G*256 + B*65536 | OS Flag)
        r, g, b = s_data["color"]
        color_int = r + (g * 256) + (b * 65536) | 0x1000000
        RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_CUSTOMCOLOR", color_int)
        
        # The last child track must close the folder depth
        if i == len(section_types) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_FOLDERDEPTH", -1)
            
        track_refs[s_name] = child_track

    # === Step 4: Define Chronological Arrangement Form ===
    # Using 1-based scale degrees for chord progressions
    structure = [
        {"type": "Intro",  "name": "Intro",    "bars": 4, "prog": [1, 1, 1, 1]},
        {"type": "Verse",  "name": "Verse 1",  "bars": 8, "prog": [1, 6, 3, 7, 1, 6, 3, 7]},
        {"type": "Chorus", "name": "Chorus 1", "bars": 8, "prog": [6, 3, 7, 1, 6, 3, 7, 1]},
        {"type": "Verse",  "name": "Verse 2",  "bars": 8, "prog": [1, 6, 3, 7, 1, 6, 3, 7]},
        {"type": "Chorus", "name": "Chorus 2", "bars": 8, "prog": [6, 3, 7, 1, 6, 3, 7, 1]},
        {"type": "Bridge", "name": "Bridge",   "bars": 4, "prog": [4, 5, 6, 7]},
        {"type": "Chorus", "name": "Chorus 3", "bars": 8, "prog": [6, 3, 7, 1, 6, 3, 7, 1]},
        {"type": "Outro",  "name": "Outro",    "bars": 4, "prog": [1, 1, 1, 1]}
    ]

    current_time = 0.0
    bar_length_sec = (60.0 / bpm) * 4
    beat_length_sec = 60.0 / bpm
    
    root_midi = NOTE_MAP.get(key, 48)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # === Step 5: Generate Items and MIDI ===
    for sec in structure:
        sec_length_sec = sec["bars"] * bar_length_sec
        target_track = track_refs[sec["type"]]
        
        # Create a dedicated MIDI item for this specific section on the corresponding track
        item = RPR.RPR_CreateNewMIDIItemInProj(target_track, current_time, current_time + sec_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", sec["name"], True)
        
        # Apply the section color to the item to make the form pop visually
        r, g, b = section_types[sec["type"]]["color"]
        color_int = r + (g * 256) + (b * 65536) | 0x1000000
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", color_int)
        
        # Populate the item with chords
        for i, degree in enumerate(sec["prog"]):
            chord_start = current_time + (i * bar_length_sec)
            # Leave a 1/16th note gap for articulation
            chord_end = chord_start + bar_length_sec - (beat_length_sec * 0.25) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_end)
            
            notes = get_chord_notes(degree, scale_intervals, root_midi)
            for note in notes:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, None)
                
        RPR.RPR_MIDI_Sort(take)
        current_time += sec_length_sec
        
    return f"Created Pop Song Blueprint with 8 labeled sections across 5 grouped tracks in {key} {scale} at {bpm} BPM."
