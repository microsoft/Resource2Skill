def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pulsing Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Staccato Pulsing Synth Pad in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major or minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated element.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add native ReaSynth to approximate the tutorial's synth pad
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a staccato, plucky Square/Saw blend
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5)  # Square wave mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5)  # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.01) # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.2)  # Decay (Short)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.4)  # Sustain (Medium)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.1)  # Release (Short/Tight)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Music Theory & Voice Leading Calculation ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 48 # Default to Octave 3 (e.g., C3)
    
    is_minor = (scale.lower() != "major")
    
    # Construct specific voicings reflecting smooth voice leading shown in the video
    if is_minor:
        # Progression: i -> iv (2nd inv) -> VII
        chord_1 = [root_pitch, root_pitch + 3, root_pitch + 7, root_pitch + 12]       # i
        chord_2 = [root_pitch, root_pitch + 5, root_pitch + 8, root_pitch + 12]       # iv (2nd inversion to keep root as common tone)
        chord_3 = [root_pitch - 2, root_pitch + 2, root_pitch + 5, root_pitch + 10]   # VII
    else:
        # Adaptation for Major key to preserve the same voice leading contour (I -> IV -> V)
        chord_1 = [root_pitch, root_pitch + 4, root_pitch + 7, root_pitch + 12]       # I
        chord_2 = [root_pitch, root_pitch + 5, root_pitch + 9, root_pitch + 12]       # IV (2nd inversion)
        chord_3 = [root_pitch - 1, root_pitch + 2, root_pitch + 7, root_pitch + 11]   # V

    # === Step 5: Generate Step-Sequenced Pattern ===
    notes_added = 0
    
    # Process in 2-bar loops
    for bar in range(0, bars, 2): 
        for beat_idx in range(16): # 16 eighth-notes in a 2-bar sequence
            # Assign chord based on timeline position
            if beat_idx < 8:
                chord = chord_1
            elif beat_idx < 12:
                chord = chord_2
            else:
                chord = chord_3
                
            # The core mechanism: 1/8th note grid (0.5 beats) but 1/16th note length (0.25 beats)
            start_beat = (bar * 4) + (beat_idx * 0.5)
            end_beat = start_beat + 0.25 
            
            # Bound check if the user asked for an odd number of bars
            if start_beat >= bars * 4:
                break
                
            start_time = (60.0 / bpm) * start_beat
            end_time = (60.0 / bpm) * end_beat
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the notes for the block chord
            for note in chord:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note), velocity_base, False)
                notes_added += 1
                
    # Sort MIDI data internally required by REAPER API
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {notes_added} staccato pulses over {bars} bars at {bpm} BPM."
