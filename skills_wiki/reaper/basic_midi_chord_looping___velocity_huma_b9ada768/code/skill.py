def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Humanized Piano Chords' MIDI loop in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for the strong downbeats.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
    """
    import reaper_python as RPR

    # === Music theory lookup tables ===
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Stock Piano-ish ReaSynth) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a more piano-like, plucky envelope
    # Param 1: Attack (fast), Param 2: Decay, Param 3: Sustain (low), Param 4: Release
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0)   # Fast Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.3)   # Medium Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.1)   # Low Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.4)   # Medium Release

    # === Step 4: Calculate Chord Voicing ===
    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Base MIDI note (C3 = 48 in some mappings, or 60. We'll use 48 to allow a low C2 bass)
    base_midi = 48 + root_val
    
    # Create the voicing shown in the tutorial: Low Root, Root, 3rd, 5th, High Root
    chord_pitches = [
        base_midi - 12,                   # Low Bass Octave
        base_midi,                        # Root
        base_midi + scale_intervals[2],   # 3rd
        base_midi + scale_intervals[4],   # 5th
        base_midi + 12                    # Top Octave
    ]

    # === Step 5: Create MIDI Item & Take ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 6: Insert Humanized Notes ===
    total_notes_added = 0
    
    for b in range(bars):
        # We will trigger two chords per bar (half-note rhythm)
        for hit in range(2):
            # Calculate timing
            start_time = (b * bar_length_sec) + (hit * 2 * sec_per_beat)
            # Make the note length slightly detached (1.8 beats instead of a full 2 beats)
            end_time = start_time + (1.8 * sec_per_beat) 
            
            # Convert absolute seconds to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Velocity Humanization: Downbeats are strong, off-beats are ~15% softer
            current_velocity = velocity_base if hit == 0 else int(velocity_base * 0.85)
            
            # Ensure velocity bounds
            current_velocity = max(1, min(127, current_velocity))

            # Insert the chord notes
            for pitch in chord_pitches:
                # Ensure pitch bounds
                pitch = max(0, min(127, pitch))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, current_velocity, False)
                total_notes_added += 1

    # Sort MIDI events after bulk insertion for proper playback
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}. Velocity humanization applied."
