def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Motif",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar 'Rule of 3' (A-A-A') melodic & harmonic sequence in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Target length (overridden to a multiple of 3 to enforce the rule).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
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

    # === Phrase Structure Enforcement ===
    # The Rule of 3 demands 3 structural blocks. 
    # We use 4-bar blocks by default (12 bars total).
    phrase_length = 4 if bars < 24 else 8
    total_bars = phrase_length * 3
    
    root_midi = NOTE_MAP.get(key, 0) + 12 # Set octave 0 root
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(scale_intervals)

    # Choose progression based on tonality
    if "minor" in scale.lower() or "dorian" in scale.lower() or "blues" in scale.lower():
        prog_roots = [0, 5, 2, 6]  # i - VI - III - VII
        turnaround = [3, 4]        # iv - v
    else:
        prog_roots = [0, 4, 5, 3]  # I - V - vi - IV
        turnaround = [1, 4]        # ii - V

    # Helper: Convert scale degree + octave into an absolute MIDI pitch
    def get_pitch(degree: int, octave: int) -> int:
        oct_offset = (degree // scale_len) + octave
        sc_deg = degree % scale_len
        pitch = root_midi + scale_intervals[sc_deg] + (oct_offset * 12)
        return max(0, min(127, int(pitch)))

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (total_bars * beats_per_bar * 60.0) / bpm
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper: Insert a MIDI note
    def insert_note(pitch, start_beat, dur_beats, vel):
        p = max(0, min(127, int(pitch)))
        v = max(1, min(127, int(vel)))
        st = (start_beat * 60.0) / bpm
        et = ((start_beat + dur_beats) * 60.0) / bpm
        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, st)
        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, et)
        RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, p, v, True)

    # === Step 3: Generate the A-A-A' Pattern ===
    note_count = 0
    for phrase in range(3):
        is_variation = (phrase == 2) # The 3rd time breaks the pattern
        start_beat_phrase = phrase * phrase_length * beats_per_bar

        for bar in range(phrase_length):
            bar_start_beat = start_beat_phrase + (bar * beats_per_bar)

            # Determine chord logic: 3rd phrase goes somewhere different halfway through
            if is_variation and bar >= phrase_length // 2:
                root_deg = turnaround[(bar - phrase_length//2) % len(turnaround)]
                is_turnaround = True
            else:
                root_deg = prog_roots[bar % len(prog_roots)]
                is_turnaround = False

            # 1. Insert Chords (Triads, held for whole bar)
            for offset in [0, 2, 4]:
                insert_note(get_pitch(root_deg + offset, 4), bar_start_beat, 4.0, velocity_base - 20)
                note_count += 1

            # 2. Insert Melody (Octave 5)
            if not is_turnaround:
                # Familiar rhythmic motif: Dotted Quarter, Eighth, Half
                insert_note(get_pitch(root_deg + 7, 5), bar_start_beat, 1.5, velocity_base)
                insert_note(get_pitch(root_deg + 8, 5), bar_start_beat + 1.5, 0.5, velocity_base - 10)
                insert_note(get_pitch(root_deg + 6, 5), bar_start_beat + 2.0, 2.0, velocity_base - 5)
                note_count += 3
            else:
                if bar == phrase_length - 2:
                    # Variation: Walk-up to build tension
                    for i in range(4):
                        # Increase velocity to swell into the resolution
                        insert_note(get_pitch(root_deg + 7 + i, 5), bar_start_beat + i, 1.0, velocity_base + (i*5))
                        note_count += 1
                else:
                    # Variation: Resolution hold
                    insert_note(get_pitch(root_deg + 7, 5), bar_start_beat, 4.0, velocity_base + 10)
                    note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (ReaSynth Pluck) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak amplitude envelope for a plucky/piano-like clarity
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.02) # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.2)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.5)  # Release

    return f"Created '{track_name}' Rule of 3 Sequence: {note_count} notes over {total_bars} bars in {key} {scale} at {bpm} BPM."
