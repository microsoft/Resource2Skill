def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "S-Curve Fade Out",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an S-Curve (Slow start/end) Volume Transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables for the sustained note
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root note (C3 base)
    root_pitch = 48 + NOTE_MAP.get(key, 0)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Synth ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Add a sustained MIDI note for the full duration
    # REAPER MIDI ticks (default 960 PPQ)
    ticks_per_sec = (bpm * 960) / 60
    end_tick = int(item_length * ticks_per_sec)
    RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_tick, 1, root_pitch, velocity_base, False)
    
    # Add a basic synth so we can hear the audio fade
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Add Volume Automation Envelope with "Slow start/end" Shape ===
    # Select only this track to safely toggle its volume envelope visibility
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env:
        # We will create a 1-bar fade out at the end of the item
        fade_start_time = item_length - bar_length_sec
        fade_end_time = item_length
        
        # Point 1: Start of item, Unity gain (1.0), Shape = 0 (Linear)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0.0, False, True) 
        
        # Point 2: Start of fade, Unity gain (1.0), Shape = 2 (Slow start/end)
        # This is the crucial technique extracted from the tutorial
        RPR.RPR_InsertEnvelopePoint(env, fade_start_time, 1.0, 2, 0.0, False, True) 
        
        # Point 3: End of fade, Silence (0.0), Shape = 0 (Linear)
        RPR.RPR_InsertEnvelopePoint(env, fade_end_time, 0.0, 0, 0.0, False, True) 
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with a 1-bar S-Curve volume transition at {bpm} BPM"
