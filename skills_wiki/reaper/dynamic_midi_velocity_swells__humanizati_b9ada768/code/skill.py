def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Velocity Swell Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    start_vel: int = 35,
    end_vel: int = 115,
    **kwargs
) -> str:
    """
    Create a chord progression with a dynamic velocity swell (crescendo).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        start_vel: Starting velocity for the ramp (0-127).
        end_vel: Ending velocity for the ramp (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add stock synth to make the MIDI audible
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Chords and Velocity Ramp ===
    root_val = NOTE_MAP.get(key, 0) + 60 # Start at C4
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Harmonic progression indices (I, vi, IV, V)
    progression = [0, 5, 3, 4] 
    total_notes_inserted = 0
    total_pulses = bars * 8 # 8th note pulses

    for bar_idx in range(bars):
        # Determine chord root for the current bar
        chord_root_deg = progression[bar_idx % len(progression)]
        
        # Build a diatonic triad (root, 3rd, 5th)
        chord_degrees = [chord_root_deg, chord_root_deg + 2, chord_root_deg + 4]
        
        pitches = []
        for deg in chord_degrees:
            octave_shift = deg // len(scale_intervals)
            scale_idx = deg % len(scale_intervals)
            pitch = root_val + (octave_shift * 12) + scale_intervals[scale_idx]
            pitches.append(pitch)
            
        # Create repeated 8th note block chords
        for eighth_idx in range(8):
            pulse_idx = bar_idx * 8 + eighth_idx
            
            # Interpolate velocity linearly to create the swell
            interp_factor = pulse_idx / max(1, total_pulses - 1)
            vel = int(start_vel + (end_vel - start_vel) * interp_factor)
            vel = max(1, min(127, vel)) # Clamp safely
            
            # Timing calculations
            start_time = bar_idx * bar_length_sec + eighth_idx * (bar_length_sec / 8)
            end_time = start_time + (bar_length_sec / 8) * 0.8 # 80% duration for articulation
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert notes
            for pitch in pitches:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
                total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {total_notes_inserted} notes over {bars} bars at {bpm} BPM. Velocity ramps from {start_vel} to {end_vel}."
