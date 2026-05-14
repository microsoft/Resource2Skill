def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' compositional structure in the current REAPER project.
    Generates 3 iterations of a phrase, introducing a variation on the 3rd iteration.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Target number of bars. Will be rounded to a multiple of 3 to satisfy the pattern.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
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

    # Input sanitization
    scale = scale.lower()
    if scale not in SCALES:
        scale = "major"
    if key not in NOTE_MAP:
        key = "C"
        
    velocity_base = max(10, min(127, velocity_base))
    scale_intervals = SCALES[scale]
    root_pitch = NOTE_MAP[key]

    # === Step 1: Set Tempo & Structure ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Enforce Rule of 3 structure: we need exactly 3 iterations.
    # We divide the requested bars by 3 to find the phrase length.
    total_bars = max(3, (bars // 3) * 3)
    phrase_bars = total_bars // 3
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Helper Functions for MIDI Generation ===
    def get_pitch(octave, degree):
        scale_len = len(scale_intervals)
        octave_offset = degree // scale_len
        scale_degree = degree % scale_len
        return root_pitch + (octave + octave_offset) * 12 + scale_intervals[scale_degree]

    def insert_chord(position_sec, duration_sec, root_deg, octave, velocity):
        # Insert Root, 3rd, and 5th
        for offset in [0, 2, 4]:
            pitch = get_pitch(octave, root_deg + offset)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, position_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, position_sec + duration_sec)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, False)

    def insert_melody(position_sec, duration_sec, root_deg, octave, velocity, descending=False):
        # Standard ascending arpeggio: Root, 3rd, 5th, Octave, 5th, 3rd, Root, 3rd
        offsets = [0, 2, 4, 7, 4, 2, 0, 2]
        
        if descending:
            # Variation descending arpeggio to emphasize the expectation break
            offsets = [7, 4, 2, 0, 2, 4, 7, 4]
            
        step_duration = duration_sec / 8.0
        for i, offset in enumerate(offsets):
            pitch = get_pitch(octave, root_deg + offset)
            start_sec = position_sec + i * step_duration
            end_sec = start_sec + step_duration * 0.8 # 80% legato length
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Accent the first note of the arpeggio
            vel = velocity if i == 0 else int(velocity * 0.8)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 4: Populate MIDI logic (The Rule of 3) ===
    notes_created = 0
    
    for iteration in range(3):
        is_variation_iteration = (iteration == 2)
        
        for bar_in_phrase in range(phrase_bars):
            global_bar = iteration * phrase_bars + bar_in_phrase
            position_sec = global_bar * bar_length_sec
            
            # Determine if we are in the "break expectation" phase 
            # (Latter half of the 3rd iteration)
            is_variation_bar = is_variation_iteration and (phrase_bars == 1 or bar_in_phrase >= phrase_bars / 2)
            
            # Select chord degrees
            if is_variation_bar:
                # Break expectation: shift to VI and V chords
                chord_deg = 5 if bar_in_phrase % 2 == 0 else 4 
            else:
                # Base pattern: alternate between I and IV chords
                chord_deg = 0 if bar_in_phrase % 2 == 0 else 3 
                
            # Insert backing block chords
            insert_chord(position_sec, bar_length_sec, chord_deg, 4, velocity_base - 30)
            notes_created += 3
            
            # Insert lead melody (flips contour during variation bars)
            insert_melody(position_sec, bar_length_sec, chord_deg, 5, velocity_base, descending=is_variation_bar)
            notes_created += 8

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)

    return f"Created '{track_name}' showcasing the Rule of 3: {notes_created} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
