def create_pattern(
    project_name: str = "Arrangement Transition",
    track_name: str = "Inst Bus (Filtered)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a pre-drop transition pattern (Low-Pass Filter Sweep + Pitch Riser) 
    in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the main instrumental track getting filtered.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Total length of the section; the transition happens in the FINAL bar.
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === 1. Setup Project & Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    total_len = bars * bar_len
    sweep_start_time = (bars - 1) * bar_len
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }
    
    root_midi = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_note_in_scale(degree):
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_midi + (octave * 12) + scale_intervals[idx]

    # === 2. Create Target Instrumental Track (The Chords) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)

    # Add Synths and EQ
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)

    # Insert MIDI Item
    item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Generate basic 4-bar progression (i - VI - III - VII)
    chord_degrees = [0, 5, 2, 4]
    for i in range(bars):
        start_time = i * bar_len
        end_time = start_time + bar_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        degree = chord_degrees[i % len(chord_degrees)]
        
        for offset in [0, 2, 4]: # Build triad
            note = get_note_in_scale(degree + offset)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)

    # Automate EQ: Turn Band 4 (High Shelf) into a Low-Pass Cut
    # Param 10 is Band 4 Gain. Setting to 0.0 effectively creates a steep cut.
    RPR.RPR_TrackFX_SetParam(chords_track, eq_idx, 10, 0.0) 
    
    # Param 9 is Band 4 Frequency. Create Envelope for automation.
    env = RPR.RPR_GetFXEnvelope(chords_track, eq_idx, 9, True)
    
    # Insert Automation Points (Shape 2 = Parabolic curve "Slow start/end")
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0.0, False, True)                   # Fully open at start
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time, 1.0, 2, 0.0, False, True)      # Begin curve at final bar
    RPR.RPR_InsertEnvelopePoint(env, total_len, 0.15, 0, 0.0, False, True)            # Drop to ~15% freq exactly at section end
    RPR.RPR_Envelope_SortPoints(env)

    # === 3. Create Custom Tension Riser Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    riser_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(riser_track, "P_NAME", "Pre-Drop Riser", True)

    # Add Riser Synth and Reverb (for the spill-over tail)
    rs_idx = RPR.RPR_TrackFX_AddByName(riser_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(riser_track, rs_idx, 1, 0.5) # Tuning
    RPR.RPR_TrackFX_SetParam(riser_track, rs_idx, 4, 1.0) # Saw shape for buzz/noise

    rv_idx = RPR.RPR_TrackFX_AddByName(riser_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(riser_track, rv_idx, 0, 0.8) # High Wet
    RPR.RPR_TrackFX_SetParam(riser_track, rv_idx, 1, 0.2) # Low Dry
    RPR.RPR_TrackFX_SetParam(riser_track, rv_idx, 2, 0.9) # Huge Room Size

    # Insert Riser MIDI Item (Exists ONLY during the final bar)
    riser_item = RPR.RPR_AddMediaItemToTrack(riser_track)
    RPR.RPR_SetMediaItemInfo_Value(riser_item, "D_POSITION", sweep_start_time)
    RPR.RPR_SetMediaItemInfo_Value(riser_item, "D_LENGTH", bar_len)
    
    # Smooth Volume Swell using item Fade-In (as done visually in the tutorial)
    RPR.RPR_SetMediaItemInfo_Value(riser_item, "D_FADEINLEN", bar_len)
    
    riser_take = RPR.RPR_AddTakeToMediaItem(riser_item)
    r_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, sweep_start_time)
    r_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, total_len)

    # Insert a dissonant high cluster to simulate tension noise
    for n in [84, 85, 86]: 
        RPR.RPR_MIDI_InsertNote(riser_take, False, False, r_start_ppq, r_end_ppq, 0, n, 100, False)

    # Insert MIDI Pitch Bend sweep (Channel 0, Msg 0xE0)
    steps = 64
    ppq_step = (r_end_ppq - r_start_ppq) / steps
    for s in range(steps):
        current_ppq = r_start_ppq + (s * ppq_step)
        # Sweep from center pitch (8192) to max pitch (16383)
        val = int(8192 + (s / (steps - 1)) * 8191)
        msg2 = val & 0x7F         # LSB
        msg3 = (val >> 7) & 0x7F  # MSB
        RPR.RPR_MIDI_InsertCC(riser_take, False, False, current_ppq, 224, 0, msg2, msg3)

    return f"Created Filter Sweep on '{track_name}' and added a 'Pre-Drop Riser' to build tension over the final bar at {bpm} BPM."
