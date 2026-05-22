def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOfThree_Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' (AAB) phrase in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (dynamically scales to 4-bar or 8-bar block).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and pattern.
    """
    import math
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
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

    def get_midi_note(degree: int, base_octave: int) -> int:
        scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
        root_pitch = NOTE_MAP.get(key.upper(), 0)
        octave_offset = degree // len(scale_intervals)
        rem_degree = degree % len(scale_intervals)
        return (base_octave + octave_offset) * 12 + scale_intervals[rem_degree] + root_pitch

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Define Rule of 3 Structure ===
    # Guarantee the pattern has room to resolve. If requested bars < 4, enforce 4.
    actual_bars = max(4, bars)
    use_8_bar_phrasing = actual_bars >= 8
    block_bars = 8 if use_8_bar_phrasing else 4
    
    notes_to_insert = []
    total_bar_groups = math.ceil(actual_bars / block_bars)
    
    for bar_group in range(total_bar_groups):
        base_beat = bar_group * block_bars * 4
        
        if use_8_bar_phrasing:
            # 8-bar slow resolution (Standard)
            def add_bar(bar_idx, chord_deg, mel_degs):
                b_start = base_beat + bar_idx * 4
                notes_to_insert.append({'type': 'chord', 'degree': chord_deg, 'beat': b_start, 'dur': 4.0})
                for i, md in enumerate(mel_degs):
                    if md is None: continue
                    notes_to_insert.append({'type': 'melody', 'degree': md, 'beat': b_start + i * 1.0, 'dur': 0.8})
            
            add_bar(0, 0, [0, 2, 4, 1])          # Iteration 1 (Idea A)
            add_bar(1, 4, [4, 6, 8, 5])
            add_bar(2, 0, [0, 2, 4, 1])          # Iteration 2 (Exact Repeat)
            add_bar(3, 4, [4, 6, 8, 5])
            add_bar(4, 0, [0, 2, 4, 1])          # Iteration 3 (Starts Same)
            add_bar(5, 5, [5, 7, 9, 8])          # Iteration 3 (Diverges halfway)
            add_bar(6, 3, [3, 5, 7, 6])          # Turnaround
            add_bar(7, 4, [4, 2, 1, None])       # Cadence
            
        else:
            # 4-bar fast resolution (Double-time harmonic rhythm)
            def add_half_bar(beat_offset, chord_deg, mel_degs):
                b_start = base_beat + beat_offset
                notes_to_insert.append({'type': 'chord', 'degree': chord_deg, 'beat': b_start, 'dur': 2.0})
                for i, md in enumerate(mel_degs):
                    if md is None: continue
                    notes_to_insert.append({'type': 'melody', 'degree': md, 'beat': b_start + i * 0.5, 'dur': 0.4})
                    
            add_half_bar(0.0, 0, [0, 2, 4, 1])   # Iteration 1 (Idea A)
            add_half_bar(2.0, 4, [4, 6, 8, 5])
            add_half_bar(4.0, 0, [0, 2, 4, 1])   # Iteration 2 (Exact Repeat)
            add_half_bar(6.0, 4, [4, 6, 8, 5])
            add_half_bar(8.0, 0, [0, 2, 4, 1])   # Iteration 3 (Starts Same)
            add_half_bar(10.0, 5, [5, 7, 9, 8])  # Iteration 3 (Diverges halfway)
            add_half_bar(12.0, 3, [3, 5, 7, 6])  # Turnaround
            add_half_bar(14.0, 4, [4, 2, 1, None]) # Cadence

    # === Step 4: Create MIDI Item & Inject Data ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * actual_bars
    max_beat = actual_bars * beats_per_bar
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    RPR.RPR_MIDI_DisableSort(take)
    
    note_count = 0
    for n in notes_to_insert:
        if n['beat'] >= max_beat:
            continue # Truncate gracefully if it exceeds exact boundaries
            
        start_pos = n['beat'] * beat_len_sec
        dur_beats = n['dur']
        if n['beat'] + dur_beats > max_beat:
            dur_beats = max_beat - n['beat']
        end_pos = start_pos + (dur_beats * beat_len_sec)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        
        if n['type'] == 'melody':
            pitch = get_midi_note(n['degree'], 5) # Octave 5 for lead
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1
        elif n['type'] == 'chord':
            pitches = [
                get_midi_note(n['degree'], 4),     # Root
                get_midi_note(n['degree'] + 2, 4), # 3rd
                get_midi_note(n['degree'] + 4, 4)  # 5th
            ]
            c_vel = int(velocity_base * 0.7) # Chords sit softer than melody
            for p in pitches:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, c_vel, False)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' demonstrating Rule of 3 ({note_count} notes over {actual_bars} bars at {bpm} BPM in {key} {scale})"
