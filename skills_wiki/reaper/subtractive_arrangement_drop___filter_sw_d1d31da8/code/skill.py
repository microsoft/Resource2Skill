def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement_Transition",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Subtractive Drop & Filter Sweep Transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars (must be at least 4 to hear the transition).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Setup basic timing
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bps = bpm / 60.0
    beat_len = 1.0 / bps
    bar_len = beat_len * beats_per_bar
    total_length = bar_len * bars

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_idx = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Deriving chord 1 (i) and chord 2 (v)
    base_octave = 48 # C3
    chord_1 = [
        base_octave + root_idx, 
        base_octave + root_idx + scale_intervals[2], 
        base_octave + root_idx + scale_intervals[4]
    ]
    chord_2 = [
        base_octave + root_idx + scale_intervals[4], 
        base_octave + root_idx + scale_intervals[6] - (12 if scale_intervals[6]>7 else 0), 
        base_octave + root_idx + scale_intervals[1] + 12
    ]

    # Helper function for MIDI notes
    def add_midi_note(take, proj_start, proj_end, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_end)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === TRACK 1: DRUMS ===
    drum_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Generate Arrangement pattern
    drop_bar = 4 # The transition happens at the start of bar 5 (index 4)

    for bar in range(bars):
        bar_start = bar * bar_len
        
        # 1. RHYTHMIC HALFTIME HI-HATS
        if bar < drop_bar:
            hat_steps = 8 # 1/8th notes for the Chorus
        else:
            hat_steps = 4 # 1/4 notes for the Verse (Halftime feel)
            
        for step in range(hat_steps):
            step_time = bar_start + step * (bar_len / hat_steps)
            add_midi_note(drum_take, step_time, step_time + 0.1, 42, velocity_base - 20)
            
        # 2. SNARE (Standard backbeat on 2 and 4)
        add_midi_note(drum_take, bar_start + beat_len * 1, bar_start + beat_len * 1 + 0.2, 38, velocity_base)
        add_midi_note(drum_take, bar_start + beat_len * 3, bar_start + beat_len * 3 + 0.2, 38, velocity_base)
        
        # 3. SUBTRACTIVE KICK DROP
        if bar != drop_bar: 
            # Normal beat 1 kick. We SKIP this on the drop bar!
            add_midi_note(drum_take, bar_start, bar_start + 0.2, 36, velocity_base + 10)
            
        # Kicks on 2.5 and 3
        add_midi_note(drum_take, bar_start + beat_len * 1.5, bar_start + beat_len * 1.5 + 0.2, 36, velocity_base - 10)
        add_midi_note(drum_take, bar_start + beat_len * 2.0, bar_start + beat_len * 2.0 + 0.2, 36, velocity_base)

    RPR.RPR_MIDI_Sort(drum_take)


    # === TRACK 2: SYNTH PAD & FILTER AUTOMATION ===
    synth_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(synth_track_idx, True)
    synth_track = RPR.RPR_GetTrack(0, synth_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", f"{track_name}_Pad", True)

    # Add Instrument & EQ
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(synth_track, "ReaEQ", False, -1)

    synth_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_LENGTH", total_length)
    synth_take = RPR.RPR_AddTakeToMediaItem(synth_item)

    # Add basic chords
    for bar in range(0, bars, 2):
        chord = chord_1 if (bar % 4) == 0 else chord_2
        bar_start = bar * bar_len
        chord_end = bar_start + (bar_len * 2) - 0.1
        for pitch in chord:
            add_midi_note(synth_take, bar_start, chord_end, pitch, velocity_base - 30)
            
    RPR.RPR_MIDI_Sort(synth_take)

    # 4. FILTER SWEEP AUTOMATION (Using ReaEQ Band 4 Gain to simulate High Cut)
    # Param 10 in ReaEQ is Band 4 Gain. 0.5 is 0dB (flat). 0.0 is -inf (cut).
    env = RPR.RPR_GetFXEnvelope(synth_track, eq_idx, 10, True)
    
    if env and drop_bar < bars:
        sweep_start = (drop_bar - 1) * bar_len      # Start cutting 1 bar before the drop
        sweep_end = drop_bar * bar_len - 0.05       # Deepest cut right before the downbeat
        snap_back = drop_bar * bar_len              # Snap back to flat on the downbeat

        # InsertEnvelopePoint(env, time, value, shape, tension, selected, noSort)
        # Shape 5 = Bezier curve (for that classic accelerating 'suck out' riser shape)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.5, 0, 0.0, False, False)
        RPR.RPR_InsertEnvelopePoint(env, sweep_start, 0.5, 5, -0.5, False, False)
        RPR.RPR_InsertEnvelopePoint(env, sweep_end, 0.0, 0, 0.0, False, False)
        RPR.RPR_InsertEnvelopePoint(env, snap_back, 0.5, 0, 0.0, False, False)
        RPR.RPR_Envelope_SortPoints(env)

    RPR.RPR_UpdateArrange()

    return f"Created subtractive drop & filter transition at Bar {drop_bar+1} across 2 tracks at {bpm} BPM."
