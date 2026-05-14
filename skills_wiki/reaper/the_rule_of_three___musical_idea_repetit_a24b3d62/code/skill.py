def create_rule_of_three_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of Three Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # Total bars: 4 (idea 1) + 4 (idea 2) + 4 (variation)
    melody_octave: int = 5,
    chord_octave: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a musical idea repeated twice, followed by a variation, demonstrating
    the "Rule of Three" for musical composition.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Total number of bars to generate (should be a multiple of 4 for this pattern).
        melody_octave: Octave for the melody (e.g., 5 for C5).
        chord_octave: Octave for the chord roots (e.g., 4 for C4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this skill).

    Returns:
        Status string, e.g., "Created 'Rule of Three Piano' with 48 notes over 12 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }
    CHORD_TYPES = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "dom7": [0, 4, 7, 10],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dim": [0, 3, 6],
    }

    import reaper_python as RPR

    # Get root key MIDI note
    key_root_midi = NOTE_MAP.get(key, 0) # Default to C

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for a basic piano sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth to a simple sound (e.g., sine wave)
    # RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.5) # Example: Waveform parameter to Sine

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length = float(bars) * beats_per_bar / (bpm / 60.0)
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)

    # Get MIDI_Take for note insertion
    midi_take = RPR.RPR_MIDI_GetTake(take)
    if not midi_take:
        return "Failed to get MIDI take."

    # Define the base musical idea (4 bars: C-G-Am-F with simple melody)
    # Chords: Root note, then add intervals from CHORD_TYPES["major"] or "minor"
    # Melody: Single note per bar, sustained
    
    # Idea 1 & 2 chord roots (MIDI notes relative to key_root_midi + chord_octave*12)
    idea_chord_roots = [
        (0, "major"),  # C
        (7, "major"),  # G
        (9, "minor"),  # Am
        (5, "major")   # F
    ]
    # Melody notes (MIDI notes relative to key_root_midi + melody_octave*12)
    idea_melody_notes = [
        (0, melody_octave), # C5
        (11, melody_octave - 1), # B4 (relative to C, 11 semitones up, then 1 octave down)
        (9, melody_octave - 1), # A4
        (7, melody_octave - 1)  # G4
    ]

    # Variation chord roots (first 2 bars same, last 2 bars different: D-G)
    variation_chord_roots = [
        (0, "major"),  # C
        (7, "major"),  # G
        (2, "major"),  # D
        (7, "major")   # G
    ]
    # Variation melody notes
    variation_melody_notes = [
        (0, melody_octave), # C5
        (11, melody_octave - 1), # B4
        (2, melody_octave), # D5 (over D)
        (7, melody_octave - 1) # G4 (over G)
    ]

    note_count = 0
    start_pos_beats = 0.0
    bar_duration = beats_per_bar * (60.0 / bpm) # Duration of one bar in seconds
    
    # Function to insert notes for a 4-bar phrase
    def insert_phrase(midi_take, current_start_beats, chord_roots, melody_notes):
        nonlocal note_count
        for i in range(4): # For each bar in the 4-bar phrase
            # Insert chord notes
            chord_root_interval = chord_roots[i][0]
            chord_type = chord_roots[i][1]
            chord_base_midi = key_root_midi + chord_root_interval + chord_octave * 12
            for interval in CHORD_TYPES[chord_type]:
                pitch = chord_base_midi + interval
                # RPR.MIDI_InsertNote(midi_take, 0, 0, start_time_beats, end_time_beats, is_selected, no_snap, pitch, velocity, no_loop)
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_start_beats + i * beats_per_bar, current_start_beats + (i + 1) * beats_per_bar, velocity_base, True, pitch, velocity_base, False)
                note_count += 1
            
            # Insert melody note (quarter note)
            melody_base_midi = key_root_midi + melody_notes[i][0] + melody_notes[i][1] * 12
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_start_beats + i * beats_per_bar, current_start_beats + i * beats_per_bar + beats_per_bar / 4.0, velocity_base + 10, True, melody_base_midi, velocity_base + 10, False)
            note_count += 1
        return current_start_beats + 4 * beats_per_bar # Return new start position

    # Repeat the musical idea twice
    start_pos_beats = insert_phrase(midi_take, start_pos_beats, idea_chord_roots, idea_melody_notes) # 1st time
    start_pos_beats = insert_phrase(midi_take, start_pos_beats, idea_chord_roots, idea_melody_notes) # 2nd time

    # Introduce a variation for the third iteration
    start_pos_beats = insert_phrase(midi_take, start_pos_beats, variation_chord_roots, variation_melody_notes) # 3rd time (variation)

    # Clean up MIDI item (sort notes, update UI)
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"

