def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOfThree",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' (AAB) arrangement structure in the current REAPER project.
    Generates 3 repetitions of the base 'bars' length. Iterations 1 & 2 are identical.
    Iteration 3 features a delayed divergence in harmony and melody.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars per idea (generates bars * 3 total).
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

    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "minor"
    
    root_midi = 48 + NOTE_MAP[key]
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    idea_bars = bars
    total_bars = idea_bars * 3
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    def get_midi_pitch(degree, scale_intervals, root_m):
        """Convert a scale degree (0-indexed) to an absolute MIDI pitch."""
        octave = degree // 7
        note_idx = degree % 7
        return root_m + scale_intervals[note_idx] + (octave * 12)

    track_idx = RPR.RPR_CountTracks(0)

    # === Track 1: Chords (Pad-like) ===
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chords", True)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "D_PAN", -0.3)
    
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_bars * bar_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # === Track 2: Melody (Pluck-like) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    melody_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(melody_track, "P_NAME", f"{track_name}_Melody", True)
    RPR.RPR_SetMediaTrackInfo_Value(melody_track, "D_PAN", 0.3)
    
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaDelay", False, -1)

    melody_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", total_bars * bar_length_sec)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)

    # === Arrangement Generation ===
    # AAB Structure definition
    sections = [
        {"type": "A", "start_bar": 0},
        {"type": "A", "start_bar": idea_bars},
        {"type": "B", "start_bar": idea_bars * 2}
    ]

    # Chord progressions represented by scale degrees
    prog_A = [0, 5, 3, 4]  # I, vi, IV, V (Standard pop/emotional)
    prog_B = [0, 5, 2, 4]  # I, vi, iii, V (Diverges on the 3rd chord)
    
    chord_length_sec = (idea_bars * bar_length_sec) / len(prog_A)
    notes_added = 0

    for section in sections:
        prog = prog_A if section["type"] == "A" else prog_B
        sec_start_sec = section["start_bar"] * bar_length_sec
        
        for c_idx, degree in enumerate(prog):
            c_start = sec_start_sec + c_idx * chord_length_sec
            c_end = c_start + chord_length_sec
            
            # 1. Insert Chord Notes
            for voice_offset in [0, 2, 4]:
                pitch = get_midi_pitch(degree + voice_offset, SCALES[scale], root_midi)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, c_start)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, c_end)
                chord_vel = max(10, velocity_base - 30)
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, chord_vel, True)
                notes_added += 1
                
            # 2. Insert Melody Notes
            # Arpeggiates quickly, then rests, leaving rhythmic space
            step_sec = chord_length_sec / 8.0 
            
            if section["type"] == "A":
                mel_offsets = [0, 2, 4, 7] # Ascending contour
            else:
                mel_offsets = [7, 4, 2, 0] # Descending (divergent) contour
                
            for m_idx, m_off in enumerate(mel_offsets):
                m_start = c_start + m_idx * step_sec
                m_end = m_start + step_sec * 0.6  # 40% gap for staccato pluck feel
                m_pitch = get_midi_pitch(degree + m_off, SCALES[scale], root_midi + 12)
                
                m_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(melody_take, m_start)
                m_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(melody_take, m_end)
                RPR.RPR_MIDI_InsertNote(melody_take, False, False, m_start_ppq, m_end_ppq, 0, m_pitch, velocity_base, True)
                notes_added += 1

    # Commit all MIDI notes
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(melody_take)

    return f"Created '{track_name}' Rule of 3 structure (AAB) with {notes_added} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
