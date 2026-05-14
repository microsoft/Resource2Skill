def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Expressive Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create Expressive / Humanized MIDI Chord Progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for the hardest note (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":          [0, 2, 4, 5, 7, 9, 11],
        "minor":          [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian":         [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":     [0, 2, 4, 5, 7, 9, 10]
    }
    
    # Fallback to major if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    
    # Define a simple progression: I - V - vi - IV (indices 0, 4, 5, 3 in 0-indexed scale)
    progression_degrees = [0, 4, 5, 3]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMediaItem(0, track, 0.0, total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Helper to get exact pitch
    def get_scale_pitch(octave, degree):
        # degree can be > 6, handle wrap around
        octave_shift = degree // 7
        scale_idx = degree % 7
        note = root_val + scale_intervals[scale_idx]
        return (octave + octave_shift + 1) * 12 + note

    # === Step 4: Generate Humanized Chords ===
    notes_created = 0
    # Create chords spanning the requested bars
    for bar in range(bars):
        # Pick chord based on current bar (looping the progression)
        degree = progression_degrees[bar % len(progression_degrees)]
        
        # Calculate time positions
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # We will build a root position triad with a doubled bass octave
        # Chord voices: Bass (root - 1 oct), Root, Third, Fifth
        voices = [
            (3, degree, 0),         # Bass (-1 octave relative to center C4)
            (4, degree, 0),         # Root
            (4, degree + 2, -20),   # Third (played softer, -20 velocity)
            (4, degree + 4, -10)    # Fifth (played medium, -10 velocity)
        ]
        
        for oct_base, scale_deg, vel_offset in voices:
            pitch = get_scale_pitch(oct_base, scale_deg)
            
            # Apply humanization to velocity as instructed in the tutorial
            human_variance = random.randint(-4, 4)
            final_velocity = max(1, min(127, velocity_base + vel_offset + human_variance))
            
            # Slightly offset start time by a tiny random amount for realistic strum/roll (0-10 PPQ)
            human_timing = random.randint(0, 8) 
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq + human_timing, end_ppq, 
                0, pitch, int(final_velocity), True
            )
            notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX (ReaSynth piano-like settings) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth to sound a bit like a mellow EP/Piano
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)   # Attack short
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.3)   # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.2)   # Sustain lower
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.4)   # Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.0)   # Saw mix

    return f"Created '{track_name}' with {notes_created} humanized chord notes over {bars} bars at {bpm} BPM in {key} {scale}."
