def create_pattern(
    project_name: str = "RhythmAndBass",
    track_name: str = "R&B Bassline (R-5-8)",
    bpm: int = 90,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a syncopated Root-5th-Octave bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (generates a I - V progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # Base octave for basslines is typically Octave 2 (MIDI Note 36 = C2)
    base_midi = 36 + NOTE_MAP.get(key.upper().capitalize(), 5) # Default to F if not found

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Setup FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth and dial in a warm R&B Bass tone (Mostly sine/triangle, minimal saw)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.1)  # Square mix (low for warmth)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.0)  # Saw mix (0 to avoid harshness)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Safely create a MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetMediaItemTake(item, 0)

    # === Step 4: Generate R-5-8 Bassline Pattern ===
    note_count = 0
    for b in range(bars):
        bar_start_sec = b * bar_length_sec
        
        # Alternate between the I chord and the V chord (e.g., F minor to C minor)
        is_five_chord = (b % 2 != 0)
        chord_root = base_midi + 7 if is_five_chord else base_midi
        
        # Determine the passing note based on scale (Minor 7th for I, descending step for V)
        if scale == "minor":
            passing_interval = 5 if is_five_chord else 10
        else:
            passing_interval = 5 if is_five_chord else 11

        # Groove Array: (beat_position, duration_in_beats, interval_from_chord_root, velocity_offset)
        groove_pattern = [
            (0.0,  0.75, 0,                0),   # Downbeat Root
            (1.25, 0.25, 12,             -15),   # Syncopated Octave Jump (lighter velocity)
            (2.0,  0.5,  0,               -5),   # Root return
            (2.5,  0.5,  7,               -5),   # Jump to Perfect 5th
            (3.5,  0.5,  passing_interval,-10)   # Passing note into next bar
        ]

        for beat_pos, duration, interval, vel_mod in groove_pattern:
            note_start_sec = bar_start_sec + beat_pos * (60.0 / bpm)
            note_end_sec = note_start_sec + duration * (60.0 / bpm)

            # Convert seconds to PPQ (ticks)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)

            pitch = chord_root + interval
            pitch = max(0, min(127, pitch)) # Clamp to valid MIDI range
            
            velocity = max(1, min(127, velocity_base + vel_mod))

            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} syncopated bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
