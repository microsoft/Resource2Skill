def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groovy Slap Bass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a humanized, syncopated slap bassline in REAPER.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Lookup ===
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

    scale_arr = SCALES.get(scale.lower(), SCALES["minor"])
    # Bass root note usually sits around E1 (MIDI 28) to C2 (MIDI 36)
    base_midi = 24 + NOTE_MAP.get(key.upper(), 4) # Default to E1 if not found

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure Instrument (ReaSynth + ReaEQ) ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak synth for a punchier bass tone (Saw/Square mix, fast attack)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)  # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.01) # Fast attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.05) # Fast release

    # Add ReaEQ for bass enhancement
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0.1)     # Band 1 Freq (~80Hz)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 6.0)     # Band 1 Gain (+6dB punch)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 8, 0.6)     # Band 4 Freq (Cut high end)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, -12.0)   # Band 4 Gain (-12dB)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Groove Pattern Definition (2 bars)
    # Format: (beat_position, scale_degree_offset, octave_jump, length_in_beats, velocity_type)
    groove_pattern = [
        (0.0,   0,  0, 0.5,   "NORMAL"), # Downbeat root
        (1.5,   0,  0, 0.25,  "NORMAL"), # Syncopated root
        (1.75,  0,  1, 0.125, "SLAP"),   # Octave slap on the 'a' of 2
        (2.5,   0,  0, 0.5,   "NORMAL"), # Offbeat root
        (3.5,  -1,  0, 0.25,  "GHOST"),  # Ghost approach note (scale degree below)
        (3.75,  0,  1, 0.125, "SLAP"),   # Slap right before bar 2
        
        (4.0,   0,  0, 0.5,   "NORMAL"), # Downbeat root bar 2
        (5.5,   0,  0, 0.25,  "NORMAL"), # Syncopated
        (5.75,  0,  1, 0.125, "SLAP"),   # Octave slap
        (6.5,   0,  0, 0.5,   "NORMAL"), # Offbeat root
        (7.25, -2,  0, 0.25,  "GHOST"),  # Walk down note 1
        (7.75, -1,  0, 0.25,  "GHOST")   # Walk down note 2
    ]

    # === Step 5: Generate and Humanize MIDI Notes ===
    note_count = 0
    for bar in range(0, bars, 2):
        for beat_pos, degree_offset, oct_jump, length_beats, vel_type in groove_pattern:
            
            # Stop if we exceed the requested number of bars (e.g. if bars = 1, we stop halfway)
            if bar + (beat_pos / 4.0) >= bars:
                continue

            # 1. Calculate absolute timing
            total_beats = (bar * 4) + beat_pos
            start_time = total_beats * (60.0 / bpm)
            end_time = start_time + (length_beats * (60.0 / bpm))

            # Humanize timing (unquantized feel, +/- 15 milliseconds)
            start_time += random.uniform(-0.015, 0.015)
            end_time += random.uniform(-0.015, 0.015)
            start_time = max(0.0, start_time) # Prevent negative times

            # 2. Calculate pitch based on scale degrees and octaves
            octave_shift = degree_offset // len(scale_arr)
            mapped_degree = degree_offset % len(scale_arr)
            
            pitch = base_midi + scale_arr[mapped_degree] + (octave_shift * 12) + (oct_jump * 12)
            pitch = max(0, min(127, pitch))

            # 3. Calculate dynamic velocity (Humanized)
            if vel_type == "SLAP":
                target_vel = 127
            elif vel_type == "GHOST":
                target_vel = 70
            else:
                target_vel = velocity_base
                
            vel = target_vel + random.randint(-8, 8)
            vel = max(1, min(127, vel))

            # 4. Insert Note
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} humanized notes (slaps & ghost notes) over {bars} bars at {bpm} BPM in {key} {scale}."
