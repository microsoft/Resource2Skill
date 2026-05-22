def create_electro_syncopated_bass(
    project_name: str = "MyProject",
    track_name: str = "Gritty Electro Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a driving, 16th-note syncopated electro bassline with analog-style grit.

    Args:
        project_name: Project identifier.
        track_name: Name for the created bass track.
        bpm: Tempo in BPM.
        key: Root note (e.g., E, F, G).
        scale: Scale type (minor, dorian, blues recommended).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), higher means more drive.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Default to minor if scale is not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_note = NOTE_MAP.get(key.upper(), 4) # Default to E if not found
    base_midi_note = 24 + base_note # C1 octave for solid bass register

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Program 16th-Note Syncopated Groove ===
    # Format: (16th_step_index, scale_degree_index, octave_offset, duration_in_16ths, velocity_multiplier)
    # This creates a classic push-pull electro rhythm.
    pattern = [
        (0,  0,  0, 1.0, 1.0),  # Beat 1: Root downbeat
        (2,  0,  0, 0.8, 0.8),  # Beat 1: Root syncopation ('&')
        (3,  0,  1, 0.8, 0.9),  # Beat 1: Octave jump up ('a')
        (5,  0,  0, 1.0, 0.9),  # Beat 2: Root syncopation ('e')
        (6,  0,  0, 0.8, 0.8),  # Beat 2: Root syncopation ('&')
        (8,  0,  0, 1.5, 1.0),  # Beat 3: Root downbeat (slightly longer)
        (11, 2,  0, 1.0, 0.8),  # Beat 3: Minor 3rd hit ('a') - degree index 2
        (12, 0,  0, 1.0, 1.0),  # Beat 4: Root downbeat
        (14, 0, -1, 1.0, 0.9),  # Beat 4: Sub octave drop ('&')
    ]

    QN_PPQ = 960 # Standard REAPER Pulses Per Quarter Note
    STEP_PPQ = QN_PPQ // 4 # One 16th note
    
    note_count = 0
    scale_len = len(scale_intervals)

    for bar in range(bars):
        bar_offset_ppq = bar * 16 * STEP_PPQ
        
        for step, degree, oct_offset, dur_steps, vel_mult in pattern:
            start_ppq = bar_offset_ppq + int(step * STEP_PPQ)
            # Gate length is slightly shorter than step duration for staccato feel (0.85)
            end_ppq = start_ppq + int(dur_steps * STEP_PPQ * 0.85) 
            
            # Calculate exact MIDI pitch based on scale rules
            note_degree = degree % scale_len
            octave_shift = (degree // scale_len) + oct_offset
            pitch = base_midi_note + scale_intervals[note_degree] + (octave_shift * 12)
            
            # Ensure pitch and velocity are within valid MIDI range
            pitch = max(0, min(127, pitch))
            vel = int(velocity_base * vel_mult)
            vel = max(1, min(127, vel))
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Sound Design (Synth + Grit) ===
    # Add a raw synthesizer
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add saturation to mimic tube overdrive and provide the gritty texture
    RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    
    # Optionally lower track volume slightly as saturation can increase perceived loudness
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.7) 

    return f"Created '{track_name}' with {note_count} syncopated bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
