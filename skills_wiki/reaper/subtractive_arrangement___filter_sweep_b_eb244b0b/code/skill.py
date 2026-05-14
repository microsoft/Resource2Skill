def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Intro Filter Build",
    bpm: int = 125,
    key: str = "E",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Subtractive Arrangement & Filter Sweep Build in the current REAPER project.
    Generates a chord progression with an automated low-pass filter that opens up over time,
    and concludes with a 1-beat silence to anticipate a drop.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total length of the build-up.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    beat_length_sec = 60.0 / bpm
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "B_PPQN", 960)
    
    # Calculate pitches
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Base octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_chord(degree):
        """Generates a diatonic triad based on the scale degree."""
        chord_pitches = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            idx = int((degree + i) % len(scale_intervals))
            octave = int((degree + i) // len(scale_intervals))
            chord_pitches.append(root_pitch + scale_intervals[idx] + (octave * 12))
        return chord_pitches
    
    # Standard i - VI - III - VII progression
    prog_degrees = [0, 5, 2, 6]
    # Ensure degrees map cleanly to scales of varying lengths (e.g. pentatonic)
    progression = [d % len(scale_intervals) for d in prog_degrees]
    bars_per_chord = bars / len(progression) 
    
    for i, degree in enumerate(progression):
        start_sec = i * bars_per_chord * bar_length_sec
        
        # Core Pattern Execution: Truncate the final chord by 1 beat to create a drop pause
        if i == len(progression) - 1:
            end_sec = (i + 1) * bars_per_chord * bar_length_sec - beat_length_sec
        else:
            end_sec = (i + 1) * bars_per_chord * bar_length_sec
            
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        chord = get_chord(degree)
        for pitch in chord:
            # Keep pitch within safe MIDI bounds
            safe_pitch = max(0, min(127, pitch))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, safe_pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Sound Design & FX ===
    # Add Synth Pad
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.1) # Attack (swell)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.1) # Release (tail)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0) # Square mix off
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 1.0) # Saw mix on
    
    # Add Lowpass Filter
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Filters/resonantlowpass", False, -1)
    
    # === Step 5: Automation (The Sweep) ===
    # Get envelope for Cutoff (Param 0), create=True
    env = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)
    if env:
        # Start muffled (0.05 normalized value)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.05, 0, 0.0, False, True)
        # Sweep to fully open (1.0 normalized value) precisely at the drop pause
        RPR.RPR_InsertEnvelopePoint(env, item_length - beat_length_sec, 1.0, 0, 0.0, False, True)
        # Hold open through the pause
        RPR.RPR_InsertEnvelopePoint(env, item_length, 1.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' build-up over {bars} bars in {key} {scale} at {bpm} BPM with automated filter sweep and 1-beat drop pause."
