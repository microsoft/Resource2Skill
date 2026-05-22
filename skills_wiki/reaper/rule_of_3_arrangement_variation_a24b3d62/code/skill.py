def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' Arrangement pattern in the current REAPER project.
    Generates three 4-bar phrases: A, A, and A' (variation on the 3rd repetition).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Forces to 12 to demonstrate the 3x 4-bar phrase rule.
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

    root_pitch = NOTE_MAP.get(key, 9) # Default to A
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Helper functions for Music Math ===
    def get_pitch(degree, octave):
        """Converts a diatonic scale degree into a raw MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_pitch + scale_intervals[scale_idx] + (octave + octave_shift) * 12

    def add_note(take, start_time, duration, pitch, vel):
        """Inserts a MIDI note taking proj_time instead of PPQ."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        
        # Clamp MIDI values safely
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 1: Create Additive Tracks ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Chords track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chords", True)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "D_VOL", 0.6)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    
    # Melody track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    melody_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(melody_track, "P_NAME", f"{track_name}_Melody", True)
    RPR.RPR_SetMediaTrackInfo_Value(melody_track, "D_VOL", 0.8)
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaSynth", False, -1)

    # === Step 2: Create Media Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = 12  # Forced to 12 to correctly demonstrate the 3 phases
    item_length = bar_length_sec * total_bars
    
    # Setup Chord Item
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", item_length)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)
    
    # Setup Melody Item
    melody_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", item_length)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)

    # === Step 3: Generate the "Rule of 3" Pattern ===
    # Using 0-indexed scale degrees
    chord_degrees_p1 = [0, 5, 2, 6] # Base Idea: i, VI, III, VII
    chord_degrees_p3 = [0, 5, 3, 4] # Variation Idea: i, VI, iv, v (Tension build)
    
    def add_chord(take, start_time, duration, root_degree, octave):
        notes = [
            get_pitch(root_degree, octave),
            get_pitch(root_degree + 2, octave),
            get_pitch(root_degree + 4, octave)
        ]
        for p in notes:
            add_note(take, start_time, duration, p, velocity_base - 10)

    def add_melody_motif(take, start_time, root_degree, octave):
        """Standard broken-chord motif played during Repetitions 1 and 2"""
        beat_len = 60.0 / bpm
        add_note(take, start_time, beat_len * 0.45, get_pitch(root_degree, octave), velocity_base)
        add_note(take, start_time + beat_len * 0.5, beat_len * 0.45, get_pitch(root_degree + 2, octave), velocity_base - 10)
        add_note(take, start_time + beat_len * 1.0, beat_len * 0.9, get_pitch(root_degree, octave), velocity_base)
        add_note(take, start_time + beat_len * 2.0, beat_len * 1.9, get_pitch(root_degree + 4, octave), velocity_base - 5)

    def add_melody_variation(take, start_time, root_degree, octave):
        """Tension-building scalar run played during Repetition 3"""
        beat_len = 60.0 / bpm
        for i in range(8):
            pitch = get_pitch(root_degree + i, octave)
            # Velocity naturally builds up during the run
            dyn_vel = velocity_base + (i * 3) 
            add_note(take, start_time + i * beat_len * 0.5, beat_len * 0.4, pitch, dyn_vel)

    # Iterate through the 3 phases of the arrangement
    for phrase in range(3):
        phrase_start = phrase * 4 * bar_length_sec
        # Switch to the Variation chords on the 3rd Repetition
        degrees = chord_degrees_p3 if phrase == 2 else chord_degrees_p1
            
        for bar in range(4):
            bar_start = phrase_start + bar * bar_length_sec
            deg = degrees[bar]
            
            # Insert Harmony
            add_chord(chords_take, bar_start, bar_length_sec * 0.95, deg, 4) # Octave 4 (~C3)
            
            # Apply the "Rule of 3" Melodic Variation halfway through the 3rd phrase
            if phrase == 2 and bar >= 2:
                add_melody_variation(melody_take, bar_start, deg, 5) # Octave 5 (~C4)
            else:
                add_melody_motif(melody_take, bar_start, deg, 5)

    # Refresh MIDI items
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(melody_take)

    return f"Created Rule of 3 Arrangement ({total_bars} bars) across 2 tracks in {key} {scale} at {bpm} BPM."
