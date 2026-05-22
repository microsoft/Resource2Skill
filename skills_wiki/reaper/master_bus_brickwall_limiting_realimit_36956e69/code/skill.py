def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Loud Synth Reference",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 127, # Deliberately maximum velocity to test the limiter
    **kwargs,
) -> str:
    """
    Create Master Bus Brickwall Limiting (ReaLimit) in the current REAPER project.
    Generates a deliberately loud test track, then applies ReaLimit to the Master Bus.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the generated test track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the tracks and FX created.
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

    # === Step 2: Create a loud test track to trigger the limiter ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Increase track volume slightly to ensure we hit the limiter threshold
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 1.5)

    # Add a basic synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item for the test signal ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Build a simple loud chord progression (i - VI - III - VII)
    root_val = NOTE_MAP.get(key.capitalize(), 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Standard triad voicings from scale degrees
    chords = [
        [0, 2, 4], # Tonic
        [5, 7, 2], # Submediant (wrapped)
        [2, 4, 6], # Mediant
        [6, 1, 3]  # Subtonic (wrapped)
    ]
    
    note_count = 0
    ticks_per_quarter = 960
    
    for bar in range(bars):
        chord_idx = bar % len(chords)
        chord_degrees = chords[chord_idx]
        
        start_pos = bar * beats_per_bar
        end_pos = start_pos + beats_per_bar # Full whole note
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos * (60.0/bpm))
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos * (60.0/bpm))
        
        for degree in chord_degrees:
            # Map degree back to chromatic MIDI note using scale
            octave_shift = degree // len(scale_intervals)
            scale_idx = degree % len(scale_intervals)
            midi_pitch = root_val + scale_intervals[scale_idx] + (octave_shift * 12)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, midi_pitch, velocity_base, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Apply ReaLimit to the Master Track ===
    master_track = RPR.RPR_GetMasterTrack(0)
    
    # Add ReaLimit
    limit_idx = RPR.RPR_TrackFX_AddByName(master_track, "VST: ReaLimit (Cockos)", False, -1)
    if limit_idx >= 0:
        # Standard ReaLimit Parameters:
        # Param 0: Threshold (set to -6.0 dB to heavily squash our loud synth)
        # Param 1: Ceiling (set to -1.0 dB for streaming True Peak compliance)
        # Param 2: True peak (1.0 = enabled)
        RPR.RPR_TrackFX_SetParamNormalized(master_track, limit_idx, 0, 0.5) # Normalized approx -6dB
        RPR.RPR_TrackFX_SetParam(master_track, limit_idx, 0, -6.0) # Explicit dB value override
        
        RPR.RPR_TrackFX_SetParam(master_track, limit_idx, 1, -1.0) # Ceiling
        RPR.RPR_TrackFX_SetParam(master_track, limit_idx, 2, 1.0)  # True Peak On

    # Add Loudness Meter AFTER the Limiter to check compliance
    meter_idx = RPR.RPR_TrackFX_AddByName(master_track, "JS: Loudness Meter Peak/RMS/LUFS", False, -1)

    return f"Created test track '{track_name}' and applied ReaLimit (Threshold: -6dB, Ceiling: -1dBTP) to the Master Bus."
