def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Swell & Spatial Panning Transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell transition.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created automated track.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
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

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add Sound Design (ReaSynth Pad) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a smoother pad-like sound
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 1.0) # Oscillator shape to Saw
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.8) # Release time (longer tail)

    # === Step 3: Create MIDI Item & Sustained Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 7] # Root, 3rd, 5th, Octave
    base_octave = 48 # C3
    
    end_ppq = int(beats_per_bar * bars * 960) # Standard 960 PPQ per quarter note
    
    for degree in chord_degrees:
        octave_offset = (degree // 7) * 12
        scale_index = degree % 7
        pitch = base_octave + root_val + scale_intervals[scale_index] + octave_offset
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 0, end_ppq, 0, pitch, velocity_base, False
        )
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Native Automation Generation ===
    # Exclusively select the track to perform actions on it
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Action 40406: Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40406, 0)
    # Action 40456: Track: Toggle track pan envelope visible
    RPR.RPR_Main_OnCommand(40456, 0)
    
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    
    # Write Volume Swell (Shape 2 = Slow Start/End 'S-Curve' for natural fade)
    if vol_env:
        # Time 0: Silence (0.0 amplitude)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, False)
        # End Time: 0dB / Unity Gain (1.0 amplitude)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 0, 0.0, False, False)
        RPR.RPR_Envelope_Sort(vol_env)
        
    # Write Bar-Synced Panning Sweep
    if pan_env:
        for b in range(bars + 1):
            time_pos = b * bar_length_sec
            # Alternate pattern: Center -> Left -> Right -> Center -> Left...
            if b % 2 == 0:
                pan_val = 0.0    # Center
            elif b % 4 == 1:
                pan_val = -1.0   # 100% Left
            else:
                pan_val = 1.0    # 100% Right
                
            # Shape 2 provides a smooth sinusoidal movement between pan points
            RPR.RPR_InsertEnvelopePoint(pan_env, time_pos, pan_val, 2, 0.0, False, False)
        RPR.RPR_Envelope_Sort(pan_env)

    # Set Automation Mode to 1 (Read Mode) so the sweeps execute on playback
    RPR.RPR_SetTrackAutomationMode(track, 1)

    return f"Created '{track_name}' with {bars}-bar Volume Swell & Pan Sweep automation at {bpm} BPM in {key} {scale}."
