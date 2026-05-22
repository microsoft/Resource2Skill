def create_algorithmic_chord_progression(
    project_name: str = "MyProject",
    track_name: str = "Algo Chords",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    complexity: int = 2,  # 1=Triads, 2=7ths, 3=9ths
    add_bass_notes: bool = True,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an algorithmic chord progression emulating the Reanspiration script.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, etc.).
        bars: Number of bars to generate.
        complexity: Number of note extensions (1 = triad, 2 = 7th chord, 3 = 9th chord).
        add_bass_notes: Whether to add a deep root note below the chords.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated progression.
    """
    import random
    import reaper_python as RPR

    # === Step 1: Music Theory Data ===
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
    }

    if scale not in SCALES:
        scale = "minor"
        
    root_midi = NOTE_MAP.get(key, 0) + 48  # Start around C3 (MIDI 48)
    scale_intervals = SCALES[scale]
    scale_len = len(scale_intervals)

    # === Step 2: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 3: Create Track & Item ===
    RPR.RPR_Undo_BeginBlock2(0)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create empty MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetMediaItemTake(item, 0)

    # === Step 4: Algorithmic Generation Logic ===
    PPQ_PER_QUARTER = 960
    PPQ_PER_BAR = PPQ_PER_QUARTER * 4
    
    notes_added = 0
    
    # Possible rhythmic subdivisions per bar (in beats)
    rhythm_patterns = [
        [4.0],                  # One whole note
        [2.0, 2.0],             # Two half notes
        [1.5, 0.5, 2.0],        # Dotted quarter, eighth, half
        [2.0, 1.0, 1.0],        # Half, quarter, quarter
        [3.0, 1.0]              # Dotted half, quarter
    ]

    for bar in range(bars):
        bar_start_ppq = bar * PPQ_PER_BAR
        current_beat_offset = 0.0
        
        # Pick a random rhythm pattern for this bar
        pattern = random.choice(rhythm_patterns)
        
        for duration_beats in pattern:
            # Pick a random diatonic chord root (scale degree 0 to scale_len-1)
            chord_root_degree = random.randint(0, scale_len - 1)
            
            # Calculate start and end PPQ
            start_ppq = int(bar_start_ppq + (current_beat_offset * PPQ_PER_QUARTER))
            end_ppq = int(start_ppq + (duration_beats * PPQ_PER_QUARTER))
            
            # Slightly shorten end_ppq for a legato gap (98% length)
            end_ppq = int(start_ppq + ((end_ppq - start_ppq) * 0.98))
            
            # Build the chord (Root, 3rd, 5th, etc. based on complexity)
            # Complexity 1 = triad (3 notes), 2 = 7th (4 notes), 3 = 9th (5 notes)
            chord_tones = 2 + complexity 
            
            for i in range(chord_tones):
                # Stack thirds diatonically
                degree = (chord_root_degree + (i * 2)) % scale_len
                octave_shift = (chord_root_degree + (i * 2)) // scale_len
                
                pitch = root_midi + scale_intervals[degree] + (octave_shift * 12)
                
                # Keep pitches reasonably voiced (invert down if too high)
                while pitch > 72:
                    pitch -= 12
                
                # Humanize velocity
                vel = max(1, min(127, velocity_base + random.randint(-10, 10)))
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
                notes_added += 1

            # Add Bass Note
            if add_bass_notes:
                bass_pitch = root_midi + scale_intervals[chord_root_degree] - 12
                # If root_midi is already low, keep it, otherwise drop another octave
                if bass_pitch > 45:
                    bass_pitch -= 12
                
                bass_vel = max(1, velocity_base - 15) # Slightly softer
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, bass_vel, False)
                notes_added += 1

            current_beat_offset += duration_beats

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Preview FX (ReaSynth) ===
    # Adds a soft keys/pad sound to preview the chords
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Turn down square/saw, turn up triangle for a softer sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)    # Vol
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)    # Saw
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)    # Square
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 1.0)    # Triangle
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.05)   # Attack (soften)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.5)    # Release

    RPR.RPR_Undo_EndBlock2(0, "Create Algorithmic Chord Progression", -1)

    return f"Created algorithmic track '{track_name}' in {key} {scale} with {notes_added} notes over {bars} bars at {bpm} BPM."
