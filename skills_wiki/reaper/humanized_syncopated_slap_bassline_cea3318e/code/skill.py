def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Slap Bass",
    bpm: int = 115,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Humanized Syncopated Slap Bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard plucked notes (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import random
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

    # Validate inputs
    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "minor"
    
    base_pitch = 24 + NOTE_MAP[key] # Shift down to Bass octave (C1/E1)
    scale_intervals = SCALES[scale]

    # Chord progression (Scale degrees: i - VI - iv - v)
    progression_indices = [0, 5, 3, 4] 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Note Generation Loop
    # Pattern schema: (beat_start, duration_beats, type, vel_offset)
    humanize_timing = 0.015  # +/- 15ms
    humanize_vel = 6

    total_notes = 0
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        
        # Determine current chord root
        chord_idx = progression_indices[bar % len(progression_indices)]
        root_pitch = base_pitch + scale_intervals[chord_idx % len(scale_intervals)]
        
        # Determine next chord root for approach notes
        next_chord_idx = progression_indices[(bar + 1) % len(progression_indices)]
        next_root_pitch = base_pitch + scale_intervals[next_chord_idx % len(scale_intervals)]

        is_last_bar_of_phrase = (bar % 2 == 1)

        # Base rhythm pattern matching the tutorial's groove
        pattern = [
            (0.0, 0.5, 'root', 0),           # Downbeat
            (0.75, 0.25, 'root', -12),       # Syncopated 16th (a of 1)
            (1.5, 0.15, 'octave', 25),       # Staccato Slap (and of 2)
            (2.5, 0.5, 'root', 5),           # Syncopated pull (and of 3)
        ]
        
        # Alter the end of the bar depending on phrasing
        if is_last_bar_of_phrase:
            # Add passing/approach notes to walk into the next chord
            pattern.extend([
                (3.25, 0.25, 'root', -5),
                (3.75, 0.25, 'approach', -8) # "a" of 4, semitone below next root
            ])
        else:
            # Standard turnaround slap
            pattern.extend([
                (3.5, 0.15, 'octave', 25)    # Staccato Slap (and of 4)
            ])

        for beat_pos, duration_beats, note_type, vel_mod in pattern:
            # Determine Pitch
            if note_type == 'root':
                pitch = root_pitch
            elif note_type == 'octave':
                pitch = root_pitch + 12
            elif note_type == 'approach':
                pitch = next_root_pitch - 1 # Chromatic approach from below
            else:
                pitch = root_pitch
                
            # Apply Humanization to Velocity
            vel = velocity_base + vel_mod + random.randint(-humanize_vel, humanize_vel)
            vel = max(1, min(127, vel))
            
            # Apply Humanization to Timing
            note_start_time = bar_start_time + (beat_pos * beat_length_sec)
            note_start_time += random.uniform(-humanize_timing, humanize_timing)
            note_start_time = max(0.0, note_start_time)
            
            note_end_time = note_start_time + (duration_beats * beat_length_sec)

            # Convert to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)

            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)
            total_notes += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (ReaSynth Bass) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a plucky/slappy bass tone
    # Param 0: Volume (Normalized 0.0-1.0, 0.5 is approx -6dB)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.6)
    # Param 2: Attack (Keep at 0 for punchy transient)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)
    # Param 3: Decay (Fast decay for plucked feel)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.15)
    # Param 4: Sustain (Low sustain)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.2)
    # Param 5: Release (Short release to respect staccato lengths)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.05)
    # Param 6: Square Wave Mix (Adds harmonic richness mimicking a bass string slap)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.35)

    return f"Created '{track_name}' with {total_notes} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
