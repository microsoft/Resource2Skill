def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Lowered from 127 as specified in the tutorial to tame string harshness
    **kwargs,
) -> str:
    """
    Create a Kick-Locked Metal Bass Line in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), optimized to 110 for virtual bass.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Note map parsing for calculating the lowest root pedal point
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Establish root pitch class. Metal bass is usually in Octave 1 (MIDI 24 for C1)
    root_pitch_class = NOTE_MAP.get(key.capitalize(), 0)
    base_pitch = 24 + root_pitch_class 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track Additively ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Place item at current edit cursor
    pos = RPR.RPR_GetCursorPosition()
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 4: Insert Syncopated MIDI Notes ===
    # Rhythm Matrix (16th notes): 
    # 1 = Root hit (Follows Kick)
    # 2 = Octave jump (+12st) on turnaround (12th fret mimic)
    # 0 = Rest
    rhythm_16ths = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 2, 0, 1, 0]
    
    note_count = 0
    
    for bar in range(bars):
        for i, hit_type in enumerate(rhythm_16ths):
            if hit_type != 0:
                # Calculate timing in beats relative to start
                beat_offset = (bar * beats_per_bar) + (i * 0.25)
                proj_start = pos + (beat_offset * 60.0 / bpm)
                
                # Use a staccato note length (0.15 beats instead of full 0.25) to allow for string muting
                note_len_beats = 0.15
                proj_end = proj_start + (note_len_beats * 60.0 / bpm)
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_end)
                
                # Determine pitch
                pitch = base_pitch
                if hit_type == 2:
                    pitch += 12  # Jump an octave up
                
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, pitch, velocity_base, False
                )
                note_count += 1

    # Sort MIDI events to finalize the item
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} syncopated notes over {bars} bars at {bpm} BPM. Note: Add your preferred Bass VST to this track."
