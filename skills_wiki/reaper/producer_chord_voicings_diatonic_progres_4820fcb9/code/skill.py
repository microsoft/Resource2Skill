def create_pattern(
    project_name: str = "MusicTheory101",
    track_name: str = "Open Voicing Chords",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    progression: list = [6, 7, 1, 3],  # VI, VII, i, III
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Producer Voiced' syncopated chord progression based on music theory.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        progression: List of scale degrees to play (1-indexed, e.g., [1, 4, 5, 1]).
        bars: Number of bars to generate (will loop the progression to fit).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

    # === Music Theory Lookup Tables ===
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
    if scale not in SCALES:
        scale = "minor"
    if key not in NOTE_MAP:
        key = "A"

    # Generate a linear array of all diatonic notes across 10 octaves
    # This allows us to easily extract 3rds, 5ths, and 7ths by just adding to the index
    scale_intervals = SCALES[scale]
    base_midi = NOTE_MAP[key]
    diatonic_grid = []
    for octave in range(10):
        for interval in scale_intervals:
            note = base_midi + (octave * 12) + interval
            if 0 <= note <= 127:
                diatonic_grid.append(note)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Set volume slightly lower to accommodate thick chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Roughly -6dB

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Rhythmic syncopation pattern per bar (in beats: 0 = beat 1, 1.5 = beat 2 "and", 3.0 = beat 4)
    # Lengths are in beats
    rhythm_pattern = [
        {"start": 0.0, "len": 1.0},
        {"start": 1.5, "len": 1.0},
        {"start": 3.0, "len": 1.0}
    ]

    # === Step 4: Write MIDI Notes (The Core Theory Implementation) ===
    # Start our chords around octave 4 (which is roughly index 28 in our diatonic grid)
    octave_offset = 4 
    base_index = (octave_offset * len(scale_intervals))

    for bar in range(bars):
        # Loop the progression if bars > progression length
        degree = progression[bar % len(progression)] 
        
        # Calculate diatonic indices (0-indexed)
        deg_idx = base_index + (degree - 1)
        
        # Retrieve the exact MIDI pitches ensuring we stay strictly in-key
        root = diatonic_grid[deg_idx]
        third = diatonic_grid[deg_idx + 2]
        fifth = diatonic_grid[deg_idx + 4]
        seventh = diatonic_grid[deg_idx + 6]
        
        # Apply "Producer Voicing" taught in the video
        bass_note = root - 12         # Root dropped an octave
        open_third = third + 12       # 3rd raised an octave (Open Voicing)
        
        chord_notes = [bass_note, root, fifth, seventh, open_third]

        # Write the syncopated rhythm for this bar
        bar_start_time = bar * bar_length_sec
        
        for hit in rhythm_pattern:
            note_start_time = bar_start_time + (hit["start"] * (60.0 / bpm))
            note_end_time = note_start_time + (hit["len"] * (60.0 / bpm))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
            
            for pitch in chord_notes:
                # Add slight velocity humanization based on pitch
                vel = velocity_base
                if pitch == bass_note: vel = min(127, velocity_base + 10) # Hit bass slightly harder
                if pitch == open_third: vel = max(1, velocity_base - 10)  # Soften the high 3rd
                
                # Insert note: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Sort MIDI to ensure proper playback
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (FX Chain) ===
    # Add basic synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    fx_idx_synth = RPR.RPR_TrackFX_GetByName(track, "ReaSynth", False)
    # Set to a mix of Saw (Param 1) and Square (Param 2)
    RPR.RPR_TrackFX_SetParam(track, fx_idx_synth, 1, 0.5) 
    RPR.RPR_TrackFX_SetParam(track, fx_idx_synth, 2, 0.5)
    # Give it a plucky envelope (Param 4=Attack, 5=Decay)
    RPR.RPR_TrackFX_SetParam(track, fx_idx_synth, 4, 0.01) 
    RPR.RPR_TrackFX_SetParam(track, fx_idx_synth, 5, 0.2)  
    
    # Add EQ to cut mud
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    fx_idx_eq = RPR.RPR_TrackFX_GetByName(track, "ReaEQ", False)
    # Set band 1 to High Pass (Type 2) at 100Hz
    RPR.RPR_TrackFX_SetParam(track, fx_idx_eq, 0, 2.0)    # Band 1 Type: High Pass
    RPR.RPR_TrackFX_SetParam(track, fx_idx_eq, 1, 100.0)  # Freq
    
    # Add Delay for width and rhythm
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    fx_idx_delay = RPR.RPR_TrackFX_GetByName(track, "ReaDelay", False)
    RPR.RPR_TrackFX_SetParam(track, fx_idx_delay, 0, 0.0) # Length (Time)
    RPR.RPR_TrackFX_SetParam(track, fx_idx_delay, 13, 0.0) # Length in Musical Notes (0 = 1/8 note)
    RPR.RPR_TrackFX_SetParam(track, fx_idx_delay, 4, -12.0) # Wet mix

    return f"Created '{track_name}' featuring {key} {scale} producer-voiced chords over {bars} bars at {bpm} BPM."
