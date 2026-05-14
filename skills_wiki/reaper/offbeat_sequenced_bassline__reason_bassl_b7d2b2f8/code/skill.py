def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat Sequenced Bass",
    bpm: int = 138,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a driving offbeat bassline sequence.
    Mimics the output of the 'OffBeat' Bassline Generator driving a plucky synth.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (138 is standard for this style).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Add FX Chain (Sound Design) ===
    # 1. Synthesizer (ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, 1)
    if synth_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.5)   # Volume
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Tuning
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 1.0)   # Square mix (Thick bottom end)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.8)   # Saw mix (Buzzy top end)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)   # Triangle mix
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.01)  # Attack (Very fast)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.15)  # Decay (Short/Plucky)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.0)   # Sustain (None)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.1)   # Release
        
    # 2. Saturation (JS: Saturation) to mimic the "Stacked" aggressive tone
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, 1)
    if sat_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, sat_idx, 0, 30.0)    # Drive amount
        
    # 3. EQ (ReaEQ) to darken the tone, acting like a lowpass filter
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, 1)
    if eq_idx >= 0:
        # Lowering the high-shelf (Band 4) to tame the raw synth highs
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 800)      # Band 4 Freq (Hz)
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, -20.0)   # Band 4 Gain (dB)
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, 1.0)     # Band 4 Q

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate base pitch (C2 range for bass)
    root_val = NOTE_MAP.get(key.upper(), 0)
    octave_base = 36 # C2
    base_pitch = octave_base + root_val
    
    # Note length is a 1/16th note
    note_length_sec = (60.0 / bpm) * 0.25 
    
    note_count = 0
    
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        
        for beat in range(4):
            # The offbeat (the "and") is exactly halfway through the beat
            offbeat_offset = (60.0 / bpm) * 0.5
            
            note_start = bar_start_time + (beat * (60.0 / bpm)) + offbeat_offset
            note_end = note_start + note_length_sec
            
            # Sequencer flair: jump up an octave on the last beat of the bar
            pitch = base_pitch + 12 if beat == 3 else base_pitch
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start), 
                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end), 
                0, pitch, velocity_base, False
            )
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_GetSetMediaItemInfo_String(item, "P_NOTES", "Offbeat Sequence", True)
    
    return f"Created '{track_name}' with {note_count} offbeat sequencer notes over {bars} bars at {bpm} BPM"
