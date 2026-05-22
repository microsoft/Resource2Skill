def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "House Drums (MIDI)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a classic Four-on-the-Floor House Drum Pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (120-128 recommended for House).
        key: Ignored for drum pattern.
        scale: Ignored for drum pattern.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (scaled internally for groove).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

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

    # === Step 4: Insert MIDI Notes (GM Drum Map) ===
    # MIDI Note definitions
    KICK = 36   # C1
    CLAP = 39   # D#1
    HAT = 42    # F#1

    # Rhythmic definition: (beat_offset, pitch, velocity_modifier, duration_in_beats)
    # Beat 0 = Beat 1, Beat 1 = Beat 2, etc.
    groove_pattern = [
        (0.0, KICK, 1.1, 0.25),  # Beat 1 Kick
        (0.5, HAT,  0.9, 0.25),  # Offbeat Hat
        (1.0, KICK, 1.1, 0.25),  # Beat 2 Kick
        (1.0, CLAP, 1.0, 0.25),  # Beat 2 Clap
        (1.5, HAT,  0.9, 0.25),  # Offbeat Hat
        (2.0, KICK, 1.1, 0.25),  # Beat 3 Kick
        (2.5, HAT,  0.9, 0.25),  # Offbeat Hat
        (3.0, KICK, 1.1, 0.25),  # Beat 4 Kick
        (3.0, CLAP, 1.0, 0.25),  # Beat 4 Clap
        (3.5, HAT,  0.9, 0.25),  # Offbeat Hat
    ]

    notes_created = 0
    midi_channel = 9 # Channel 10 (0-indexed) is the standard drum channel

    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        
        for beat_pos, pitch, vel_mod, dur in groove_pattern:
            start_beat = bar_offset_beats + beat_pos
            end_beat = start_beat + dur

            # Convert beats to time, then to PPQ for accurate placement
            start_time = start_beat * (60.0 / bpm)
            end_time = end_beat * (60.0 / bpm)

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Calculate final velocity, keeping it safely within 1-127 bounds
            final_velocity = int(velocity_base * vel_mod)
            final_velocity = max(1, min(127, final_velocity))

            RPR.RPR_MIDI_InsertNote(
                take, 
                False,          # selected
                False,          # muted
                start_ppq,      # start time
                end_ppq,        # end time
                midi_channel,   # channel
                pitch,          # pitch
                final_velocity, # velocity
                True            # noSort (we sort once at the end for performance)
            )
            notes_created += 1

    # Sort the MIDI stream after all notes are added
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} GM drum notes over {bars} bars at {bpm} BPM"
