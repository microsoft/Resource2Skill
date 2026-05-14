def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "EDM Chords",
    bpm: int = 128,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM/Pop Layered Triad Progression with inversions and sidechain pumping.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (128 is EDM standard).
        key: Root note (C, C#, D, etc.).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). EDM usually uses high uniform velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if scale not in SCALES:
        scale = "major"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Progression: I - V - vi - IV (1, 5, 6, 4) - Standard Pop/EDM progression
    progression = [1, 5, 6, 4]
    
    root_midi = NOTE_MAP[key] + 60 # Center around Middle C (C4 = 60)
    scale_intervals = SCALES[scale]

    def get_inverted_chord(degree):
        """Calculates a diatonic triad and applies voice-leading inversions."""
        idx = degree - 1
        notes = []
        # Build 1st, 3rd, and 5th of the chord
        for offset in [0, 2, 4]:
            scale_idx = idx + offset
            octave = scale_idx // len(scale_intervals)
            interval = scale_intervals[scale_idx % len(scale_intervals)]
            n = root_midi + interval + (octave * 12)

            # Invert notes to keep them tightly clustered around the root_midi anchor
            while n > root_midi + 7:
                n -= 12
            while n < root_midi - 5:
                n += 12
            notes.append(n)
        return notes

    # Generate chord sequence
    chords = []
    for i in range(bars):
        chord_degree = progression[i % len(progression)]
        chords.append(get_inverted_chord(chord_degree))

    # Helper function to create a track with chords
    def build_layer(name: str, add_pumping: bool):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Add native synth
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create 4-bar MIDI Item
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_length_sec * bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        ppq_per_quarter = 960
        
        # Insert Block Chords
        for i, chord in enumerate(chords):
            start_qn = i * beats_per_bar
            end_qn = start_qn + beats_per_bar
            
            start_ppq = int(start_qn * ppq_per_quarter)
            end_ppq = int(end_qn * ppq_per_quarter)
            
            for pitch in chord:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

        # Add sidechain pumping effect via CC11 Expression automation if requested
        if add_pumping:
            for qn in range(bars * beats_per_bar):
                # Duck at the start of the beat
                RPR.RPR_MIDI_InsertCC(take, False, False, int(qn * ppq_per_quarter), 0xB0, 0, 11, 30)
                # Swell up 1/8th note in
                RPR.RPR_MIDI_InsertCC(take, False, False, int((qn + 0.25) * ppq_per_quarter), 0xB0, 0, 11, 80)
                # Hit max volume 1/4 note in (the offbeat)
                RPR.RPR_MIDI_InsertCC(take, False, False, int((qn + 0.5) * ppq_per_quarter), 0xB0, 0, 11, 127)

        RPR.RPR_MIDI_Sort(take)
        return track

    # Build the layers
    build_layer(f"{track_name} Piano", add_pumping=False)
    build_layer(f"{track_name} Synth (Pump)", add_pumping=True)

    return f"Created layered inverted chords over {bars} bars at {bpm} BPM in {key} {scale} with pumping sidechain simulation."
