def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algo Beatbox",
    bpm: int = 105,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a grooving, generative drum sequence mimicking a step-sequencer.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused for drums, maintained for signature).
        scale: Scale type (unused for drums, maintained for signature).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Stock Sampler Placeholders) ===
    # Instance 1: Kick
    RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 36) # Note start
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 36) # Note end
    # Instance 2: Snare
    RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 1, 3, 38)
    RPR.RPR_TrackFX_SetParam(track, 1, 4, 38)
    # Instance 3: Hi-Hat
    RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 2, 3, 42)
    RPR.RPR_TrackFX_SetParam(track, 2, 4, 46) # Range allows closed and open hat

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    ppq = 960
    qn_per_bar = 4

    KICK = 36
    SNARE = 38
    HAT_CLOSED = 42
    HAT_OPEN = 46

    # 16-step rhythmic grids (0 to 15)
    kick_pattern = [0, 7, 8, 10]  # Syncopated offbeat kicks
    snare_pattern = [4, 12]       # Standard backbeat

    note_count = 0

    for bar in range(bars):
        bar_start_qn = bar * qn_per_bar

        for step in range(16):
            pos_qn = bar_start_qn + (step * 0.25)
            start_ppq = int(pos_qn * ppq)
            end_ppq = int((pos_qn + 0.125) * ppq) # 1/32th duration

            # --- Kick Logic ---
            if step in kick_pattern:
                # Stronger velocity on downbeats
                vel = min(127, velocity_base + 10) if step in [0, 8] else max(0, velocity_base - 15)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, KICK, vel, False)
                note_count += 1

            # --- Snare Logic ---
            if step in snare_pattern:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, min(127, velocity_base + 15), False)
                note_count += 1
            # Ghost snare fill at the end of every 2nd bar
            elif step == 15 and bar % 2 == 1: 
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, max(0, velocity_base - 40), False)
                note_count += 1

            # --- Hi-Hat Logic ---
            # Accent on 8th notes (even steps), softer on 16th notes (odd steps)
            hat_vel = velocity_base if step % 2 == 0 else max(0, velocity_base - 30)
            pitch = HAT_CLOSED
            
            # Open hat on the 'and' of 4 every other bar
            if step == 14 and bar % 2 == 0:
                pitch = HAT_OPEN
                hat_vel = min(127, velocity_base + 5)

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, hat_vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} sequenced drum notes and pre-routed RS5K samplers over {bars} bars at {bpm} BPM."
