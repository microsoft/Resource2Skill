def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Reese Bass",
    bpm: int = 140,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a dark, detuned Reese Bass foundation using native REAPER plugins.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Media Item and Take ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    item_length_sec = beat_len_sec * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate MIDI Progression (i - VI - VII) ===
    # Using Octave 1 (MIDI 24+) for deep sub/bass register
    root_midi = NOTE_MAP.get(key, 4) + 24 
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Define sequence: (scale_degree, start_beat, length_in_beats)
    # Default is a 4-bar dark progression
    sequence = [
        (0, 0, 8),    # Bars 1 & 2: Root note (i)
        (5, 8, 4),    # Bar 3: 6th note (VI)
        (6, 12, 4)    # Bar 4: 7th note (VII)
    ]
    
    note_count = 0
    for degree, start_beat, length_beats in sequence:
        # Wrap degree to scale length
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        pitch = root_midi + scale_intervals[scale_idx] + (octave_shift * 12)
        
        # Calculate timing in Pulses Per Quarter Note (PPQ)
        start_ppq = start_beat * 960
        # Add 0.2 beats of overlap to trigger Legato/Portamento glide in ReaSynth
        end_ppq = (start_beat + length_beats + 0.2) * 960
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False,
            start_ppq, end_ppq,
            0, int(pitch), int(velocity_base), False
        )
        note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain for Reese Bass Sound ===
    # 1. ReaSynth (Sawtooth core)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 7, 0.0) # Turn off default Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 8, 1.0) # Turn on Sawtooth mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.2) # Add Portamento for glides
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 6, 0.1) # Short release

    # 2. JS: Chorus (Creates the detuned, wide "Reese" phase beating)
    fx_chorus = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    # Default settings usually provide a good stereo spread, 
    # but we ensure it's active.
    
    # 3. JS: Saturation (Adds the 1972 vintage grit and harmonics)
    fx_sat = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_sat, 0, 45.0) # Set Amount (%) to drive the bass

    return f"Created '{track_name}' (Reese Bass) with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
