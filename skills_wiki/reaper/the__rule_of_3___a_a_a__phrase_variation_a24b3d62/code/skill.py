def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Variation",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # Hardcoded to 12 in the logic below to demonstrate the 3x4-bar rule
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' (A-A-A') phrase structure in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored here (forced to 12 to demonstrate the concept).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created musical structure.
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 48 # Base octave C3

    def get_pitch(degree):
        """Converts a 0-indexed scale degree into a MIDI pitch."""
        octaves = degree // len(scale_intervals)
        rem = degree % len(scale_intervals)
        return root_pitch + (octaves * 12) + scale_intervals[rem]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Attenuate to avoid clipping

    # === Step 3: Define the "Rule of 3" Structural Progression ===
    # Format: Tuple of (Bar Index, Diatonic Chord Root Degree)
    # Degrees are 0-indexed (0=I, 4=V, 5=vi, 3=IV, 1=ii)
    progression = [
        # Iteration 1: Establish the pattern (Bars 1-4)
        (0, 0), (1, 4), (2, 5), (3, 3),
        
        # Iteration 2: Reinforce the pattern verbatim (Bars 5-8)
        (4, 0), (5, 4), (6, 5), (7, 3),
        
        # Iteration 3: "Rule of 3" Variation (Bars 9-12)
        # Starts the exact same way for 2 bars, then subverts expectation!
        (8, 0), (9, 4), (10, 1), (11, 4) 
    ]

    total_bars = 12
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars

    # Create MIDI Item
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def add_midi_note(start_beat, length_beats, pitch, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 4: Populate Notes Algorithmically ===
    note_count = 0
    for bar, root_deg in progression:
        start_b = bar * beats_per_bar
        
        # 1. Bass Note (1 Octave down, whole note)
        add_midi_note(start_b, 4.0, get_pitch(root_deg - 7), velocity_base + 10)
        note_count += 1
        
        # 2. Block Chords (Root position triad, whole note)
        add_midi_note(start_b, 4.0, get_pitch(root_deg), velocity_base - 10)
        add_midi_note(start_b, 4.0, get_pitch(root_deg + 2), velocity_base - 10)
        add_midi_note(start_b, 4.0, get_pitch(root_deg + 4), velocity_base - 10)
        note_count += 3
        
        # 3. Motif Melody (1 Octave up to avoid masking)
        # Rhythmic motif: Beat 1 (1/4 note), Beat 2 (1/4 note), Beat 3 (1/2 note)
        mel_root = root_deg + 7 
        add_midi_note(start_b + 0.0, 1.0, get_pitch(mel_root), velocity_base)
        add_midi_note(start_b + 1.0, 1.0, get_pitch(mel_root + 1), velocity_base)
        add_midi_note(start_b + 2.0, 2.0, get_pitch(mel_root + 2), velocity_base + 5)
        note_count += 3

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' demonstrating Rule of 3. Generated {note_count} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
