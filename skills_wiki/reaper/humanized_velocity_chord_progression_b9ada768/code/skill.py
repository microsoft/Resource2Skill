def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a chord progression with humanized, ramping MIDI velocities.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (used as a reference, locks to project).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for the peak of the swell (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math
    import random

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

    # Setup core pitch info
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Anchor at C3
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_pitch(degree):
        """Convert a scale degree (0-indexed) to absolute MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        interval = scale_intervals[degree % len(scale_intervals)]
        return root_pitch + (octave_shift * 12) + interval

    # Standard pop progression: I, V, vi, IV (represented by scale degrees)
    progression = [0, 4, 5, 3]

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Calculate Timing & Create Item ===
    # Use standard 4/4 time signature calculations
    qn_per_bar = 4.0
    start_time = RPR.RPR_GetCursorPosition()
    start_qn = RPR.RPR_TimeMap2_TimeToQN(0, start_time)
    end_qn = start_qn + (bars * qn_per_bar)
    end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
    item_length = end_time - start_time

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Generate Notes with Humanized Velocity Ramp ===
    notes_per_bar = 8
    step_qn = qn_per_bar / notes_per_bar # 0.5 QN for 8th notes
    total_steps = bars * notes_per_bar
    notes_added = 0

    for step in range(total_steps):
        # Calculate timing
        current_qn = start_qn + (step * step_qn)
        note_end_qn = current_qn + (step_qn * 0.85) # 85% length for slight detachment
        
        n_start_time = RPR.RPR_TimeMap2_QNToTime(0, current_qn)
        n_end_time = RPR.RPR_TimeMap2_QNToTime(0, note_end_qn)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_end_time)

        # Determine chord
        bar_idx = step // notes_per_bar
        chord_root_degree = progression[bar_idx % len(progression)]
        chord_pitches = [
            get_pitch(chord_root_degree),     # Root
            get_pitch(chord_root_degree + 2), # 3rd
            get_pitch(chord_root_degree + 4)  # 5th
        ]

        # Velocity Macro-Ramp (Sine wave swell simulating a hand-drawn velocity curve)
        progress = step / max(1, total_steps - 1)
        swell_multiplier = math.sin(progress * math.pi) # 0.0 -> 1.0 -> 0.0
        
        min_vel = max(10, velocity_base - 40)
        max_vel = min(127, velocity_base + 10)
        macro_vel = min_vel + (max_vel - min_vel) * swell_multiplier

        # Insert notes
        for i, pitch in enumerate(chord_pitches):
            # Humanization: Strum stagger (0-15 PPQ per note) and velocity jitter
            stagger_ppq = i * random.randint(5, 15)
            vel_jitter = random.randint(-6, 6)
            final_vel = int(max(1, min(127, macro_vel + vel_jitter)))
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq + stagger_ppq, 
                end_ppq, 
                0, int(pitch), final_vel, True
            )
            notes_added += 1

    # Apply sorting after all notes are inserted with noSort=True
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Simple Synth FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' with {notes_added} humzanized velocity notes over {bars} bars."
