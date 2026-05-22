def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Virtual Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly defaulting to 110 to reduce harshness as per tutorial
    **kwargs,
) -> str:
    """
    Create a Metal Bass Kick-Locking pattern with Octave Jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), intentionally lowered to avoid clank.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Step 1: Initialize Variables ===
    # Map key to a low bass octave (Octave 2 in standard MIDI mapping, 36 = C2)
    NOTE_MAP = {"C": 36, "C#": 37, "Db": 37, "D": 38, "D#": 39, "Eb": 39,
                "E": 40, "F": 41, "F#": 42, "Gb": 42, "G": 43, "G#": 44,
                "Ab": 44, "A": 45, "A#": 46, "Bb": 46, "B": 47}
    
    root_note = NOTE_MAP.get(key, 36)
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a basic synth and shape it for bass
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape ReaSynth: Square wave for grind, low filter
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.5)    # Square mix (more aggressive)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.0)    # Saw mix

    # Add EQ to carve metal bass tone
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # === Step 3: Define Rhythmic Pattern ===
    # Array represents 16th notes.
    # 0 = rest, 1 = root note (following kick), 2 = octave jump fill
    # Pattern simulates a syncopated metalcore breakdown
    base_bar_pattern =   [1, 0, 0, 1,  0, 0, 1, 0,  1, 0, 0, 0,  1, 0, 2, 0]
    fill_bar_pattern =   [1, 0, 0, 1,  0, 0, 1, 0,  1, 0, 0, 0,  2, 0, 2, 0]

    full_pattern = []
    for i in range(bars):
        # Every even-numbered bar gets the extra octave jump fill
        if i % 2 == 1:
            full_pattern.extend(fill_bar_pattern)
        else:
            full_pattern.extend(base_bar_pattern)

    # === Step 4: Create MIDI Item & Notes ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    sixteenth_length_sec = beat_length_sec / 4.0
    item_length = beat_length_sec * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    note_count = 0
    
    for idx, hit in enumerate(full_pattern):
        if hit > 0:
            # Calculate timing
            start_time = idx * sixteenth_length_sec
            # Staccato lengths (80% of a 16th note) to leave room for kick transient
            end_time = start_time + (sixteenth_length_sec * 0.8) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # hit == 1 is root, hit == 2 is 12th fret (octave up)
            pitch = root_note + 12 if hit == 2 else root_note
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take,
                False,      # selected
                False,      # muted
                start_ppq,
                end_ppq,
                0,          # channel
                pitch,
                velocity_base, 
                False       # noSort
            )
            note_count += 1

    # Finalize MIDI
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} locked-kick bass notes over {bars} bars at {bpm} BPM (Velocity: {velocity_base})."
