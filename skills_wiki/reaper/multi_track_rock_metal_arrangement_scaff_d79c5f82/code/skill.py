def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RockBand",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Multi-Track Rock/Metal Arrangement Scaffold' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the creation.
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

    # Set project tempo
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, bpm, 4, 4, True)

    root_val = NOTE_MAP.get(key, 11) # Default to B
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # Determine progression based on scale flavor
    if "minor" in scale:
        progression = [0, 5, 2, 6] # i, VI, III, VII
    else:
        progression = [0, 5, 3, 4] # I, vi, IV, V

    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    def add_note(take, start_time, duration, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    def get_pitch_for_idx(idx, base_octave):
        octave_shift = idx // len(scale_intervals)
        scale_deg = idx % len(scale_intervals)
        return root_val + scale_intervals[scale_deg] + ((base_octave + octave_shift) * 12)

    def get_chord_pitches(degree, base_octave):
        return [
            get_pitch_for_idx(degree, base_octave),
            get_pitch_for_idx(degree + 2, base_octave),
            get_pitch_for_idx(degree + 4, base_octave)
        ]

    tracks_to_create = [
        {"name": f"{track_name} Drums", "type": "drums"},
        {"name": f"{track_name} Bass", "type": "bass"},
        {"name": f"{track_name} Rhythm", "type": "rhythm"},
        {"name": f"{track_name} Lead", "type": "lead"},
    ]

    total_notes = 0

    for track_info in tracks_to_create:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_info["name"], True)

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * bar_len)
        take = RPR.RPR_AddTakeToMediaItem(item)

        t_type = track_info["type"]

        for b in range(bars):
            start_of_bar = b * bar_len
            deg = progression[b % len(progression)]
            
            if t_type == "drums":
                # Driving Rock Kick
                for pos in [0.0, 2.0, 2.5]:
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.5, 36, velocity_base)
                    total_notes += 1
                # Snare
                for pos in [1.0, 3.0]:
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.5, 38, velocity_base)
                    total_notes += 1
                # 8th note Hi-hats with velocity dynamics
                for pos_idx in range(8):
                    pos = pos_idx * 0.5
                    vel = velocity_base if pos_idx % 2 == 0 else velocity_base - 20
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.25, 42, vel)
                    total_notes += 1
                # Crash on the downbeat of the loop
                if b == 0:
                    add_note(take, start_of_bar, beat_len, 49, velocity_base + 10)
                    total_notes += 1

            elif t_type == "bass":
                # Root notes, octave 2, chugging 8th notes
                root_pitch = get_pitch_for_idx(deg, 2)
                for i in range(8):
                    pos = i * 0.5
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.45, root_pitch, velocity_base)
                    total_notes += 1

            elif t_type == "rhythm":
                # Triad block chords, octave 3, chugging 8th notes
                pitches = get_chord_pitches(deg, 3)
                for i in range(8):
                    pos = i * 0.5
                    for p in pitches:
                        add_note(take, start_of_bar + pos * beat_len, beat_len * 0.4, p, velocity_base - 10)
                        total_notes += 1

            elif t_type == "lead":
                # Arpeggiated melody, octave 5, quarter notes
                pitches = get_chord_pitches(deg, 5)
                arp_pattern = [pitches[0], pitches[1], pitches[2], pitches[1]]
                for i in range(4):
                    pos = i * 1.0 
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.8, arp_pattern[i], velocity_base)
                    total_notes += 1

        RPR.RPR_MIDI_Sort(take)

    return f"Created {len(tracks_to_create)} tracks ({track_name} group) with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}."
