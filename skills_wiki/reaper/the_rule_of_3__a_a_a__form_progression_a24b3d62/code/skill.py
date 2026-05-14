def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a chord progression demonstrating the 'Rule of 3' (A-A-A' variation) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.). Defaults to minor for the standard pop progression.
        bars: Number of bars to generate (ideally a multiple of 12 to complete the 3-cycle phases).
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

    # Ensure valid inputs
    key = key if key in NOTE_MAP else "C"
    scale = scale if scale in SCALES else "minor"
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Prevent master bus clipping
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Roughly -6dB

    # === Step 3: Add FX Chain First (to ensure it plays) ===
    # Add simple synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a smoother pad/keys sound (Square blend, slightly lower cutoff)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.4) # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.6) # Release

    # Add Reverb
    fx_verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_verb_idx, 0, 0.8) # Wet
    RPR.RPR_TrackFX_SetParam(track, fx_verb_idx, 1, 0.2) # Dry
    RPR.RPR_TrackFX_SetParam(track, fx_verb_idx, 2, 0.7) # Room size

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define the chord progressions by scale degrees
    # 0 = i, 1 = ii, 2 = III, 3 = iv, 4 = v, 5 = VI, 6 = VII
    progression_A = [0, 5, 2, 6]  # i - VI - III - VII
    progression_A_prime = [0, 5, 3, 4]  # i - VI - iv - v (The Variation)

    scale_intervals = SCALES[scale]
    scale_len = len(scale_intervals)
    root_offset = NOTE_MAP[key]
    octave_base = 48  # C3 for chords
    bass_octave = 36  # C2 for bassline

    notes_created = 0

    # Insert notes bar by bar
    for b in range(bars):
        # Determine macro structure (4-bar chunks)
        chunk_idx = b // 4
        bar_in_chunk = b % 4

        # APPLY THE RULE OF 3: Every 3rd iteration (index 2), play the variation
        if chunk_idx % 3 == 2:
            current_degree = progression_A_prime[bar_in_chunk]
        else:
            current_degree = progression_A[bar_in_chunk]

        # Time calculations
        start_time = b * bar_length_sec
        # Chords ring out for almost the whole bar
        end_time = start_time + (bar_length_sec * 0.95) 

        # Convert to PPQ for REAPER MIDI API
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        # 1. Generate Triad (Root, 3rd, 5th)
        for chord_tone in [0, 2, 4]:
            deg_index = current_degree + chord_tone
            
            # Calculate octave shifts if the interval wraps past the scale end (e.g. 7th note)
            octave_shift = (deg_index // scale_len) * 12
            interval = scale_intervals[deg_index % scale_len]
            
            pitch = octave_base + root_offset + octave_shift + interval
            
            # Ensure pitch is in valid MIDI range (0-127)
            pitch = max(0, min(127, pitch))
            
            # Insert Triad Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
            notes_created += 1

        # 2. Add rhythmic bass notes (quarter notes on beats 1 and 3)
        bass_pitch = bass_octave + root_offset + scale_intervals[current_degree % scale_len]
        bass_pitch = max(0, min(127, bass_pitch))
        
        for beat in [0, 2]:
            b_start_time = start_time + (beat * (60.0 / bpm))
            b_end_time = b_start_time + (60.0 / bpm * 0.9) # Slightly detached
            b_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, b_start_time)
            b_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, b_end_time)
            
            # Bass notes hit slightly harder
            RPR.RPR_MIDI_InsertNote(take, False, False, b_start_ppq, b_end_ppq, 0, int(bass_pitch), velocity_base + 15, False)
            notes_created += 1

    # Force MIDI evaluation
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' applying the 'Rule of 3' with {notes_created} notes over {bars} bars at {bpm} BPM in {key} {scale}."
