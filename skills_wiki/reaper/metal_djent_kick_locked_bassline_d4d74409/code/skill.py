def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal/Djent Kick-Locked Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note for the drop tuning (e.g., "C").
        scale: Scale type (unused here as it plays a static root chug).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (kept below 127 to avoid fret clank).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note lookup for Drop tuning root
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave is low (C1 = 24 in standard MIDI mapping for bass)
    root_pitch = 24 + NOTE_MAP.get(key, 0)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a stock synth + distortion as a placeholder for a real Virtual Bass VST
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length)
    take = RPR.RPR_GetActiveTake(item)

    # Define the syncopated rhythm pattern extracted from the video
    # Format: (start_beat_relative_to_bar, length_in_beats, octave_shift)
    # Note lengths are slightly gated (e.g., 0.4 instead of 0.5) to simulate palm muting
    rhythm = [
        (0.0,  0.4, 0),   # Beat 1 (1/8th)
        (0.5,  0.4, 0),   # Beat 1 & (1/8th)
        (1.0,  0.2, 0),   # Beat 2 (1/16th)
        (1.25, 0.2, 0),   # Beat 2 e (1/16th)
        (1.5,  0.4, 1),   # Beat 2 & (1/8th) -> OCTAVE JUMP (+12 semitones / 12th fret)
        (2.0,  0.4, 0),   # Beat 3 (1/8th)
        (2.5,  0.4, 0),   # Beat 3 & (1/8th)
        (3.0,  0.2, 0),   # Beat 4 (1/16th)
        (3.25, 0.2, 0),   # Beat 4 e (1/16th)
        (3.5,  0.2, 0),   # Beat 4 & (1/16th)
        (3.75, 0.2, 0),   # Beat 4 a (1/16th)
    ]

    qn_ticks = 960  # Default ticks per quarter note
    note_count = 0

    for bar in range(bars):
        bar_start_qn = bar * beats_per_bar
        for start_beat, length_beats, oct_shift in rhythm:
            start_qn = bar_start_qn + start_beat
            end_qn = start_qn + length_beats
            
            start_ppq = int(start_qn * qn_ticks)
            end_ppq = int(end_qn * qn_ticks)
            
            # Apply octave jump if specified
            pitch = root_pitch + (12 * oct_shift)
            
            # Slightly lower velocity for off-beat 16th notes to create groove
            is_accent = (start_beat % 1.0 == 0) or oct_shift == 1
            vel = velocity_base if is_accent else max(1, velocity_base - 10)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort MIDI events to ensure they process correctly
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} lock-in bass notes over {bars} bars at {bpm} BPM."
