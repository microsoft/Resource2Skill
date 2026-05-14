def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Sub Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a generative-style 16th-note sub-bass pattern and FX chain.
    Approximates the workflow of an algorithmic sequencer driving an analog sub-bass.
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

    # Normalize inputs
    key = key.upper()
    if key not in NOTE_MAP:
        key = "C"
    scale_name = scale.lower()
    scale_intervals = SCALES.get(scale_name, SCALES["minor"])

    # Setup basic timing
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    step_length_sec = bar_length_sec / 16.0  # 1/16th note grid
    item_length = bar_length_sec * bars

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Base pitch in Octave 1 for sub-bass (MIDI note 24 = C1)
    base_midi_note = NOTE_MAP[key] + 24 

    # Generative sequence matrix mimicking an algorithmic sequencer
    # Format: (16th_step_index, scale_degree_index, octave_offset, velocity_pct, gate_length_steps)
    sequence = [
        (0, 0, 0, 100, 1.0),   # Downbeat Root
        (2, 0, 0, 85, 0.8),    # Offbeat Root
        (3, 0, 1, 110, 0.5),   # Syncopated Octave Jump
        (5, 0, 0, 90, 0.8),    # Root
        (6, 4, 0, 100, 1.0),   # Syncopated 5th
        (8, 0, 0, 100, 1.0),   # Downbeat Root
        (10, 0, 0, 85, 0.8),   # Offbeat Root
        (11, 2, 0, 95, 0.8),   # Syncopated 3rd (passing tone)
        (13, 0, 0, 90, 0.8),   # Root
        (14, 0, 0, 100, 1.0)   # Root leading into next bar
    ]

    # === Step 3: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        
        for step, degree_idx, oct_offset, vel_pct, dur_steps in sequence:
            # Calculate pitch based on scale
            safe_degree = degree_idx % len(scale_intervals)
            pitch = base_midi_note + scale_intervals[safe_degree] + (oct_offset * 12)
            
            # Calculate timing
            start_time = bar_start_time + (step * step_length_sec)
            end_time = start_time + (dur_steps * step_length_sec * 0.8) # 80% gate length for plucky feel
            
            # Convert time to PPQ for MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Calculate velocity
            vel = int(velocity_base * (vel_pct / 100.0))
            vel = max(1, min(127, vel))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design FX Chain ===
    # Add ReaSynth for the raw sub-bass waveform
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add ReaEQ to shape the tone (Low Pass Filter to simulate the SubTractor)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # We leave the specific parameter tweaking to default or manual adjustment 
    # to maintain API compatibility across REAPER versions, but the basic 
    # Sine/Square mix of default ReaSynth paired with EQ creates a solid sub.

    return f"Created '{track_name}' generative bassline with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
