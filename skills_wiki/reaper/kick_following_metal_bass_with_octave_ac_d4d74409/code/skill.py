def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Modern Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 'Kick-Following Metal Bass' pattern with octave accents in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "D").
        scale: Scale type (informational here, as we only use Root and Octave).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (pulled back to ~110 to avoid harsh pick layers).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    # Note map for finding the base MIDI pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add basic Synth placeholder for Bass ===
    # A simple saw wave to act as a placeholder for a dedicated Bass VSTi
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set waveform mix to mostly sawtooth for a grittier bass tone (Param 1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.8) 
    # Set a fast release for tighter, percussive bass (Param 5)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.05) 

    # === Step 4: Create MIDI Item & Notes ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Bass octave mapping (e.g., Drop C = C1 = MIDI note 24)
    base_pitch = NOTE_MAP.get(key, 0) + 24  

    # Define the 2-bar syncopated metal groove
    # 1 = Root note, 2 = Octave note (12th fret pop), 0 = Rest
    rhythm_pattern = [
        # Bar 1: Driving syncopated kick pattern
        1, 0, 0, 1,  0, 0, 1, 0,  # Beats 1, 2
        1, 0, 1, 0,  1, 0, 0, 0,  # Beats 3, 4
        # Bar 2: Same intro, but with octave pops on the back half
        1, 0, 0, 1,  0, 0, 1, 0,  # Beats 1, 2
        1, 0, 2, 0,  1, 0, 2, 0   # Beats 3, 4 (Octave jumps)
    ]

    step_len_beats = 0.25  # 16th notes
    step_len_sec = step_len_beats * beat_length_sec
    total_steps = int(bars * 16)
    note_count = 0

    for step in range(total_steps):
        pat_val = rhythm_pattern[step % len(rhythm_pattern)]
        if pat_val > 0:
            # Assign pitch based on whether it's a root or an octave jump
            pitch = base_pitch if pat_val == 1 else base_pitch + 12
            
            start_time = step * step_len_sec
            # Length is 85% of a 16th note. Held out, but leaves a tiny gap for the pick-attack to reset.
            end_time = start_time + (step_len_sec * 0.85)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time), 
                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time), 
                0, pitch, velocity_base, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM. (Note: Replace ReaSynth with your preferred Bass VSTi for optimal results)"
