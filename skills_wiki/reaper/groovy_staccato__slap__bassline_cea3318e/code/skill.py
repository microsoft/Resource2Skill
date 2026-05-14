def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groovy Slap Bass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Groovy Staccato Slap Bassline with humanization in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for root notes (0-127).

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    # Get base pitch (Octave 1 or 2 for Bass, e.g., E1 = 28)
    base_note_val = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    root_midi = base_note_val + 24 # Bass range (C1 is 24)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Function to get diatonic note by scale degree (0-indexed)
    def get_scale_note(degree):
        octave_shift = (degree // len(scale_intervals)) * 12
        interval = scale_intervals[degree % len(scale_intervals)]
        return root_midi + octave_shift + interval

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Setup Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth and configure for a plucky bass sound
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape: Square/Saw mix for buzz
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.4)  # Square mix
    # Envelope: Fast attack, quick decay, low sustain to create "pluck"
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.15) # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.1)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.1)  # Release

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Standard groove structure per bar (16th note grid, 4 beats)
    # Format: (Beat_position, Scale_Degree, Duration_in_beats, Velocity_Multiplier)
    # Durations are kept short (0.15 - 0.2 beats) for the staccato "slap" feel
    groove_pattern = [
        (0.0,  0, 0.20, 1.0),   # Beat 1: Root downbeat
        (1.5,  0, 0.15, 0.8),   # Beat 2 "and": Root syncopation
        (2.0,  0, 0.20, 0.9),   # Beat 3: Root
        (2.75, 7, 0.15, 1.25),  # Beat 3 "a": Octave Slap (degree 7 = Root + octave)
        (4.25, -2, 0.15, 0.7),  # Beat 4 "e": Passing note (-2 degrees)
        (4.75, -1, 0.15, 0.8)   # Beat 4 "a": Passing note leading back to root
    ]
    
    notes_added = 0
    
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        for beat_offset, degree, duration_beats, vel_mult in groove_pattern:
            # Calculate absolute beat timing
            abs_beat_start = bar_start_beat + beat_offset
            abs_beat_end = abs_beat_start + duration_beats
            
            # Add Humanization: Random timing offset (+/- 0.03 beats)
            timing_offset = random.uniform(-0.03, 0.03)
            # Don't offset the absolute downbeat of the entire loop to keep it anchored
            if bar == 0 and beat_offset == 0.0:
                timing_offset = 0.0
                
            start_time_sec = ((abs_beat_start + timing_offset) / bpm) * 60.0
            end_time_sec = ((abs_beat_end + timing_offset) / bpm) * 60.0
            
            # Convert to PPQ (Pulses Per Quarter Note)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            # Humanize velocity
            base_vel = min(127, max(1, int(velocity_base * vel_mult)))
            vel = min(127, max(1, base_vel + random.randint(-8, 8)))
            
            pitch = get_scale_note(degree)
            
            # Ensure pitch is in valid MIDI bounds
            pitch = min(127, max(0, pitch))
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, vel, False
            )
            notes_added += 1

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} staccato notes over {bars} bars at {bpm} BPM in {key} {scale}."
