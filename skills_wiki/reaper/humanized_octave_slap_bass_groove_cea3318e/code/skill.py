def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass Groove",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a humanized, octave-jumping slap bass groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = NOTE_MAP.get(key.capitalize(), 4) + 24 # Start in octave 1/2 (e.g. E1 = 28)

    # Progression: I - VI - IV - V (represented by scale degrees: 0, 5, 3, 4)
    progression_degrees = [0, 5, 3, 4] 
    
    def get_chord_root(bar_idx):
        degree = progression_degrees[bar_idx % len(progression_degrees)]
        octave_offset = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_midi + (octave_offset * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Groove (MIDI Notes) ===
    # Rhythmic blueprint: (start_beat, length_beats, is_octave_slap, vel_offset)
    groove_blueprint = [
        (0.00, 0.50, False, 5),   # Downbeat anchor
        (0.75, 0.20, True,  20),  # 16th pickup slap
        (1.50, 0.25, False, -10), # Offbeat low root (ghostly)
        (1.75, 0.20, True,  15),  # 16th pickup slap
        (2.00, 0.50, False, 0),   # Beat 3 anchor
        (2.75, 0.20, True,  18),  # 16th pickup slap
    ]

    note_count = 0
    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        current_root = get_chord_root(bar)
        next_root = get_chord_root(bar + 1)

        # 1. Add main groove notes
        for hit in groove_blueprint:
            beat_pos, length, is_octave, vel_mod = hit
            
            pitch = current_root + 12 if is_octave else current_root
            vel = min(127, max(1, velocity_base + vel_mod + random.randint(-6, 6)))
            
            # Humanize timing
            timing_drift = random.uniform(-0.02, 0.02) * beat_length_sec
            note_start_sec = bar_start_sec + (beat_pos * beat_length_sec) + timing_drift
            note_end_sec = note_start_sec + (length * beat_length_sec)

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

        # 2. Add chromatic approach notes ("steps up to the root") at the end of the bar
        approach_notes = [
            (3.50, next_root + 2, 0.20), # Whole step above/below (simplified)
            (3.75, next_root + 1 if current_root < next_root else next_root - 1, 0.20) # Chromatic leading tone
        ]
        
        for beat_pos, pitch, length in approach_notes:
            vel = min(127, max(1, velocity_base - 5 + random.randint(-6, 6)))
            timing_drift = random.uniform(-0.02, 0.02) * beat_length_sec
            note_start_sec = bar_start_sec + (beat_pos * beat_length_sec) + timing_drift
            note_end_sec = note_start_sec + (length * beat_length_sec)

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (ReaSynth) ===
    # Using ReaSynth to mimic a plucky, slightly buzzy bass that cuts through
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Param 0: Volume (bring it down to prevent clipping)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)
    # Param 3: Square Mix (adds upper harmonics for the 'slap' feel)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.25)
    # Param 7: Attack (instant)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.0)
    # Param 8: Decay (short, plucky)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.08)
    # Param 9: Sustain (low, keeps it staccato)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.1)
    # Param 10: Release (quick stop)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 0.05)

    return f"Created '{track_name}' with {note_count} humanized slap bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
