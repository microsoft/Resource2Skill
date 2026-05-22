def create_pattern(
    project_name: str = "Neo Soul Project",
    track_name: str = "Neo-Soul Bass",
    bpm: int = 90,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul/R&B bassline featuring root anchors, octave jumps, and passing tones.

    Args:
        project_name: Project identifier.
        track_name: Name for the created bass track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "F").
        scale: Scale type (e.g., "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Optional 'chord_progression' list (1-indexed scale degrees).

    Returns:
        Status string describing the generated bassline track.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Default to the i -> v progression shown in the video (Fm -> Cm)
    chord_progression = kwargs.get("chord_progression", [1, 5])
    
    # Format key strictly
    key_formatted = key[0].upper() + key[1:].lower() if len(key) > 1 else key.upper()
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Deep Neo-Soul Tone) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth: Sine/Triangle mix for warm low end, tight release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume (-6dB)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5)   # Tuning (Center)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)   # Square (Off)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Saw (Off)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 1.0)   # Triangle (Full)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0)   # Extra Sine (Full)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.01)  # Attack (Fast, punchy)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.3)   # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.7)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.1)   # Release (Tight for syncopation)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_qn = bars * beats_per_bar
    item_length_sec = RPR.RPR_TimeMap2_QNToTime(0, total_qn)
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Neo-Soul MIDI Pattern ===
    note_count = 0
    
    for i in range(bars):
        chord_idx = i % len(chord_progression)
        degree = chord_progression[chord_idx]
        
        # Calculate root note in scale
        degree_zero_indexed = (degree - 1) % len(scale_intervals)
        octave_offset = (degree - 1) // len(scale_intervals)
        
        # Force bass notes into Octave 1 (MIDI 24-35)
        base_midi = NOTE_MAP.get(key_formatted, 0) + 24 
        root_midi = base_midi + scale_intervals[degree_zero_indexed] + (octave_offset * 12)
        
        while root_midi >= 36:
            root_midi -= 12
        while root_midi < 24:
            root_midi += 12

        notes_to_add = []
        
        # Pattern structure per bar:
        # 1. Beat 1 (0.0): Heavy foundational root note
        notes_to_add.append((0.0, 1.5, root_midi, velocity_base))
        
        # 2. Beat 3 'and' (2.5): Syncopated octave jump
        notes_to_add.append((2.5, 0.5, root_midi + 12, int(velocity_base * 0.85)))
        
        # 3. Beat 4 'and' (3.5): Voice-leading passing tone into next bar
        if i % 2 == 0:
            passing_midi = root_midi + 10  # Minor 7th (creates tension)
        else:
            passing_midi = root_midi + 7   # Perfect 5th (solidifies harmony)
            
        notes_to_add.append((3.5, 0.5, passing_midi, int(velocity_base * 0.80)))
        
        # Insert notes into MIDI take
        for start_beat, duration_beats, pitch, vel in notes_to_add:
            start_qn = (i * beats_per_bar) + start_beat
            end_qn = start_qn + duration_beats
            
            start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} syncopated bass notes over {bars} bars at {bpm} BPM."
