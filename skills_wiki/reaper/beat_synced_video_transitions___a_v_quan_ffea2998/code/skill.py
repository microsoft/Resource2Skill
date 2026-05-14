def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Beat-Synced AV Cuts",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a synchronized Audio/Video track setup with rhythmic 'Dip to Black' transitions.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated A/V pattern.
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

    # Calculate rhythm timings
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    total_length_sec = beat_length_sec * beats_per_bar * bars
    
    # Calculate Chord Pitches (Root, 3rd, 5th)
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    # Safely get a triad if the scale has at least 5 notes
    chord_pitches = [
        root_pitch,
        root_pitch + scale_intervals[2 % len(scale_intervals)],
        root_pitch + scale_intervals[4 % len(scale_intervals)]
    ]

    # === Step 2: Create Audio/MIDI Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    audio_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(audio_track, "P_NAME", f"{track_name} (Audio/MIDI)", True)
    
    # Add a basic synth for auditory feedback
    RPR.RPR_TrackFX_AddByName(audio_track, "ReaSynth", False, -1)
    
    # Create MIDI Item for the entire duration
    midi_item = RPR.RPR_CreateNewMIDIItemInProj(audio_track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(midi_item)
    
    # === Step 3: Create Parallel Video Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    video_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(video_track, "P_NAME", f"{track_name} (Video Cuts)", True)
    
    # Add Video Processor to allow item fades to act as Opacity fades (Fade to Black)
    RPR.RPR_TrackFX_AddByName(video_track, "Video processor", False, -1)

    # === Step 4: Generate Syncronized A/V Events ===
    event_count = 0
    
    for bar in range(bars):
        for beat in range(beats_per_bar):
            start_time = (bar * beats_per_bar * beat_length_sec) + (beat * beat_length_sec)
            # Create a staccato pulse (half a beat long)
            end_time = start_time + (beat_length_sec * 0.5)
            
            # --- Insert Audio (MIDI Notes) ---
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            for pitch in chord_pitches:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
            
            # --- Insert Video Cut (Empty Item with Fade) ---
            # Empty items act as transparent windows or colored solids in REAPER Video
            video_item = RPR.RPR_AddMediaItemToTrack(video_track)
            RPR.RPR_SetMediaItemInfo_Value(video_item, "D_POSITION", start_time)
            RPR.RPR_SetMediaItemInfo_Value(video_item, "D_LENGTH", beat_length_sec)
            
            # Create the "Dip to Black" transition shown in the tutorial using item fade-outs
            fade_out_len = beat_length_sec * 0.35 # Last 35% of the beat fades to black
            RPR.RPR_SetMediaItemInfo_Value(video_item, "D_FADEOUTLEN", fade_out_len)
            RPR.RPR_SetMediaItemInfo_Value(video_item, "C_FADEOUTSHAPE", 1) # Slow start curve
            
            event_count += 1

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(take)

    return f"Created synced A/V structure: {event_count} beat-synced video transitions and {key} {scale} MIDI chords over {bars} bars at {bpm} BPM."
