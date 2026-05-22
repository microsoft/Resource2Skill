def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "A/V Transition Sync",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Rhythmic Video Transitions & Audio Sync Setup in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created video track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (creates a cut/transition per bar).
        velocity_base: Base MIDI velocity for the transition SFX (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
    }

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    fade_duration = bar_length_sec / 2.0 # Half-bar fade transitions

    # Determine Root Pitch for Audio Trigger (Octave 2 for a low impact/swell)
    root_pitch = 36 + NOTE_MAP.get(key, 0)

    # === TRACK 1: VIDEO EDITING TRACK ===
    v_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(v_track_idx, True)
    v_track = RPR.RPR_GetTrack(0, v_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(v_track, "P_NAME", f"{track_name} (Video)", True)

    # Add Video Processor (Native REAPER video engine)
    v_fx_idx = RPR.RPR_TrackFX_AddByName(v_track, "Video processor", False, -1)
    
    # Get the envelope for Parameter 0 (Often Opacity/Crossfade in standard presets)
    v_env = RPR.RPR_GetFXEnvelope(v_track, v_fx_idx, 0, True)

    # === TRACK 2: SYNCED AUDIO SFX TRACK ===
    a_track_idx = v_track_idx + 1
    RPR.RPR_InsertTrackAtIndex(a_track_idx, True)
    a_track = RPR.RPR_GetTrack(0, a_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(a_track, "P_NAME", f"{track_name} (Audio SFX)", True)
    
    # Add a simple synth to act as our transition "whoosh/impact"
    RPR.RPR_TrackFX_AddByName(a_track, "ReaSynth", False, -1)
    
    # Create MIDI Item for Audio
    a_item = RPR.RPR_AddMediaItemToTrack(a_track)
    RPR.RPR_SetMediaItemInfo_Value(a_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(a_item, "D_LENGTH", bar_length_sec * bars)
    a_take = RPR.RPR_AddTakeToMediaItem(a_item)

    # === GENERATE PATTERN ===
    for i in range(bars):
        start_time = i * bar_length_sec
        fade_start_time = start_time + (bar_length_sec - fade_duration)
        end_time = start_time + bar_length_sec

        # 1. Video Placeholders (Empty Items)
        v_item = RPR.RPR_AddMediaItemToTrack(v_track)
        RPR.RPR_SetMediaItemInfo_Value(v_item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(v_item, "D_LENGTH", bar_length_sec)
        
        # 2. Video Automation (Dip to Black using "Slow start/end" curve)
        if v_env:
            # Shape 0 = Linear, Shape 2 = Slow start/end (As recommended in tutorial)
            # Hold at full opacity
            RPR.RPR_InsertEnvelopePoint(v_env, start_time, 1.0, 0, 0, False, True)
            RPR.RPR_InsertEnvelopePoint(v_env, fade_start_time, 1.0, 2, 0, False, True)
            # Dip to black
            RPR.RPR_InsertEnvelopePoint(v_env, end_time, 0.0, 0, 0, False, True)

        # 3. Audio Sync (Insert MIDI note precisely during the video fade)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(a_take, fade_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(a_take, end_time)
        
        RPR.RPR_MIDI_InsertNote(
            a_take, False, False, 
            start_ppq, end_ppq, 
            0, root_pitch, velocity_base, False
        )

    if v_env:
        RPR.RPR_Envelope_SortPoints(v_env)
    
    RPR.RPR_UpdateArrange()

    return f"Created A/V Sync setup over {bars} bars. Added Video Processor automation (Shape: Slow start/end) with paired MIDI triggers in {key} {scale} at {bpm} BPM."
