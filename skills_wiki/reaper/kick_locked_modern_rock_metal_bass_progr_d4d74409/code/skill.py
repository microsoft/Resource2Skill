def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a kick-locked, modern rock/metal bass MIDI pattern in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (mostly rides the root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (110 removes harsh clack from bass VSTs).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Note map starting at octave 1 (common for modern metal/drop tunings)
    NOTE_MAP = {
        "C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
        "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
        "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35
    }
    
    root_note = NOTE_MAP.get(key.upper(), 24) # Default to C1

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qn_duration = 60.0 / bpm
    bar_length_sec = qn_duration * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Simulated modern metal Kick/Djent rhythm mapped relative to a 4-beat bar.
    # Format: (start_beat, end_beat, octave_offset)
    rhythm_pattern = [
        (0.0, 0.5, 0),    # Beat 1 (Downbeat)
        (0.75, 1.0, 0),   # Syncopated 16th before Beat 2
        (1.5, 2.0, 0),    # The 'AND' of Beat 2
        (2.5, 2.75, 0),   # The 'AND' of Beat 3
        (3.0, 3.25, 0),   # Beat 4 Downbeat
        (3.5, 4.0, 1),    # The 'AND' of Beat 4 -> 12th Fret Octave Jump (+1)
    ]

    # === Step 4: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        for hit in rhythm_pattern:
            start_time = (bar_start_beat + hit[0]) * qn_duration
            end_time = (bar_start_beat + hit[1]) * qn_duration
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Apply octave variation (simulating moving to the 12th fret)
            pitch = root_note + (hit[2] * 12)
            
            # Video core lesson: 110 velocity to remove sample harshness
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Placeholder FX ===
    # Adds ReaSynth to ensure the track makes sound out of the box. 
    # In a real scenario, the user would swap this for DjinnBass/Eurobass.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM. Velocity capped at {velocity_base} to prevent sample harshness."
