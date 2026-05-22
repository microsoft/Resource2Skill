def create_pattern(
    project_name: str = "TranceProject",
    track_name: str = "Rolling Bass",
    bpm: int = 138,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Trance/EDM Rolling 16th Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (Trance is typically 135-140).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the bassline.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) and Configure Envelope ===
    # For a rolling bass, we want 100% saw wave, fast attack, zero sustain, short release.
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth Param Mapping:
    # 0: Volume, 1: Tuning, 2: Attack, 3: Decay, 4: Sustain, 5: Release
    # 6: Square Mix, 7: Saw Mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.4)    # Volume (slightly lower)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)    # Attack (0 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.05)   # Decay (~50 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)    # Sustain (0%)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.05)   # Release (~50 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0)    # Square mix (0%)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 1.0)    # Saw mix (100%)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Notes ===
    base_midi = 36 # C2
    root_offset = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = base_midi + root_offset - 12 # Octave 1 (Sub/Bass)

    # Progression: i - VI - VII - i (indices 0, 5, 6, 0 in minor scale)
    progression = [0, 5, 6, 0]
    
    sixteenth_len_sec = beat_len_sec / 4.0
    note_duration = sixteenth_len_sec * 0.85 # Staccato articulation
    note_count = 0

    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        
        # Determine the pedal root note for this bar
        deg_idx = progression[bar % len(progression)] % len(scale_intervals)
        pitch = root_midi + scale_intervals[deg_idx]

        for beat in range(beats_per_bar):
            beat_start_sec = bar_start_sec + beat * beat_len_sec

            # Trance roll: skip 0 (downbeat for kick), play on 1, 2, 3 (16ths: e, &, a)
            for sixteenth in [1, 2, 3]:
                note_start_sec = beat_start_sec + sixteenth * sixteenth_len_sec
                note_end_sec = note_start_sec + note_duration

                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)

                # Minor velocity variation to groove
                vel = velocity_base if sixteenth == 2 else velocity_base - 10

                RPR.RPR_MIDI_InsertNote(
                    take, False, False,
                    start_ppq, end_ppq,
                    0, int(pitch), vel, -1
                )
                note_count += 1

    # Apply notes
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} rolling bass notes over {bars} bars at {bpm} BPM."
