def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Notation-Ready Piano Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (forces 4 for the chord loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if scale not in SCALES:
        scale = "major"  # Fallback to major
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES[scale]
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Take ===
    beats_per_bar = 4
    # Calculate exactly 1 quarter note in REAPER's time base
    qn_length = 60.0 / bpm 
    bar_length = qn_length * beats_per_bar
    total_length = bar_length * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # We will generate a I - V - vi - IV progression (or i - v - VI - iv in minor)
    # Degrees are 0-indexed: 0=I, 4=V, 5=vi, 3=IV
    progression = [0, 4, 5, 3] 
    
    note_count = 0
    base_octave = 5  # MIDI octave 5 (treble clef)
    bass_octave = 3  # MIDI octave 3 (bass clef)
    
    # Loop over bars to create the sequence
    for bar in range(bars):
        # Repeat progression if bars > 4
        degree_idx = progression[bar % len(progression)]
        
        # Calculate root note for this chord
        chord_root_pitch = root_val + scale_intervals[degree_idx]
        
        # Calculate triad intervals (1st, 3rd, 5th of the chord)
        third_idx = (degree_idx + 2) % 7
        fifth_idx = (degree_idx + 4) % 7
        
        # Adjust for octave wrapping inside the scale
        third_pitch = root_val + scale_intervals[third_idx] + (12 if third_idx < degree_idx else 0)
        fifth_pitch = root_val + scale_intervals[fifth_idx] + (12 if fifth_idx < degree_idx else 0)
        
        # Absolute MIDI note numbers
        chord_notes = [
            chord_root_pitch + (base_octave * 12),
            third_pitch + (base_octave * 12),
            fifth_pitch + (base_octave * 12)
        ]
        
        bass_note = chord_root_pitch + (bass_octave * 12)
        
        # Timings for this bar
        bar_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar * bar_length)
        half_bar_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (bar * bar_length) + (qn_length * 2))
        end_bar_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (bar + 1) * bar_length)
        
        # 1. Insert Right-Hand Chords (Two Half Notes per bar)
        for chord_note in chord_notes:
            # First half note
            RPR.RPR_MIDI_InsertNote(take, False, False, bar_start_ppq, half_bar_ppq, 1, chord_note, velocity_base, False)
            # Second half note
            RPR.RPR_MIDI_InsertNote(take, False, False, half_bar_ppq, end_bar_ppq, 1, chord_note, velocity_base - 15, False)
            note_count += 2
            
        # 2. Insert Left-Hand Bass (Four Quarter notes per bar)
        for beat in range(4):
            beat_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (bar * bar_length) + (beat * qn_length))
            beat_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (bar * bar_length) + ((beat + 1) * qn_length))
            
            # Accent the downbeat
            vel = velocity_base + 10 if beat == 0 else velocity_base - 10
            
            RPR.RPR_MIDI_InsertNote(take, False, False, beat_start_ppq, beat_end_ppq, 1, bass_note, vel, False)
            note_count += 1

    # Force MIDI editor to update
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add simple synth for auditioning ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' with {note_count} notation-ready notes over {bars} bars in {key} {scale} at {bpm} BPM."
