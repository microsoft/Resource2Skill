def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal Bass foundation track that mimics locking to a kick drum,
    using lowered velocity for tone control and octave jumps for fills.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (lowered to 110 to tame harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root pitch (Octave 1 for low metal bass, e.g., Drop C = MIDI 24)
    # Using .title() or .upper() appropriately to safely extract the note
    safe_key = key.capitalize() if len(key) == 1 else key[0].upper() + key[1:]
    root_pitch = NOTE_MAP.get(safe_key, 0) + 24

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
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)

    # 2-bar rhythmic pattern representing syncopated metal double-kicks
    # Tuples of (start_beat, duration_beats, octave_offset)
    pattern = [
        # Bar 1 (Beats 0-3): Syncopated chugs
        (0.0,  0.25, 0),
        (0.75, 0.25, 0),
        (1.5,  0.25, 0),
        (2.0,  0.25, 0),
        (2.5,  0.25, 0),
        (3.0,  0.5,  0),  # Slightly sustained 8th note
        
        # Bar 2 (Beats 4-7): Identical start, but includes an octave jump fill at the end
        (4.0,  0.25, 0),
        (4.75, 0.25, 0),
        (5.5,  0.25, 0),
        (6.0,  0.25, 0),
        (6.5,  0.25, 0),
        (7.0,  0.25, 12), # Octave jump (+12st)
        (7.5,  0.25, 12), # Octave jump (+12st)
    ]

    beats_total = bars * beats_per_bar
    note_count = 0
    
    for current_bar in range(0, bars, 2):
        bar_offset_beats = current_bar * beats_per_bar
        
        for start_b, dur_b, oct_offset in pattern:
            absolute_beat = bar_offset_beats + start_b
            if absolute_beat >= beats_total:
                continue
                
            start_time = absolute_beat * (60.0 / bpm)
            end_time = (absolute_beat + dur_b) * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = root_pitch + oct_offset
            
            # Insert the note utilizing the lowered velocity_base (110) as directed by the tutorial
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add a stock synth just to ensure the track makes sound. 
    # To truly utilize this script, the user would load a virtual bass VST in place of ReaSynth.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"
