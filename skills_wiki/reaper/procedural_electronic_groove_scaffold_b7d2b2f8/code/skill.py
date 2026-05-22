def create_pattern(
    project_name: str = "GrooveProject",
    track_name: str = "Procedural",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a procedural Tech-House/Electronic Drum and Bass groove in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks (Drums and Bass).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and elements.
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    step_len_sec = bar_length_sec / 16.0  # 1/16th note grid

    # === Define Procedural Sequences ===
    # Drum Sequence (step_index, midi_pitch)
    # 36 = Kick, 38 = Snare, 42 = Closed Hat, 46 = Open Hat
    drum_sequence = [
        (0, 36), (4, 36), (8, 36), (12, 36),  # 4-to-the-floor Kick
        (4, 38), (12, 38),                    # Snare on 2 and 4
        (2, 46), (6, 46), (10, 46), (14, 46), # Open hats on upbeats
        (3, 42), (7, 42), (11, 42),           # Syncopated closed hats
    ]

    # Bass Sequence (step_index, scale_degree_index, octave_offset)
    # Syncopated to weave between the kick drums
    scale_arr = SCALES.get(scale, SCALES["minor"])
    bass_sequence = [
        (1, 0, 0),                            # 1 e (Root)
        (3, 0, 0),                            # 1 a (Root)
        (6, 2, 0),                            # 2 & (3rd degree)
        (9, 0, 1),                            # 3 e (Root Octave Up)
        (12, len(scale_arr)-1, 0),            # 4   (Highest degree, e.g. 7th)
        (14, 4 % len(scale_arr), 0),          # 4 & (5th degree approximation)
    ]

    track_idx = RPR.RPR_CountTracks(0)

    # === Step 2: Create Drum Track & MIDI ===
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", bar_length_sec * bars)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    for b in range(bars):
        bar_offset = b * bar_length_sec
        for step, pitch in drum_sequence:
            start_time = bar_offset + step * step_len_sec
            end_time = start_time + step_len_sec * 0.6  # Punchy, short hits
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_time)
            
            # Add velocity variation for groove
            vel = velocity_base
            if pitch == 42:  # Closed hats are softer ghost notes
                vel = int(velocity_base * 0.6)
            elif pitch == 46: # Open hats slightly louder
                vel = int(velocity_base * 0.9)
                
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, pitch, vel, False)
            
    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: Create Bass Track & MIDI ===
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)
    
    # Add native synth for the bass
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", bar_length_sec * bars)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    base_midi = 36 + NOTE_MAP.get(key, 0)  # Starting from C2 register
    
    for b in range(bars):
        bar_offset = b * bar_length_sec
        for step, degree, oct_offset in bass_sequence:
            start_time = bar_offset + step * step_len_sec
            end_time = start_time + step_len_sec * 0.8  # slightly staccato for bass
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
            
            # Map diatonic degree to actual MIDI pitch
            note_idx = degree % len(scale_arr)
            octaves = degree // len(scale_arr) + oct_offset
            pitch = base_midi + scale_arr[note_idx] + (octaves * 12)
            
            vel = int(velocity_base * 0.9)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            
    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created Procedural Groove: '{track_name} Drums' & '{track_name} Bass' over {bars} bars at {bpm} BPM in {key} {scale}"
