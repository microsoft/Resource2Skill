def create_pattern(
    project_name: str = "MetalProject",
    track_name: str = "Locked Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create Kick-Locked Metal Bass with Octave Fills in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (capped at 110 to reduce harsh pick attack per tutorial).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Note map to calculate the root pitch. 
    # Metal bass typically sits in the C1-C2 octave range (MIDI 24-36)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave 1 (e.g., C1 = 24)
    root_pitch = 24 + NOTE_MAP.get(key, 0)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item_pos = 0.0
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Define a classic metalcore syncopated kick/bass rhythm pattern
    # Format: (start_16th_step, length_in_16ths, octave_jump_semitones)
    rhythm_pattern = [
        (0, 1, 0),   # Beat 1 (Downbeat)
        (2, 1, 0),   # Beat 1 (&)
        (4, 1, 0),   # Beat 2
        (7, 1, 0),   # Beat 2 (a)
        (8, 1, 0),   # Beat 3
        (10, 1, 0),  # Beat 3 (&)
        (14, 1, 12), # Beat 4 (e) - The signature 12th fret octave jump!
    ]
    
    step_length_sec = (60.0 / bpm) / 4.0
    note_count = 0
    
    for bar in range(bars):
        for note in rhythm_pattern:
            start_step = note[0] + (bar * 16)
            
            # Make the note slightly staccato (80% of a 16th note length) 
            # to leave space between chugs, simulating aggressive palm muting.
            duration_16ths = note[1] * 0.8 
            
            abs_start_time = item_pos + (start_step * step_length_sec)
            abs_end_time = item_pos + ((start_step + duration_16ths) * step_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, abs_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, abs_end_time)
            
            pitch = root_pitch + note[2]
            
            # Insert note with velocity restricted to the user's base (default 110)
            # noSort flag = True (we will sort at the end)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add FX Chain ===
    # Add a stock synth tuned to a square/saw wave to act as a placeholder bass
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add a stock JS Amp Simulator to mimic the distortion of a heavy metal bass tone
    amp_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Guitar/amp-model", False, -1)
    # Drive the amp slightly to make the low-end aggressive
    RPR.RPR_TrackFX_SetParam(track, amp_idx, 0, 0.7) # Pre-amp drive

    return f"Created '{track_name}' with {note_count} locked bass notes over {bars} bars at {bpm} BPM"
