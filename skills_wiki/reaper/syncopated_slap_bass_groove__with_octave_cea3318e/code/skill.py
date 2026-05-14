def create_pattern(
    project_name: str = "SlapBassGroove",
    track_name: str = "Groove Bass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a syncopated, humanized slap bass groove in REAPER.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard notes.
        
    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

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

    # Safely get scale or fallback to minor
    scale_arr = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 24 + NOTE_MAP.get(key.capitalize(), 4) # Base octave around E1-C2

    def get_pitch(degree):
        """Convert a scale degree (can be negative or > len(scale)) to a MIDI pitch."""
        octave_shift = degree // len(scale_arr)
        idx = degree % len(scale_arr)
        return root_midi + (octave_shift * 12) + scale_arr[idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Setup FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth as a placeholder
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define the Groove Motif ===
    # Format: (quarter_note_start, quarter_note_duration, scale_degree, is_slap)
    # A 1-bar rhythmic funk motif based on 16th notes
    motif = [
        (0.0,  0.75,  0, False),  # Beat 1: Downbeat root
        (1.25, 0.25,  7, True),   # Beat 2 "e": Syncopated slap (Octave up)
        (2.0,  0.50,  0, False),  # Beat 3: Root again
        (2.75, 0.25,  7, True),   # Beat 3 "a": Syncopated slap
        (3.5,  0.25, -2, False),  # Beat 4 "and": Approach note (-2 degrees)
        (3.75, 0.25, -1, False),  # Beat 4 "a": Approach note (-1 degree)
    ]

    note_count = 0

    # === Step 5: Generate and Humanize Notes ===
    for bar in range(bars):
        bar_offset_qn = bar * beats_per_bar
        
        for qn_start, qn_dur, degree, is_slap in motif:
            # Calculate base timings in seconds
            base_start_sec = (bar_offset_qn + qn_start) * (60.0 / bpm)
            base_end_sec = base_start_sec + (qn_dur * (60.0 / bpm))
            
            # "Imitate Reality": Add humanization to timing (+/- 15ms)
            humanize_offset = random.uniform(-0.015, 0.015)
            # Ensure the very first note doesn't get pushed before 0.0
            if base_start_sec == 0.0 and humanize_offset < 0:
                humanize_offset = 0.0 
                
            start_sec = base_start_sec + humanize_offset
            
            # Make the end slightly disjointed/staccato based on humanization
            end_sec = base_end_sec + random.uniform(-0.02, 0.00) 

            # Convert seconds to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

            # Pitch and Velocity logic
            pitch = get_pitch(degree)
            
            if is_slap:
                # Slaps are louder, punchier, and heavily accented
                velocity = min(127, velocity_base + 30 + random.randint(-5, 5))
            else:
                # Standard plucks get minor velocity variation
                velocity = max(1, min(127, velocity_base + random.randint(-8, 8)))

            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, False)
            note_count += 1

    # Force UI update
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
