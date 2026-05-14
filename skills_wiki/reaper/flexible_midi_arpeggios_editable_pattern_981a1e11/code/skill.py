def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Flexible Arp",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an editable, explicit 16th-note Arpeggio directly into a MIDI item.
    This emulates the result of recording an Input FX Arpeggiator, allowing
    for note-level editing, syncopation, and velocity humanization.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
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

    # === Step 1: Set Tempo ===
    bpm_float = float(bpm)
    RPR.RPR_SetCurrentBPM(0, bpm_float, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure ReaSynth for a Tight Pluck ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth parameters for an "Arp Pluck"
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.6)   # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)   # Attack (0 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.1)   # Decay (~200ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)   # Sustain (0%)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.1)   # Release (~200ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.6)   # Sawtooth mix

    # === Step 4: Music Theory / Arp Generation ===
    def get_diatonic_chord(scale_intervals, root_pitch, degree, num_notes=4):
        scale_len = len(scale_intervals)
        chord_pitches = []
        for i in range(num_notes):
            scale_idx = (degree + i * 2) % scale_len
            octave_shift = (degree + i * 2) // scale_len
            pitch = root_pitch + scale_intervals[scale_idx] + (octave_shift * 12)
            chord_pitches.append(pitch)
        return chord_pitches

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    base_pitch = 48 + NOTE_MAP.get(key.upper(), 0) # Octave 4
    
    # Simple 4-bar functional progression
    if "minor" in scale.lower() or scale.lower() == "dorian":
        progression = [0, 5, 2, 4] # i, VI, III, VII
    else:
        progression = [0, 5, 3, 4] # I, vi, IV, V
        
    progression = (progression * (bars // 4 + 1))[:bars]

    beats_per_bar = 4
    division = 0.25  # 1/16th notes
    all_notes = []

    # Generate the explicit arpeggiator sequence
    for bar in range(bars):
        degree = progression[bar]
        chord_pitches = get_diatonic_chord(scale_intervals, base_pitch, degree, num_notes=4)
        chord_pitches = sorted(chord_pitches)
        
        start_beat = bar * beats_per_bar
        end_beat = (bar + 1) * beats_per_bar
        
        current_beat = start_beat
        note_idx = 0
        
        while current_beat < end_beat - 0.01:
            # Emulate the Arpeggiator "Up" pattern
            pitch = chord_pitches[note_idx]
            
            # Pulse velocity on the downbeats for groove
            is_on_beat = abs((current_beat % 1.0) - 0.0) < 0.01
            vel = min(127, velocity_base + 20) if is_on_beat else velocity_base
            
            # Staccato note duration (80% of grid step)
            dur = division * 0.8
            
            all_notes.append({
                "pitch": pitch,
                "velocity": vel,
                "start": current_beat,
                "end": current_beat + dur
            })
            
            current_beat += division
            note_idx = (note_idx + 1) % len(chord_pitches)

    # === Step 5: Insert MIDI Item and Notes ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    bar_length_sec = (60.0 / bpm_float) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)

    for note in all_notes:
        start_sec = note["start"] * (60.0 / bpm_float)
        end_sec = note["end"] * (60.0 / bpm_float)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note["pitch"], note["velocity"], False)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {len(all_notes)} arpeggiated 16th notes over {bars} bars at {bpm} BPM"
