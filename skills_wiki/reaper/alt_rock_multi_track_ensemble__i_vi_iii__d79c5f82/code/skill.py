def create_pattern(
    project_name: str = "MultiTrackArrangement",
    track_name: str = "Alt-Rock Ensemble",
    bpm: int = 110,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Alt-Rock ensemble (Rhythm, Bass, Drums, Lead) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "B").
        scale: Scale type ("minor" or "major").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    scale = scale.lower()
    if scale not in SCALES:
        scale = "minor"  # Fallback to minor for this specific progression

    root_val = NOTE_MAP.get(key.capitalize(), 11) # Default to B if invalid
    scale_intervals = SCALES[scale]

    # Progression: i - VI - III - VII (Minor) or vi - IV - I - V (Major)
    progression = [0, 5, 2, 6] if scale == "minor" else [5, 3, 0, 4]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Helper function to generate tracks and items
    def create_track_with_item(name, is_drum=False):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)

        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_length_sec * bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Add default stock FX so it makes sound immediately
        if not is_drum:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        else:
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)

        return take

    # Helper function for timing and MIDI insertion
    def insert_note(take, start_beat, end_beat, pitch, vel):
        # Bound velocity
        vel = max(1, min(127, int(vel)))
        
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, False)

    # Helper function to compute triad intervals from scale degrees
    def get_chord_notes(degree, octave_shift=0):
        n1 = scale_intervals[degree]
        n2 = scale_intervals[(degree + 2) % 7] + (12 if degree+2 < degree else 0)
        n3 = scale_intervals[(degree + 4) % 7] + (12 if degree+4 < degree else 0)
        
        # C3 is MIDI 48
        base = root_val + 48 + (octave_shift * 12)
        return [base + n1, base + n2, base + n3]


    # === Step 2: Generate Track 1 (Rhythm Guitar / Pad) ===
    take_gtr = create_track_with_item(f"{track_name} - Chords")
    for bar in range(bars):
        degree = progression[bar % 4]
        chord = get_chord_notes(degree, 0)
        start_b = bar * 4
        end_b = start_b + 4
        
        for pitch in chord:
            insert_note(take_gtr, start_b, end_b, pitch, velocity_base - 10)


    # === Step 3: Generate Track 2 (Driving Bassline) ===
    take_bass = create_track_with_item(f"{track_name} - Bass")
    for bar in range(bars):
        degree = progression[bar % 4]
        root_pitch = root_val + 24 + scale_intervals[degree] # C1/C2 range
        start_b = bar * 4
        
        # Straight 8th notes
        for i in range(8): 
            insert_note(take_bass, start_b + i*0.5, start_b + i*0.5 + 0.45, root_pitch, velocity_base)


    # === Step 4: Generate Track 3 (Rock Drums) ===
    take_drums = create_track_with_item(f"{track_name} - Drums", True)
    KICK = 36
    SNARE = 38
    HIHAT = 42
    CRASH = 49

    for bar in range(bars):
        start_b = bar * 4

        # Rock Kick: beat 1, beat 2-and, beat 3
        insert_note(take_drums, start_b + 0, start_b + 0.25, KICK, velocity_base)
        insert_note(take_drums, start_b + 1.5, start_b + 1.75, KICK, velocity_base)
        insert_note(take_drums, start_b + 2.0, start_b + 2.25, KICK, velocity_base)

        # Backbeat Snare: beat 2, beat 4
        insert_note(take_drums, start_b + 1.0, start_b + 1.25, SNARE, velocity_base + 5)
        insert_note(take_drums, start_b + 3.0, start_b + 3.25, SNARE, velocity_base + 5)

        # Constant Hi-hats: 8th notes
        for i in range(8):
            insert_note(take_drums, start_b + i*0.5, start_b + i*0.5 + 0.25, HIHAT, velocity_base - 15)

        # Occasional Crash
        if bar % 4 == 0:
            insert_note(take_drums, start_b, start_b + 0.5, CRASH, velocity_base + 10)


    # === Step 5: Generate Track 4 (Lead Arpeggio) ===
    take_lead = create_track_with_item(f"{track_name} - Lead Arp")
    for bar in range(bars):
        degree = progression[bar % 4]
        chord = get_chord_notes(degree, 1) # Shift up an octave
        start_b = bar * 4
        
        # Motif pattern: High, Mid, Low, High, Mid, Low, High, Mid
        pattern_indices = [2, 1, 0, 2, 1, 0, 2, 1]
        for i in range(8):
            pitch = chord[pattern_indices[i]]
            insert_note(take_lead, start_b + i*0.5, start_b + i*0.5 + 0.4, pitch, velocity_base)


    # === Step 6: Finalize ===
    RPR.RPR_MIDI_Sort(take_gtr)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_lead)
    
    RPR.RPR_UpdateArrange()

    return f"Created multi-track arrangement '{track_name}' (4 unified tracks) over {bars} bars at {bpm} BPM in {key} {scale}."
