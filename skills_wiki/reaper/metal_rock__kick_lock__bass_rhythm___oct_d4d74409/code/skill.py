def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal/Rock "Kick-Lock" Bass rhythm with octave leaps in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", representing Drop C tuning).
        scale: Scale type (not strictly used here as the pattern relies on root and octave).
        bars: Number of bars to generate (pattern loops every 2 bars).
        velocity_base: Base MIDI velocity (lowered to ~110 to reduce harsh attack transients).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Note map centered on MIDI octave 1 (typical for metal virtual basses in drop tunings)
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
    
    # Normalize key input and fetch root pitch
    key_formatted = key.capitalize() if len(key) == 1 else key[0].capitalize() + key[1:]
    root_pitch = NOTE_MAP.get(key_formatted, 24) # Default to C1

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define a 2-bar kick-locking rhythm
    # Tuple format: (beat_position, duration_in_beats, velocity, pitch_offset)
    pattern = [
        # Bar 1: Straight syncopated chugs
        (0.0, 0.25, velocity_base, 0),       # 16th
        (0.25, 0.25, velocity_base, 0),      # 16th
        (0.5, 0.5, velocity_base, 0),        # 8th
        (1.5, 0.5, velocity_base + 5, 0),    # 8th Accent
        (2.0, 0.25, velocity_base, 0),       # 16th
        (2.25, 0.25, velocity_base, 0),      # 16th
        (2.5, 0.5, velocity_base, 0),        # 8th
        (3.5, 0.5, velocity_base + 5, 0),    # 8th Accent
        
        # Bar 2: Chugs with octave leaps (simulating 12th fret guitar slides)
        (4.0, 0.25, velocity_base, 0),       # 16th
        (4.25, 0.25, velocity_base, 0),      # 16th
        (4.5, 0.5, velocity_base, 0),        # 8th
        (5.5, 0.5, velocity_base + 10, 12),  # +12 Octave jump!
        (6.0, 0.25, velocity_base, 0),       # 16th
        (6.25, 0.25, velocity_base, 0),      # 16th
        (6.5, 0.5, velocity_base, 0),        # 8th
        (7.5, 0.5, velocity_base + 10, 12),  # +12 Octave jump!
    ]

    note_count = 0
    # Loop over the requested number of bars
    for bar in range(bars):
        # The pattern is 2 bars long (8 beats). We find which half of the pattern to use.
        bar_pattern_offset = (bar % 2) * beats_per_bar
        bar_start_time = bar * bar_length_sec
        
        for beat, duration, vel, pitch_mod in pattern:
            # Check if this pattern note belongs in the current 1-bar slice
            if beat >= bar_pattern_offset and beat < bar_pattern_offset + beats_per_bar:
                # Normalize beat relative to the current bar
                local_beat = beat - bar_pattern_offset
                
                note_start_time = bar_start_time + (local_beat * sec_per_beat)
                note_end_time = note_start_time + (duration * sec_per_beat)
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
                
                # Apply pitch offsets (for octave leaps) and clamp velocities
                final_pitch = min(127, max(0, root_pitch + pitch_mod))
                final_vel = min(127, max(1, vel))
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, final_pitch, final_vel, True)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain for rough Metal Bass approximation ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if synth_idx >= 0:
        # Increase Sawtooth mix for a grittier bass tone
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.5)  # Volume
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 1.0)  # Saw mix
    
    # Add a touch of distortion to emulate an overdriven bass amp
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    if dist_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 3.0)   # Gain/Drive

    return f"Created '{track_name}' with {note_count} metal bass notes over {bars} bars at {bpm} BPM (Base Velocity: {velocity_base})."
