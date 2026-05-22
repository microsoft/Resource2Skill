def create_dynamic_slap_bassline(
    project_name: str = "MyProject",
    main_bass_track_name: str = "Main Bass",
    slap_bass_track_name: str = "Slap Bass Layer",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    main_bass_velocity_base: int = 90,
    slap_bass_velocity_base: int = 110,
    humanize_strength: float = 0.1, # 0.0 to 1.0 for random offset/velocity
    **kwargs,
) -> str:
    """
    Create a dynamic, groovy bassline with a layered slap emulation in the current REAPER project.
    The bassline follows a I-IV-V-I chord progression.

    Args:
        project_name: Project identifier (for logging).
        main_bass_track_name: Name for the main bass track.
        slap_bass_track_name: Name for the slap bass layer track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (must be a multiple of 4 for I-IV-V-I).
        main_bass_velocity_base: Base MIDI velocity for main bass (0-127).
        slap_bass_velocity_base: Base MIDI velocity for slap bass layer (0-127).
        humanize_strength: Strength of random timing/velocity humanization (0.0 to 1.0).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Main Bass' and 'Slap Bass Layer' with N notes over 4 bars at 120 BPM"
    """
    import reaper_python as RPR
    import random

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
        return f"Error: Scale '{scale}' not found. Choose from {', '.join(SCALES.keys())}"
    if key not in NOTE_MAP:
        return f"Error: Key '{key}' not found. Choose from {', '.join(NOTE_MAP.keys())}"
    if bars % 4 != 0:
        RPR.RPR_ShowConsoleMsg("Warning: Bassline is designed for 4-bar chord progressions. Adjusting bars to nearest multiple of 4.\n")
        bars = (bars // 4) * 4 if bars >= 4 else 4

    # Helper to get MIDI pitch
    def get_midi_pitch(root_note_val, scale_intervals, degree, octave):
        octave_midi_offset = (octave + 1) * 12 # C-1 is 0, C0 is 12, C1 is 24 etc. C-based octaves.
        # Scale intervals are 0-indexed, so degree 0 is root, degree 1 is 2nd, etc.
        # If degree is out of scale bounds, wrap it around
        if degree >= len(scale_intervals):
            actual_degree = degree % len(scale_intervals)
            octave_offset = degree // len(scale_intervals)
        else:
            actual_degree = degree
            octave_offset = 0

        # Calculate the base pitch without octave offset first
        base_pitch = root_note_val + scale_intervals[actual_degree]

        # Calculate the pitch including the target octave and any wrap-around
        midi_pitch = base_pitch + (octave * 12) + (octave_offset * 12)
        return midi_pitch

    root_note_val = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    
    # Define chord progression (I-IV-V-I) in terms of scale degrees
    # I = root (0), IV = 4th degree (3rd index in scale_intervals), V = 5th degree (4th index)
    chord_roots_degrees = [0, 3, 4, 0] # Scale degrees for I, IV, V, I (0-indexed)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_idx = RPR.RPR_CountTracks(0)

    # Main Bass Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    main_bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(main_bass_track, "P_NAME", main_bass_track_name, True)
    RPR.RPR_TrackFX_AddByName(main_bass_track, "ReaSynth", False, -1)
    # Configure ReaSynth for main bass
    # RPR_TrackFX_SetParam(track, fx_idx, param_idx, value)
    # ReaSynth: Osc1 Waveform (0=Sine, 0.25=Saw, 0.5=Square, 0.75=Tri, 1=Noise), Osc2 Waveform (same)
    # Osc1 Detune: 0.5 center, <0.5 down, >0.5 up
    # Filter Cutoff: 0-1 (0 low, 1 high), Filter Resonance: 0-1
    # Amp ADSR: A=0-1, D=0-1, S=0-1, R=0-1
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 0, 0.25) # Osc1 Saw
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 2, 0.5)  # Osc2 Square
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 4, 0.51) # Osc2 Detune slightly up
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 10, 0.3) # Filter Cutoff (moderate low-pass)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 11, 0.15) # Filter Resonance
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 12, 0.01) # Amp Attack (10ms)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 13, 0.4)  # Amp Decay (400ms)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 14, 0.0)  # Amp Sustain
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 15, 0.0)  # Amp Release

    RPR.RPR_TrackFX_AddByName(main_bass_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 4, 1.0) # Band 1 enable
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 5, 40.0/20000.0) # Band 1 Freq 40Hz
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 6, -15.0/20.0 + 0.5) # Band 1 Gain -15dB (High-pass-ish)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 8, 1.0) # Band 2 enable
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 9, 150.0/20000.0) # Band 2 Freq 150Hz
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 10, 2.0/20.0 + 0.5) # Band 2 Gain +2dB
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 12, 1.0) # Band 3 enable
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 13, 1000.0/20000.0) # Band 3 Freq 1kHz
    RPR.RPR_TrackFX_SetParam(main_bass_track, 1, 14, 2.0/20.0 + 0.5) # Band 3 Gain +2dB

    RPR.RPR_TrackFX_AddByName(main_bass_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 2, 0, 0.5) # Threshold -24dB
    RPR.RPR_TrackFX_SetParam(main_bass_track, 2, 1, 0.3) # Ratio 3:1
    RPR.RPR_TrackFX_SetParam(main_bass_track, 2, 2, 0.005) # Attack 5ms
    RPR.RPR_TrackFX_SetParam(main_bass_track, 2, 3, 0.100) # Release 100ms
    RPR.RPR_TrackFX_SetParam(main_bass_track, 2, 4, 0.2) # Gain +4dB

    # Slap Bass Layer Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    slap_bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(slap_bass_track, "P_NAME", slap_bass_track_name, True)
    RPR.RPR_TrackFX_AddByName(slap_bass_track, "ReaSynth", False, -1)
    # Configure ReaSynth for slap bass
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 0, 0.75) # Osc1 Tri for brighter sound
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 2, 0.5)  # Osc2 Square
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 4, 0.505) # Osc2 Detune slightly up
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 10, 0.6) # Filter Cutoff (higher for slap)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 11, 0.3) # Filter Resonance (more for snap)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 12, 0.001) # Amp Attack (1ms)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 13, 0.05) # Amp Decay (50ms)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 14, 0.0) # Amp Sustain
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 15, 0.0) # Amp Release

    RPR.RPR_TrackFX_AddByName(slap_bass_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 1, 4, 1.0) # Band 1 enable
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 1, 5, 300.0/20000.0) # Band 1 Freq 300Hz (High-pass)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 1, 6, -10.0/20.0 + 0.5) # Band 1 Gain -10dB
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 1, 8, 1.0) # Band 2 enable
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 1, 9, 3000.0/20000.0) # Band 2 Freq 3kHz
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 1, 10, 5.0/20.0 + 0.5) # Band 2 Gain +5dB (for snap)

    RPR.RPR_TrackFX_AddByName(slap_bass_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 2, 0, 0.6) # Threshold -18dB (more aggressive)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 2, 1, 0.5) # Ratio 5:1
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 2, 2, 0.001) # Attack 1ms
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 2, 3, 0.050) # Release 50ms
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 2, 4, 0.4) # Gain +8dB

    # === Step 3: Create MIDI Items ===
    ppq = 960 # Pulses Per Quarter note for MIDI timing
    seconds_per_beat = 60.0 / bpm
    seconds_per_bar = seconds_per_beat * 4
    notes_inserted = 0

    main_item = RPR.RPR_AddMediaItemToTrack(main_bass_track)
    RPR.RPR_SetMediaItemInfo_Value(main_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(main_item, "D_LENGTH", seconds_per_bar * bars)
    main_take = RPR.RPR_AddTakeToMediaItem(main_item)
    RPR.RPR_MIDI_SetItemExtents(main_item, 0, 0, 0) # Create empty MIDI take

    slap_item = RPR.RPR_AddMediaItemToTrack(slap_bass_track)
    RPR.RPR_SetMediaItemInfo_Value(slap_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(slap_item, "D_LENGTH", seconds_per_bar * bars)
    slap_take = RPR.RPR_AddTakeToMediaItem(slap_item)
    RPR.RPR_MIDI_SetItemExtents(slap_item, 0, 0, 0) # Create empty MIDI take

    # Begin editing MIDI takes
    RPR.RPR_MIDI_BeginEdit(main_take)
    RPR.RPR_MIDI_BeginEdit(slap_take)

    for bar_idx in range(bars):
        chord_root_degree_idx = chord_roots_degrees[bar_idx % 4]
        current_root_midi_val = get_midi_pitch(root_note_val, scale_intervals, chord_root_degree_idx, 0) # Base octave C0

        # Pattern for a single bar (root is current_root_midi_val)
        # Main Bass (Octave 2, 3)
        main_bass_notes = [
            (current_root_midi_val + 24, 0.0, 0.4), # Root (C2) on beat 1, longer
            (get_midi_pitch(root_note_val, scale_intervals, (chord_root_degree_idx + 4) % 7, 2), 0.5, 0.2), # 5th (G2) off-beat 1
            (get_midi_pitch(root_note_val, scale_intervals, (chord_root_degree_idx + 2) % 7, 3), 1.0, 0.2), # 3rd (E3) on beat 2
            (get_midi_pitch(root_note_val, scale_intervals, (chord_root_degree_idx + 4) % 7, 2), 1.5, 0.2), # 5th (G2) off-beat 2
            (get_midi_pitch(root_note_val, scale_intervals, chord_root_degree_idx, 3), 2.0, 0.2), # Root (C3) on beat 3
            (get_midi_pitch(root_note_val, scale_intervals, (chord_root_degree_idx + 4) % 7, 2), 2.5, 0.2), # 5th (G2) off-beat 3
            (current_root_midi_val + 24, 3.0, 0.4), # Root (C2) on beat 4, longer
        ]

        # Slap Bass Layer (Octave 4, 5) - shorter duration, higher velocity
        slap_bass_notes = [
            (get_midi_pitch(root_note_val, scale_intervals, (chord_root_degree_idx + 4) % 7, 4), 0.5, 0.1), # 5th (G4) off-beat 1
            (get_midi_pitch(root_note_val, scale_intervals, chord_root_degree_idx, 5), 1.5, 0.1), # Root (C5) off-beat 2
            (get_midi_pitch(root_note_val, scale_intervals, (chord_root_degree_idx + 4) % 7, 4), 2.5, 0.1), # 5th (G4) off-beat 3
            (get_midi_pitch(root_note_val, scale_intervals, chord_root_degree_idx, 5), 3.5, 0.1), # Root (C5) off-beat 4
        ]

        for pitch_offset, beat_pos, duration_beats in main_bass_notes:
            # Humanize timing and velocity
            time_offset = random.uniform(-humanize_strength * 0.02, humanize_strength * 0.02) # +/- 2% of a beat
            vel_offset = random.randint(int(-humanize_strength * 20), int(humanize_strength * 20))
            final_velocity = max(0, min(127, main_bass_velocity_base + vel_offset))

            start_time_beats = bar_idx * 4 + beat_pos + time_offset
            end_time_beats = start_time_beats + duration_beats
            
            # Insert note: take, selected, muted, start_time, end_time, channel, pitch, velocity
            RPR.RPR_MIDI_InsertNote(main_take, False, False, start_time_beats * ppq / 4, end_time_beats * ppq / 4, 0, pitch_offset, final_velocity, True)
            notes_inserted += 1

        for pitch_offset, beat_pos, duration_beats in slap_bass_notes:
            # Humanize timing and velocity
            time_offset = random.uniform(-humanize_strength * 0.01, humanize_strength * 0.01) # Smaller offset for sharper feel
            vel_offset = random.randint(int(-humanize_strength * 10), int(humanize_strength * 10))
            final_velocity = max(0, min(127, slap_bass_velocity_base + vel_offset))

            start_time_beats = bar_idx * 4 + beat_pos + time_offset
            end_time_beats = start_time_beats + duration_beats
            
            RPR.RPR_MIDI_InsertNote(slap_take, False, False, start_time_beats * ppq / 4, end_time_beats * ppq / 4, 0, pitch_offset, final_velocity, True)
            notes_inserted += 1

    RPR.RPR_MIDI_EndEdit(main_take)
    RPR.RPR_MIDI_EndEdit(slap_take)

    return f"Created '{main_bass_track_name}' and '{slap_bass_track_name}' with {notes_inserted} notes over {bars} bars at {bpm} BPM."

