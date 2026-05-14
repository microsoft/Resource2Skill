def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lofi Chords",
    bpm: int = 80,
    key: str = "G",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Lo-fi Staggered Chord Progression (IV-iii-ii-I) with Tape FX.
    Implements the "1-3-2" major / "1-2-3" minor strum pattern.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (70-85 recommended for Lo-fi).
        key: Root note (e.g., G).
        scale: Scale type (major).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: MIDI Generation Logic ===
    # Progression: IV - iii - ii - I
    progression = [3, 2, 1, 0] 
    base_note = 36 + NOTE_MAP.get(key, 7) # Octave 2 (e.g., G2 = 43)

    def get_pitch(octave_base, scale_arr, deg):
        octave_shift = deg // len(scale_arr)
        scale_deg = deg % len(scale_arr)
        return octave_base + (octave_shift * 12) + scale_arr[scale_deg]

    notes_created = 0
    
    for bar in range(bars):
        degree = progression[bar % 4]
        
        # Calculate triad notes based on scale
        n1 = get_pitch(base_note, SCALES[scale], degree)      # Root
        n2 = get_pitch(base_note, SCALES[scale], degree + 2)  # 3rd
        n3 = get_pitch(base_note, SCALES[scale], degree + 4)  # 5th

        # Determine if triad is major (interval of 4 semitones from root to 3rd)
        is_major = (n2 - n1) == 4

        start_time_sec = bar * bar_length_sec
        
        # 16th note = 0.25 beats
        if is_major:
            # "1-3-2" Strum for Major: Root -> 5th -> 3rd
            t1 = start_time_sec + 0.00 * beat_length_sec
            t3 = start_time_sec + 0.25 * beat_length_sec
            t2 = start_time_sec + 0.50 * beat_length_sec
        else:
            # "1-2-3" Strum for Minor: Root -> 3rd -> 5th
            t1 = start_time_sec + 0.00 * beat_length_sec
            t2 = start_time_sec + 0.25 * beat_length_sec
            t3 = start_time_sec + 0.50 * beat_length_sec

        # End slightly before the next bar to prevent overlap
        end_time_sec = (bar + 1) * bar_length_sec - 0.05 

        # Insert Notes (Velocity slightly trails off for humanization)
        times = [(t1, n1, velocity_base), (t2, n2, velocity_base - 10), (t3, n3, velocity_base - 20)]
        
        for t_start, pitch, vel in times:
            ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
            ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, pitch, vel, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Sound Design) ===
    # 1. Soft Synth Generator
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Origin Emulation - Telephone EQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "JS: 3-Band EQ", False, -1)
    if eq_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, -20.0) # Cut Lows
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 2.0)   # Boost Mids
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, -18.0) # Cut Highs

    # 3. Origin Emulation - Tape Wow/Flutter (Chorus)
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus (Stereo)", False, -1)
    if chorus_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, chorus_idx, 0, 5.0)  # Delay length
        RPR.RPR_TrackFX_SetParam(track, chorus_idx, 1, 0.4)  # Slow Rate (Wow)
        RPR.RPR_TrackFX_SetParam(track, chorus_idx, 2, 2.5)  # Noticeable Depth
        RPR.RPR_TrackFX_SetParam(track, chorus_idx, 3, 100.0) # 100% Mix

    return f"Created '{track_name}' with {notes_created} staggered lo-fi chord notes over {bars} bars at {bpm} BPM"
