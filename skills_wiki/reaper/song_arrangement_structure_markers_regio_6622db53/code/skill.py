def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 40,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Song Arrangement Structure (Markers, Regions & Guide Chords)
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created arrangement track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars to generate before stopping.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
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

    # === Step 1: Initialize Project Temp & Key Data ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # Helper function to generate basic triadic chords diatonically
    def get_chord_notes(degree, octave=4):
        notes = []
        for offset in [0, 2, 4]:  # Root, Third, Fifth
            idx = (degree + offset) % len(scale_intervals)
            oct_shift = (degree + offset) // len(scale_intervals)
            note = root_val + (octave + oct_shift) * 12 + scale_intervals[idx]
            notes.append(note)
        return notes

    # === Step 2: Create Additive Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add simple synth to hear the arrangement, lower track vol to avoid clipping
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Define Dynamic Song Form ===
    # Format: (Section Name, Default Length, RGB Color, Chord Progression Degrees)
    pop_form = [
        ("Intro",  4, (200, 200, 50), [0]),                        # I (Yellow)
        ("Verse",  8, (50, 200, 50),  [0, 4, 5, 3]),               # I-V-vi-IV (Green)
        ("Chorus", 8, (50, 50, 200),  [3, 0, 4, 5]),               # IV-I-V-vi (Blue)
        ("Bridge", 8, (200, 50, 200), [5, 3, 0, 4]),               # vi-IV-I-V (Purple)
        ("Outro",  4, (200, 100, 50), [0, 3, 0, 0])                # I-IV-I-I  (Orange)
    ]

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    current_bar = 0
    marker_id = 1
    form_idx = 0

    # === Step 4: Generate Regions, Markers, and MIDI Items ===
    while current_bar < bars:
        name_base, default_len, color_rgb, chord_loop = pop_form[form_idx % len(pop_form)]
        
        # Ensure we don't exceed the requested 'bars' parameter
        length_bars = min(default_len, bars - current_bar)
        if length_bars <= 0:
            break
            
        name = f"{name_base} {marker_id}"

        start_sec = current_bar * bar_length_sec
        end_sec = (current_bar + length_bars) * bar_length_sec

        # Parse native OS color required by REAPER with custom flag OR'd (0x1000000)
        r, g, b = color_rgb
        color_val = RPR.RPR_ColorToNative(r, g, b) | 0x1000000

        # Insert Region (isrgn = True)
        RPR.RPR_AddProjectMarker2(0, True, start_sec, end_sec, name, marker_id, color_val)
        
        # Insert Point Marker (isrgn = False)
        RPR.RPR_AddProjectMarker2(0, False, start_sec, 0, f"Start {name}", marker_id + 100, color_val)

        # Create MIDI Item to map the region's duration
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_sec, end_sec, False)
        take = RPR.RPR_GetActiveTake(item)

        # Populate the region with chords
        for i in range(length_bars):
            chord_degree = chord_loop[i % len(chord_loop)]
            notes = get_chord_notes(chord_degree)

            chord_start_time = start_sec + (i * bar_length_sec)
            chord_end_time = start_sec + ((i + 1) * bar_length_sec)

            # Securely retrieve PPQ directly from project time to avoid rounding errors
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_end_time)

            for pitch in notes:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

        RPR.RPR_MIDI_Sort(take)

        current_bar += length_bars
        marker_id += 1
        form_idx += 1

    RPR.RPR_UpdateTimeline()

    return f"Created Macro-Arrangement ({current_bar} bars) featuring {marker_id - 1} Regions/Markers and Diatonic Guide Chords in {key} {scale} at {bpm} BPM."
