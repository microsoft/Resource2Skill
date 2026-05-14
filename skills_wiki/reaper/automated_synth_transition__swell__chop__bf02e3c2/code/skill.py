def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Transition Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Synth Transition (Swell, Chop, & Widen) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the transition build.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track and elements.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
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
    
    # Calculate chord voicing (Root, 5th, +8va 3rd, +8va 7th)
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Base octave 3
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    notes = [
        root_midi,                               # Root
        root_midi + intervals[4 % len(intervals)], # 5th
        root_midi + 12 + intervals[2 % len(intervals)], # 3rd (octave up)
        root_midi + 12 + intervals[6 % len(intervals)]  # 7th (octave up)
    ]

    start_ppq = 0
    end_ppq = int(bars * 4 * 960) # 960 pulses per quarter note
    
    for p in notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # A. Synthesizer
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 1.0) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.4) # Attack time (slow)

    # B. Space / Reverb
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.6) # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.3) # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.8) # Room size

    # C. Stereo Width Control
    width_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Stereo Width", False, -1)
    
    # D. Volume Control (For swell and chop)
    vol_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)

    # === Step 5: Automate Envelopes ===
    # Get envelope pointers (Param 0 is Width for Stereo Width, Param 0 is Adjustment(dB) for Volume Adjustment)
    width_env = RPR.RPR_GetFXEnvelope(track, width_idx, 0, True)
    vol_env = RPR.RPR_GetFXEnvelope(track, vol_idx, 0, True)

    # 5a. Width Automation: 0% to 100%
    RPR.RPR_InsertEnvelopePoint(width_env, 0.0, 0.0, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(width_env, item_length, 100.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortStates(width_env)

    # 5b. Volume Automation: Swell up, then chop
    swell_duration = item_length - bar_length_sec # Swell over all bars except the last one
    if swell_duration <= 0:
        swell_duration = item_length / 2.0 # Fallback if only 1 bar is generated

    # Shape 2 is 'Slow start/end' for a dramatic, cinematic swell
    RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, -120.0, 2, 0.0, False, True) 
    RPR.RPR_InsertEnvelopePoint(vol_env, swell_duration, 0.0, 0, 0.0, False, True)

    # Create the square-wave chopping effect in the final section
    chop_start = swell_duration
    chop_duration_sec = item_length - swell_duration
    chops_per_beat = 4 # 16th note rhythm
    total_chops = int(beats_per_bar * chops_per_beat)
    chop_length = chop_duration_sec / total_chops

    for i in range(total_chops):
        t = chop_start + (i * chop_length)
        val = 0.0 if (i % 2 == 0) else -18.0 # Toggle between 0dB and -18dB
        # Shape 1 is 'Square' to cleanly gate the audio
        RPR.RPR_InsertEnvelopePoint(vol_env, t, val, 1, 0.0, False, True)

    RPR.RPR_Envelope_SortStates(vol_env)

    return f"Created '{track_name}' synth transition. Placed {len(notes)}-note pad over {bars} bars at {bpm} BPM with width swell and 16th-note volume chop."
