def create_pattern(
    project_name: str = "GroovyBassProject",
    track_name: str = "Groovy Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a Groovy Split-Articulation Slap Bassline in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard notes (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Setup ===
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
        scale = "minor"
    scale_intervals = SCALES[scale]
    root_pitch = NOTE_MAP.get(key, 0) + 36 # Octave 2 for bass

    # Simple chord progression degrees based on scale length
    # e.g., i - iv - VI - V (or I - IV - vi - V)
    progression_degrees = [0, 3, 5, 4] 

    def get_pitch(chord_degree, interval_offset, octave_shift=0):
        """Calculate exact MIDI pitch based on scale degree and octave."""
        idx = (chord_degree + interval_offset) % len(scale_intervals)
        octave_bump = (chord_degree + interval_offset) // len(scale_intervals)
        note = root_pitch + scale_intervals[idx] + (12 * (octave_shift + octave_bump))
        return min(max(note, 0), 127)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Track & Item Setup Helper ===
    def setup_bass_track(name, is_slap):
        RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
        track_idx = RPR.RPR_CountTracks(0) - 1
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Insert MIDI item
        bar_length_sec = (60.0 / bpm) * 4
        item_length = bar_length_sec * bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Sound Design (Stock FX)
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
        
        if is_slap:
            # Slap Bass: Bright, Saw-heavy, shorter decay
            RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0)    # Vol
            RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0)    # Tuning
            RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.7)    # Square mix
            RPR.RPR_TrackFX_SetParam(track, 0, 3, 1.0)    # Saw mix
            RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.05)   # Attack
            RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.2)    # Release
            # EQ Boost high-mids for the "click"
            RPR.RPR_TrackFX_SetParam(track, 1, 8, 3000.0) # Band 3 Freq
            RPR.RPR_TrackFX_SetParam(track, 1, 9, 6.0)    # Band 3 Gain
        else:
            # Main Bass: Subby, mellow, square/triangle
            RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.2)    # Vol
            RPR.RPR_TrackFX_SetParam(track, 0, 2, 1.0)    # Square mix
            RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.0)    # Saw mix
            RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5)    # Triangle mix
            # EQ Lowpass to remove harshness
            RPR.RPR_TrackFX_SetParam(track, 1, 11, 0.0)   # Band 4 type (Lowpass)
            RPR.RPR_TrackFX_SetParam(track, 1, 12, 800.0) # Band 4 Freq

        return take

    main_take = setup_bass_track(f"{track_name} - Foundation", False)
    slap_take = setup_bass_track(f"{track_name} - Slap Accents", True)

    # === Step 3: Rhythmic Pattern Definition ===
    # Tuple: (beat_offset, interval_from_root, length_in_beats, is_slap)
    groove_blueprint = [
        (0.00, 0, 0.75, False), # Downbeat root
        (1.50, 0, 0.25, False), # Syncopated anticipatory note
        (2.50, 0, 0.15, True),  # Slap Octave jump (interval handled below if is_slap)
        (3.00, 4, 0.50, False), # Perfect 5th walk
        (3.75, 4, 0.15, True)   # Slap Octave 5th
    ]

    total_notes_created = 0

    # === Step 4: Generate MIDI with Humanization ===
    for bar in range(bars):
        # Determine the root degree for this bar based on the simple progression
        chord_deg = progression_degrees[bar % len(progression_degrees)]
        bar_start_beat = bar * 4.0

        for note_def in groove_blueprint:
            beat_offset, interval, length, is_slap = note_def
            
            # 1. Pitch Logic
            octave = 1 if is_slap else 0 
            pitch = get_pitch(chord_deg, interval, octave_shift=octave)
            
            # 2. Timing Humanization ("imitate reality")
            # Downbeat (beat 0) should remain strict to anchor the groove.
            # Other notes get a +/- 0.02 beat shift.
            human_shift = random.uniform(-0.02, 0.02) if beat_offset != 0.0 else 0.0
            actual_start_beat = bar_start_beat + beat_offset + human_shift
            actual_end_beat = actual_start_beat + length
            
            start_time = actual_start_beat * (60.0 / bpm)
            end_time = actual_end_beat * (60.0 / bpm)
            
            # 3. Velocity Humanization
            if is_slap:
                vel = min(127, velocity_base + 20 + random.randint(-5, 10))
                active_take = slap_take
            else:
                vel = max(1, min(127, velocity_base + random.randint(-12, 8)))
                active_take = main_take
            
            # Insert Note
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(active_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(active_take, end_time)
            
            RPR.RPR_MIDI_InsertNote(active_take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            total_notes_created += 1

    # Sort MIDI notes in both takes
    RPR.RPR_MIDI_Sort(main_take)
    RPR.RPR_MIDI_Sort(slap_take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' (Split Articulation) with {total_notes_created} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
