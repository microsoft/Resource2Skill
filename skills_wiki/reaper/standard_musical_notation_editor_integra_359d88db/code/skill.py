def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano (Notation Demo)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Grand Staff Piano arrangement and open it in REAPER's Musical Notation View.

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

    root_pitch = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Step 1: Set Tempo & Environment ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    # Unselect all items cleanly so our new item is the only one selected
    RPR.RPR_Main_OnCommand(40289, 0) 

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    RPR.RPR_SetMediaItemSelected(item, True) # Mark for Editor opening

    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to compute precise pitches diatonically
    def get_pitch_in_scale(degree, octave):
        scale_len = len(scale_intervals)
        octave_shift = (degree // scale_len) + octave
        note_idx = degree % scale_len
        # +1 to octave_shift because in standard REAPER MIDI, C4 (60) is octave_shift=4+1=5*12=60
        pitch = ((octave_shift + 1) * 12) + root_pitch + scale_intervals[note_idx]
        return max(0, min(127, pitch))

    # Progression template: I - V - vi - IV (degrees: 0, 4, 5, 3)
    progression = [
        {"bass": (0, 2), "chord": [(0, 4), (2, 4), (4, 4)]},
        {"bass": (4, 1), "chord": [(4, 3), (6, 3), (8, 3)]},
        {"bass": (5, 1), "chord": [(5, 3), (7, 3), (9, 3)]},
        {"bass": (3, 1), "chord": [(3, 3), (5, 3), (7, 3)]},
    ]

    total_notes_inserted = 0

    # Programmatic Note Insertion
    for b in range(bars):
        chord_data = progression[b % len(progression)]
        bar_start_qn = b * beats_per_bar

        # Bass Note (Left Hand - Whole Note)
        bass_degree, bass_octave = chord_data["bass"]
        bass_pitch = get_pitch_in_scale(bass_degree, bass_octave)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + 4)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, False)
        total_notes_inserted += 1

        # Right Hand Syncopated Chords (Quarter notes)
        rhythm_offsets = [0.0, 1.5, 3.0] 
        durations = [1.0, 1.0, 1.0]

        for i, offset in enumerate(rhythm_offsets):
            note_start_qn = bar_start_qn + offset
            note_end_qn = note_start_qn + durations[i]

            chord_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, note_start_qn)
            chord_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, note_end_qn)

            for degree, octave in chord_data["chord"]:
                pitch = get_pitch_in_scale(degree, octave)
                RPR.RPR_MIDI_InsertNote(take, False, False, chord_start_ppq, chord_end_ppq, 0, pitch, velocity_base - 10, False)
                total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Piano Tone) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.4)  # Release

    # === Step 5: Open in Musical Notation View ===
    # 40153: Item: Open in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Target the newly opened MIDI editor
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        # 40954: View: Mode: musical notation
        RPR.RPR_MIDIEditor_OnCommand(editor, 40954)

    return f"Created '{track_name}' with {total_notes_inserted} notes over {bars} bars at {bpm} BPM, and switched to Notation View."
