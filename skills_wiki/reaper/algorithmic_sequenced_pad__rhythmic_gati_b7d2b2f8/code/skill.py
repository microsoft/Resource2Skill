def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic Sequenced Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a rhythmically sliced pad progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Music Theory Lookups ===
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
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Helper to build diatonic 7th chords
    def get_chord(degree):
        n_notes = len(scale_intervals)
        return [
            root_val + scale_intervals[degree % n_notes] + (12 * (degree // n_notes)),
            root_val + scale_intervals[(degree + 2) % n_notes] + (12 * ((degree + 2) // n_notes)),
            root_val + scale_intervals[(degree + 4) % n_notes] + (12 * ((degree + 4) // n_notes)),
            root_val + scale_intervals[(degree + 6) % n_notes] + (12 * ((degree + 6) // n_notes))
        ]

    # === Step 3: Create Track & Item ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    beats_per_bar = 4
    bar_len_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_len_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Algorithmic Rhythm Generation ===
    # A standard 16-step Euclidean-style syncopation
    rhythm = [1, 0, 0, 1,  0, 0, 1, 0,  0, 1, 0, 0,  1, 0, 1, 0]
    step_len_sec = bar_len_sec / 16.0
    note_len_sec = step_len_sec * 0.8  # Staccato gating effect
    
    # Progression spanning scale degrees (e.g., i, VI, v, i)
    progression = [0, 5, 4, 0] 
    base_octave = 48 # Octave 3 for a warm pad range

    note_count = 0
    for b in range(bars):
        chord_deg = progression[b % len(progression)]
        chord_notes = get_chord(chord_deg)
        
        for step_idx, val in enumerate(rhythm):
            if val == 1:
                pos_sec = (b * bar_len_sec) + (step_idx * step_len_sec)
                end_sec = pos_sec + note_len_sec
                
                # Convert seconds to REAPER PPQ
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                
                for note in chord_notes:
                    pitch = int(base_octave + note)
                    pitch = max(0, min(127, pitch)) # Clamp to valid MIDI
                    
                    RPR.RPR_MIDI_InsertNote(
                        take, False, False, 
                        start_ppq, end_ppq, 
                        0, pitch, velocity_base, False
                    )
                    note_count += 1
                    
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Sliced Pad Tone) ===
    # Emulate a rich, gated pad using ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set Attack, Decay to 0; Sustain to full, Release fast (creates a gate envelope)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.0)   # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 1.0)   # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.03)  # Release
    # Mix Saw and Square waves for maximum harmonic depth
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.5)   # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.8)   # Saw mix

    # Add ReaDelay to widen the rhythm
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 0, 0.2)   # Wet mix

    return f"Created '{track_name}' with {note_count} rhythmic pad notes over {bars} bars at {bpm} BPM."
