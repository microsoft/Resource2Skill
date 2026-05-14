def create_pattern(
    project_name: str = "Workflow_Demo_Beat",
    track_name: str = "Trap Drums",
    bpm: int = 137,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 137 BPM Half-Time Trap Skeleton based on the example project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created drum track.
        bpm: Tempo in BPM (defaults to 137).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }

    # Ensure valid inputs
    key_upper = key.capitalize()
    if key_upper not in NOTE_MAP:
        key_upper = "F"
    root_note = NOTE_MAP[key_upper]
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Calculate bass root (Octave 1)
    bass_pitch = root_note + 24 

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Time calculations
    beat_length = 60.0 / bpm
    bar_length = beat_length * 4.0
    total_length = bar_length * bars

    # Helper function to insert MIDI notes safely
    def add_midi_note(take, start_time, duration, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- 1. CREATE DRUM TRACK ---
    num_tracks = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    drum_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", track_name, True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Standard GM Drum Map
    KICK = 36
    SNARE = 38
    HIHAT = 42

    # Populate Drum Pattern
    for b in range(bars):
        bar_start = b * bar_length
        
        # Kick: Beat 1 and the "and" of 2 (syncopated)
        add_midi_note(drum_take, bar_start, beat_length * 0.25, KICK, velocity_base)
        add_midi_note(drum_take, bar_start + (beat_length * 1.5), beat_length * 0.25, KICK, velocity_base - 10)
        
        # Snare: Beat 3 (Half-time feel)
        add_midi_note(drum_take, bar_start + (beat_length * 2.0), beat_length * 0.25, SNARE, velocity_base + 10)
        
        # Hi-Hats: 8th notes
        for h in range(8):
            hat_time = bar_start + (h * (beat_length / 2.0))
            hat_vel = velocity_base if h % 2 == 0 else velocity_base - 20
            add_midi_note(drum_take, hat_time, beat_length * 0.2, HIHAT, hat_vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # --- 2. CREATE SUB BASS TRACK ---
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    sub_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(sub_track, "P_NAME", "Sub Bass", True)

    # Add native sine wave synth
    RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)

    sub_item = RPR.RPR_AddMediaItemToTrack(sub_track)
    RPR.RPR_SetMediaItemInfo_Value(sub_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(sub_item, "D_LENGTH", total_length)
    sub_take = RPR.RPR_AddTakeToMediaItem(sub_item)

    # Populate Sub Pattern (following the kick drum)
    for b in range(bars):
        bar_start = b * bar_length
        # Long sustained sub note on beat 1
        add_midi_note(sub_take, bar_start, beat_length * 1.5, bass_pitch, velocity_base)
        
        # Move pitch up by a minor 3rd (interval index 1) for the second half of the 2nd/4th bars for movement
        current_pitch = bass_pitch
        if b % 2 != 0:
            current_pitch = bass_pitch + scale_intervals[2] # 3rd degree of scale

        add_midi_note(sub_take, bar_start + (beat_length * 1.5), beat_length * 2.0, current_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(sub_take)

    # Update UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' and 'Sub Bass' tracks over {bars} bars at {bpm} BPM in {key} {scale}."
