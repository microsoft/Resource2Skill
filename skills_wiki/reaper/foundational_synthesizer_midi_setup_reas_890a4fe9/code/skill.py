def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "ReaSynth Arp",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create 'Foundational Synthesizer MIDI Setup' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # Input parsing
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track (Additive) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain ===
    # Add native synth and effects as demonstrated in the tutorial
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create MIDI item and get the active take
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate MIDI Arpeggio ===
    # Sequence of scale degrees for a standard electronic arp (Root, 3rd, 5th, Octave)
    arp_sequence = [0, 2, 4, 7, 4, 2, 0, 2] 
    
    notes_added = 0
    for b in range(bars):
        for step in range(8): # 1/8 notes
            degree = arp_sequence[step % len(arp_sequence)]
            
            # Resolve octave shifts if the sequence pushes past the scale length
            octave_shift = degree // len(scale_intervals)
            scale_idx = degree % len(scale_intervals)
            
            # Base octave 4 (MIDI note 60 = Middle C)
            pitch = 60 + root_val + scale_intervals[scale_idx] + (octave_shift * 12)
            
            # Timing calculations (seconds)
            start_sec = (b * bar_length_sec) + (step * (bar_length_sec / 8))
            end_sec = start_sec + (bar_length_sec / 16) # Staccato 1/16th duration
            
            # Convert seconds to PPQ (Pulses Per Quarter Note) for MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, int(pitch), velocity_base, False
            )
            notes_added += 1

    # Finalize MIDI processing
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} arpeggiated MIDI notes over {bars} bars at {bpm} BPM in {key} {scale}."
