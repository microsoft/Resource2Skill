def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Catchy Motif Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "pentatonic_major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pentatonic Motif Melody in the current REAPER project.
    Implements the "Establish -> Repeat -> Vary -> Complete Variation" method.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (default to pentatonic_major).
        bars: Number of bars to generate (should be multiples of 4 for phrasing).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Normalize inputs
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_major"])
    
    # Base octave for a lead melody (C4 = 60)
    base_octave = 5 

    def calc_pitch(degree: int) -> int:
        """Converts a scale degree into a pure MIDI pitch."""
        scale_len = len(scale_intervals)
        octave_shift = degree // scale_len
        scale_idx = degree % scale_len
        return (base_octave + octave_shift) * 12 + root_val + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Define the Melodic Phrase (4-Bar structure) ===
    # Each note dictionary defines start_beat, length_in_beats, and scale degree
    phrase_blueprint = [
        # Bar 1 (Establish): 2-note motif
        {"b_start": 0.0, "b_len": 1.0, "degree": 1},
        {"b_start": 1.0, "b_len": 1.0, "degree": 2},
        
        # Bar 2 (Exact Repetition)
        {"b_start": 4.0, "b_len": 1.0, "degree": 1},
        {"b_start": 5.0, "b_len": 1.0, "degree": 2},
        
        # Bar 3 (Repetition with Variation): Speeds up, adds the root note (degree 0)
        {"b_start": 8.0, "b_len": 1.0, "degree": 1},
        {"b_start": 9.0, "b_len": 0.5, "degree": 2},
        {"b_start": 9.5, "b_len": 1.5, "degree": 0},
        
        # Bar 4 (Complete Variation): Reaches higher into the scale
        {"b_start": 12.0, "b_len": 1.0, "degree": 2},
        {"b_start": 13.0, "b_len": 1.0, "degree": 3},
        {"b_start": 14.0, "b_len": 2.0, "degree": 4}
    ]

    # === Step 4: Create MIDI Item and Populate Notes ===
    beats_per_bar = 4.0
    sec_per_beat = 60.0 / bpm
    
    # Ensure minimum of 4 bars to complete one full phrase loop
    total_bars = max(4, bars - (bars % 4) if bars % 4 != 0 else bars)
    total_beats = total_bars * beats_per_bar
    item_length_sec = total_beats * sec_per_beat
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Loop the 4-bar phrase across the requested total bars
    phrase_repeats = total_bars // 4
    note_count = 0

    for repeat in range(phrase_repeats):
        beat_offset = repeat * 16.0  # 4 bars * 4 beats
        
        for note in phrase_blueprint:
            absolute_beat_start = beat_offset + note["b_start"]
            absolute_beat_end = absolute_beat_start + note["b_len"]
            
            start_time = absolute_beat_start * sec_per_beat
            end_time = absolute_beat_end * sec_per_beat
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = calc_pitch(note["degree"])
            
            # Add slight velocity humanization on downbeats vs upbeats
            vel = velocity_base if (absolute_beat_start % 1.0 == 0) else max(10, velocity_base - 15)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Sound Design) ===
    # Add native ReaSynth to create a catchy pluck lead
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth: Saw/Square blend with a moderate release for a "pluck" sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Waveform blend (mix of saw/square)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.01)  # Attack time (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.35)  # Release time (musical fade)

    return f"Created '{track_name}' with {note_count} catchy melody notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
