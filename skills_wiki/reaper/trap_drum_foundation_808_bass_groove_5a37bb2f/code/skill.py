def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Trap Beat",
    bpm: int = 145,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Trap Drum Foundation & 808 Bass Groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (140-150 recommended for this style).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (4 is optimal for the progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
                
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

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Step 2: Create Drums Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    def add_midi_note(take, pitch, start_beat, length_beats, vel):
        pos_sec = start_beat * (60.0 / bpm)
        end_sec = pos_sec + (length_beats * (60.0 / bpm))
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Sequence Drums
    for b in range(bars):
        bar_start_beat = b * 4.0
        
        # Kick (GM 36) - Syncopated Trap rhythm
        add_midi_note(drum_take, 36, bar_start_beat + 0.0, 0.25, velocity_base)
        add_midi_note(drum_take, 36, bar_start_beat + 1.5, 0.25, velocity_base)
        add_midi_note(drum_take, 36, bar_start_beat + 2.5, 0.25, velocity_base)
        
        # Layered Snare (GM 38) & Clap (GM 39) on backbeats (beats 2 and 4)
        add_midi_note(drum_take, 38, bar_start_beat + 1.0, 0.25, velocity_base)
        add_midi_note(drum_take, 39, bar_start_beat + 1.0, 0.25, velocity_base)
        add_midi_note(drum_take, 38, bar_start_beat + 3.0, 0.25, velocity_base)
        add_midi_note(drum_take, 39, bar_start_beat + 3.0, 0.25, velocity_base)
        
        # Hi-hats (GM 42)
        if b == bars - 1:
            # First 3 beats are standard 8th notes (6 hits)
            for i in range(6):
                add_midi_note(drum_take, 42, bar_start_beat + (i * 0.5), 0.25, int(velocity_base * 0.8))
            
            # 4th beat is a 32nd note roll (8 hits in 1 beat)
            for i in range(8):
                roll_beat = bar_start_beat + 3.0 + (i * 0.125)
                roll_vel = int(70 + (i * 4)) # Ramping velocity swell
                add_midi_note(drum_take, 42, roll_beat, 0.1, roll_vel)
        else:
            # Standard 8th notes
            for i in range(8):
                add_midi_note(drum_take, 42, bar_start_beat + (i * 0.5), 0.25, int(velocity_base * 0.8))

    RPR.RPR_MIDI_Sort(drum_take)

    # Step 3: Create 808 Bass Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} 808 Bass", True)
    
    # 808 FX Chain: ReaSynth Sine Wave
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Calculate 808 pitches
    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    base_octave = 24 # C1
    root_pitch = base_octave + root_val
    sixth_pitch = base_octave + root_val + scale_intervals[5 % len(scale_intervals)]
    
    # Keep the 6th degree strictly in the sub-bass register
    if sixth_pitch > 36:
        sixth_pitch -= 12

    # Sequence 808
    for b in range(bars):
        bar_start_beat = b * 4.0
        
        # Harmonic progression: Root for first half, 6th degree for second half
        p = root_pitch if b < (bars / 2) else sixth_pitch
        
        # 808 follows the syncopated kick rhythm but sustains longer
        add_midi_note(bass_take, p, bar_start_beat + 0.0, 0.8, velocity_base)
        add_midi_note(bass_take, p, bar_start_beat + 1.5, 0.8, velocity_base)
        add_midi_note(bass_take, p, bar_start_beat + 2.5, 0.8, velocity_base)

    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created '{track_name}' Drums and 808 tracks over {bars} bars at {bpm} BPM in {key} {scale}."
