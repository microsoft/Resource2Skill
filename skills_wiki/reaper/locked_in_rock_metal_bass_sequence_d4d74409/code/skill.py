def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass (Locked)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 'Locked-In Rock/Metal Bass Sequence' in the current REAPER project.
    
    This script generates a syncopated, kick-following bassline utilizing
    controlled velocities and octave leaps, as common in heavy rock/metal production.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Defaults to C (Drop C style).
        scale: Scale type (not strictly used here as it rides the root, but accepted for compatibility).
        bars: Number of bars to generate (should be a multiple of 2 for the loop).
        velocity_base: Base MIDI velocity (0-127). Set to 110 to reduce VST string noise.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

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
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine base pitch. Assuming a low tuned bass (e.g., C1 for modern metal)
    # MIDI note 24 is C1.
    root_offset = NOTE_MAP.get(key.upper(), 0)
    base_pitch = 24 + root_offset

    # Define a 2-bar 16th-note syncopated rhythm pattern typical of metal kick drums
    # Format: (start_16th_index, length_in_16ths, pitch_offset_semitones)
    pattern = [
        # Bar 1: Driving rhythm riding the open root note
        (0, 2, 0),   # Beat 1
        (2, 2, 0),   # Beat 1.5
        (4, 1, 0),   # Beat 2 (two fast 16ths)
        (5, 1, 0),
        (8, 2, 0),   # Beat 3
        (10, 2, 0),  # Beat 3.5
        (14, 2, 0),  # Beat 4.5 syncopation
        
        # Bar 2: Same rhythm but introducing the 12th-fret octave jump
        (16, 2, 0),  
        (18, 2, 0),  
        (20, 1, 0),  
        (21, 1, 0),
        (24, 2, 0),  
        (26, 2, 12), # Beat 3.5 - OCTAVE JUMP (+12 semitones)
        (30, 2, 0)   
    ]
    
    pattern_length_16ths = 32 # 2 bars * 16 sixteenth notes
    
    note_count = 0
    # Loop the 2-bar pattern to fill the requested number of bars
    loop_iterations = max(1, bars // 2)
    if bars % 2 != 0:
        loop_iterations += 1 # Ensure we cover odd numbers of bars
        
    for bar_pair in range(loop_iterations):
        bar_offset_16ths = bar_pair * pattern_length_16ths
        
        for start_idx, length, pitch_offset in pattern:
            start_16th = bar_offset_16ths + start_idx
            
            # Stop adding notes if we exceed the requested total bars
            if start_16th >= (bars * 16):
                continue
                
            end_16th = start_16th + length
            
            # Convert 16th note indices to Quarter Notes, then to Seconds
            start_qn = start_16th / 4.0
            end_qn = end_16th / 4.0
            
            start_pos = start_qn * (60.0 / bpm)
            end_pos = end_qn * (60.0 / bpm)
            
            # Convert Seconds to REAPER PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            
            pitch = base_pitch + pitch_offset
            
            # Insert note (using the specified 110 velocity base to tame transient harshness)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain Placeholder ===
    # Add ReaSynth as a stock placeholder to ensure the track produces low-end sound
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if synth_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Volume
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4)   # Square mix
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.6)   # Saw mix (bite)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.01)  # Fast attack
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.3)   # Snappy decay

    return f"Created '{track_name}' with {note_count} locked-in bass notes (including octave leaps) over {bars} bars at {bpm} BPM."
