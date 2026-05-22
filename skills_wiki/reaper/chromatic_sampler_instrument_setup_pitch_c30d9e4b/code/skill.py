def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pitched Chop Sampler",
    bpm: int = 110,
    key: str = "D",
    scale: str = "pentatonic_minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a track with ReaSamplOmatic5000 and a syncopated, staccato MIDI pattern 
    designed for chopped samples. 

    Note: Drag your own audio sample into the RS5K interface and set the mode to 
    'Semitone shifted' to complete the tutorial's effect. ReaSynth is included as 
    a temporary fallback so the pattern makes sound immediately.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain ===
    # Add the Sampler from the tutorial
    RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
    # Add ReaSynth as a fallback so the MIDI clip produces sound before a sample is loaded
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Syncopated 16th-note rhythm grid for "chopped" feel
    # Format: (16th note position, duration in 16ths, scale degree index)
    rhythm_grid = [
        (0, 1, 0),    # Beat 1
        (3, 1, 2),    # Beat 1 'a' (syncopation)
        (6, 1, 1),    # Beat 2 'and' (syncopation)
        (8, 1, 0),    # Beat 3
        (11, 1, 3),   # Beat 3 'a' (syncopation)
        (14, 1, 4)    # Beat 4 'and' (syncopation)
    ]

    sixteenth_sec = bar_length_sec / 16.0
    root_midi = 60 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    
    note_count = 0

    # === Step 5: Insert MIDI Notes ===
    for bar in range(bars):
        bar_offset_sec = bar * bar_length_sec
        for pos, dur, degree in rhythm_grid:
            # Calculate timing in seconds
            start_sec = bar_offset_sec + (pos * sixteenth_sec)
            # Multiply duration by 0.6 to make it sharply staccato, forcing RS5K "note-off" behavior
            end_sec = start_sec + (dur * sixteenth_sec * 0.6)  
            
            # Convert to PPQ for REAPER API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Calculate Pitch
            octave = degree // len(scale_intervals)
            note_idx = degree % len(scale_intervals)
            pitch = root_midi + (octave * 12) + scale_intervals[note_idx]
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} staccato notes over {bars} bars at {bpm} BPM. Please open RS5K to drag in a sample."
