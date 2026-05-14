def create_pattern(
    project_name: str = "MetalProject",
    track_name: str = "Metal Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly 110 based on tutorial advice
    **kwargs,
) -> str:
    """
    Creates a syncopated, kick-following metal bass pattern with octave variations.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created bass track.
        bpm: Tempo in BPM (120-160 typical for this style).
        key: Root note (e.g., 'C' for Drop C style).
        scale: Scale type (primarily uses root, but accepted for architecture).
        bars: Number of bars to generate.
        velocity_base: Reduced velocity (110 instead of 127) to avoid string harshness.
        **kwargs: Additional overrides.
        
    Returns:
        Status string indicating the track and notes created.
    """
    import reaper_python as RPR

    # Setup basic pitch tracking (putting the bass in the 1st/2nd octave)
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
    
    root_pitch = NOTE_MAP.get(key.upper(), 24) # Default to C1 (MIDI 24)
    octave_pitch = root_pitch + 12             # Jump to 12th fret

    # 16th-note syncopated "Kick groove" pattern representation
    # 1 = Root note, 2 = Octave jump, 0 = Rest
    # This perfectly mimics the "chug - rest - chug chug" tight metal breakdown feel
    kick_syncopation_grid = [
        1, 0, 1, 1,   # Beat 1: Root, rest, Root, Root
        0, 1, 0, 1,   # Beat 2: rest, Root, rest, Root
        0, 1, 1, 2,   # Beat 3: rest, Root, Root, OCTAVE JUMP (tutorial variation)
        0, 1, 1, 0    # Beat 4: rest, Root, Root, rest
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Take ===
    beats_per_bar = 4
    beat_duration_sec = 60.0 / bpm
    bar_length_sec = beat_duration_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 4: Program MIDI Notes ===
    sixteenth_duration_sec = beat_duration_sec / 4.0
    note_duration_sec = sixteenth_duration_sec * 0.85 # Staccato for tight palm-mute feel
    
    note_count = 0
    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        for step, note_type in enumerate(kick_syncopation_grid):
            if note_type == 0:
                continue # Rest
                
            pitch = root_pitch if note_type == 1 else octave_pitch
            
            # Add slight humanization to velocity
            vel = max(1, min(127, velocity_base + (step % 3) - 1))
            
            start_time = bar_start_sec + (step * sixteenth_duration_sec)
            end_time = start_time + note_duration_sec
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (ReaSynth Bass Placeholder) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tune ReaSynth to act as a gritty bass:
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)  # Vol
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)  # Square wave mix (for metal grit)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)  # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)  # Triangle mix
    
    # Update timeline
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} tight syncopated bass notes (Velocity ~{velocity_base}) over {bars} bars at {bpm} BPM."
