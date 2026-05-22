def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Programmed Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Kick-Locked Bass pattern with Octave Variations.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (capped around 110 per the tutorial to avoid clank).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Setup FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth as a stock placeholder for a virtual bass instrument
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Lower track volume to avoid clipping since ReaSynth defaults are loud
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.25) # Approx -12dB

    # === Step 3: Define Pitch and Rhythm ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Drop to Octave 1 for a deep bass sound (MIDI note 24 = C1)
    base_note = NOTE_MAP.get(key.upper(), 0) + 24 

    # 2-bar syncopated metal/rock pattern simulating a kick drum groove
    # Format: (start_beat, length_beats, is_octave_jump)
    pattern_loop = [
        # Bar 1
        (0.0, 0.25, False),
        (0.5, 0.25, False),
        (1.25, 0.25, False),
        (2.0, 0.25, False),
        (2.5, 0.25, True),   # Octave jump variation
        (3.0, 0.25, False),
        (3.5, 0.25, False),
        
        # Bar 2
        (4.0, 0.25, False),
        (4.5, 0.25, False),
        (5.25, 0.25, True),  # Octave jump variation
        (6.0, 0.25, False),
        (6.5, 0.25, False),
        (7.0, 0.125, False), # 32nd note gallop
        (7.25, 0.125, False),
        (7.5, 0.25, False),
    ]

    # Generate full sequence across desired bars
    full_pattern = []
    for b in range(0, bars, 2):
        for note in pattern_loop:
            start_b, len_b, oct_jump = note
            if b + (start_b / 4) < bars: # Prevent writing past requested bars
                full_pattern.append((start_b + b*4, len_b, oct_jump))

    # === Step 4: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    beat_sec = 60.0 / bpm
    
    # Cap velocity to avoid harsh sampler layers as taught in tutorial
    vel = min(120, max(1, velocity_base))

    for start_b, len_b, oct_jump in full_pattern:
        start_time = start_b * beat_sec
        end_time = (start_b + len_b) * beat_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Apply +12 semitones if this note is an octave jump
        pitch = base_note + 12 if oct_jump else base_note
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {len(full_pattern)} notes locked to rhythm over {bars} bars at {bpm} BPM."
