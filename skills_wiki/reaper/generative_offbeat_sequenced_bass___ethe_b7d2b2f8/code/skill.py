def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative_Pad_Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a generative offbeat bassline synced to a sustained chord pad.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name prefix for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the tracks and notes generated.
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

    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    base_pc = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Diatonic chord progression: i - VI - iv - v
    progression = [0, 5, 3, 4]

    quarter_len = 60.0 / bpm
    bar_len = quarter_len * 4.0
    sixteenth_len = quarter_len / 4.0

    # ==========================================
    # Track 1: The Ethereal Pad
    # ==========================================
    track1_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track1_idx, True)
    pad_track = RPR.RPR_GetTrack(0, track1_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", "Ghost Pad", True)

    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", bar_len * bars)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)

    pad_base_note = 60 + base_pc # Start around C4
    
    for bar in range(bars):
        bar_start = bar * bar_len
        bar_end = bar_start + bar_len
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, bar_start)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, bar_end)
        
        chord_degree = progression[bar % len(progression)]
        
        # Build triad (root, 3rd, 5th)
        for interval in [0, 2, 4]:
            target_idx = chord_degree + interval
            safe_idx = target_idx % len(scale_intervals)
            oct_shift = target_idx // len(scale_intervals)
            pitch = pad_base_note + scale_intervals[safe_idx] + (oct_shift * 12)
            
            # Insert sustained whole note
            RPR.RPR_MIDI_InsertNote(pad_take, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base * 0.6), False)
            
    RPR.RPR_MIDI_Sort(pad_take)
    
    # Pad Sound Design
    RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 0, 0.2)  # Low Volume (-14dB)
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 2, 0.8)  # Slow Attack
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 4, 1.0)  # Full Sustain
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 5, 0.8)  # Slow Release
    RPR.RPR_TrackFX_AddByName(pad_track, "ReaVerbate", False, -1)

    # ==========================================
    # Track 2: The Generative Offbeat Bass
    # ==========================================
    track2_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track2_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track2_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", "Offbeat Seq Bass", True)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", bar_len * bars)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    bass_base_note = 36 + base_pc # Start around C2
    
    # Sequence definition: (start_16th_step, duration_16ths, scale_degree_offset_from_chord, octave_offset)
    bass_pattern = [
        (2, 1, 0, 0),    # Syncopated upbeat: 1.& (Root)
        (6, 1, 0, 1),    # Syncopated upbeat: 2.& (Root, octave up)
        (9, 1, 0, 0),    # 16th hit: 3.e
        (10, 1, 0, 0),   # 16th hit: 3.&
        (14, 1, 4, -1),  # Syncopated upbeat: 4.& (5th interval, octave down)
        (15, 1, 0, 0)    # Pickup 16th: 4.a
    ]
    
    notes_added = 0
    for bar in range(bars):
        bar_start = bar * bar_len
        chord_degree = progression[bar % len(progression)]
        
        for step, dur, deg_offset, oct_offset in bass_pattern:
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + (dur * sixteenth_len) * 0.85 # Staccato 16th
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
            
            target_idx = chord_degree + deg_offset
            safe_idx = target_idx % len(scale_intervals)
            deg_oct_shift = target_idx // len(scale_intervals)
            
            pitch = bass_base_note + scale_intervals[safe_idx] + ((deg_oct_shift + oct_offset) * 12)
            
            # Constrain extreme high/low pitches to maintain bass integrity
            while pitch > 55: pitch -= 12
            while pitch < 24: pitch += 12
            
            # Accent specific offbeats dynamically
            vel = velocity_base if step in [2, 6, 14] else int(velocity_base * 0.8)
            
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_added += 1

    RPR.RPR_MIDI_Sort(bass_take)
    
    # Bass Sound Design
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.4)  # Normal volume
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.0)  # Instant attack
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.1)  # Short decay
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.0)  # Zero sustain (Pluck)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.1)  # Fast release
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.3)  # Add square wave for edge/bite
    
    return f"Created 'Ghost Pad' and 'Offbeat Seq Bass' tracks with {notes_added} sequenced bass notes over {bars} bars at {bpm} BPM."
