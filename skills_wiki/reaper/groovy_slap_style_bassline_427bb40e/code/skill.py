def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Groovy Slap-Style Bassline in the current REAPER project.

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

    if scale not in SCALES:
        scale = "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup FX Chain for Plucky Slap Sound ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape the waveform: 70% Saw, 30% Square for rich harmonics
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.7) # Saw
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.3) # Square
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.3) # Volume (prevent clipping)
    # Envelope: Fast attack, short decay/sustain for pluck
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.1) # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.1) # Release

    # Add Saturation for transient bite
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(track, sat_idx, 0, 0.4) # Saturation Amount

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    grid_16th = bar_length_sec / 16.0
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Music Theory Driven Pattern ===
    # A standard funk progression using scale degrees: I - I - IV - V
    progression = [0, 0, 3, 4] 
    note_count = 0

    for bar in range(bars):
        current_chord = progression[bar % len(progression)]
        next_chord = progression[(bar + 1) % len(progression)]

        # Pattern mapping: (16th_step, length_in_16ths, scale_degree_offset, octave_offset, velocity_multiplier)
        pattern = [
            (0,  1.5, current_chord,          0, 1.0),   # Beat 1 Downbeat pluck
            (2,  0.5, current_chord,          1, 1.2),   # Offbeat octave POP
            (3,  0.5, current_chord,          0, 0.5),   # Ghost note
            (6,  1.0, current_chord + 4,      0, 0.9),   # Perfect 5th of chord
            (8,  1.5, current_chord,          0, 1.0),   # Beat 3 pluck
            (10, 0.5, current_chord,          1, 1.2),   # Offbeat octave POP
            (13, 0.5, current_chord,          0, 0.5),   # Ghost note setup
            (14, 0.5, current_chord,          0, 0.5),   # Ghost note 2
            (15, 0.5, next_chord - 1,         0, 0.9),   # Diatonic approach note to next chord
        ]

        for step, length, deg, oct_val, vel_mult in pattern:
            # Calculate exact MIDI pitch based on scale degrees and octaves
            # Div/Mod handles wraparounds naturally (e.g. going below root drops an octave)
            normalized_deg = deg % len(SCALES[scale])
            octave_shift = deg // len(SCALES[scale])
            semi_offset = SCALES[scale][normalized_deg]

            # Base MIDI 36 is C1. A good sub/bass foundation range.
            midi_note = 36 + NOTE_MAP[key] + semi_offset + (octave_shift + oct_val) * 12
            
            # Constrain velocity
            vel = int(velocity_base * vel_mult)
            vel = max(1, min(127, vel))

            # Calculate timing
            start_time = bar * bar_length_sec + step * grid_16th
            end_time = start_time + length * grid_16th

            # Humanization / Swing: Delay offbeat 16ths slightly
            swing_amt = 0.015 if step % 2 != 0 else 0.0
            start_time += swing_amt
            end_time += swing_amt

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_note, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} dynamic notes over {bars} bars at {bpm} BPM in {key} {scale}."
