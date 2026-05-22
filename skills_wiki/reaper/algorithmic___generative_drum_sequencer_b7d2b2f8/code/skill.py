def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic Drums",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    complexity: float = 0.6, # Range: 0.0 to 1.0 (Controls ghost note density & syncopation)
    **kwargs,
) -> str:
    """
    Creates an algorithmic, generative drum pattern replicating step-sequencer logic.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note to anchor the General MIDI drum map (Default 'C' sets Kick to C1/36).
        scale: Unused mechanically for drums, included for parameter compliance.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        complexity: Float from 0.0 to 1.0 driving the generative algorithm's density.
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the generated output.
    """
    import random
    import reaper_python as RPR

    # === Step 1: Initialize Setup & Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
    track_idx = int(RPR.RPR_CountTracks(0))
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: MIDI Mapping (General MIDI based on Key) ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Standardize C1 (36) as the baseline root if 'C' is passed
    base_note = NOTE_MAP.get(key.upper(), 0) + 36 
    
    # Relative General MIDI intervals
    KICK = base_note           # 36
    SNARE = base_note + 2      # 38
    CLOSED_HAT = base_note + 6 # 42
    OPEN_HAT = base_note + 10  # 46

    # === Step 4: Timing & Item Setup ===
    beats_per_bar = 4
    steps_per_beat = 4 # 16th note subdivisions
    total_steps = bars * beats_per_bar * steps_per_beat
    step_len_sec = (60.0 / bpm) / steps_per_beat
    
    item_length = bars * (60.0 / bpm) * beats_per_bar
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Deterministic generation based on complexity parameter
    random.seed(int(complexity * 1000))
    note_count = 0

    # === Step 5: Generative Sequencing Algorithm ===
    for step in range(total_steps):
        step_in_bar = step % 16
        notes_to_add = []
        
        # --- Kick Logic ---
        # Anchor on beat 1. Introduce syncopation based on complexity.
        k_vel = int(velocity_base + random.uniform(-10, 10))
        if step_in_bar == 0:
            notes_to_add.append((KICK, k_vel))
        elif step_in_bar == 8 and complexity > 0.3:
            notes_to_add.append((KICK, int(k_vel * 0.85)))
        elif step_in_bar in [2, 7, 10, 14, 15] and random.random() < (complexity * 0.5):
            notes_to_add.append((KICK, int(k_vel * 0.7))) # Syncopated kick

        # --- Snare Logic ---
        # Anchor on beats 2 and 4. Introduce ghost notes based on complexity.
        s_vel = int(velocity_base + random.uniform(-5, 5))
        if step_in_bar in [4, 12]:
            notes_to_add.append((SNARE, s_vel))
        elif step_in_bar in [7, 9, 13] and random.random() < (complexity * 0.4):
            notes_to_add.append((SNARE, int(s_vel * 0.45))) # Snare ghost note

        # --- Hi-Hat Logic ---
        # Continuous flow with groove dynamics. Open hats appear randomly.
        hat_base_prob = 0.8 if complexity < 0.5 else 1.0
        if random.random() < hat_base_prob:
            # Accent every 8th note, soften off-beat 16ths
            h_vel = int(velocity_base * 0.8 + random.uniform(-10, 10)) if step_in_bar % 2 == 0 else int(velocity_base * 0.6 + random.uniform(-10, 10))
            
            if random.random() < (complexity * 0.25):
                notes_to_add.append((OPEN_HAT, h_vel))
            else:
                notes_to_add.append((CLOSED_HAT, h_vel))

        # --- MIDI Insertion ---
        if notes_to_add:
            proj_time = step * step_len_sec
            start_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time))
            # 80% gate length to avoid note overlaps on the same pitch
            end_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time + step_len_sec * 0.8))
            
            for pitch, vel in notes_to_add:
                vel = max(1, min(127, int(vel))) # Hard clamp to valid MIDI bounds
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                note_count += 1

    # Cleanup and sort MIDI events
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} algorithmic drum hits over {bars} bars at {bpm} BPM (Complexity parameter: {complexity})"
