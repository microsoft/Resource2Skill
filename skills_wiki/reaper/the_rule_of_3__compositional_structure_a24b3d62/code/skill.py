def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOfThree_Melody",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' Compositional Structure in the current REAPER project.
    Generates a dynamically varying melody/chord progression that changes on the 3rd repetition.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (loops the 4-bar rule-of-3 macro structure).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7)   # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.5)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5)   # Triangle mix
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.05)  # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.5)   # Decay
    
    # Add room reverb to create space
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root_midi = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(intervals)

    def get_note(degree, octave):
        """Converts a scale degree and octave into a precise MIDI note number."""
        octave_offset = degree // scale_len
        scale_degree = degree % scale_len
        return root_midi + intervals[scale_degree] + (octave + 1) * 12

    def insert_midi_note(start_qtr, length_qtr, pitch, vel):
        """Helper to insert MIDI notes accurately quantized to project time/PPQ."""
        start_pos = start_qtr * (60.0 / bpm)
        end_pos = (start_qtr + length_qtr) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        pitch = max(0, min(127, int(pitch)))
        vel = max(0, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Define the "Rule of 3" sequence (A - A - B - C)
    block_phrases = [
        {"chord": 0, "melody": [0, 2, 4, 2]}, # Bar 1: Idea Statement
        {"chord": 0, "melody": [0, 2, 4, 2]}, # Bar 2: Idea Reinforcement
        {"chord": 3, "melody": [3, 5, 7, 5]}, # Bar 3: The Rule of 3 (Deviation!)
        {"chord": 4, "melody": [4, 5, 6, 7]}, # Bar 4: Resolution / Cadence
    ]

    # Syncopated rhythm pattern (offsets in quarter notes, length in quarter notes)
    melody_rhythm = [
        (0.0, 1.0), # Beat 1 (On-beat)
        (1.5, 0.5), # Beat 2 "And" (Off-beat, syncopated)
        (2.0, 1.0), # Beat 3 (On-beat)
        (3.0, 1.0)  # Beat 4 (On-beat)
    ]

    note_count = 0
    # Generate the pattern, looping the 4-bar macro structure if needed
    for bar in range(bars):
        p = block_phrases[bar % 4]
        bar_start_qtr = bar * beats_per_bar
        
        # 1. Insert Chords (Sustained whole notes)
        chord_root = p["chord"]
        insert_midi_note(bar_start_qtr, 4.0, get_note(chord_root, 2), velocity_base * 0.8)       # Bass
        insert_midi_note(bar_start_qtr, 4.0, get_note(chord_root, 3), velocity_base * 0.6)       # Root
        insert_midi_note(bar_start_qtr, 4.0, get_note(chord_root + 2, 3), velocity_base * 0.6)   # 3rd
        insert_midi_note(bar_start_qtr, 4.0, get_note(chord_root + 4, 3), velocity_base * 0.6)   # 5th
        note_count += 4

        # 2. Insert Melody (Plucked rhythm)
        for i, (offset, length) in enumerate(melody_rhythm):
            melody_degree = p["melody"][i]
            insert_midi_note(bar_start_qtr + offset, length, get_note(melody_degree, 4), velocity_base)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"
