def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Scaffold",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Build-up to Drop arrangement featuring a rhythmic vacuum and an automated filter sweep.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base setup
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = max(8, bars) # Enforce at least 8 bars to demonstrate the transition
    
    root_val = NOTE_MAP.get(key.capitalize(), 0) + 48 # C3 base

    # Progression Logic
    is_minor = "minor" in scale.lower() or "dorian" in scale.lower() or "phrygian" in scale.lower()
    if is_minor:
        # i - VI - III - VII
        chords = [[0, 3, 7, -12], [-4, 0, 3, -16], [3, 7, 10, -9], [-2, 2, 5, -14]]
    else:
        # I - V - vi - IV
        chords = [[0, 4, 7, -12], [-5, -1, 2, -17], [-3, 0, 4, -15], [5, 9, 12, -7]]

    # Helper for MIDI insertion
    def insert_note(take, pitch, start_beat, duration_beats, vel):
        start_sec = start_beat * (60.0 / bpm)
        end_sec = (start_beat + duration_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # ==========================================
    # TRACK 1: CHORDS & FILTER SWEEP
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    tr_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_chords, "P_NAME", f"{track_name} - Chords", True)

    # Add thick synth
    fx_synth = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_chords, fx_synth, 7, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(tr_chords, fx_synth, 8, 0.8) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(tr_chords, fx_synth, 5, 0.6) # Release

    # Add EQ to act as Lowpass
    fx_eq = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaEQ", False, -1)
    # Param 10 is Band 4 (High Shelf) Gain. 0.0 normalized = -120dB.
    RPR.RPR_TrackFX_SetParamNormalized(tr_chords, fx_eq, 10, 0.0) 

    # Create MIDI Item
    item_chords = RPR.RPR_AddMediaItemToTrack(tr_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bar_length_sec * total_bars)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    # Insert Chords
    for bar in range(total_bars):
        chord = chords[bar % 4]
        start_b = bar * beats_per_bar
        for note_offset in chord:
            insert_note(take_chords, root_val + note_offset, start_b, 4.0, velocity_base - 15)

    # Filter Automation (Param 9 is Band 4 Frequency)
    env = RPR.RPR_GetFXEnvelope(tr_chords, fx_eq, 9, True)
    
    # Envelope shape indices: 0=Linear, 2=Slow start/end (Bezier-like)
    t_start = 0.0
    t_sweep_start = bar_length_sec * 2.0                 # Start sweeping at Bar 3
    t_sweep_deep = bar_length_sec * 4.0 - 0.05           # Hit lowest point just before the drop
    t_drop = bar_length_sec * 4.0                        # The Drop (Bar 5)
    t_end = bar_length_sec * total_bars

    RPR.RPR_InsertEnvelopePoint(env, t_start, 1.0, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, t_sweep_start, 1.0, 2, 0.0, False, True) 
    RPR.RPR_InsertEnvelopePoint(env, t_sweep_deep, 0.2, 0, 0.0, False, True) 
    RPR.RPR_InsertEnvelopePoint(env, t_drop, 1.0, 0, 0.0, False, True)        
    RPR.RPR_InsertEnvelopePoint(env, t_end, 1.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    # ==========================================
    # TRACK 2: DRUMS & RHYTHMIC VACUUM
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    tr_drums = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_drums, "P_NAME", f"{track_name} - Drums", True)

    # Add quick percussive synth placeholder to make the MIDI audible
    fx_drum_synth = RPR.RPR_TrackFX_AddByName(tr_drums, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_drums, fx_drum_synth, 3, 0.05) # Fast decay
    RPR.RPR_TrackFX_SetParamNormalized(tr_drums, fx_drum_synth, 4, 0.0)  # No sustain

    item_drums = RPR.RPR_AddMediaItemToTrack(tr_drums)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_LENGTH", bar_length_sec * total_bars)
    take_drums = RPR.RPR_AddTakeToMediaItem(item_drums)

    kick, snare, hat = 36, 38, 42

    for bar in range(total_bars):
        start_b = bar * beats_per_bar

        if bar == 3: # Bar 4: The Transition "Vacuum"
            insert_note(take_drums, kick, start_b, 0.25, velocity_base)
            insert_note(take_drums, snare, start_b + 1, 0.25, velocity_base)
            insert_note(take_drums, hat, start_b, 0.125, velocity_base - 20)
            insert_note(take_drums, hat, start_b + 0.5, 0.125, velocity_base - 20)
            insert_note(take_drums, hat, start_b + 1, 0.125, velocity_base - 20)
            # INTENTIONAL SILENCE: Beats 3 and 4 are empty to create contrast
        else:
            # Normal Beat
            insert_note(take_drums, kick, start_b, 0.25, velocity_base)
            insert_note(take_drums, kick, start_b + 2.5, 0.25, velocity_base)
            insert_note(take_drums, snare, start_b + 1, 0.25, velocity_base)
            insert_note(take_drums, snare, start_b + 3, 0.25, velocity_base)
            for beat in range(8):
                insert_note(take_drums, hat, start_b + (beat * 0.5), 0.125, velocity_base - 25)

    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created Arrangement Scaffold (Filter Sweep + Vacuum Drop) over {total_bars} bars at {bpm} BPM in {key} {scale}."
