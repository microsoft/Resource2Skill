def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Subtractive Drop",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an 8-bar arrangement demonstrating the "Subtractive Drop" transition.
    Features an automated filter sweep building up to the halfway mark, 
    followed by a drop where the kick drum is deliberately muted for maximum impact.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }

    # === Timing Calculations ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_length = bars * bar_len
    
    # Calculate the structural boundary (The "Drop")
    drop_bar = bars // 2
    sweep_start_time = (drop_bar - 1) * bar_len
    drop_time = drop_bar * bar_len

    # === Track 1: Chords with Filter Sweep Automation ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name} - Chords", True)

    # Add Synths and EQ for the transition
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaEQ", False, -1)

    # In ReaEQ, Band 4 (High Shelf) parameters: 9 is Freq, 10 is Gain.
    # Pulling gain to minimum to act as a low-pass filter
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, eq_idx, 10, 0.0) 

    # Automate the Frequency (Param 9)
    env = RPR.RPR_GetFXEnvelope(chord_track, eq_idx, 9, True)
    
    # Insert envelope points for the transition "Sawtooth" shape
    # 1. Wide open at the start
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0.0, False, True)
    # 2. Stay wide open until 1 bar before the drop
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time, 1.0, 0, 0.0, False, True)
    # 3. Sweep down rapidly to muffle the sound right before the drop
    RPR.RPR_InsertEnvelopePoint(env, drop_time - 0.05, 0.15, 0, 0.0, False, True)
    # 4. Snap wide open exactly on the drop
    RPR.RPR_InsertEnvelopePoint(env, drop_time, 1.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    # Create MIDI Item for Chords
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_length)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    # Generate chord progression
    root_val = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Simple i - VI - III - VII progression logic mapped to bars
    progression_degrees = [0, 5, 2, 4] 
    
    for bar in range(bars):
        degree = progression_degrees[bar % 4]
        # Build a basic triad
        chord_notes = [
            root_val + scale_intervals[degree % len(scale_intervals)] + (12 * (degree // len(scale_intervals))),
            root_val + scale_intervals[(degree + 2) % len(scale_intervals)] + (12 * ((degree + 2) // len(scale_intervals))),
            root_val + scale_intervals[(degree + 4) % len(scale_intervals)] + (12 * ((degree + 4) // len(scale_intervals)))
        ]
        
        start_pos = bar * bar_len
        end_pos = start_pos + bar_len
        
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_pos, end_pos, 0, note, velocity_base - 20, True)

    RPR.RPR_MIDI_Sort(chord_take)

    # === Track 2: Drums with Subtractive Arrangement ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    GM_KICK = 36
    GM_SNARE = 38
    GM_CRASH = 49

    for beat in range(bars * beats_per_bar):
        pos = beat * beat_len
        is_drop_bar = (beat >= drop_bar * beats_per_bar) and (beat < (drop_bar + 1) * beats_per_bar)
        
        # 1. KICK LOGIC (Hits on beats 1 and 3)
        if beat % 2 == 0:
            # THE CORE SKILL: "Deleting things is adding things."
            # Mute the kick drum for the first two beats of the drop section.
            skip_kick = is_drop_bar and (beat % beats_per_bar < 2)
            
            if not skip_kick:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, pos, pos + beat_len*0.25, 0, GM_KICK, velocity_base, True)
                
        # 2. SNARE LOGIC (Hits on beats 2 and 4)
        if beat % 2 == 1:
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, pos, pos + beat_len*0.25, 0, GM_SNARE, velocity_base, True)

        # 3. CRASH CYMBAL (Marks the drop boundary)
        if beat == drop_bar * beats_per_bar:
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, pos, pos + bar_len, 0, GM_CRASH, velocity_base + 10, True)

    RPR.RPR_MIDI_Sort(drum_take)

    return f"Created subtractive transition at Bar {drop_bar + 1} over a {bars}-bar arrangement at {bpm} BPM."
