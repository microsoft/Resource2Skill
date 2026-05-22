def create_pattern(
    project_name: str = "MetalProject",
    track_name: str = "MIDI Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 127,
    **kwargs,
) -> str:
    """
    Create a Metal/Djent MIDI Bass rhythm track in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for accents.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note mapping to identify the lowest bass root note (targeting C1/C2 range)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Place root note in the bass range (C1 = 24)
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a stock ReaSynth to act as a placeholder bass
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Volume Mix
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 1.0) # Sawtooth waveform
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1) # Short decay for tight staccato sound

    # === Step 3: Setup MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Syncopated Metal Rhythm ===
    step_len_qn = 0.25 # One 16th note in REAPER Quarter Notes (QN)
    
    # Pattern layout: (start_step, duration_steps, is_accent, octave_offset)
    # Using 16 steps per bar
    # 'duration_steps' is slightly less than actual grid spacing to create tight gating
    bar_standard = [
        (0, 1.6, True, 0),   # Downbeat accent
        (2, 1.6, True, 0),   # 8th note accent
        (4, 0.8, False, 0),  # Consecutive fast 16ths (lowered velocity)
        (5, 0.8, False, 0),
        (6, 1.6, True, 0),
        (8, 1.6, True, 0),
        (10, 1.6, True, 0),
        (12, 0.8, False, 0),
        (13, 0.8, False, 0),
        (14, 1.6, True, 0),
    ]
    
    # Variation with Octave leaps mirroring a fretboard fill
    bar_fill = [
        (0, 1.6, True, 0),
        (2, 1.6, True, 0),
        (4, 0.8, False, 0),
        (5, 0.8, False, 0),
        (6, 1.6, True, 0),
        (8, 1.6, True, 0),
        (10, 1.6, True, 0),
        (12, 0.8, False, 1), # +1 Octave Jump (+12 semitones)
        (13, 0.8, False, 1), # +1 Octave Jump
        (14, 1.6, True, 1),  # +1 Octave Jump accent
    ]

    # === Step 5: Insert MIDI Notes ===
    total_notes = 0
    for bar in range(bars):
        # Apply the fill pattern on every even bar (2nd, 4th, etc.)
        current_pattern = bar_fill if (bar % 2 == 1) else bar_standard
        
        for step_start, step_dur, is_accent, oct_offset in current_pattern:
            # Calculate positions in QN
            start_pos_qn = (bar * beats_per_bar) + (step_start * step_len_qn)
            end_pos_qn = start_pos_qn + (step_dur * step_len_qn)
            
            # Convert QN to exact PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_pos_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_pos_qn)
            
            # Apply Pitch
            pitch = root_pitch + (oct_offset * 12)
            
            # Apply Velocity Rule (Accents = 127, Fast Notes = ~110)
            velocity = min(127, velocity_base) if is_accent else max(1, velocity_base - 17)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)
            total_notes += 1
            
    # Clean up and notify arrange view
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()
    
    return f"Created '{track_name}' with {total_notes} notes over {bars} bars at {bpm} BPM (Tuned to {key}1)."
