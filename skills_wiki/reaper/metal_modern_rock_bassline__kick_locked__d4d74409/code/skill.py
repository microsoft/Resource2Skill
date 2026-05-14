def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass (Kick Locked)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Kick-Locked Metal Bassline with octave jumps in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (Set to 110 to tame harsh pick attack).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Metal bass typically sits in the 1st or 0th octave depending on tuning.
    # We will set the root to Octave 1 (MIDI notes 24-35).
    root_midi = NOTE_MAP.get(key, 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qn_length = 60.0 / bpm
    bar_length_sec = qn_length * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create the MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # Breakdown / Double-kick syncopated pattern
    # Format: (beat_start, length_in_beats, is_octave_jump)
    kick_pattern = [
        (0.0,  0.25, False), # 1 e
        (0.75, 0.25, False), #   a
        (1.5,  0.25, False), # 2 &
        (2.0,  0.25, True),  # 3   (Accent! Octave jump)
        (2.5,  0.5,  False), # 3 & (Sustain)
        (3.5,  0.25, False), # 4 &
        (3.75, 0.25, False)  #   a
    ]

    # === Step 4: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        for beat_start, length, is_octave in kick_pattern:
            # Calculate absolute beat positions
            abs_beat_start = (bar * beats_per_bar) + beat_start
            abs_beat_end = abs_beat_start + length
            
            # Convert to seconds
            start_time = abs_beat_start * qn_length
            end_time = abs_beat_end * qn_length
            
            # Convert to PPQ (Pulses Per Quarter Note) for the MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Apply pitch logic (+12 for octave jumps)
            pitch = root_midi + 12 if is_octave else root_midi
            
            # Ensure velocity doesn't exceed 127
            vel = max(1, min(127, velocity_base))

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Dynamics Control) ===
    # Add ReaSynth as a temporary placeholder tone so it makes sound immediately
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add ReaComp to aggressively pin the dynamics (common in metal bass)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Set Ratio to 8:1 (param 3: ratio is roughly represented by standard normalized curves, ~0.25 for high ratio)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 3, 0.25)
    # Set fast attack (param 4) to clamp transients
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 4, 0.05)
    # Pull threshold down (param 0)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 0, 0.4) 

    return f"Created '{track_name}' with {note_count} syncopated notes over {bars} bars at {bpm} BPM. (Note: Load your favorite Bass VST over ReaSynth for best results)."
