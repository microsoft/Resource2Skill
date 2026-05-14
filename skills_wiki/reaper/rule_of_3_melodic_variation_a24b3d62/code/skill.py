def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule_of_3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a "Rule of 3" Melodic Variation structure in the current REAPER project.
    Generates a repeating 4-bar phrase that deliberately deviates on its 3rd iteration
    to retain listener interest.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, etc.).
        scale: "major" or "minor".
        bars: Total number of bars to generate (will loop the 12-bar macro structure).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_offset = NOTE_MAP.get(key.capitalize(), 0)
    is_minor = "minor" in scale.lower()

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Step 2: Create Additive Tracks
    def add_track(name):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        return track

    chords_track = add_track(f"{track_name}_Chords")
    melody_track = add_track(f"{track_name}_Melody")

    # Step 3: Create Media Items
    beats_per_bar = 4
    item_length = (60.0 / bpm) * beats_per_bar * bars
    
    c_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(c_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(c_item, "D_LENGTH", item_length)
    c_take = RPR.RPR_AddTakeToMediaItem(c_item)
    
    m_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(m_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(m_item, "D_LENGTH", item_length)
    m_take = RPR.RPR_AddTakeToMediaItem(m_item)

    def add_note(take, start_qn, end_qn, pitch, vel):
        v = max(1, min(127, int(vel)))
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), v, False)

    # Define Harmonic Structure (12-bar cycle)
    if is_minor:
        chords_dict = {
            "IV": [41, 44, 48, 53, 56],      # Fm (iv)
            "I": [36, 43, 48, 51, 55],       # Cm (i)
            "V": [43, 50, 55, 58, 62],       # Gm (v)
            "vi": [44, 51, 56, 60, 63],      # Ab Major (VI)
            "bVII": [49, 56, 61, 65, 68],    # Db Major (bII) - Deviation
            "VI": [50, 57, 62, 66, 69]       # D Major - Deviation
        }
        melody_dict = [
            # A & A repeated phrases (iv-i-v-VI)
            (0, 1, 68), (1, 1.5, 67), (1.5, 2, 65), (2, 4, 72),
            (4, 5.5, 67), (5.5, 6, 63), (6, 8, 60),
            (8, 9, 70), (9, 9.5, 68), (9.5, 10, 67), (10, 12, 74),
            (12, 16, 72),
            # A' phrase deviation (iv-i-bII-V/v)
            (32, 33, 68), (33, 33.5, 67), (33.5, 34, 65), (34, 36, 72),
            (36, 37.5, 67), (37.5, 38, 63), (38, 40, 60),
            (40, 41, 73), (41, 41.5, 72), (41.5, 42, 68), (42, 44, 77), 
            (44, 48, 74),                                        
        ]
    else:
        chords_dict = {
            "IV": [41, 45, 48, 53, 57],      # F Major
            "I": [36, 43, 48, 52, 55],       # C Major
            "V": [43, 50, 55, 59, 62],       # G Major
            "vi": [45, 52, 57, 60, 64],      # A Minor
            "bVII": [46, 53, 58, 62, 65],    # Bb Major - Borrowed Deviation
            "VI": [45, 52, 57, 61, 64]       # A Major - Secondary Dominant Deviation
        }
        melody_dict = [
            # A & A repeated phrases
            (0, 1, 69), (1, 1.5, 67), (1.5, 2, 65), (2, 4, 72),
            (4, 5.5, 67), (5.5, 6, 64), (6, 8, 60),
            (8, 9, 71), (9, 9.5, 69), (9.5, 10, 67), (10, 12, 74),
            (12, 16, 72),
            # A' phrase deviation
            (32, 33, 69), (33, 33.5, 67), (33.5, 34, 65), (34, 36, 72),
            (36, 37.5, 67), (37.5, 38, 64), (38, 40, 60),
            (40, 41, 74), (41, 41.5, 72), (41.5, 42, 70), (42, 44, 77),
            (44, 48, 76),
        ]

    # Duplicate phrase 'A' at offset 16 to fulfill A-A-A'
    full_melody = melody_dict[:12] + [(s+16, e+16, p) for s, e, p in melody_dict[:12]] + melody_dict[12:]

    base_chord_seq = [
        ("IV", 0, 4), ("I", 4, 8), ("V", 8, 12), ("vi", 12, 16),
        ("IV", 16, 20), ("I", 20, 24), ("V", 24, 28), ("vi", 28, 32),
        ("IV", 32, 36), ("I", 36, 40), ("bVII", 40, 44), ("VI", 44, 48)
    ]

    # Step 4: Populate MIDI (Looping over 'bars' parameter if extended)
    for b in range(bars):
        bar_in_macro = b % 12
        # Determine chord
        for c_name, start, end in base_chord_seq:
            if start <= bar_in_macro * 4 < end:
                for p in chords_dict[c_name]:
                    add_note(c_take, b * 4, (b + 1) * 4, p + root_offset, velocity_base - 15)
                break

    for cycle in range((bars + 11) // 12):
        offset = cycle * 48
        for start, end, p in full_melody:
            real_start = start + offset
            real_end = end + offset
            if real_start < bars * 4:
                real_end = min(real_end, bars * 4)
                add_note(m_take, real_start, real_end, p + root_offset, velocity_base + 10)

    RPR.RPR_MIDI_Sort(c_take)
    RPR.RPR_MIDI_Sort(m_take)

    # Step 5: Assign Synths and Mix Levels
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "D_VOL", 0.4) 

    RPR.RPR_TrackFX_AddByName(melody_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaDelay", False, -1)
    RPR.RPR_SetMediaTrackInfo_Value(melody_track, "D_VOL", 0.8)

    return f"Created 'Rule of 3' structure across {bars} bars at {bpm} BPM in key {key} {scale}."
