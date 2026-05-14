def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Funk Clav/Synth",
    bpm: int = 115,
    key: str = "C",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a highly syncopated 16th-note funk triad groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (105-125 recommended).
        key: Root note (C, C#, D, ..., B).
        scale: Ignored technically since pattern overrides to Dorian by definition.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # We lock into the Dorian scale structure as it is essential for this funk pattern
    dorian_intervals = [0, 2, 3, 5, 7, 9, 10]
    
    # Establish root base in Octave 4 (MIDI note 60 = C4)
    root_pitch = 60 + NOTE_MAP.get(key, 0)
    
    def get_scale_pitch(degree: int, octave: int = 0) -> int:
        """Returns the absolute MIDI pitch for a scale degree (0-indexed) with octave shift."""
        octave_shift = (octave * 12) + ((degree // 7) * 12)
        return root_pitch + dorian_intervals[degree % 7] + octave_shift

    # Voice leading our Dorian Triads
    chords = {
        "root_bass": [get_scale_pitch(0, -2), get_scale_pitch(0, -1)],   # LH Octaves
        "i_min":     [get_scale_pitch(0, 0), get_scale_pitch(2, 0), get_scale_pitch(4, 0)],   # e.g., C Eb G
        "IV_maj":    [get_scale_pitch(3, 0), get_scale_pitch(5, 0), get_scale_pitch(0, 1)],   # e.g., F A C (inverted)
        "VII_maj":   [get_scale_pitch(6, -1), get_scale_pitch(1, 0), get_scale_pitch(3, 0)],  # e.g., Bb D F (inverted)
    }

    # Define the core 1-bar rhythmic "conversation" (offset in quarter notes, length in quarter notes)
    # 0.25 = 16th note length. Rhythmic points: 0.0=Beat1, 1.0=Beat2, 2.0=Beat3, 3.0=Beat4
    pattern = [
        (0.25, 0.15, "root_bass", 0.90), # LH: 1 'e'
        (0.75, 0.15, "root_bass", 1.00), # LH: 1 'a'
        (1.00, 0.20, "i_min",     1.10), # RH: 2 (Downbeat stab)
        (1.50, 0.20, "i_min",     0.95), # RH: 2 '&'
        (2.25, 0.15, "root_bass", 0.90), # LH: 3 'e'
        (2.50, 0.20, "IV_maj",    1.05), # RH: 3 '&'
        (2.75, 0.15, "root_bass", 0.85), # LH: 3 'a'
        (3.00, 0.20, "VII_maj",   1.10), # RH: 4 (Downbeat stab)
        (3.75, 0.15, "root_bass", 1.00), # LH: 4 'a' (pickup into next bar)
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Take ===
    beats_per_bar = 4
    quarter_len_sec = 60.0 / bpm
    bar_length_sec = quarter_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Populate MIDI Notes ===
    total_notes_added = 0
    for b in range(bars):
        bar_start_time = b * bar_length_sec
        for offset_q, dur_q, chord_type, vel_mod in pattern:
            start_time = bar_start_time + (offset_q * quarter_len_sec)
            end_time = start_time + (dur_q * quarter_len_sec)
            
            # Convert project time to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Calculate and constrain velocity
            vel = int(velocity_base * vel_mod)
            vel = max(1, min(127, vel))
            
            # Insert notes
            for pitch in chords[chord_type]:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, "")
                total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (ReaSynth Clavinet shaping) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        # Tweak ReaSynth for a plucky, funky Clavinet/Synth vibe
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.00)  # Attack (Instant)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.25)  # Decay (Short)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.00)  # Sustain (Zero for staccato punch)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.05)  # Release (Quick cutoff)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.70)  # Mix in Saw wave for analog grit
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.50)  # Level normalization

    return f"Created '{track_name}' containing {total_notes_added} notes over {bars} bars at {bpm} BPM in {key} Dorian. Applied plucky ReaSynth envelope."
