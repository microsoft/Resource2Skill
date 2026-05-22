def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat Synth Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a driving offbeat 1/8th note synth bassline.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Music theory lookup for base pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate MIDI note for the bass register (Octave 2)
    root_pitch = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    bass_note = root_pitch + 36 

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
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Offbeat MIDI Notes ===
    qn_length_sec = 60.0 / bpm
    note_len_sec = qn_length_sec * 0.5  # 8th note duration
    
    note_count = 0
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        for beat in range(beats_per_bar):
            # Calculate the time for the "and" of the beat (0.5 beats offset)
            offbeat_start = bar_start_time + (beat * qn_length_sec) + (qn_length_sec * 0.5)
            offbeat_end = offbeat_start + note_len_sec
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, offbeat_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, offbeat_end)
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_note, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Synthesizer & Sound Design FX ===
    
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tune
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.8) # Square mix (hollow bass tone)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5) # Saw mix (adds bite)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0) # Triangle mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.0) # Extra Sine
    
    # Add Lowpass Filter to shape the tone into a bass
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Filters/resonantlowpass", False, -1)
    RPR.RPR_TrackFX_SetParam(track, filter_idx, 0, 800.0) # Frequency cutoff at 800Hz
    RPR.RPR_TrackFX_SetParam(track, filter_idx, 1, 0.2)   # Mild resonance

    return f"Created '{track_name}' with {note_count} offbeat notes over {bars} bars at {bpm} BPM."
