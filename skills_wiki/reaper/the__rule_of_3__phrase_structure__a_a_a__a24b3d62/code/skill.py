def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Fixed to 12 to demonstrate the 3x4-bar structure
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' structured phrase (A - A - A') in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Expected to be 12 (three 4-bar blocks).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    # Ensure key and scale are valid
    root_val = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    def get_pitch(degree, base_octave=4):
        """Convert a 0-indexed scale degree to a MIDI pitch."""
        scale_len = len(scale_intervals)
        oct_shift = degree // scale_len
        scale_deg = degree % scale_len
        return root_val + (base_octave + oct_shift + 1) * 12 + scale_intervals[scale_deg]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # 3 iterations of a 4-bar phrase
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Timing Constants
    PPQ = 960
    TICKS_PER_BAR = PPQ * beats_per_bar

    def add_note_evt(start_bar, length_bars, degree, octave, vel):
        start_tick = int(start_bar * TICKS_PER_BAR)
        end_tick = int((start_bar + length_bars) * TICKS_PER_BAR)
        pitch = get_pitch(degree, octave)
        # Ensure velocity is within MIDI bounds
        safe_vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, pitch, safe_vel, False)

    def add_chord(start_bar, length_bars, degrees, octave, vel):
        for d in degrees:
            add_note_evt(start_bar, length_bars, d, octave, vel)

    # --- Phrase Data ---
    # Standard 4-bar Phrase (A)
    chords_A = [
        (0, [0, 2, 4]), # I
        (1, [4, 6, 8]), # V
        (2, [5, 7, 9]), # vi
        (3, [3, 5, 7])  # IV
    ]
    melody_A = [
        (0.0, 0.5, 0), (0.5, 0.5, 2), # Motif part 1
        (1.0, 0.5, 4), (1.5, 0.5, 1), # Motif part 2
        (2.0, 0.5, 5), (2.5, 0.5, 7), # Motif part 3
        (3.0, 1.0, 3)                 # Resolution
    ]

    # Deviated 4-bar Phrase (A') - Changes at Bar 3
    chords_B = [
        (0, [0, 2, 4]), # I  (Same)
        (1, [4, 6, 8]), # V  (Same)
        (2, [1, 3, 5]), # ii (Different - Tension)
        (3, [4, 6, 8])  # V  (Different - Turnaround)
    ]
    melody_B = [
        (0.0, 0.5, 0), (0.5, 0.5, 2), # Motif part 1 (Same)
        (1.0, 0.5, 4), (1.5, 0.5, 1), # Motif part 2 (Same)
        (2.0, 0.5, 8), (2.5, 0.5, 5), # Motif part 3 (Deviated, higher energy)
        (3.0, 1.0, 4)                 # Resolution (Deviated, pulling back to I)
    ]

    note_count = 0

    # Iteration 1: Introduce Idea (Bars 0-3)
    for bar_offset, degrees in chords_A:
        add_chord(0 + bar_offset, 1.0, degrees, 3, velocity_base)
        note_count += len(degrees)
    for m_start, m_len, m_deg in melody_A:
        add_note_evt(0 + m_start, m_len, m_deg, 4, velocity_base + 5)
        note_count += 1

    # Iteration 2: Reinforce Pattern (Bars 4-7)
    for bar_offset, degrees in chords_A:
        add_chord(4 + bar_offset, 1.0, degrees, 3, velocity_base)
        note_count += len(degrees)
    for m_start, m_len, m_deg in melody_A:
        add_note_evt(4 + m_start, m_len, m_deg, 4, velocity_base + 5)
        note_count += 1

    # Iteration 3: "Rule of 3" Deviation (Bars 8-11)
    for bar_offset, degrees in chords_B:
        # Increase velocity slightly on the turnaround to emphasize the arrangement change
        vel_bump = 10 if bar_offset >= 2 else 0 
        add_chord(8 + bar_offset, 1.0, degrees, 3, velocity_base + vel_bump)
        note_count += len(degrees)
    for m_start, m_len, m_deg in melody_B:
        vel_bump = 10 if m_start >= 2.0 else 0
        add_note_evt(8 + m_start, m_len, m_deg, 4, velocity_base + 5 + vel_bump)
        note_count += 1

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add ReaSynth to immediately hear the harmonic structure
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the synth so it sounds more like a gentle pluck/key
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.1) # Shorter decay/release characteristic if available
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.5) # Lower square wave mix

    return f"Created '{track_name}' with {note_count} notes. Applied 'Rule of 3' structure over {total_bars} bars at {bpm} BPM in {key} {scale}."
