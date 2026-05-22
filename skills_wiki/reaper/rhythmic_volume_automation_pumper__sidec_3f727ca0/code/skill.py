def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Rhythmic Volume Automation Pumper in the current REAPER project.
    Generates a sustained synth pad and automates the track volume to 'pump' on every quarter note.

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
        Status string describing the operation.
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

    # Helper: get MIDI pitch from degree
    def get_pitch(degree, root_note, scale_intervals, octave=4):
        scale_len = len(scale_intervals)
        octave_shift = degree // scale_len
        note_in_scale = degree % scale_len
        return (octave + octave_shift + 1) * 12 + root_note + scale_intervals[note_in_scale]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more pad-like sound (lower attack, max sustain)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Attack a bit slower
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 1.0) # Sustain full
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5) # Release

    # === Step 3: Create MIDI Item for Pad Chords ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    root_val = NOTE_MAP.get(key, 0)
    scale_arr = SCALES.get(scale, SCALES["minor"])
    
    # Generate 1 long chord per bar
    progression_degrees = [0, 3, 4, 5] # e.g., i, iv, v, VI depending on scale
    
    note_count = 0
    for bar in range(bars):
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        degree = progression_degrees[bar % len(progression_degrees)]
        
        # Voicing: Root, 3rd, 5th, Octave
        chord_pitches = [
            get_pitch(degree, root_val, scale_arr, octave=3),
            get_pitch(degree + 2, root_val, scale_arr, octave=3),
            get_pitch(degree + 4, root_val, scale_arr, octave=3),
            get_pitch(degree, root_val, scale_arr, octave=4)
        ]
        
        for pitch in chord_pitches:
            # Insert notes slightly shortened to prevent overlap click
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq - 10, 0, pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Volume Automation Envelope (The Pump) ===
    # Force Volume Envelope to be visible and active
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env:
        total_beats = bars * beats_per_bar
        beat_len = 60.0 / bpm
        
        for b in range(total_beats):
            time_on_beat = b * beat_len
            time_off_beat = time_on_beat + (beat_len * 0.5)
            time_end_beat = time_on_beat + beat_len - 0.01
            
            # Shape: 5 = Bezier curve, 2 = Slow start/end. We'll use 2 for a smooth pump
            # RPR_InsertEnvelopePoint(env, time, value, shape, tension, selected, noSort)
            
            # 1. Duck exactly on the beat (Value 0.1 is roughly -20dB)
            RPR.RPR_InsertEnvelopePoint(env, time_on_beat, 0.15, 2, 0.0, False, True)
            
            # 2. Swell to full unity gain (1.0) by the off-beat
            RPR.RPR_InsertEnvelopePoint(env, time_off_beat, 1.0, 0, 0.0, False, True)
            
            # 3. Hold unity gain until the next beat triggers
            RPR.RPR_InsertEnvelopePoint(env, time_end_beat, 1.0, 5, 0.0, False, True)
            
        RPR.RPR_Envelope_SortRect(env)
        env_status = "Volume envelope successfully automated."
    else:
        env_status = "Warning: Could not retrieve Volume envelope."

    return f"Created '{track_name}' with {note_count} pad notes over {bars} bars at {bpm} BPM. {env_status}"
