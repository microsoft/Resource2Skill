def create_generative_bassline_chain(
    project_name: str = "MyProject",
    track_name: str = "Generative Arp Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a modular MIDI sequencing chain (MIDI Generator -> Synth VST) 
    replicating the Reason Player -> Massive X workflow using native REAPER plugins.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add MIDI Generator (Arpeggiator) ===
    # This acts as our "Reason Bassline Generator"
    arp_idx = RPR.RPR_TrackFX_AddByName(track, "JS: MIDI Arpeggiator", False, -1)
    
    # Configure JS Arpeggiator to a 1/16 note pattern spanning 2 octaves
    # Param 0: Rate (4 = 1/16 notes)
    # Param 1: Note length (0.8 = punchy staccato)
    # Param 2: Octaves (1 = spans 2 octaves)
    RPR.RPR_TrackFX_SetParam(track, arp_idx, 0, 4.0) 
    RPR.RPR_TrackFX_SetParam(track, arp_idx, 1, 0.8) 
    RPR.RPR_TrackFX_SetParam(track, arp_idx, 2, 1.0) 

    # === Step 4: Add Synthesizer ===
    # This acts as our "Massive X" downstream sound engine
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Dial in a fat bass tone (mix of Square and Saw waves)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.7)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.6)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.02) # Fast Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.2)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 10, 0.1) # Fast Release

    # === Step 5: Create a sustained "Feed" MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory lookup for base triad
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    base_pitch = NOTE_MAP.get(key.upper(), 0) + 36 # C2 octave for bass
    is_minor = "minor" in scale.lower() or "dorian" in scale.lower() or "phrygian" in scale.lower()
    third = 3 if is_minor else 4
    fifth = 7

    ppq = 960 # Standard REAPER pulses per quarter note
    total_qn = bars * 4.0
    
    # Insert a single sustained triad chord holding for the entire duration.
    # The Arpeggiator FX will intercept this chord and turn it into the 1/16 generative bassline.
    for note in [base_pitch, base_pitch + third, base_pitch + fifth]:
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, int(ppq * total_qn), 0, note, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", f"{key} {scale} Sustained Feed", True)

    return f"Created '{track_name}' using Modular MIDI Seq -> Synth routing over {bars} bars at {bpm} BPM."
