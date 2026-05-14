def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Melody",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar phrase demonstrating the 'Rule of 3' (A-A-A') variation technique.
    (Note: The 'bars' parameter is internally overridden to 12 to preserve the 4+4+4 macro-structure).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Overridden to 12 internally.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Setup Root and Scale
    root_midi = 48 + NOTE_MAP.get(key, 0) # Octave 3
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_note(degree: int, octave_offset: int = 0) -> int:
        """Calculate MIDI pitch from a scale degree (0-indexed). Supports negative degrees."""
        octaves = (degree // len(scale_intervals)) + octave_offset
        deg = degree % len(scale_intervals)
        return root_midi + scale_intervals[deg] + (octaves * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = 12 # Hardcoded to ensure the 3-phrase structure is intact
    total_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def add_midi_note(take, start_time, end_time, pitch, vel):
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        # noSort=True for bulk insertions
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Step 4: Generate Rule of 3 (A-A-A') MIDI ===
    # Phrase A chords: I, V, vi, IV
    phrase_chords_A = [0, 4, 5, 3] 
    # Phrase A' chords: I, V, ii, V (The variation/turnaround)
    phrase_chords_A_prime = [0, 4, 1, 4] 
    
    note_count = 0

    for phrase in range(3):
        phrase_start_time = phrase * 4 * bar_length_sec
        is_variation = (phrase == 2) # The 3rd repetition
        chords = phrase_chords_A_prime if is_variation else phrase_chords_A
        
        for bar in range(4):
            bar_start = phrase_start_time + bar * bar_length_sec
            chord_root_deg = chords[bar]
            beat_len = bar_length_sec / 4
            
            # 1. Add background chords (Triads, slightly detached)
            chord_end = bar_start + (bar_length_sec * 0.9)
            for triad_deg in [0, 2, 4]:
                pitch = get_note(chord_root_deg + triad_deg, octave_offset=0)
                add_midi_note(take, bar_start, chord_end, pitch, velocity_base - 20)
                note_count += 1
                
            # 2. Add Melody
            if not is_variation or bar < 2:
                # Regular Phrase A Melody (Ascending Arpeggios)
                p1 = get_note(chord_root_deg, octave_offset=1)
                add_midi_note(take, bar_start, bar_start + 2*beat_len, p1, velocity_base)
                
                p2 = get_note(chord_root_deg + 2, octave_offset=1)
                add_midi_note(take, bar_start + 2*beat_len, bar_start + 3*beat_len, p2, velocity_base)
                
                p3 = get_note(chord_root_deg + 4, octave_offset=1)
                add_midi_note(take, bar_start + 3*beat_len, bar_start + 4*beat_len, p3, velocity_base)
                note_count += 3
            else:
                # Variation Melody for the last 2 bars (Breaking the Rule of 3)
                if bar == 2:
                    # Rhythmic walk-down melody
                    for step, deg_offset in enumerate([4, 3, 2, 1]):
                        p = get_note(chord_root_deg + deg_offset, octave_offset=1)
                        add_midi_note(take, bar_start + step*beat_len, bar_start + (step+1)*beat_len, p, velocity_base + 10)
                        note_count += 1
                elif bar == 3:
                    # Final resolving turnaround melody
                    p1 = get_note(chord_root_deg + 2, octave_offset=1)
                    add_midi_note(take, bar_start, bar_start + 2*beat_len, p1, velocity_base)
                    p2 = get_note(chord_root_deg - 3, octave_offset=1) # Drop down
                    add_midi_note(take, bar_start + 2*beat_len, bar_start + 4*beat_len, p2, velocity_base - 10)
                    note_count += 2

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' demonstrating Rule of 3 (A-A-A') with {note_count} notes over {total_bars} bars at {bpm} BPM."
