def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Fixed to 12 to demonstrate the 3x4-bar rule
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar progression demonstrating the 'Rule of 3' (AA' form) in REAPER.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Must be 12 to demonstrate the rule correctly. Overrides to 12.
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
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Normalize inputs
    key = key.capitalize() if key.capitalize() in NOTE_MAP else "C"
    scale = scale.lower() if scale.lower() in SCALES else "major"
    scale_intervals = SCALES[scale]
    root_midi = 48 + NOTE_MAP[key] # Start around C3

    # Helper function to get MIDI pitch from diatonic scale degree
    def get_pitch(degree, octave_offset=0):
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_midi + (octave_offset * 12) + (octave_shift * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = 12 # 3 iterations of 4 bars
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # RPR_MIDI_InsertNote takes: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
    # We will use REAPER's time-to-PPQ function
    
    # Define the 4-bar harmonic progression (0-indexed scale degrees)
    # Standard: I (0) - V (4) - vi (5) - IV (3)
    # Variation: I (0) - V (4) - ii (1) - V (4)
    progression_standard = [0, 4, 5, 3]
    progression_variation = [0, 4, 1, 4]

    note_count = 0
    
    # Generate 3 iterations (Rule of 3)
    for iteration in range(3):
        # Iteration 0 and 1 use standard progression. Iteration 2 uses the variation.
        current_prog = progression_standard if iteration < 2 else progression_variation
        
        for bar_in_phrase in range(4):
            absolute_bar = (iteration * 4) + bar_in_phrase
            start_time = absolute_bar * bar_length_sec
            
            root_degree = current_prog[bar_in_phrase]
            
            # Chord Tones: Root, 3rd, 5th (diatonic)
            chord_degrees = [root_degree, root_degree + 2, root_degree + 4]
            
            # 1. Insert Chords (Hold for the whole bar)
            chord_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            chord_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + bar_length_sec * 0.95) # Slight gap
            
            for degree in chord_degrees:
                pitch = get_pitch(degree, octave_offset=0)
                RPR.RPR_MIDI_InsertNote(take, False, False, chord_start_ppq, chord_end_ppq, 0, pitch, velocity_base - 20, False)
                note_count += 1
                
            # 2. Insert Melody (To make the variation obvious)
            # Motif: Play chord 5th on beat 1, then a rhythmic variation on beat 3.
            melody_pitch_1 = get_pitch(chord_degrees[2], octave_offset=1) # 5th, one octave up
            
            mel_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            mel_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + (bar_length_sec / 4) * 1.5) # 1.5 beats
            RPR.RPR_MIDI_InsertNote(take, False, False, mel_start_ppq, mel_end_ppq, 0, melody_pitch_1, velocity_base, False)
            note_count += 1
            
            # Second melody note on Beat 3 (Time = start + 2 beats)
            # Standard iteration: goes to root of chord
            # Variation iteration (3rd time): jumps an octave higher for extra emphasis
            mel2_time = start_time + (bar_length_sec / 4) * 2
            mel2_pitch = get_pitch(chord_degrees[0], octave_offset=1 if iteration < 2 else 2)
            
            mel2_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, mel2_time)
            mel2_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + bar_length_sec * 0.9)
            RPR.RPR_MIDI_InsertNote(take, False, False, mel2_start_ppq, mel2_end_ppq, 0, mel2_pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add ReaSynth so the pattern is immediately audible
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Soften the attack and add a little release to make it sound more like a pad/keys
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.05) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.2)  # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.5)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Release

    return f"Created '{track_name}': AAB 'Rule of 3' structure with {note_count} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
