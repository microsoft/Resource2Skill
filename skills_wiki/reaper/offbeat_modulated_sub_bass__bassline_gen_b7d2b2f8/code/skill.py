def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat Mod Sub Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create an Offbeat Modulated Sub Bass pattern in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Insert Pattern ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Octave 2 for Sub Bass (e.g., C2 = 36)
    base_midi = NOTE_MAP[key] + 24 
    ticks_per_quarter = 960
    notes_added = 0
    
    for bar in range(bars):
        for beat in range(beats_per_bar):
            # Calculate tick positions for 8th note offbeats (exactly halfway through the beat)
            start_tick = int((bar * beats_per_bar * ticks_per_quarter) + (beat * ticks_per_quarter) + (ticks_per_quarter / 2))
            end_tick = int(start_tick + (ticks_per_quarter / 4)) # 16th note duration for a short pluck
            
            # Algorithmic variation: Octave jump on the 4th beat of the bar
            note = base_midi
            if beat == 3:
                note = base_midi + 12 
                
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, note, velocity_base, False)
            notes_added += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design (ReaSynth Pluck) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure Timbre (Sine wave with a hint of triangle for upper harmonics)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.0)  # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.15) # Triangle mix
    
    # Configure Envelope (Fast attack, short decay, zero sustain - mimics "Sinus Pluck")
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.03)  # Decay (~snappy)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.0)   # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 9, 0.05)  # Release

    # === Step 5: Add Modulation (Chorus) ===
    # Emulates the Kilohearts BLENDZ effect for stereo width
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    if chorus_idx >= 0:
        # Lower the wet mix to keep the low end relatively stable while widening the harmonics
        RPR.RPR_TrackFX_SetParamNormalized(track, chorus_idx, 3, 0.3) # Wet mix

    return f"Created '{track_name}' with {notes_added} sequenced offbeat notes over {bars} bars at {bpm} BPM."
