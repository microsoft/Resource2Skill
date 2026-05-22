def create_pattern(
    project_name: str = "CinematicArp",
    track_name: str = "Sci-Fi Arp",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Cinematic Sci-Fi Synth Arpeggio in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created arpeggio track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated elements.
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

    # Calculate timing
    beats_per_bar = 4
    quarter_note_len = 60.0 / bpm
    sixteenth_len = quarter_note_len / 4.0
    bar_length_sec = quarter_note_len * beats_per_bar
    item_length = bar_length_sec * bars
    start_time = 0.0
    end_time = item_length

    # Calculate base pitch (C4)
    root_midi = NOTE_MAP.get(key, 0) + 60 
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # 1st, 3rd, 5th, 7th, Octave, 7th, 5th, 3rd (indices for a 7-note scale)
    pattern_indices = [0, 2, 4, 6, 7, 6, 4, 2] 

    # === Step 2: Create Arpeggio Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    arp_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(arp_track, "P_NAME", track_name, True)

    arp_item = RPR.RPR_CreateNewMIDIItemInProj(arp_track, start_time, end_time, False)
    arp_take = RPR.RPR_GetActiveTake(arp_item)

    notes_created = 0
    
    # Generate 16th note arpeggio
    for bar in range(bars):
        for beat in range(beats_per_bar):
            for sixteenth in range(4):
                step = sixteenth + (beat * 4) + (bar * 16)
                idx = pattern_indices[step % 8]
                
                octave_shift = idx // 7
                scale_degree = idx % 7
                pitch = root_midi + scale_intervals[scale_degree] + (octave_shift * 12)
                
                pos_sec = start_time + (step * sixteenth_len)
                end_pos_sec = pos_sec + (sixteenth_len * 0.85) # 85% gate length for plucky feel
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(arp_take, pos_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(arp_take, end_pos_sec)
                
                RPR.RPR_MIDI_InsertNote(arp_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                notes_created += 1

    RPR.RPR_MIDI_Sort(arp_take)
    RPR.RPR_TrackFX_AddByName(arp_track, "ReaSynth", False, -1)
    
    # Adjust ReaSynth for a plucky sound (Lower sustain/release)
    RPR.RPR_TrackFX_SetParam(arp_track, 0, 3, 0.1) # Release
    
    # === Step 3: Create Bass Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)

    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, start_time, end_time, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)
    
    bass_pitch = root_midi - 24 # Two octaves down for deep bass
    
    # Generate whole-note bass pedal points
    for bar in range(bars):
        pos_sec = start_time + (bar * bar_length_sec)
        end_pos_sec = pos_sec + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_pos_sec)
        
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base - 10, True)

    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Adjust ReaSynth for Bass (Square wave focus)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.8) # Square mix

    return f"Created '{track_name}' (Arp & Bass tracks) with {notes_created} arp notes over {bars} bars in {key} {scale} at {bpm} BPM."
