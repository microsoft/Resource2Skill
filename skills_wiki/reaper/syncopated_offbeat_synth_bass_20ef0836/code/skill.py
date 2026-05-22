def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat Bass",
    bpm: int = 124,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Syncopated Offbeat Synth Bass sequence in the current REAPER project.

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
        Status string describing the created element.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Define Rhythm & Harmony Pattern ===
    # Base MIDI note for Bass Octave 2 (e.g., C2 = 36)
    root_midi = 36 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_note(degree, oct_offset=0):
        """Calculates exact MIDI pitch allowing for negative degrees (going below root)"""
        octaves = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_midi + scale_intervals[idx] + ((octaves + oct_offset) * 12)

    # Pattern tuples: (16th_step_offset, scale_degree, octave_offset, velocity_modifier, length_in_16ths)
    pattern = [
        (2,   0,  0,  10,  1.5),  # 1.1.50 (off-beat 8th)
        (5,   0,  1, -10,  0.8),  # 1.2.25 (syncopated 16th, octave up jump)
        (6,   0,  0,   0,  1.0),  # 1.2.50 (off-beat 8th)
        (8,   0,  0, -10,  1.0),  # 1.3.00 (downbeat anchor)
        (10,  0,  0,  10,  1.5),  # 1.3.50 (off-beat 8th)
        (14, -3,  0,   5,  1.0),  # 1.4.50 (off-beat 8th, drops to a 5th/4th below root)
        (15,  0,  0, -10,  1.0)   # 1.4.75 (16th pickup into next bar)
    ]

    # === Step 4: Create MIDI Item & Insert Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    item_start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    note_count = 0

    for b in range(bars):
        bar_start_qn = item_start_qn + (b * 4)
        
        for step, degree, oct_offset, vel_mod, dur_16ths in pattern:
            start_qn = bar_start_qn + (step * 0.25)
            end_qn = start_qn + (dur_16ths * 0.25)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            pitch = get_note(degree, oct_offset)
            pitch = max(0, min(127, pitch)) # Clamp to valid MIDI range
            
            vel = max(1, min(127, velocity_base + vel_mod))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (FX Chain) ===
    
    # 1. ReaSynth (The Bass Pluck Engine)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param indexes: 0=Vol, 2=Square, 3=Saw, 6=Attack, 7=Decay, 8=Sustain, 9=Release
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.5)     # Volume (prevent clipping)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)     # 0% Square
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 1.0)     # 100% Sawtooth for aggressive buzz
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.005)   # Attack (very fast, 5ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.150)   # Decay (short, 150ms for the pluck)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.0)     # Sustain (0% to ensure rests are silent)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.050)   # Release (short, 50ms)

    # 2. JS Saturation (To mimic the drive of Massive X)
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    # Param 0: Amount %
    RPR.RPR_TrackFX_SetParam(track, sat_idx, 0, 35.0)      # 35% Drive

    return f"Created '{track_name}' with {note_count} offbeat syncopated notes over {bars} bars at {bpm} BPM in {key} {scale}."
