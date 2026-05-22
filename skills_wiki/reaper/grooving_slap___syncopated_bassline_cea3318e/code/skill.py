def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Grooving Bassline",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a highly syncopated, humanized bassline with octave slaps and diatonic walk-ups.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the created pattern.
    """
    import random
    import reaper_python as RPR

    # --- Music Theory Lookups ---
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    
    # Establish a bass octave (E1 is MIDI 28. Let's aim for the 24-35 range)
    base_midi = 24 + root_val
    if base_midi < 28: 
        base_midi += 12

    def get_pitch(degree):
        """Returns MIDI pitch for a given scale degree (0-indexed)."""
        octave_shift = degree // len(scale_intervals)
        rem = degree % len(scale_intervals)
        return base_midi + (octave_shift * 12) + scale_intervals[rem]

    # --- Step 1: Set Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Step 2: Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Step 3: Configure ReaSynth for Bass Tone ---
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 0: Volume (-6dB roughly)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)
    # Param 3: Square wave mix (add harmonics)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.7)
    # Param 4: Saw wave mix (add bite)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)

    # --- Step 4: Create MIDI Item ---
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to insert humanized MIDI notes
    note_count = 0
    def add_note(start_beat, length_beats, pitch, vel):
        nonlocal note_count
        # Humanization: random offset between -15ms and +15ms
        human_offset = random.uniform(-0.015, 0.015)
        
        start_time = (start_beat * beat_len_sec) + human_offset
        # Prevent negative start times on the very first note
        if start_time < 0: 
            start_time = 0.0
            
        end_time = start_time + (length_beats * beat_len_sec)
        
        # Add slight velocity humanization
        vel = max(1, min(127, int(vel + random.uniform(-8, 8))))
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, False)
        note_count += 1

    # --- Step 5: Generate the Grooving Bass Pattern ---
    # Progression: I - vi - IV - V (Scale degrees: 0, 5, 3, 4)
    progression = [0, 5, 3, 4]
    
    for b in range(bars):
        bar_start_beat = b * 4
        
        curr_deg = progression[b % len(progression)]
        next_deg = progression[(b + 1) % len(progression)]
        
        curr_root = get_pitch(curr_deg)
        next_root = get_pitch(next_deg)
        octave_slap = curr_root + 12

        # 1. Downbeat (Solid root foundation)
        # Position: 1.1 | Length: 1/8 | Velocity: 105
        add_note(bar_start_beat + 0.0, 0.5, curr_root, velocity_base + 5)
        
        # 2. Syncopated Split (The "a" of beat 1)
        # Position: 1.4.5 (16th before beat 2) | Length: 1/16 | Velocity: 85
        add_note(bar_start_beat + 0.75, 0.25, curr_root, velocity_base - 15)
        
        # 3. Solid anchor on beat 2
        # Position: 1.2 | Length: 1/8 | Velocity: 95
        add_note(bar_start_beat + 1.0, 0.5, curr_root, velocity_base - 5)
        
        # 4. Octave Slap! (The "e" of beat 2)
        # Position: 1.2.25 | Length: 1/32 (very short!) | Velocity: 127
        add_note(bar_start_beat + 1.25, 0.125, octave_slap, 127)
        
        # 5. Syncopated bounce on the "&" of beat 2
        # Position: 1.2.5 | Length: 1/16 | Velocity: 90
        add_note(bar_start_beat + 1.5, 0.25, curr_root, velocity_base - 10)
        
        # 6. Rest on beat 3, hit the "&" of 3
        # Position: 1.3.5 | Length: 1/8 | Velocity: 100
        add_note(bar_start_beat + 2.5, 0.5, curr_root, velocity_base)
        
        # 7. Walk-up/Walk-down Step to the next chord (The "&" of beat 4)
        # Position: 1.4.5 | Length: 1/8 | Velocity: 95
        # We find a diatonic step that leads nicely into the next root
        step_deg = next_deg - 1 if curr_deg < next_deg else next_deg + 1
        step_pitch = get_pitch(step_deg)
        add_note(bar_start_beat + 3.5, 0.5, step_pitch, velocity_base - 5)

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} humanized groove notes over {bars} bars at {bpm} BPM in {key} {scale}."
