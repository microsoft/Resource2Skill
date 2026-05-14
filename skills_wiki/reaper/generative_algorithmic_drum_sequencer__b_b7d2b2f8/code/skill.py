def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic Drums (GM)",
    bpm: int = 120,
    key: str = "C",  # Unused for standard GM drums
    scale: str = "minor", # Unused for standard GM drums
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a generative/algorithmic drum pattern in the style of Reason's Beat Map.
    Outputs standard General MIDI drum notes.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Unused for GM drums.
        scale: Unused for GM drums.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Can accept 'complexity' (0.0 to 1.0) to increase off-beat hits.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

    # Extract complexity parameter to control algorithmic density (0.0 = basic beat, 1.0 = highly syncopated)
    complexity = float(kwargs.get("complexity", 0.5))

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

    # GM Drum Map Constants
    KICK = 36
    SNARE = 38
    CHAT = 42

    steps_per_bar = 16
    step_sec = (60.0 / bpm) / 4.0 # 16th note duration

    note_count = 0

    # === Step 4: Algorithmic Generation Loop ===
    for bar in range(bars):
        for step in range(steps_per_bar):
            pos_sec = (bar * steps_per_bar + step) * step_sec
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
            
            # --- Kick Logic (Four-on-the-floor + generative syncopations) ---
            is_downbeat = (step % 4 == 0)
            kick_chance = 100 if is_downbeat else (30 * complexity if step in [7, 10, 14, 15] else 0)
            
            if random.randint(0, 99) < kick_chance:
                vel = random.randint(int(velocity_base*0.9), int(velocity_base*1.1)) if is_downbeat else random.randint(int(velocity_base*0.5), int(velocity_base*0.7))
                vel = min(127, max(1, vel))
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec + step_sec * 0.8)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, KICK, vel, False)
                note_count += 1
                
            # --- Snare/Clap Logic (Backbeat + generative ghost notes) ---
            is_backbeat = (step == 4 or step == 12)
            snare_chance = 100 if is_backbeat else (25 * complexity if step in [3, 7, 11, 15] else 0)
            
            if random.randint(0, 99) < snare_chance:
                vel = random.randint(int(velocity_base*0.9), int(velocity_base*1.1)) if is_backbeat else random.randint(int(velocity_base*0.3), int(velocity_base*0.6))
                vel = min(127, max(1, vel))
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec + step_sec * 0.8)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, vel, False)
                note_count += 1
                
            # --- Hi-Hat Logic (Offbeats + 16th variations) ---
            is_offbeat = (step % 4 == 2)
            hat_chance = 90 if is_offbeat else (70 * complexity if step % 2 != 0 else 30 * complexity)
            
            if random.randint(0, 99) < hat_chance:
                vel = random.randint(int(velocity_base*0.7), int(velocity_base*0.9)) if is_offbeat else random.randint(int(velocity_base*0.4), int(velocity_base*0.6))
                vel = min(127, max(1, vel))
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec + step_sec * 0.5)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, CHAT, vel, False)
                note_count += 1

    # Sort MIDI events to ensure clean playback
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' containing {note_count} algorithmically generated drum notes over {bars} bars at {bpm} BPM."
