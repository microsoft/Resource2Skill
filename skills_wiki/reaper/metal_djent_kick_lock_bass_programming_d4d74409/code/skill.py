def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Kick-Lock Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal/Djent Kick-Lock Bass sequence in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (110-150 recommended for this style).
        key: Root note (e.g., "C" for Drop C tuning).
        scale: Scale type (affects the fret jumps).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (fixed to 110 per tutorial to avoid harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Insert a placeholder synth (User should replace this with DjinnBass or MODO Bass)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define root note in the lowest register (e.g., C1 = MIDI 24)
    base_midi_note = 24 + NOTE_MAP.get(key, 0)
    
    # Define syncopated rhythm patterns (Start QN, Length QN, Pitch Offset)
    # Bar A: Pure percussive pedal on the root note mimicking a kick drum breakdown
    pattern_bar_a = [
        (0.0, 0.5, 0),    # Beat 1 (legato impact)
        (0.75, 0.25, 0),  # Beat 1a (staccato)
        (1.0, 0.25, 0),   # Beat 2 (staccato)
        (1.25, 0.25, 0),  # Beat 2e (staccato)
        (1.5, 0.5, 0),    # Beat 2& (legato)
        (2.5, 0.25, 0),   # Beat 3& (staccato)
        (2.75, 0.25, 0),  # Beat 3a (staccato)
        (3.0, 0.5, 0),    # Beat 4 (legato)
    ]
    
    # Bar B: Same rhythm, but incorporates 12th fret (+12) and 3rd fret (+3) jumps 
    # to mirror a hypothetical guitar riff as advised in the tutorial
    pattern_bar_b = [
        (0.0, 0.5, 0),    # Beat 1
        (0.75, 0.25, 0),  # Beat 1a
        (1.0, 0.25, 12),  # Beat 2  -> OCTAVE JUMP
        (1.25, 0.25, 12), # Beat 2e -> OCTAVE JUMP
        (1.5, 0.5, 0),    # Beat 2&
        (2.5, 0.25, 3),   # Beat 3& -> MINOR 3RD JUMP
        (2.75, 0.25, 3),  # Beat 3a -> MINOR 3RD JUMP
        (3.0, 0.5, 0),    # Beat 4
    ]

    qn_per_bar = 4.0
    note_count = 0

    # === Step 4: Insert Notes ===
    for b in range(bars):
        bar_offset = b * qn_per_bar
        # Alternate between the pedal pattern and the jump pattern
        current_pattern = pattern_bar_a if b % 2 == 0 else pattern_bar_b
        
        for start_qn, len_qn, pitch_offset in current_pattern:
            # Convert Quarter Notes (Beats) to Seconds
            start_sec = ((start_qn + bar_offset) / bpm) * 60.0
            end_sec = ((start_qn + len_qn + bar_offset) / bpm) * 60.0
            
            # Convert Seconds to Project Pulse Quarter (PPQ) for ReaScript MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            note_pitch = base_midi_note + pitch_offset
            
            # Insert the note. Crucially, velocity is forced to `velocity_base` (110)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note_pitch), velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} bass notes over {bars} bars at {bpm} BPM (Velocity strictly at {velocity_base} to reduce harshness)."
