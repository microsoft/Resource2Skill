def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Atmospheric Chords & Melody",
    bpm: int = 120,
    key: str = "F",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create Diatonic "Cloud Piano" Chords & Q/A Melody in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (should ideally be multiple of 4 for Q&A).
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

    # Internal helper to safely get pitch for ANY scale degree (handles multiple octaves)
    def get_diatonic_pitch(root_midi_note, scale_intervals, degree):
        scale_len = len(scale_intervals)
        octave_shift = degree // scale_len
        idx = degree % scale_len
        return root_midi_note + (octave_shift * 12) + scale_intervals[idx]

    # Initialize Environment
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # 1. Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 2. Add FX Chain (Cloud Piano Vibe)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.05) # Attack (soften transient)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.6)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.8)  # Release (long tail)
    
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 1, 0, 0.1)  # Wet
    
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 2, 0, 0.6)  # Wet
    RPR.RPR_TrackFX_SetParam(track, 2, 1, 0.7)  # Dry
    RPR.RPR_TrackFX_SetParam(track, 2, 2, 0.9)  # Roomsize (massive)

    # 3. Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper for MIDI insertion
    def insert_note(start_beat, duration_beats, pitch, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + duration_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        vel = max(1, min(127, int(vel))) # Clamp velocity
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Music Configuration
    root_pitch = 48 + NOTE_MAP.get(key, 0) # e.g., C3 = 48
    active_scale = SCALES.get(scale, SCALES["minor"])
    
    # Common chord progression: 1 - 6 - 3 - 7 (0, 5, 2, 6 relative scale indices)
    progression = [0, 5, 2, 6] 
    
    # Q&A Melody Phrasing Rules (Format: (start_beat, duration_beats, scale_degree_relative_to_root))
    m_Q1 = [(0.0, 1.5, 7), (1.5, 0.5, 6), (2.0, 1.0, 5), (3.0, 1.0, 4)] # Question starts high, walks down
    m_Q2 = [(0.0, 2.0, 4), (2.0, 1.0, 3), (3.0, 1.0, 4)]                # Ends on tension note (5th of scale, degree 4)
    m_A1 = m_Q1                                                         # Answer repeats Question motif
    m_A2 = [(0.0, 2.0, 4), (2.0, 1.0, 1), (3.0, 1.0, 0)]                # Answer resolves to Tonic (Root, degree 0)
    phrases = [m_Q1, m_Q2, m_A1, m_A2]

    note_count = 0

    # 4. Generate Content
    for bar in range(bars):
        start_beat = bar * beats_per_bar
        prog_idx = bar % len(progression)
        degree = progression[prog_idx]
        
        # --- BASS NOTE ---
        p_bass = get_diatonic_pitch(root_pitch - 12, active_scale, degree)
        insert_note(start_beat, 4.0, p_bass, velocity_base + 15)
        note_count += 1
        
        # --- CHORD (Triad) ---
        p1 = get_diatonic_pitch(root_pitch, active_scale, degree)
        p3 = get_diatonic_pitch(root_pitch, active_scale, degree + 2)
        p5 = get_diatonic_pitch(root_pitch, active_scale, degree + 4)
        
        # INVERSION LOGIC: Force notes to stay within a central register (voice leading)
        # Keeps everything glued together between MIDI 55 (G3) and 67 (G4)
        for p in [p1, p3, p5]:
            shifted_p = p
            while shifted_p < 55: shifted_p += 12
            while shifted_p > 67: shifted_p -= 12
            insert_note(start_beat, 4.0, shifted_p, velocity_base - 10)
            note_count += 1
            
        # --- MELODY ---
        current_phrase = phrases[bar % 4]
        for note_start, note_dur, note_degree in current_phrase:
            # Place melody roughly an octave above the chords
            m_pitch = get_diatonic_pitch(root_pitch + 12, active_scale, note_degree)
            insert_note(start_beat + note_start, note_dur, m_pitch, velocity_base + 5)
            note_count += 1

    # Sort MIDI at the end
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}"
