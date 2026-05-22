def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Call and Response Lead",
    bpm: int = 128,
    key: str = "A",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Call and Response Melodic Phrase with EQ variation in REAPER.
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

    if scale not in SCALES:
        scale = "minor"
    scale_array = SCALES[scale]
    
    # Base octave 4
    root_midi = 60 + NOTE_MAP.get(key, 9) # Default to A minor if not found

    def get_note(degree, octave_offset=0):
        scale_length = len(scale_array)
        oct_shift = degree // scale_length
        scale_deg = degree % scale_length
        return root_midi + ((octave_shift + octave_offset) * 12) + scale_array[scale_deg]

    # Set project tempo
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, 0, 0, bpm, 4, 4, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth (configure as pluck)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.1)  # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.1)  # Release

    # Add ReaEQ (for the "thin to full" automation)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Set Band 1 Gain low (-24dB) to act as a pseudo High-Pass when frequency is swept up
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 1, 0.0) 
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True) # Envelope for Band 1 Frequency

    # Create MIDI Item
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Phrasing Array: (scale_degree, beat_position, duration_beats, octave_offset)
    # Beats are 0 to 31 (for 8 bars)
    note_events = []

    # Bar 1-2: CALL (Unresolved, ends on 3rd)
    note_events.extend([
        (0, 0.0, 0.5, 0),  # Root
        (4, 1.5, 0.5, 0),  # 5th
        (3, 2.5, 0.5, 0),  # 4th
        (2, 3.5, 0.5, 0),  # 3rd
        (0, 4.0, 1.0, 0),  # Root
        (2, 6.0, 1.0, 0),  # 3rd (Hanging/Unresolved)
    ])

    # Bar 3-4: RESPONSE 1 (Resolved, ends on Root)
    note_events.extend([
        (0, 8.0, 0.5, 0),
        (4, 9.5, 0.5, 0),
        (3, 10.5, 0.5, 0),
        (2, 11.5, 0.5, 0),
        (-1, 12.0, 1.0, 0), # 7th degree below root
        (0, 14.0, 1.0, 0),  # Root (Resolved)
    ])

    # Bar 5-6: CALL (Repeated)
    note_events.extend([
        (0, 16.0, 0.5, 0),
        (4, 17.5, 0.5, 0),
        (3, 18.5, 0.5, 0),
        (2, 19.5, 0.5, 0),
        (0, 20.0, 1.0, 0),
        (2, 22.0, 1.0, 0),
    ])

    # Bar 7-8: RESPONSE 2 (Variation: Octave Down)
    note_events.extend([
        (0, 24.0, 0.5, -1),
        (4, 25.5, 0.5, -1),
        (3, 26.5, 0.5, -1),
        (2, 27.5, 0.5, -1),
        (-1, 28.0, 1.0, -1),
        (0, 30.0, 1.0, -1),
    ])

    # Insert notes and build EQ envelope points
    item_start = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")

    for ne in note_events:
        degree, start_beat, duration_beats, oct_offset = ne
        pitch = get_note(degree, oct_offset)
        
        start_time = item_start + (start_beat * beat_sec)
        end_time = start_time + (duration_beats * beat_sec)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)

    RPR.RPR_MIDI_Sort(take)

    # Insert EQ Automation Points (Thin vs Full)
    # Normalized frequency: 0.4 is mid-high (thin), 0.0 is very low (full)
    automation_points = [
        (0.0 * bar_length_sec, 0.4),  # Bar 1 start: Thin (Call)
        (2.0 * bar_length_sec, 0.0),  # Bar 3 start: Full (Response)
        (4.0 * bar_length_sec, 0.4),  # Bar 5 start: Thin (Call)
        (6.0 * bar_length_sec, 0.0),  # Bar 7 start: Full (Response)
    ]
    
    for pt_time, pt_val in automation_points:
        # Insert square shape points (shape=1) to instantly jump between sections
        RPR.RPR_InsertEnvelopePoint(env, pt_time, pt_val, 1, 0.0, False, True)

    RPR.RPR_Envelope_Sort(env)

    return f"Created '{track_name}' with Call/Response melody ({len(note_events)} notes) and EQ automation over {bars} bars at {bpm} BPM in {key} {scale}."
