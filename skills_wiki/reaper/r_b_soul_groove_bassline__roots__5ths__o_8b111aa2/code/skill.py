def create_pattern(
    project_name: str = "ViralBass",
    track_name: str = "RnB_Groove_Bass",
    bpm: int = 95,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates an R&B/Soul bassline using Roots, Octaves, Perfect 5ths, and Passing Notes.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, F#, Bb).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the generated bassline.
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

    # === Step 2: Create Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth for the Bass Tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a fatter bass sound (Increase Sawtooth and Square mix)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.8) # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4) # Square mix

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Musical Pattern ===
    # Set base pitch to the 2nd octave for bass
    base_pitch = NOTE_MAP.get(key, 0) + 36 
    
    # Define a classic progression to groove over
    # If minor context, use iv -> i (like the video's Fm9 -> Cm9)
    # If major context, use ii -> vi
    is_minor = scale in ["minor", "dorian", "harmonic_minor", "pentatonic_minor", "blues"]
    progression_degrees = [3, 0] if is_minor else [1, 5] 

    note_count = 0

    for bar in range(bars):
        # Determine the root of the current chord in the progression
        current_degree = progression_degrees[bar % len(progression_degrees)]
        chord_root_pitch = base_pitch + SCALES.get(scale, SCALES["minor"])[current_degree]

        # Syncopated rhythm pattern based on the instructor's drills
        # Format: (start_beat, duration_beats, pitch_interval_from_root, velocity_offset)
        rhythm_pattern = [
            (0.0,  1.0,   0,   0),    # Beat 1: Solid Root note
            (1.0,  0.5,   0,  -10),   # Beat 2: Quick Root pickup
            (1.5,  0.5,  12,  -5),    # Beat 2.5 ("&"): Syncopated Octave pop
            (2.0,  0.75,  7,  -5),    # Beat 3: Perfect 5th 
            (2.75, 0.25,  0,  -15),   # Beat 3.75 ("a"): 16th note Root ghost note
            (3.0,  1.0,  -2,  -10),   # Beat 4: The minor 7th passing note leading to next bar
        ]

        for start_b, dur_b, pitch_offset, vel_offset in rhythm_pattern:
            # Calculate precise timing
            start_time = (bar * bar_length_sec) + (start_b * beat_length_sec)
            end_time = start_time + (dur_b * beat_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Apply pitch and velocity math
            pitch = chord_root_pitch + pitch_offset
            vel = max(1, min(127, velocity_base + vel_offset))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' bassline with {note_count} syncopated notes over {bars} bars at {bpm} BPM."
