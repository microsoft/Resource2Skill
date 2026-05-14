def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a 12-bar progression demonstrating the 'Rule of 3' (A-A-A' structure).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: The length is structurally tied to 12 bars to show 3 iterations.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument & Sound Design ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape ReaSynth to be a plucky, piano-like sound
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.0)  # Attack 
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.2)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3)  # Release

    # === Step 4: Music Theory Lookup ===
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
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_pitch = 60 + NOTE_MAP.get(key.capitalize(), 0)
    # Keep the root pitch comfortably in the midrange
    if root_pitch > 65: 
        root_pitch -= 12

    def get_note(degree, oct_offset=0):
        """Converts a scale degree into an absolute MIDI pitch."""
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_pitch + scale_intervals[idx] + (octave + oct_offset) * 12

    # === Step 5: Setup MIDI Item ===
    # Forcing exactly 12 bars (3 iterations of a 4-bar phrase) to demonstrate the rule
    total_bars = 12
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    notes_to_add = []

    def add_note(start_bar, start_beat, duration_beats, degree, oct_offset=0, velocity=100):
        note_start_sec = ((start_bar * beats_per_bar) + start_beat) * (60.0 / bpm)
        note_end_sec = note_start_sec + (duration_beats * (60.0 / bpm))
        
        # Convert absolute project time to MIDI PPQ exactly
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
        
        pitch = get_note(degree, oct_offset)
        pitch = int(max(0, min(127, pitch)))
        velocity = int(max(1, min(127, velocity)))
        
        notes_to_add.append((start_ppq, end_ppq, pitch, velocity))

    # === Step 6: Generate A-A-A' Structure ===
    # Phrase A: I - V - vi - IV
    # Phrase A' (Deviation): I - V - ii - V
    chords_A = [0, 4, 5, 3] 
    chords_B = [0, 4, 1, 4] 

    for global_bar in range(total_bars):
        iteration = global_bar // 4
        bar_in_phrase = global_bar % 4
        
        # Select progression based on the Rule of 3
        root_deg = chords_A[bar_in_phrase] if iteration < 2 else chords_B[bar_in_phrase]
            
        # 1. Bass Note (held for the whole bar, low velocity)
        add_note(global_bar, 0, 4.0, root_deg, oct_offset=-2, velocity=velocity_base + 10)
        
        # 2. Sustained Triad (held for the whole bar)
        add_note(global_bar, 0, 4.0, root_deg, oct_offset=-1, velocity=velocity_base - 10)
        add_note(global_bar, 0, 4.0, root_deg + 2, oct_offset=-1, velocity=velocity_base - 10)
        add_note(global_bar, 0, 4.0, root_deg + 4, oct_offset=-1, velocity=velocity_base - 10)
        
        # 3. Melody Generation
        if iteration < 2 or bar_in_phrase < 2:
            # Iterations 1 & 2 (and start of 3): Predictable 1/8th note arpeggio
            m_pattern = [root_deg+4, root_deg+2, root_deg, root_deg+2] * 2
            for i, m_deg in enumerate(m_pattern):
                add_note(global_bar, i * 0.5, 0.5, m_deg, oct_offset=1, velocity=velocity_base)
        else:
            # Iteration 3 Deviation (Bars 11 & 12): Tension-building 1/16th notes
            # Climbs overlapping sequence: 0-1-2-3, 1-2-3-4, 2-3-4-5, 3-4-5-6
            m_pattern = [(root_deg + (i % 4) + (i // 4)) for i in range(16)]
            for i, m_deg in enumerate(m_pattern):
                # Dynamically swell velocity as the pitch climbs
                swell_vel = velocity_base - 10 + int((i / 15) * 30) 
                add_note(global_bar, i * 0.25, 0.25, m_deg, oct_offset=1, velocity=swell_vel)

    # === Step 7: Insert & Finalize ===
    for note in notes_to_add:
        RPR.RPR_MIDI_InsertNote(take, False, False, note[0], note[1], 0, note[2], note[3], True)
        
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' demonstrating the 'Rule of 3' (A-A-A' form) over 12 bars in {key} {scale} at {bpm} BPM."
