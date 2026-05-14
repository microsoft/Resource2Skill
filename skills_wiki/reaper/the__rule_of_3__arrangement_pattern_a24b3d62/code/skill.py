def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule_of_3_Theme",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create The "Rule of 3" Arrangement Pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (forces to 12 to demonstrate 3x4-bar blocks).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    root_midi = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # Helper to convert scale degrees (0-indexed) into MIDI note numbers
    def get_pitch(degree, oct_offset):
        octaves = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_midi + scale_intervals[idx] + (octaves + oct_offset) * 12

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    # Forcing exactly 12 bars to demonstrate the 3x4 block structure
    total_bars = 12 
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    item_length = bar_len * total_bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper to safely insert MIDI notes
    def add_note(start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Helper to draw a continuous 8th note arpeggio for a given diatonic triad
    def draw_arpeggio(start_time, chord_degrees):
        r1, r3, r5 = chord_degrees
        # 8th note pattern: Root, 5th, 3rd, 5th
        pattern = [r1, r5, r3, r5, r1, r5, r3, r5]
        
        for i, deg in enumerate(pattern):
            t_start = start_time + i * (beat_len / 2.0)
            t_end = t_start + (beat_len / 2.0) * 0.85 # Slight staccato
            p = get_pitch(deg, 4) # Melody in Octave 4
            add_note(t_start, t_end, p, velocity_base - 15)
            
            # Root bass note every half note
            if i % 4 == 0:
                p_bass = get_pitch(r1, 2) # Bass in Octave 2
                add_note(t_start, t_start + beat_len * 1.8, p_bass, velocity_base + 5)

    # Define Diatonic Triads (degrees)
    chord_I  = [0, 2, 4]
    chord_IV = [3, 5, 7]
    chord_V  = [4, 6, 8]
    chord_vi = [5, 7, 9]

    # Block A: The Theme
    progression_A = [chord_I, chord_IV, chord_vi, chord_IV]
    # Block B: The Deviation (subverts the expected IV chord by going to V)
    progression_B = [chord_I, chord_V, chord_vi, chord_V] 

    # Loop 3 blocks of 4 bars
    for block in range(3):
        block_start_time = block * 4 * bar_len
        # Apply the "Rule of 3": Block 1 & 2 are A, Block 3 is B
        current_progression = progression_A if block < 2 else progression_B
        
        for bar, chord in enumerate(current_progression):
            bar_start = block_start_time + bar * bar_len
            draw_arpeggio(bar_start, chord)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Shape ReaSynth into a pluck to enhance rhythmic perception
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.01) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.30) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 4, 0.10) # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 5, 0.40) # Release

    # Add ReaDelay for atmosphere
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    
    # Mixdown (lower fader so synths don't clip master)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) 

    return f"Created '{track_name}' demonstrating the 'Rule of 3' structure over 12 bars at {bpm} BPM."
