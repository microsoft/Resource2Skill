def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Bassline",
    bpm: int = 85,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul Syncopated Bassline (Root-Fifth-Octave) in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (85 is ideal for this bounce).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # === Step 1: Initialize Setup & Track ===
    # Set tempo safely if REAPER environment allows
    try:
        RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, bpm, 0, 0, True)
    except:
        pass

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add Instrument (ReaSynth Sub Bass) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        # Configure a deep Triangle wave sub-bass
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.6) # Volume
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.0) # Square mix (0%)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.0) # Saw mix (0%)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 1.0) # Triangle mix (100%)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Syncopated MIDI Notes ===
    # Using Octave 2 for deep bass
    base_midi = 36 + NOTE_MAP.get(key.capitalize(), 0) 
    
    # Progression: Plagal Cadence (iv -> i in minor, IV -> I in major)
    # Scale degree 3 is the 4th note (IV), degree 0 is the 1st note (I)
    chord_roots_degrees = [3, 0] 
    active_scale = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(active_scale)

    note_count = 0

    for b in range(bars):
        is_even_bar = (b % 2 == 0)
        chord_deg = chord_roots_degrees[0] if is_even_bar else chord_roots_degrees[1]
        next_chord_deg = chord_roots_degrees[1] if is_even_bar else chord_roots_degrees[0]
        
        # Calculate MIDI note for the current chord's root
        oct_offset = chord_deg // scale_len
        note_in_scale = chord_deg % scale_len
        root_note = base_midi + active_scale[note_in_scale] + (oct_offset * 12)
        
        # Calculate next chord's root for passing note logic
        next_oct_offset = next_chord_deg // scale_len
        next_note_in_scale = next_chord_deg % scale_len
        next_root_note = base_midi + active_scale[next_note_in_scale] + (next_oct_offset * 12)
        
        # Core Intervals
        fifth_note = root_note + 7
        octave_note = root_note + 12
        
        bar_start_beat = b * beats_per_bar
        
        # Rhythm Tuples: (Pitch, Start Beat, End Beat, Velocity)
        notes_to_add = [
            (root_note,   0.0,  0.75, velocity_base),               # Downbeat Root
            (fifth_note,  0.75, 1.0,  int(velocity_base * 0.85)),   # Syncopated 5th (16th before beat 2)
            (octave_note, 1.5,  2.0,  int(velocity_base * 0.95)),   # Octave (Offbeat of 2)
            (fifth_note,  2.5,  3.0,  int(velocity_base * 0.80)),   # 5th (Offbeat of 3)
        ]
        
        # Advanced Passing Note Strategy
        if is_even_bar:
            # Diatonic 7th passing note bridging the IV chord to the I chord
            passing_offset = 10 if scale in ["minor", "dorian", "mixolydian", "pentatonic_minor", "blues"] else 11
            passing_note = root_note + passing_offset
            notes_to_add.append((passing_note, 3.5, 4.0, int(velocity_base * 0.85)))
        else:
            # Chromatic leading tone (half-step approach) pushing back into the IV chord
            passing_note = next_root_note - 1
            notes_to_add.append((passing_note, 3.5, 4.0, int(velocity_base * 0.85)))
            
        # Insert notes into the REAPER MIDI Take
        for pitch, start_b, end_b, vel in notes_to_add:
            start_time = (bar_start_beat + start_b) * (60.0 / bpm)
            end_time = (bar_start_beat + end_b) * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)
            note_count += 1

    # Sort MIDI events after batch insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} syncopated notes over {bars} bars at {bpm} BPM in {key} {scale}."
