def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, 
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 12-bar AAB "Rule of 3" chord and melody pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Overridden internally to 12 to explicitly demonstrate the AAB form.
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
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 48 # Octave 4 base

    # Helper function to get MIDI pitch by diatonic scale degree
    def get_pitch(degree, octave_offset=0):
        octave = (degree // scale_len) + octave_offset
        idx = degree % scale_len
        return root_pitch + scale_intervals[idx] + (octave * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Synth and FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.4) # Saw blend
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.5) # Pulse width
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.02) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5) # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3) # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.8) # Release

    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, -12.0) # Wet (dB approx)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 1, 0.25) # Delay length in musical notation (1/4 note)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # Force 12 bars for AAB form
    item_length = (60.0 / bpm) * beats_per_bar * total_bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Progression mapping: 
    # A (Bars 1-4):  IV, V, I, vi  -> Degrees 3, 4, 0, 5
    # A (Bars 5-8):  IV, V, I, vi  -> Degrees 3, 4, 0, 5
    # B (Bars 9-12): IV, V, ii, V  -> Degrees 3, 4, 1, 4 (Diverges in the second half)
    progression_degrees = [3, 4, 0, 5, 3, 4, 0, 5, 3, 4, 1, 4]

    RPR.RPR_MIDI_DisableSort(take)

    for bar_idx, chord_deg in enumerate(progression_degrees):
        bar_start_qn = bar_idx * 4.0

        # 1. Base Chords (Whole notes, Octave 3)
        chord_pitches = [get_pitch(chord_deg, -1), get_pitch(chord_deg + 2, -1), get_pitch(chord_deg + 4, -1)]
        for p in chord_pitches:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + 4.0)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, velocity_base - 20, False)

        # 2. Melody Lines (Octave 5)
        # Identify if we are in Motif A or the expected start of Motif B
        if bar_idx < 10:
            # Standard repeated motif melody: Root -> 3rd -> 5th
            mel_pitches = [get_pitch(chord_deg, 1), get_pitch(chord_deg + 2, 1), get_pitch(chord_deg + 4, 1)]
            timings = [(0.0, 1.5), (1.5, 2.0), (2.0, 3.0)] # (start_beat, end_beat)
            for i, (st, en) in enumerate(timings):
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + st)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + en)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, mel_pitches[i], velocity_base, False)
        else:
            # The "Surprise": Divergent melody for the end of Motif B
            if bar_idx == 10: # ii chord
                # Faster ascending arpeggio
                mel_pitches = [
                    get_pitch(chord_deg, 0),
                    get_pitch(chord_deg + 2, 0),
                    get_pitch(chord_deg + 4, 0),
                    get_pitch(chord_deg, 1),
                    get_pitch(chord_deg + 2, 1)
                ]
                timings = [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 4.0)]
                for i, (st, en) in enumerate(timings):
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + st)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + en)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, mel_pitches[i], velocity_base + 10, False)
            elif bar_idx == 11: # V chord
                # Powerful resolving long note
                mel_pitch = get_pitch(chord_deg, 1)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + 4.0)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, mel_pitch, velocity_base + 15, False)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' featuring a 12-bar AAB 'Rule of 3' Form at {bpm} BPM in {key} {scale}"
