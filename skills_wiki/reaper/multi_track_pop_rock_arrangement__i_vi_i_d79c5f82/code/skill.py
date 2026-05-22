def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Multi_Track_Loop",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-part pop-rock arrangement (Drums, Bass, Chords, Lead) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
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

    base_midi = NOTE_MAP.get(key.capitalize(), 11)  # Default to B
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Define progression based on scale type
    if scale.lower() == "major":
        # I - vi - IV - V
        prog_degrees = [0, 5, 3, 4]
    else:
        # i - VI - III - VII
        prog_degrees = [0, 5, 2, 6]

    def get_diatonic_pitch(degree, octave):
        """Calculates exact MIDI pitch for a given diatonic scale degree and octave."""
        octave_shift = degree // len(scale_intervals)
        note_idx = degree % len(scale_intervals)
        return base_midi + scale_intervals[note_idx] + (12 * (octave + octave_shift))

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    total_len_sec = bars * beats_per_bar * beat_len_sec

    # Track setups (Name, Color RGB, Needs Synth)
    track_definitions = [
        (f"{track_name}_Drums", (200, 50, 50), False),
        (f"{track_name}_Bass", (255, 128, 0), True),     # Orange
        (f"{track_name}_Chords", (128, 0, 128), True),   # Purple
        (f"{track_name}_Lead", (0, 128, 255), True)      # Blue
    ]

    created_takes = {}

    # Create Tracks & Items
    for i, (t_name, color, needs_synth) in enumerate(track_definitions):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Set Name and Color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_name, True)
        native_color = color[0] + (color[1] * 256) + (color[2] * 65536) | 0x1000000
        RPR.RPR_SetTrackColor(track, native_color)
        
        # Add ReaSynth if needed
        if needs_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        created_takes[t_name] = take

    # === Note Insertion Logic ===
    
    def insert_note(take, start_beat, end_beat, pitch, vel):
        """Helper to insert a note via beats."""
        start_time = start_beat * beat_len_sec
        end_time = end_beat * beat_len_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        current_degree = prog_degrees[bar % len(prog_degrees)]
        
        # Get Diatonic Triad Tones
        root_pitch_bass = get_diatonic_pitch(current_degree, 2)
        root_pitch_chord = get_diatonic_pitch(current_degree, 3)
        third_pitch_chord = get_diatonic_pitch(current_degree + 2, 3)
        fifth_pitch_chord = get_diatonic_pitch(current_degree + 4, 3)
        octave_pitch_lead = get_diatonic_pitch(current_degree + 7, 4)

        # 1. DRUMS (Standard Rock Beat)
        take_drums = created_takes[f"{track_name}_Drums"]
        kick, snare, hat = 36, 38, 42
        # Kicks on 0 and 2.5
        insert_note(take_drums, bar_start_beat + 0.0, bar_start_beat + 0.25, kick, velocity_base)
        insert_note(take_drums, bar_start_beat + 2.5, bar_start_beat + 2.75, kick, velocity_base)
        # Snares on 1 and 3
        insert_note(take_drums, bar_start_beat + 1.0, bar_start_beat + 1.25, snare, velocity_base)
        insert_note(take_drums, bar_start_beat + 3.0, bar_start_beat + 3.25, snare, velocity_base)
        # Hats every 8th note
        for hat_i in range(8):
            insert_note(take_drums, bar_start_beat + (hat_i * 0.5), bar_start_beat + (hat_i * 0.5) + 0.25, hat, velocity_base - 20)

        # 2. BASS (Driving 8th notes on the root)
        take_bass = created_takes[f"{track_name}_Bass"]
        for b_i in range(8):
            insert_note(take_bass, bar_start_beat + (b_i * 0.5), bar_start_beat + (b_i * 0.5) + 0.45, root_pitch_bass, velocity_base)

        # 3. CHORDS (Whole notes)
        take_chords = created_takes[f"{track_name}_Chords"]
        insert_note(take_chords, bar_start_beat, bar_start_beat + 4.0, root_pitch_chord, velocity_base - 20)
        insert_note(take_chords, bar_start_beat, bar_start_beat + 4.0, third_pitch_chord, velocity_base - 25)
        insert_note(take_chords, bar_start_beat, bar_start_beat + 4.0, fifth_pitch_chord, velocity_base - 25)

        # 4. LEAD (8th note arpeggios cycling Root -> Third -> Fifth -> Octave)
        take_lead = created_takes[f"{track_name}_Lead"]
        arp_pitches = [root_pitch_chord + 12, third_pitch_chord + 12, fifth_pitch_chord + 12, octave_pitch_lead]
        for l_i in range(8):
            p = arp_pitches[l_i % 4]
            insert_note(take_lead, bar_start_beat + (l_i * 0.5), bar_start_beat + (l_i * 0.5) + 0.25, p, velocity_base - 10)

    # Finalize MIDI sorts
    for take in created_takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track pop-rock arrangement over {bars} bars in {key} {scale} at {bpm} BPM."
