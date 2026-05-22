def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Sweep",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an automated Low Pass filter sweep on a sustained synth pad.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars for the sweep to evolve.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., start_freq, end_freq).

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # Configuration 
    start_freq = kwargs.get("start_freq", 200.0)
    end_freq = kwargs.get("end_freq", 12000.0)

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root MIDI pitch (Octave 3 for a nice pad sound)
    root_pitch = NOTE_MAP.get(key, 0) + 48 

    # 1. Add new track
    RPR.RPR_Undo_BeginBlock2(0)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 2. Timing calculations based on project master tempo
    current_bpm = RPR.RPR_Master_GetTempo()
    beats_per_bar = 4
    bar_length_sec = (60.0 / current_bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Set cursor to start
    start_pos = RPR.RPR_GetCursorPosition()

    # 3. Create MIDI Item and Take
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Enable MIDI in the take
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)

    # Convert seconds to MIDI pulses (PPQ) for note lengths
    # REAPER's default is 960 PPQ per quarter note
    quarter_notes = bars * beats_per_bar
    end_ppq = int(quarter_notes * 960)

    # Insert a single long drone note spanning the whole item
    RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, root_pitch, velocity_base, False)
    # Add a perfect fifth for thickness
    RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, root_pitch + 7, velocity_base - 10, False)

    # 4. Sound Design: Add Synth and Filter FX Chain
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more harmonically rich sound (mix in sawtooth/square)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5) # Square mix

    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: resonantlowpass", False, -1)

    # 5. Create Automation Envelope for the Filter Sweep
    # JS: resonantlowpass parameter 0 is Frequency (Hz)
    env = RPR.RPR_GetFXEnvelope(track, filter_idx, 0, True)

    if env:
        # shape 2 is "Slow Start/End" for a musical, non-linear swelling curve
        shape = 2 
        tension = 0.0
        
        # Point 1: Start muffled
        RPR.RPR_InsertEnvelopePoint(env, start_pos, start_freq, shape, tension, False, True)
        
        # Point 2: Sweep up completely by the end of the bars
        RPR.RPR_InsertEnvelopePoint(env, start_pos + item_length, end_freq, shape, tension, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    RPR.RPR_Undo_EndBlock2(0, "Create Automated Filter Sweep", -1)

    return f"Created '{track_name}' sweeping filter from {start_freq}Hz to {end_freq}Hz over {bars} bars at {current_bpm} BPM."
