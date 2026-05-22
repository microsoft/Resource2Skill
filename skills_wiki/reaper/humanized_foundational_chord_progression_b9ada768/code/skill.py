def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Creates a basic humanized MIDI chord progression in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), will be humanized around this.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 60, "C#": 61, "Db": 61, "D": 62, "D#": 63, "Eb": 63,
                "E": 64, "F": 65, "F#": 66, "Gb": 66, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}
    
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
        scale = "major"
    scale_intervals = SCALES[scale]
    root_midi = NOTE_MAP.get(key, 60)

    # === Step 1: Initialize Project Routing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add stock instrument to audition the MIDI
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 2: Establish Media Item Details ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    start_time = 0.0
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Progression Selection based on tonality
    if scale in ["minor", "harmonic_minor", "dorian", "pentatonic_minor", "blues"]:
        progression = [0, 5, 2, 4]  # i, VI, III, VII
    else:
        progression = [0, 4, 5, 3]  # I, V, vi, IV

    notes_created = 0

    # === Step 3: Generate Humanized MIDI ===
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # Build Triad
        chord_notes = []
        for i in [0, 2, 4]:
            scale_degree = degree + i
            octave = scale_degree // len(scale_intervals)
            idx = scale_degree % len(scale_intervals)
            note = root_midi + (octave * 12) + scale_intervals[idx]
            chord_notes.append(note)

        # Enhance voicing (Left hand bass note)
        chord_notes.append(chord_notes[0] - 12)
        
        # Base Timing
        start_sec = bar * bar_length_sec
        end_sec = start_sec + (bar_length_sec * 0.85) # Leave a slight staccato gap
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

        for i, note in enumerate(chord_notes):
            # Humanize Velocity 
            vel_offset = random.randint(-15, 15)
            vel = max(1, min(127, int(velocity_base + vel_offset)))
            
            # Humanize Timing: global slop + staggered 'strum' effect
            strum_offset = i * random.randint(5, 15) 
            global_offset = random.randint(-10, 10)
            
            note_start = max(0, start_ppq + global_offset + strum_offset)
            note_end = max(note_start + 10, end_ppq + global_offset)
            
            # Insert Note (noSort = True for batch processing)
            RPR.RPR_MIDI_InsertNote(take, False, False, note_start, note_end, 0, note, vel, True)
            notes_created += 1

    # Apply sorting after batch insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' track with {notes_created} dynamically humanized notes over {bars} bars at {bpm} BPM."
