def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Programmed Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Specifically lowered from 127 to remove harshness
    **kwargs,
) -> str:
    """
    Create a Metal Kick-Locked Bassline with Octave Fills in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (not heavily used as this relies on the root note).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), defaults to 110 to tame VST attack.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Note Map for root pitch (Base Octave 1 for bass)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root MIDI note. Octave 1 starting at C1 = 24
    root_pitch = 24 + NOTE_MAP.get(key, 0)
    octave_pitch = root_pitch + 12 # 12th fret jump

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
    
    # Standard PPQ in REAPER is typically 960 per quarter note
    ppq_per_quarter = 960
    ppq_per_16th = ppq_per_quarter // 4
    
    # Rhythmic Pattern: 1 = Root note, 2 = Octave note, 0 = Rest
    # This simulates a complex syncopated double-kick pattern
    # 16 steps per bar (16th notes)
    kick_syncopation = [
        1, 0, 0, 1,   0, 0, 1, 1,   0, 1, 0, 0,   1, 0, 0, 0, # Bar 1
        1, 0, 0, 1,   0, 0, 1, 1,   0, 1, 0, 0,   1, 0, 0, 0, # Bar 2
        1, 0, 0, 1,   0, 0, 1, 1,   0, 1, 0, 0,   1, 0, 0, 0, # Bar 3
        1, 0, 0, 1,   0, 0, 2, 2,   0, 2, 0, 0,   2, 0, 0, 0, # Bar 4: Break/Fill with 12th fret jumps
    ]
    
    # Ensure pattern length matches requested bars
    full_pattern = kick_syncopation * (bars // 4 + 1)
    
    # === Step 4: Insert MIDI Notes ===
    for bar in range(bars):
        for step in range(16):
            pattern_idx = (bar * 16 + step) % len(kick_syncopation)
            hit_type = kick_syncopation[pattern_idx]
            
            if hit_type > 0:
                pitch = octave_pitch if hit_type == 2 else root_pitch
                
                # Make notes slightly staccato (length = 80% of a 16th note)
                start_ppq = (bar * 4 * ppq_per_quarter) + (step * ppq_per_16th)
                end_ppq = start_ppq + int(ppq_per_16th * 0.8)
                
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    False,          # muted
                    start_ppq,      # start_ppqpos
                    end_ppq,        # end_ppqpos
                    0,              # channel
                    pitch,          # pitch
                    velocity_base,  # velocity (110 limits harshness)
                    True            # noSort
                )
    
    # Sort notes after all insertions
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Placeholder FX (ReaSynth) ===
    # Configure ReaSynth to sound like a low, filtered bass
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for heavy bass response
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)    # Volume (0.0 = 0dB approx)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)    # Tuning (no shift)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.8)    # Square mix (0-1) for grit
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.5)    # Saw mix (0-1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.1)    # Lowpass filter cutoff (roll off highs to emulate 'velocity taming')

    return f"Created '{track_name}' locked to kick with octave fills over {bars} bars at {bpm} BPM. Max velocity set to {velocity_base}."
