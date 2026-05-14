def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Drums",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    density: float = 0.6,
    swing: float = 0.25,
    **kwargs,
) -> str:
    """
    Create an Algorithmic Probabilistic Drum Generator in the current REAPER project.
    Mimics the behavior of generative MIDI drum plugins.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Unused for drum generator.
        scale: Unused for drum generator.
        bars: Number of bars to generate.
        density: Float (0.0 to 1.0). Higher values generate more syncopations/ghost notes.
        swing: Float (0.0 to 1.0). Delays off-beat 16th notes.
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the generated pattern.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    total_len_sec = bars * beats_per_bar * beat_len_sec

    # Create new MIDI item and retrieve the active take
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_len_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Algorithmic Note Generation ===
    step_sec = beat_len_sec / 4.0  # Length of a 16th note in seconds
    note_count = 0

    # General MIDI standard drum mapping
    KICK = 36
    SNARE = 38
    HAT_CLOSED = 42
    HAT_OPEN = 46

    for bar in range(bars):
        for step in range(16):
            # Calculate base time in seconds for this step
            step_time = (bar * beats_per_bar * beat_len_sec) + (step * step_sec)
            
            # Apply swing to odd 16th steps (off-beats)
            if step % 2 != 0:
                step_time += swing * (step_sec * 0.33)  # Max swing pushes it to triplet feel
                
            # Convert physical time to absolute PPQ position
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, step_time)
            
            # Define end points (durations)
            end_ppq_short = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, step_time + step_sec * 0.5)
            end_ppq_standard = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, step_time + step_sec * 0.8)
            end_ppq_long = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, step_time + step_sec * 1.5)

            # --- KICK GENERATION ---
            p_kick = 0.0
            if step == 0: p_kick = 1.0                                # Solid downbeat
            elif step == 8: p_kick = 0.8                              # Solid beat 3
            elif step in [2, 6, 10, 14]: p_kick = density * 0.6       # 8th-note offbeats
            else: p_kick = density * 0.2                              # 16th-note syncopations

            if random.random() < p_kick:
                vel = random.randint(90, 110) if step in [0, 8] else random.randint(60, 85)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq_standard, 0, KICK, vel, True)
                note_count += 1

            # --- SNARE GENERATION ---
            p_snare = 0.0
            if step in [4, 12]: p_snare = 1.0                         # Backbeat on 2 and 4
            elif step in [7, 15]: p_snare = density * 0.5             # Drag/ghost notes right before kicks/snares
            else: p_snare = density * 0.15                            # Sparse random ghosts

            if random.random() < p_snare:
                vel = random.randint(100, 120) if step in [4, 12] else random.randint(40, 70)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq_standard, 0, SNARE, vel, True)
                note_count += 1

            # --- HI-HAT GENERATION ---
            p_hat = 0.0
            if step % 2 == 0: p_hat = 0.8 + (density * 0.2)           # Solid 8th notes
            else: p_hat = density * 0.9                               # Fill in 16th notes based on density
            
            if random.random() < p_hat:
                # Decide if it's an open hat (higher chance on upbeats)
                is_open = (random.random() < density * 0.3) and (step % 2 != 0)
                pitch = HAT_OPEN if is_open else HAT_CLOSED
                vel = random.randint(70, 95) if step % 2 == 0 else random.randint(50, 75)
                duration_ppq = end_ppq_long if is_open else end_ppq_short
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, duration_ppq, 0, pitch, vel, True)
                note_count += 1

    # Sort the MIDI stream after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Mix FX Scaffold ===
    # Add an EQ and Compressor to set up a basic drum bus for when the user loads a VSTi
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    if comp_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -12.0)  # Threshold
        RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 3.0)    # Ratio
        RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 5.0)    # Attack (ms)
        RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 100.0)  # Release (ms)

    return f"Created '{track_name}' with {note_count} algorithmically generated notes over {bars} bars at {bpm} BPM (Density: {density})."
