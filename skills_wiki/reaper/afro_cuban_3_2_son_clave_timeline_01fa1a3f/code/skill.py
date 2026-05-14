def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "3-2 Son Clave",
    bpm: int = 100,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a foundational 3-2 Son Clave rhythm track.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused for unpitched percussion, but accepted per signature).
        scale: Scale type (unused for unpitched percussion).
        bars: Number of bars to generate (should ideally be an even number for full phrases).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    item_length_sec = beat_len_sec * beats_per_bar * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 3-2 Son Clave rhythm pattern defined in beats relative to a 2-bar sequence
    # Bar 1 (3 side): Beats 1.0, 2.5 (2 AND), 4.0
    # Bar 2 (2 side): Beats 2.0, 3.0 (which are 5.0 and 6.0 relatively)
    clave_pattern_beats = [0.0, 1.5, 3.0, 5.0, 6.0]

    pitch = 75     # General MIDI note for Claves
    channel = 9    # MIDI Channel 10 (0-indexed = 9) for drums
    notes_added = 0

    # Generate the pattern across the requested number of bars
    for bar_pair in range(0, bars, 2):
        offset_beats = bar_pair * beats_per_bar
        for b in clave_pattern_beats:
            absolute_beat = offset_beats + b
            
            # Ensure we don't write notes past the requested total bars
            if absolute_beat < (bars * beats_per_bar):
                # Calculate project time in seconds for conversion
                start_time_sec = absolute_beat * beat_len_sec
                # 16th note duration
                end_time_sec = start_time_sec + (beat_len_sec * 0.25)
                
                # Convert time to PPQ
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
                
                # Slightly emphasize the very first downbeat of the 3-side
                vel = velocity_base + 10 if b == 0.0 else velocity_base
                vel = min(127, vel)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, channel, pitch, vel, True)
                notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design (Fallback Synth Clave) ===
    # Add a stock synthesizer to ensure it makes a percussive click 
    # even if no dedicated drum VST is loaded.
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Shape the ReaSynth envelope to act like a struck block of wood
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume: -6dB
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)   # Square mix: Adds "wooden" odd harmonics
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0)   # Attack: 0 ms (sharp transient)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.05)  # Decay: very short
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.0)   # Sustain: 0
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.05)  # Release: very short

    return f"Created '{track_name}' with {notes_added} clave strikes over {bars} bars at {bpm} BPM."
