def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Motif",
    bpm: int = 110,
    key: str = "A",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar compositional structure demonstrating the "Rule of 3" (A-A-B variation).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Overridden to 12 internally to accommodate the 3-phrase structure.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # Setup core parameters
    root_midi = NOTE_MAP.get(key, 9) + 48 # Base octave (e.g., A3 = 57)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    actual_bars = 12 # Enforce 12 bars to fit 3 phrases of 4 bars
    beats_per_bar = 4
    
    # Helper to convert scale degrees (can be negative or >7) to absolute MIDI pitch
    def get_pitch(degree):
        octave = degree // len(scale_intervals)
        rem = degree % len(scale_intervals)
        pitch = root_midi + scale_intervals[rem] + (octave * 12)
        return max(0, min(127, pitch))

    # === Define the Rule of 3 Composition ===
    # Phrase A: The loop you want to establish
    chords_A = [
        [-7, -5, -3],  # i   (Minor: Am)
        [-9, -7, -5],  # VI  (Minor: F)
        [-5, -3, -1],  # III (Minor: C)
        [-8, -6, -4]   # VII (Minor: G)
    ]
    melody_A = [
        # (beat_offset, scale_degree, duration_in_beats)
        [(0.0, 7, 1.0), (1.0, 9, 1.0), (2.0, 7, 1.0), (3.0, 4, 1.0)],
        [(0.0, 5, 1.0), (1.0, 7, 1.0), (2.0, 5, 1.0), (3.0, 2, 1.0)],
        [(0.0, 9, 1.0), (1.0, 11, 1.0), (2.0, 9, 1.0), (3.0, 6, 1.0)],
        [(0.0, 6, 1.0), (1.0, 8, 1.0), (2.0, 6, 1.0), (3.0, 4, 1.0)]
    ]
    
    # Phrase B: The variation (starts same, ends completely differently)
    chords_B = [
        [-7, -5, -3],  # i   (Minor: Am) - Starts the same
        [-9, -7, -5],  # VI  (Minor: F)  - Same
        [-4, -2, 0],   # iv  (Minor: Dm) - Variation! Creates a turnaround
        [-3, -1, 1]    # v   (Minor: Em) - Variation! Resolves back to start
    ]
    melody_B = [
        [(0.0, 7, 1.0), (1.0, 9, 1.0), (2.0, 7, 1.0), (3.0, 4, 1.0)], # Same
        [(0.0, 5, 1.0), (1.0, 7, 1.0), (2.0, 5, 1.0), (3.0, 2, 1.0)], # Same
        [(0.0, 10, 1.0), (1.0, 12, 1.0), (2.0, 14, 1.0), (3.0, 12, 1.0)], # Climbs up!
        [(0.0, 11, 1.0), (1.0, 13, 1.0), (2.0, 15, 1.0), (3.0, 18, 1.0)]  # Climax!
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    item_length_sec = (60.0 / bpm) * beats_per_bar * actual_bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Generate the 3 phrases
    total_notes_added = 0
    for phrase_idx in range(3):
        # Apply the Rule of 3: Repetition 1 (A), Repetition 2 (A), Variation (B)
        chords = chords_A if phrase_idx < 2 else chords_B
        melody = melody_A if phrase_idx < 2 else melody_B
        
        phrase_start_beat = phrase_idx * 4 * beats_per_bar
        
        for bar_idx in range(4):
            bar_start_beat = phrase_start_beat + bar_idx * beats_per_bar
            
            # 1. Insert Block Chords
            for deg in chords[bar_idx]:
                pitch = get_pitch(deg)
                start_sec = bar_start_beat * (60.0 / bpm)
                end_sec = (bar_start_beat + 4.0) * (60.0 / bpm)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                # Play chords at a lower velocity to let melody shine
                chord_vel = max(1, velocity_base - 30)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, chord_vel, False)
                total_notes_added += 1
                
            # 2. Insert Melody Motif
            for (beat_offset, deg, length) in melody[bar_idx]:
                pitch = get_pitch(deg)
                start_sec = (bar_start_beat + beat_offset) * (60.0 / bpm)
                end_sec = (bar_start_beat + beat_offset + length) * (60.0 / bpm)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
                total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain for a Mellow Synth Piano Tone ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Dial in a plucky, piano-like shape using ReaSynth params
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.4)  # Vol
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.01) # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.3)  # Decay 
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.3)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.4)  # Release
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.0)  # Square Mix
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.2)  # Saw Mix (Adds a little bite)
    RPR.RPR_TrackFX_SetParam(track, 0, 8, 0.8)  # Triangle Mix (Soft core tone)

    return f"Created '{track_name}' containing an A-A-B Rule of 3 arrangement ({total_notes_added} notes over 12 bars in {key} {scale} at {bpm} BPM)."
