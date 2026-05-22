def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard (Notation Demo)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a syncopated I-IV-V chord progression on a new track.
    Open the resulting MIDI item and press Alt+4 to view it in REAPER's Notation mode.
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
    }

    # Validate inputs
    root_val = NOTE_MAP.get(key.upper() if len(key) == 1 else key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Base octave for chords
    base_octave = 4 
    root_midi = (base_octave + 1) * 12 + root_val

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for basic sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth slightly to sound more like an electric piano (less harsh)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) # Saw shape down
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5) # Triangle shape up
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3) # Release time

    # Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define the syncopated rhythm pattern for a bar (start_beat, duration_beats)
    rhythm_pattern = [
        (0.0,  0.5),   # Beat 1 (eighth note)
        (0.75, 0.25),  # "ah" of 1 (sixteenth note)
        (1.5,  0.5),   # "and" of 2 (eighth note syncopation)
        (2.5,  0.5),   # "and" of 3 (eighth note syncopation)
        (3.5,  0.5)    # "and" of 4 (eighth note syncopation)
    ]

    # Define harmonic progression by scale degrees (0-indexed)
    # I = degrees 0, 2, 4
    # IV = degrees 3, 5, 7
    # V = degrees 4, 6, 8
    progression = [
        [0, 2, 4], # Bar 1: I chord
        [3, 5, 7], # Bar 2: IV chord
        [4, 6, 8], # Bar 3: V chord
        [3, 5, 7], # Bar 4: IV chord
    ]

    def get_midi_note(degree_idx):
        """Helper to safely calculate MIDI pitch from a scale degree index, handling octave wrapping."""
        octave_shift = degree_idx // len(intervals)
        scale_idx = degree_idx % len(intervals)
        return root_midi + (octave_shift * 12) + intervals[scale_idx]

    # Generate notes
    notes_added = 0
    ticks_per_quarter = 960 # REAPER default PPQ
    
    RPR.RPR_MIDI_DisableSort(take)
    
    for bar_idx in range(bars):
        # Loop the 4-bar progression if 'bars' > 4
        chord_degrees = progression[bar_idx % len(progression)]
        
        for start_beat, dur_beats in rhythm_pattern:
            # Calculate absolute tick positions
            start_ppq = (bar_idx * beats_per_bar + start_beat) * ticks_per_quarter
            end_ppq = start_ppq + (dur_beats * ticks_per_quarter)
            
            # Slight velocity variation for humanization
            vel = velocity_base
            if start_beat != 0.0:
                vel = max(10, velocity_base - 15) # Syncopated notes slightly quieter

            # Insert notes for the chord
            for degree in chord_degrees:
                pitch = get_midi_note(degree)
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, pitch, vel, False
                )
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM. Open MIDI item and use View -> Mode: musical notation."
