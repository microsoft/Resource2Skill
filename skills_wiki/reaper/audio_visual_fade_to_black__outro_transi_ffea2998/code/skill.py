def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "FadeToBlack",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Audio-Visual Fade to Black transition in the current REAPER project.
    Generates an audio pad and a paired video placeholder that fade out simultaneously.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the final chord sustains.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated tracks and fades.
    """
    import reaper_python as RPR

    # Music theory lookup tables for the final resolving chord
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

    # === Step 1: Calculate Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    # We will fade out over the final 1.5 bars of the section
    fade_length_sec = bar_length_sec * 1.5 
    
    # MIDI timing (960 ticks per quarter note)
    end_tick = bars * 4 * 960

    # Determine pitch stack (Tonic triad I chord)
    root_midi = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_notes = [
        root_midi,                          # Root
        root_midi + scale_intervals[2],     # 3rd
        root_midi + scale_intervals[4]      # 5th
    ]

    # === Step 2: Create Audio Track (Musical Anchor) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    audio_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(audio_track, "P_NAME", f"{track_name}_AudioPad", True)

    # Add ReaSynth and configure it as a pad
    RPR.RPR_TrackFX_AddByName(audio_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(audio_track, 0, 3, 0.5)  # Attack time
    RPR.RPR_TrackFX_SetParam(audio_track, 0, 4, 0.8)  # Release time

    # Create MIDI Item for Audio
    audio_item = RPR.RPR_AddMediaItemToTrack(audio_track)
    RPR.RPR_SetMediaItemInfo_Value(audio_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(audio_item, "D_LENGTH", total_length_sec)
    
    # Apply Audio Item Fade Out
    RPR.RPR_SetMediaItemInfo_Value(audio_item, "D_FADEOUTLEN", fade_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(audio_item, "C_FADEOUTDIR", 1.0) # Slight exponential curve
    
    take = RPR.RPR_AddTakeToMediaItem(audio_item)
    
    # Insert notes
    for pitch in chord_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_tick, 0, pitch, velocity_base, False)

    # === Step 3: Create Video Track (Visual Anchor) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    video_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(video_track, "P_NAME", f"{track_name}_VideoOverlay", True)

    # Add Video Processor (User must select 'Item fades affect video' preset manually)
    RPR.RPR_TrackFX_AddByName(video_track, "Video processor", False, -1)

    # Create placeholder item for video to apply the matching fade
    video_item = RPR.RPR_AddMediaItemToTrack(video_track)
    RPR.RPR_SetMediaItemInfo_Value(video_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(video_item, "D_LENGTH", total_length_sec)
    
    # Apply identical Fade Out to video item to ensure sync
    RPR.RPR_SetMediaItemInfo_Value(video_item, "D_FADEOUTLEN", fade_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(video_item, "C_FADEOUTDIR", 1.0)
    
    # Empty take allows the item to be visible and editable on the timeline
    RPR.RPR_AddTakeToMediaItem(video_item)

    return f"Created synced Audio/Video tracks with {fade_length_sec:.2f}s fade-out over {bars} bars at {bpm} BPM (Key: {key} {scale})."
