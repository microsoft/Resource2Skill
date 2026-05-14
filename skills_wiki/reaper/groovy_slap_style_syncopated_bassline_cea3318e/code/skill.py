def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groovy Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a groovy, humanized slap-style bassline in REAPER.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., E, A).
        scale: Scale type (e.g., minor, major, dorian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard plucked notes.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Data ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 4) # Default to E
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Place in bass range (Octave 1 and 2, MIDI notes 28-50ish)
    base_midi_note = root_val + 24 

    # === Setup Track and Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = sec_per_beat * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Bass Motif Definition ===
    # Tuple: (beat_start, beat_duration, degree_offset, octave_offset, is_slap)
    motif = [
        (0.00, 0.75,  0,  0, False), # Main downbeat (split length)
        (1.50, 0.25,  0,  0, False), # Syncopated offbeat
        (2.75, 0.125, 0,  1, True),  # Short Octave Slap
        (3.50, 0.25, -2,  0, False), # Walk-up step 1
        (3.75, 0.25, -1,  0, False), # Walk-up step 2
    ]

    notes_created = 0

    # === Generate Rhythmic Pattern ===
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Chord progression: Alternate between I and IV (index 0 and index 3 of scale)
        # Fallback to index 0 if it's a short scale
        target_degree_idx = 0 if bar % 2 == 0 else min(3, len(scale_intervals)-1)
        chord_root_pitch = base_midi_note + scale_intervals[target_degree_idx]

        for note in motif:
            b_start, b_dur, deg_offset, oct_off, is_slap = note
            
            # Calculate pitch mapping diatonic steps
            # Wrap around scale arrays to stay in key
            combined_degree = target_degree_idx + deg_offset
            octave_shift = oct_off + (combined_degree // len(scale_intervals))
            scale_idx = combined_degree % len(scale_intervals)
            
            pitch = base_midi_note + scale_intervals[scale_idx] + (octave_shift * 12)
            
            # Apply Humanization (Imitate Reality)
            # 1. Timing: shift by +/- 0.02 beats (slight swing/imperfection)
            human_offset = random.uniform(-0.02, 0.02)
            actual_beat_start = bar_start_beat + b_start + human_offset
            actual_beat_end = actual_beat_start + b_dur
            
            # 2. Velocity: Slaps hit at max 127. Normal notes fluctuate around base.
            if is_slap:
                vel = 127
            else:
                vel = int(velocity_base * random.uniform(0.85, 1.1))
                vel = max(1, min(127, vel))
            
            # Convert beats to time, then to PPQ (MIDI ticks)
            start_time = actual_beat_start * sec_per_beat
            end_time = actual_beat_end * sec_per_beat
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_created += 1

    # Sort MIDI to finalize the item
    RPR.RPR_MIDI_Sort(take)

    # === Add Synth FX ===
    # Add ReaSynth to immediately hear the bassline
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Optional: Tweak ReaSynth for a more bass-heavy square/saw character
    # Param 1 is Tuning, Param 2 is Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.7)  # Mix in Square wave

    return f"Created '{track_name}' with {notes_created} groovy bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
