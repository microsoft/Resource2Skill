def create_rule_of_three_phrase(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Pattern",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an 8-bar chord and melody phrase demonstrating the 'Rule of 3'.
    Iterations 1 and 2 are identical. Iteration 3 branches off to create surprise.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C').
        scale: Scale type (e.g., 'major').
        bars: Total bars (overrides to 8 for this specific structural pattern).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

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

    # Fallback to C major if inputs are unrecognized
    root_val = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Ensure standard root octave (Octave 4 for chords, 5 for melody)
    chord_root_midi = 48 + root_val 
    melody_root_midi = 60 + root_val
    
    def get_pitch(root_midi, degree):
        """Helper to get MIDI pitch from 0-indexed scale degree."""
        octave_offset = degree // 7
        note_idx = degree % 7
        return root_midi + (octave_offset * 12) + scale_intervals[note_idx]

    beats_per_bar = 4
    ppq = 960 # Standard REAPER pulses per quarter note
    
    # Create Tracks
    track_idx = RPR.RPR_CountTracks(0)
    
    # 1. Chord Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name} (Chords)", True)
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "D_VOL", 0.4) # Lower volume for backing
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    
    # 2. Melody Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    melody_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(melody_track, "P_NAME", f"{track_name} (Melody)", True)
    RPR.RPR_SetMediaTrackInfo_Value(melody_track, "D_VOL", 0.8)
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaSynth", False, -1)
    # Give the melody ReaSynth a slightly different character (e.g., Sawtooth)
    RPR.RPR_TrackFX_SetParam(melody_track, 0, 1, 1.0) # Mix saw (approx index 1)
    
    # Calculate lengths
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * 8 # Force 8 bars for this structure
    
    # Insert Items
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_length_sec)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    melody_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", total_length_sec)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)
    
    # We will build an A-A-A'-B progression
    # Degrees are 0-indexed: 0=I, 1=ii, 2=iii, 3=IV, 4=V, 5=vi, 6=vii
    
    # Progression structures per 2-bar iteration
    iterations = [
        # Iteration 1 (Bars 1-2): IV -> I
        {"bar1_deg": 3, "bar2_deg": 0},
        # Iteration 2 (Bars 3-4): IV -> I (Exact Repeat)
        {"bar1_deg": 3, "bar2_deg": 0},
        # Iteration 3 (Bars 5-6): IV -> V (Rule of 3: Branch Off!)
        {"bar1_deg": 3, "bar2_deg": 4},
        # Iteration 4 (Bars 7-8): vi -> I (Resolution)
        {"bar1_deg": 5, "bar2_deg": 0}
    ]
    
    # Insert Notes
    for i, step in enumerate(iterations):
        start_bar = i * 2
        
        # Chord 1 (Bar 1 of the iteration)
        deg1 = step["bar1_deg"]
        start_ppq_1 = start_bar * 4 * ppq
        end_ppq_1 = start_ppq_1 + (4 * ppq) # Whole note
        
        # Chord 1 Triad
        for offset in [0, 2, 4]:
            pitch = get_pitch(chord_root_midi, deg1 + offset)
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq_1, end_ppq_1, 0, pitch, velocity_base, False)
            
        # Melody 1 (Arpeggio over Chord 1)
        m_pitch1 = get_pitch(melody_root_midi, deg1)
        m_pitch2 = get_pitch(melody_root_midi, deg1 + 2)
        m_pitch3 = get_pitch(melody_root_midi, deg1 + 4)
        
        RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq_1, start_ppq_1 + ppq, 0, m_pitch1, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq_1 + ppq, start_ppq_1 + (2*ppq), 0, m_pitch2, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq_1 + (2*ppq), start_ppq_1 + (4*ppq), 0, m_pitch3, velocity_base, False)

        # Chord 2 (Bar 2 of the iteration)
        deg2 = step["bar2_deg"]
        start_ppq_2 = (start_bar + 1) * 4 * ppq
        end_ppq_2 = start_ppq_2 + (4 * ppq) # Whole note
        
        # Chord 2 Triad
        for offset in [0, 2, 4]:
            pitch = get_pitch(chord_root_midi, deg2 + offset)
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq_2, end_ppq_2, 0, pitch, velocity_base, False)
            
        # Melody 2 (Arpeggio over Chord 2 - changes dynamically on Iteration 3)
        m2_pitch1 = get_pitch(melody_root_midi, deg2)
        m2_pitch2 = get_pitch(melody_root_midi, deg2 + 2)
        m2_pitch3 = get_pitch(melody_root_midi, deg2 + 4)
        
        RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq_2, start_ppq_2 + ppq, 0, m2_pitch1, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq_2 + ppq, start_ppq_2 + (2*ppq), 0, m2_pitch2, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq_2 + (2*ppq), start_ppq_2 + (3*ppq), 0, m2_pitch3, velocity_base+10, False) # Accent

    # Update items to process the inserted notes
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(melody_take)
    RPR.RPR_UpdateArrange()

    return f"Created 'Rule of 3' structure over 8 bars on tracks '{track_name} (Chords)' and '{track_name} (Melody)' in {key} {scale} at {bpm} BPM."
