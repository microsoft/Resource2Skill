def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SynthRock",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an interlocking 4-track Synth-Rock loop (Drums, Bass, Chords, Lead).
    Implements the classic i-VI-III-VII progression demonstrated in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'B', 'C').
        scale: Scale type (defaults to minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the multi-track arrangement.
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
    }

    # Setup Key and Scale (Fallback to minor if unsupported scale is provided)
    root_val = NOTE_MAP.get(key, 11) # Default to B as in the tutorial
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    if len(scale_intervals) != 7:
        scale_intervals = SCALES["minor"]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    qn_duration = 60.0 / bpm
    bar_length_sec = qn_duration * beats_per_bar

    # Helper: Create track with MIDI item
    def create_track_with_midi(name, length_sec):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # Helper: Insert MIDI note via Project Quarter Notes (QN)
    def insert_note(take, start_qn, end_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        # Ensure pitch is clamped strictly to MIDI boundaries
        pitch = max(0, min(127, pitch))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Progression definition: i - VI - III - VII
    progression_indices = [0, 5, 2, 6]

    # --- 1. DRUMS (Standard GM Map) ---
    drum_track, drum_take = create_track_with_midi(f"{track_name}_Drums", bars * bar_length_sec)
    for b in range(bars):
        start_qn = b * 4
        # Kick (36)
        insert_note(drum_take, start_qn + 0.0, start_qn + 0.5, 36, velocity_base)
        insert_note(drum_take, start_qn + 2.0, start_qn + 2.5, 36, velocity_base)
        insert_note(drum_take, start_qn + 2.5, start_qn + 3.0, 36, int(velocity_base * 0.85)) 
        # Snare (38)
        insert_note(drum_take, start_qn + 1.0, start_qn + 1.5, 38, velocity_base)
        insert_note(drum_take, start_qn + 3.0, start_qn + 3.5, 38, velocity_base)
        # Closed Hi-Hat (42) - 8th notes
        for i in range(8):
            hat_vel = velocity_base if i % 2 == 0 else int(velocity_base * 0.6)
            insert_note(drum_take, start_qn + i*0.5, start_qn + i*0.5 + 0.25, 42, hat_vel)

    # --- 2. BASS ---
    bass_track, bass_take = create_track_with_midi(f"{track_name}_Bass", bars * bar_length_sec)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.5)  # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 1.0)  # Pulse mix

    for b in range(bars):
        start_qn = b * 4
        chord_idx = progression_indices[b % len(progression_indices)]
        root_pitch = root_val + scale_intervals[chord_idx] + 36 # Octave 3
        # 8th note pumping rhythm
        for i in range(8):
            insert_note(bass_take, start_qn + i*0.5, start_qn + i*0.5 + 0.45, root_pitch, int(velocity_base * 0.9))

    # --- 3. CHORDS ---
    chord_track, chord_take = create_track_with_midi(f"{track_name}_Chords", bars * bar_length_sec)
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 0, 1.0) # Square
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 1, 1.0) # Sawtooth
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 4, 0.2) # Attack (slower)
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 5, 0.8) # Decay

    for b in range(bars):
        start_qn = b * 4
        chord_idx = progression_indices[b % len(progression_indices)]
        
        # Diatonic logic
        r = root_val + scale_intervals[chord_idx] + 48
        t = root_val + scale_intervals[(chord_idx + 2) % 7] + 48 + (12 if (chord_idx + 2) >= 7 else 0)
        f = root_val + scale_intervals[(chord_idx + 4) % 7] + 48 + (12 if (chord_idx + 4) >= 7 else 0)

        # Voice leading constraint (keep notes under G4)
        while r > 67: r -= 12
        while t > 67: t -= 12
        while f > 67: f -= 12

        # Whole notes
        chord_vel = int(velocity_base * 0.75)
        insert_note(chord_take, start_qn, start_qn + 4.0, r, chord_vel)
        insert_note(chord_take, start_qn, start_qn + 4.0, t, chord_vel)
        insert_note(chord_take, start_qn, start_qn + 4.0, f, chord_vel)

    # --- 4. LEAD ARPEGGIO ---
    lead_track, lead_take = create_track_with_midi(f"{track_name}_Lead", bars * bar_length_sec)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, 0, 0, 0.0) # Square off
    RPR.RPR_TrackFX_SetParam(lead_track, 0, 1, 1.0) # Sawtooth on
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaDelay", False, -1) # Add delay for depth
    RPR.RPR_TrackFX_SetParam(lead_track, 1, 0, 0.25) # Delay length to roughly 1/8 note

    for b in range(bars):
        start_qn = b * 4
        chord_idx = progression_indices[b % len(progression_indices)]
        
        r = root_val + scale_intervals[chord_idx] + 60
        t = root_val + scale_intervals[(chord_idx + 2) % 7] + 60 + (12 if (chord_idx + 2) >= 7 else 0)
        f = root_val + scale_intervals[(chord_idx + 4) % 7] + 60 + (12 if (chord_idx + 4) >= 7 else 0)

        arp_notes = [r, t, f, t]
        
        # 16th note arpeggios
        for i in range(16):
            pitch = arp_notes[i % 4]
            insert_note(lead_take, start_qn + i*0.25, start_qn + i*0.25 + 0.15, pitch, velocity_base)

    RPR.RPR_UpdateArrange()
    
    return f"Created 4-track interlocking arrangement '{track_name}' (Drums, Bass, Chords, Lead) with progression {key} {scale} i-VI-III-VII over {bars} bars."
