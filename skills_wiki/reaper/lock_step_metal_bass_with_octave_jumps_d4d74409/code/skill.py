def create_pattern(
    project_name: str = "MetalcoreProject",
    track_name: str = "Djent Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Deliberately lowered from 127 to tame VST harshness
    **kwargs,
) -> str:
    """
    Creates a lock-step metal bassline matching kick/guitar patterns with octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), recommended ~110 for virtual bass.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Base low octaves for heavy bass (C1/C2 range)
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}

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
    
    # Place at current edit cursor
    start_time = RPR.RPR_GetCursorPosition()
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define the Riff Pattern ===
    root_pitch = NOTE_MAP.get(key, 24) # Default to low C if key not found
    
    # Riff definition: (beat_start, length_in_beats, pitch_offset, velocity_offset)
    # This creates a chugging, syncopated 1-bar pattern with an octave jump at the end
    riff_beats = [
        (0.0,  0.25, 0,  0),   # Beat 1 (Downbeat Kick)
        (0.5,  0.25, 0,  0),   # Beat 1 &
        (1.25, 0.25, 0,  -5),  # Beat 2 e (syncopated, slightly softer)
        (1.5,  0.25, 0,  0),   # Beat 2 &
        (2.0,  0.25, 0,  0),   # Beat 3 (Downbeat Kick)
        (2.5,  0.25, 12, +5),  # Beat 3 & -> OCTAVE JUMP (12th fret), accented
        (3.0,  0.25, 12, +5),  # Beat 4   -> OCTAVE JUMP (12th fret), accented
        (3.5,  0.25, 0,  0),   # Beat 4 & -> Back to root
    ]

    # === Step 5: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        for b_start, b_len, p_off, v_off in riff_beats:
            
            # Calculate absolute beat positions
            abs_beat_start = bar_start_beat + b_start
            abs_beat_end = abs_beat_start + b_len
            
            # Convert to seconds relative to item start
            start_time_sec = start_time + (abs_beat_start * (60.0 / bpm))
            end_time_sec = start_time + (abs_beat_end * (60.0 / bpm))
            
            # Convert seconds to PPQ (MIDI ticks)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            # Calculate final pitch and bounded velocity
            pitch = root_pitch + p_off
            vel = int(min(127, max(1, velocity_base + v_off)))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add Placeholder Bass Instrument ===
    # Adds ReaSynth so it makes sound immediately, tweaked for a low, saw-heavy bass tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth parameters: Sawtooth mix up, square down, tune down 1 octave
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Vol (Square) down
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.8) # Vol (Saw) up
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.0) # Tune down (-12 semitones relative to default)
    
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} lock-step octave-jump bass notes over {bars} bars at {bpm} BPM in {key}."
