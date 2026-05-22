def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Dynamic Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 40,   # Starting velocity
    velocity_peak: int = 115,  # Ending velocity
    **kwargs,
) -> str:
    """
    Create a pulsing, velocity-sloped chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Starting velocity for the ramp (0-127).
        velocity_peak: Ending velocity for the ramp (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Dictionary & Lookup Setup ===
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

    # Format inputs safely
    key = key.capitalize()
    if key not in NOTE_MAP:
        key = "C"
    if scale not in SCALES:
        scale = "major"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Setup FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add native synth to play the chords
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Notes with Velocity Slope ===
    root_val = NOTE_MAP[key]
    octave_base = 48 # Start around C3
    root_pitch = octave_base + root_val
    
    # Build a basic root position triad (1-3-5) based on the scale array
    scale_deg = SCALES[scale]
    chord_pitches = [
        root_pitch + scale_deg[0], # Root
        root_pitch + scale_deg[2], # Third
        root_pitch + scale_deg[4]  # Fifth
    ]

    # Pulse 8th notes (2 per beat)
    steps_per_beat = 2
    total_steps = bars * beats_per_bar * steps_per_beat
    step_duration_sec = sec_per_beat / steps_per_beat
    
    notes_created = 0
    
    for i in range(total_steps):
        # Calculate time boundaries for the current 8th note
        note_start_time = i * step_duration_sec
        # Leave a tiny gap (90% gate) so repeated notes articulate cleanly
        note_end_time = note_start_time + (step_duration_sec * 0.90) 
        
        # Convert absolute time to MIDI PPQ (Pulses Per Quarter Note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
        
        # Calculate linear velocity slope
        if total_steps > 1:
            progress = i / float(total_steps - 1)
        else:
            progress = 0.0
            
        current_vel = int(velocity_base + (velocity_peak - velocity_base) * progress)
        current_vel = max(1, min(127, current_vel)) # Clamp safety
        
        # Insert the chord's notes
        for pitch in chord_pitches:
            RPR.RPR_MIDI_InsertNote(
                take, 
                False,      # selected
                False,      # muted
                start_ppq,  # start time
                end_ppq,    # end time
                0,          # channel
                pitch,      # pitch
                current_vel,# velocity
                True        # noSort (we will sort once at the end)
            )
            notes_created += 1

    # Finalize the MIDI data
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM (Velocity sloped from {velocity_base} to {velocity_peak})."
