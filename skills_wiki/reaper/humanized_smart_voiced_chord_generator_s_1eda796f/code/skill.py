def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Strummed Chords",
    bpm: int = 90,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 85,
    strum_ms: int = 30,         # Milliseconds to stagger each note
    humanize_vel: int = 12,     # +/- velocity variation
    **kwargs,
) -> str:
    """
    Creates a humanized, strummed 4-bar chord progression replicating "Chordable" plugin output.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars (determines how many times the progression loops).
        velocity_base: Base MIDI velocity (0-127).
        strum_ms: Delay in milliseconds between notes in a chord to create a "strum".
        humanize_vel: Random velocity variance amount.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created element.
    """
    import random
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

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    def get_pitch(degree, base_octave=4):
        """Converts a 1-based scale degree into a MIDI pitch."""
        degree -= 1 
        octave_offset = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        # MIDI note 48 is C3, 60 is C4
        return root_val + (base_octave + octave_offset) * 12 + scale_intervals[idx]

    # Standard Diatonic Progression: I - vi - IV - V
    base_progression = [1, 6, 4, 5]
    
    # Loop progression to fill requested bars
    progression = []
    for i in range(bars):
        progression.append(base_progression[i % len(base_progression)])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * len(progression)
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Humanized MIDI Data ===
    RPR.RPR_MIDI_DisableSort(take)
    
    note_count = 0
    strum_sec = strum_ms / 1000.0

    for i, scale_degree in enumerate(progression):
        start_time_sec = i * bar_length_sec
        # Leave a 10% gap before the next chord for clarity
        end_time_sec = start_time_sec + (bar_length_sec * 0.90) 
        
        # Build a 7th chord (Root, 3rd, 5th, 7th) relative to the scale
        chord_degrees = [
            scale_degree, 
            scale_degree + 2, 
            scale_degree + 4, 
            scale_degree + 6
        ]
        
        for j, degree in enumerate(chord_degrees):
            pitch = get_pitch(degree, base_octave=4)
            
            # Strum Timing: Offset start time based on note position in chord (bottom to top)
            note_start = start_time_sec + (j * strum_sec)
            note_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start)
            note_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            # Velocity Humanization: Lower notes anchor the chord slightly harder
            human_offset = random.randint(-humanize_vel, humanize_vel)
            velocity = velocity_base - (j * 4) + human_offset
            velocity = max(1, min(127, int(velocity)))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, note_start_ppq, note_end_ppq, 0, pitch, velocity, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ADSR for a warmer, keys/pad-like sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.05) # Slight attack so it's not clicky
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.40) # Distinct release tail

    return f"Created '{track_name}' with {note_count} strummed, humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
