def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Viral Syncopated Bass",
    bpm: int = 90,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a syncopated Neo-Soul/R&B bassline using the root-octave-5th technique.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (generates a 2-bar A/B looping pattern).
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string.
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

    # Normalize inputs
    key_upper = key.upper()
    scale_lower = scale.lower()
    root_val = NOTE_MAP.get(key_upper, 0)
    scale_intervals = SCALES.get(scale_lower, SCALES["minor"])
    
    # Bass occupies the 2nd octave (C2 = 36)
    base_midi = 36 + root_val 

    # Determine dynamic passing notes based on the scale
    p5 = 7 # Perfect 5th interval
    # The passing note to slide into the root from below (usually the 7th degree)
    pass_under = scale_intervals[-1] - 12 

    # Construct the sequence (Time in beats, Pitch Offset, Duration in beats, Velocity)
    pattern = []
    for bar in range(bars):
        bar_start = bar * 4.0

        if bar % 2 == 0:
            # Bar A: Root chord focus
            pattern.append((bar_start + 0.0, 0, 1.5, int(velocity_base * 1.1)))       # Downbeat Root
            pattern.append((bar_start + 1.75, 12, 0.25, int(velocity_base * 0.85)))   # Syncopated Octave Jump (16th note)
            pattern.append((bar_start + 2.5, p5, 0.5, int(velocity_base * 1.0)))      # 5th
            pattern.append((bar_start + 3.5, pass_under, 0.5, int(velocity_base * 0.9))) # Passing tone (e.g. minor 7th)
        else:
            # Bar B: 5th chord focus (provides harmonic movement)
            pattern.append((bar_start + 0.0, p5 - 12, 1.5, int(velocity_base * 1.1))) # Downbeat 5th (low octave)
            pattern.append((bar_start + 1.75, p5, 0.25, int(velocity_base * 0.85)))   # Syncopated Octave Jump
            pattern.append((bar_start + 2.5, 0, 0.5, int(velocity_base * 1.0)))       # Return to root shape
            pattern.append((bar_start + 3.5, pass_under, 0.5, int(velocity_base * 0.9))) # Passing tone back to Bar A

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Sub Bass Sound Design) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.7)  # Volume
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.02) # Fast Attack
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)  # Punchy Decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5)  # Sustain Level
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.2)  # Quick Release
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0)  # 0% Square
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.0)  # 0% Saw
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.7)  # 70% Triangle (Adds warm harmonic distortion to Sine)

    # === Step 4: Create MIDI Item & Insert Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    for beat_pos, pitch_offset, duration_beats, vel in pattern:
        # Convert beats to time, then time to PPQ
        start_time = beat_pos * (60.0 / bpm)
        end_time = (beat_pos + duration_beats) * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        pitch = int(base_midi + pitch_offset)
        
        # Clamp MIDI values for safety
        pitch = max(0, min(127, pitch))
        vel = max(1, min(127, vel))

        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Force UI update
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with a {bars}-bar syncopated bass groove in {key} {scale} at {bpm} BPM."
