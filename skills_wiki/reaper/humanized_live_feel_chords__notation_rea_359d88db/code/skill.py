def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Keyboard",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Humanized Live-Feel Chords in the current REAPER project.
    Generates a I-IV-V-I progression with randomized timing and velocity
    to simulate a live keyboard performance.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (loops the progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a stock synth to hear the chords
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Humanized MIDI ===
    root_midi = 60 + NOTE_MAP.get(key, 0) # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_pitch(degree):
        """Converts a scale degree (0-based) to a MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_midi + scale_intervals[scale_idx] + (octave_shift * 12)

    # I - IV - V - I chord progression (0-based scale degrees)
    progression = [
        [0, 2, 4], # I chord
        [3, 5, 7], # IV chord
        [4, 6, 8], # V chord
        [0, 2, 4], # I chord
    ]

    notes_created = 0
    
    for bar_idx in range(bars):
        chord_degrees = progression[bar_idx % len(progression)]
        base_start_beat = bar_idx * beats_per_bar
        
        for degree in chord_degrees:
            pitch = get_pitch(degree)
            
            # Simulate human timing inaccuracies (flamming/strumming)
            start_offset_beats = random.uniform(-0.04, 0.04)
            end_offset_beats = random.uniform(-0.1, 0.1)
            
            start_beat = max(0.0, base_start_beat + start_offset_beats)
            # Chords ring out for almost the whole bar
            end_beat = base_start_beat + 3.7 + end_offset_beats
            
            start_time = start_beat * beat_length_sec
            end_time = end_beat * beat_length_sec
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Simulate human velocity differences between fingers
            vel = max(1, min(127, velocity_base + random.randint(-18, 18)))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized chord notes over {bars} bars at {bpm} BPM in {key} {scale}."
