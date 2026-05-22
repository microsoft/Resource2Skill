def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "808 Sub Bass",
    bpm: int = 140,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a synthesized 808 Sub Bass patch and pattern using native REAPER plugins.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (130-150 recommended).
        key: Root note (F or G recommended for sub bass).
        scale: Scale type (e.g., minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

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
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Sound Design (ReaSynth + Saturation) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for an 808 sound
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.6)    # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5)    # Tuning (Center)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.0)    # Attack (Instant for punch)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.2)    # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.4)    # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.1)    # Release
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.03)   # Portamento (Subtle glide)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 1.0)    # Sine mix (Fundamental)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.0)    # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 9, 0.0)    # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 10, 0.15)  # Triangle mix (Adds upper harmonics)

    # Add Saturation to thicken the tone
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    if sat_idx >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, sat_idx, 0, 0.4)  # Saturation Amount (40%)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    item_length = beat_length_sec * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate root note in a very low octave (Octave 1)
    # C1 is MIDI 24. F1 is MIDI 29.
    root_midi = NOTE_MAP.get(key, 0) + 24 
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # 2-bar syncopated trap bass pattern
    # Format: (beat_start_position, duration_in_beats, scale_degree_index, octave_offset)
    pattern = [
        (0.0, 1.0, 0,  0),  # Beat 1: Root
        (1.5, 0.5, 0,  0),  # Beat 2 "and": Root
        (2.0, 1.0, 2,  0),  # Beat 3: 3rd degree
        (3.0, 1.0, 4,  0),  # Beat 4: 5th degree
        (4.0, 1.0, 0,  0),  # Bar 2 Beat 1: Root
        (5.5, 0.5, 0,  0),  # Bar 2 Beat 2 "and": Root
        (6.5, 0.5, 6, -1),  # Bar 2 Beat 3 "and": 7th degree (dropped one octave)
        (7.0, 1.0, 0,  0)   # Bar 2 Beat 4: Root
    ]

    note_count = 0
    # Loop the 2-bar pattern across the requested number of bars
    for bar_pair in range(0, bars, 2):
        base_beat = bar_pair * 4
        
        for beat_pos, duration, scale_idx, oct_offset in pattern:
            if base_beat + beat_pos >= bars * 4:
                continue
            
            # Calculate final MIDI pitch
            interval = scale_intervals[scale_idx % len(scale_intervals)]
            pitch = root_midi + interval + (oct_offset * 12)
            
            # Calculate precise start and end times
            start_time = (base_beat + beat_pos) * beat_length_sec
            end_time = start_time + (duration * beat_length_sec)
            
            start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
            end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            # Insert the MIDI note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with native 808 synth patch and {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
