def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an 'Evolving Swell & Auto-Pan Automation' pattern in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (used to calculate timings).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the swell should last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define chord intervals based on scale quality
    is_minor = any(m in scale.lower() for m in ["minor", "dorian", "phrygian", "aeolian"])
    chord_intervals = [0, 3, 7, 10] if is_minor else [0, 4, 7, 11] # min7 vs maj7

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add Synth & Configure Timbre ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Increase attack and release so it acts like a pad
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 1.0) # Param 1: Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 1.0) # Param 2: Release
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.3) # Param 3: Sawtooth mix (add harmonics)

    # === Step 3: Create MIDI Item & Insert Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Start at Octave 4

    for interval in chord_intervals:
        pitch = root_pitch + interval
        # Insert sustained notes for the entire item duration
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Volume and Pan Automation Envelopes ===
    
    # We must select only our new track to ensure actions apply correctly to it
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Toggling standard envelopes visibility via Main Actions guarantees they are created/active
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40407, 0) # Track: Toggle track pan envelope visible

    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")

    # Volume Envelope: Slow Swell (0.0 to 1.0 gain) over the entire item
    # Shape 2 is "Slow start/end" which gives a natural, musical curve
    RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 2, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_vol, item_length, 1.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_Sort(env_vol)

    # Pan Envelope: 1-Bar Rhythmic Sweeps (-1.0 Left to 1.0 Right)
    for b in range(bars + 1):
        time_pos = b * bar_length_sec
        pan_val = -1.0 if b % 2 == 0 else 1.0
        # Shape 2 creates a smooth sine-like transition between hard left and right
        RPR.RPR_InsertEnvelopePoint(env_pan, time_pos, pan_val, 2, 0.0, False, True)
    
    RPR.RPR_Envelope_Sort(env_pan)

    return f"Created '{track_name}': {bars}-bar Volume Swell and Auto-Pan automation over a {key} {scale} pad at {bpm} BPM."
