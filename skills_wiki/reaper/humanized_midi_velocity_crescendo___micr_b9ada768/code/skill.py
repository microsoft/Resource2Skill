def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 40,
    **kwargs,
) -> str:
    """
    Create Humanized MIDI Velocity Crescendo & Micro-Timing pattern.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Starting MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for basic auditioning (Stock Plugin)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the synth slightly so chords aren't harsh
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Attack time

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: MIDI Pitch & Harmony Engine ===
    root_midi = 48 + NOTE_MAP.get(key, 0) # Base Octave 3
    scale_intervals = SCALES.get(scale, SCALES["major"])

    def get_midi_note(degree, root):
        octave_shift = degree // 7
        scale_degree = degree % 7
        return root + (octave_shift * 12) + scale_intervals[scale_degree]

    # I - IV - V - vi progression mapped to scale degrees
    progression = [0, 3, 4, 5]
    if bars < 4:
        progression = progression[:bars]
    else:
        progression = (progression * (bars // 4 + 1))[:bars]

    # === Step 5: Velocity Ramp & Humanization ===
    notes_per_bar = 8
    note_len_sec = bar_length_sec / notes_per_bar
    vel_start = max(10, velocity_base)
    vel_end = min(127, velocity_base + 60) # Ramp up by 60 for an audible crescendo
    
    total_notes = 0

    for bar_idx, chord_root_degree in enumerate(progression):
        # Triad voicing: root, 3rd, 5th
        chord_degrees = [chord_root_degree, chord_root_degree + 2, chord_root_degree + 4]

        for i in range(notes_per_bar):
            # 1. Micro-timing humanization (Emulates Shift+Drag bypassing grid)
            time_offset = random.uniform(-0.015, 0.015) 
            start_time = (bar_idx * bar_length_sec) + (i * note_len_sec) + time_offset
            
            # Note length variation
            dur = note_len_sec * random.uniform(0.75, 0.90)
            end_time = start_time + dur

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # 2. Velocity Ramping (Emulates drawing a slant in the velocity CC lane)
            ramp_progress = i / max(1, (notes_per_bar - 1))
            current_vel = int(vel_start + (vel_end - vel_start) * ramp_progress)

            for degree in chord_degrees:
                pitch = get_midi_note(degree, root_midi)
                
                # Micro-strum effect: offset higher notes slightly
                strum_offset_ppq = start_ppq + (chord_degrees.index(degree) * 12)

                # Insert note natively
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    strum_offset_ppq, end_ppq, 
                    0, pitch, current_vel, True
                )
                total_notes += 1

    # Sort the MIDI buffer after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {total_notes} humanized, velocity-ramped notes over {bars} bars in {key} {scale} at {bpm} BPM."
