def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Create Humanized Rhythmic Chords with a velocity crescendo ramp.

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
        Status string describing what was created.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_GetNumTracks()
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Native Synth Placeholder) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower ReaSynth volume to avoid clipping with dense chords (Param 0 = Volume)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.1) 

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Determine Pitch Strategy ===
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    chord_pitches = []
    octave = 4 
    
    # Build a diatonic root position triad (1st, 3rd, 5th degree of the scale)
    for i in [0, 2, 4]:
        idx = i % len(scale_intervals)
        oct_offset = i // len(scale_intervals)
        chord_pitches.append(root_val + scale_intervals[idx] + (octave + oct_offset) * 12)
        
    # Add a root bass note an octave lower for depth
    chord_pitches.append(root_val + scale_intervals[0] + (octave - 1) * 12)

    # === Step 6: Insert Notes with Velocity Automation ===
    total_8th_notes = bars * beats_per_bar * 2
    note_length_beats = 0.5 
    
    notes_added = 0
    for step in range(int(total_8th_notes)):
        start_beat = step * note_length_beats
        # Make the note slightly staccato (plays for 85% of its length)
        end_beat = start_beat + (note_length_beats * 0.85) 
        
        start_time = (60.0 / bpm) * start_beat
        end_time = (60.0 / bpm) * end_beat
        
        # Convert absolute time to MIDI PPQ (Pulses Per Quarter note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Calculate Humanized Velocity:
        # 1. Accent downbeats (+15), soften upbeats (-15)
        # 2. Linear crescendo ramp over the entire length (rises by 40 over time)
        accent = 15 if step % 2 == 0 else -15
        ramp_progress = step / max(1, (total_8th_notes - 1))
        
        # Start slightly below base to allow room for the ramp
        vel = int((velocity_base - 10) + accent + (ramp_progress * 40))
        vel = max(1, min(127, vel)) # Clamp to valid MIDI range
        
        for pitch in chord_pitches:
            # noSort=True during the loop for performance
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            notes_added += 1
            
    # Sort the MIDI note buffer after all insertions
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes across {bars} bars at {bpm} BPM, featuring a programmatic velocity crescendo."
