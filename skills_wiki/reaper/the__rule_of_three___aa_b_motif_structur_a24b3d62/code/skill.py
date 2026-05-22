def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an AA-B-C phrase structure demonstrating the 'Rule of 3' compositional technique.
    Generates a Melody track and a Chords track to provide full harmonic context.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C', 'F#').
        scale: Scale type ('major', 'minor', 'pentatonic_minor', etc.).
        bars: Total length to generate (loops the 4-bar rule-of-3 structure).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # === State Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    formatted_key = key.capitalize() if len(key) == 1 else key[0].capitalize() + key[1:]
    root_midi = 60 + NOTE_MAP.get(formatted_key, 0) # Base Middle C
    scale_arr = SCALES.get(scale.lower(), SCALES["major"])

    def get_note_from_scale(degree, octave_offset=0):
        """Safely calculates absolute MIDI pitch from a 0-indexed scale degree."""
        octave_shift = (degree // len(scale_arr)) + octave_offset
        note_in_scale = scale_arr[degree % len(scale_arr)]
        return root_midi + note_in_scale + (octave_shift * 12)

    def insert_note(take, start_sec, end_sec, pitch, vel):
        """Translates seconds to PPQ and inserts a MIDI note safely."""
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_sec)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        pitch_safe = max(0, min(127, int(pitch)))
        vel_safe = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch_safe, vel_safe, False)

    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    track_idx = RPR.RPR_CountTracks(0)
    note_count = 0

    # ==========================================
    # Track 1: MELODY (Demonstrates the Variation)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_m = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_m, "P_NAME", f"{track_name}_Melody", True)

    item_m = RPR.RPR_AddMediaItemToTrack(track_m)
    RPR.RPR_SetMediaItemInfo_Value(item_m, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_m, "D_LENGTH", item_length)
    take_m = RPR.RPR_AddTakeToMediaItem(item_m)

    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        bar_position = bar % 4
        current_beat = 0.0

        if bar_position == 0 or bar_position == 1:
            # Iteration 1 & 2: Motif A (Establish Expectation)
            degrees = [0, 2, 4, 7, 4, 2] # 1, 3, 5, 8, 5, 3
            durations = [0.5, 0.5, 0.5, 0.5, 1.0, 1.0]
        elif bar_position == 2:
            # Iteration 3: Motif B (THE RULE OF 3 - Contrast/Break Expectation)
            degrees = [7, 6, 5, 4] # 8, 7, 6, 5 walking down
            durations = [1.0, 0.5, 0.5, 2.0]
        else:
            # Iteration 4: Motif C (Resolution)
            degrees = [4, 6, 7] # 5, 7, 8 Cadence
            durations = [1.0, 1.0, 2.0]

        for deg, dur in zip(degrees, durations):
            start_sec = bar_start_sec + (current_beat * beat_length_sec)
            end_sec = start_sec + (dur * beat_length_sec)
            pitch = get_note_from_scale(deg, 0)
            
            # Slight accent on downbeats
            vel = velocity_base if current_beat % 1.0 == 0 else velocity_base - 15
            
            insert_note(take_m, start_sec, end_sec, pitch, vel)
            current_beat += dur
            note_count += 1

    RPR.RPR_MIDI_Sort(take_m)
    RPR.RPR_TrackFX_AddByName(track_m, "ReaSynth", False, -1)

    # ==========================================
    # Track 2: CHORDS (Provides Context)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_c = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_c, "P_NAME", f"{track_name}_Chords", True)

    item_c = RPR.RPR_AddMediaItemToTrack(track_c)
    RPR.RPR_SetMediaItemInfo_Value(item_c, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_c, "D_LENGTH", item_length)
    take_c = RPR.RPR_AddTakeToMediaItem(item_c)

    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        bar_position = bar % 4
        
        if bar_position == 0 or bar_position == 1:
            chord_degrees = [0, 2, 4] # Tonic Chord
        elif bar_position == 2:
            chord_degrees = [3, 5, 7] # Subdominant Chord (Aligns with Motif B)
        else:
            chord_degrees = [4, 6, 8] # Dominant Chord (Aligns with Motif C)
            
        start_sec = bar_start_sec
        end_sec = bar_start_sec + bar_length_sec
        
        for idx, deg in enumerate(chord_degrees):
            pitch = get_note_from_scale(deg, -1)
            # Roll the chord slightly for acoustic realism
            strum_offset = idx * 0.03
            insert_note(take_c, start_sec + strum_offset, end_sec, pitch, velocity_base - 20)

    RPR.RPR_MIDI_Sort(take_c)
    RPR.RPR_TrackFX_AddByName(track_c, "ReaSynth", False, -1)
    
    # Mix down the chords so melody stands out (0.5 = approx -6dB)
    RPR.RPR_SetMediaTrackInfo_Value(track_c, "D_VOL", 0.5)
    # Pan chords slightly left, melody slightly right for separation
    RPR.RPR_SetMediaTrackInfo_Value(track_m, "D_PAN", 0.2)
    RPR.RPR_SetMediaTrackInfo_Value(track_c, "D_PAN", -0.2)

    return f"Created AA-B phrase structure on '{track_name}_Melody' and '{track_name}_Chords' with {note_count} notes over {bars} bars at {bpm} BPM."
