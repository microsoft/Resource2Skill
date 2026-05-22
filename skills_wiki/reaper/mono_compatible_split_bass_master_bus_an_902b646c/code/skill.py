def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Split_Bass_Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a Mono-Compatible Split Bass and Spectrum Analyzer setup in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR

    # Set tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Note map and scales for MIDI generation
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Base octave for sub bass (C2 = 36)
    base_pitch = 36 + root_val

    # Helper function to add MIDI notes
    def add_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === TRACK CREATION & ROUTING ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # 1. Create Parent Folder (Bus & Analyzer)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    bus_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1) # Start folder
    RPR.RPR_TrackFX_AddByName(bus_track, "Frequency Spectrum Analyzer Meter", False, -1)

    # 2. Create Child Track 1 (Sub Bass - Mono)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    sub_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(sub_track, "P_NAME", "Sub_Bass_Mono", True)
    
    # Setup Sub FX: Sine Wave + Lowpass
    fx_synth_sub = RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(sub_track, fx_synth_sub, 2, 0.0) # Sawtooth mix 0%
    fx_eq_sub = RPR.RPR_TrackFX_AddByName(sub_track, "3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(sub_track, fx_eq_sub, 1, -120.0) # Mid Gain cut
    RPR.RPR_TrackFX_SetParam(sub_track, fx_eq_sub, 2, -120.0) # High Gain cut
    RPR.RPR_TrackFX_SetParam(sub_track, fx_eq_sub, 3, 120.0)  # Low-Mid Crossover Hz

    # 3. Create Child Track 2 (Mid Bass - Stereo)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 2, True)
    wide_track = RPR.RPR_GetTrack(0, num_tracks + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(wide_track, "P_NAME", "Mid_Bass_Wide", True)
    RPR.RPR_SetMediaTrackInfo_Value(wide_track, "I_FOLDERDEPTH", -1) # End folder
    
    # Setup Wide FX: Saw Wave + Highpass + Stereo Width
    fx_synth_wide = RPR.RPR_TrackFX_AddByName(wide_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(wide_track, fx_synth_wide, 2, 1.0) # Sawtooth mix 100%
    fx_eq_wide = RPR.RPR_TrackFX_AddByName(wide_track, "3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(wide_track, fx_eq_wide, 0, -120.0) # Low Gain cut
    RPR.RPR_TrackFX_SetParam(wide_track, fx_eq_wide, 3, 120.0)  # Low-Mid Crossover Hz
    RPR.RPR_TrackFX_AddByName(wide_track, "Chorus", False, -1)

    # === MIDI GENERATION ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    
    # Create items on both child tracks
    item_sub = RPR.RPR_AddMediaItemToTrack(sub_track)
    item_wide = RPR.RPR_AddMediaItemToTrack(wide_track)
    
    for item in [item_sub, item_wide]:
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_sec * bars)
        
    take_sub = RPR.RPR_AddTakeToMediaItem(item_sub)
    take_wide = RPR.RPR_AddTakeToMediaItem(item_wide)

    # Driving 1/8th and 1/16th syncopated bassline pattern
    note_count = 0
    for bar in range(bars):
        bar_offset = bar * bar_sec
        
        # Define rhythm in beats (1/4 = 1.0, 1/8 = 0.5, 1/16 = 0.25)
        # Sequence: Root(0) -> Root(0.5) -> Octave(1.5) -> Third(2.5) -> Fifth(3.0)
        pattern = [
            (0.0, 0.45, 0),                       # Beat 1
            (0.5, 0.95, 0),                       # Beat 1 &
            (1.5, 1.95, 12),                      # Beat 2 & (Octave jump)
            (2.5, 2.95, scale_intervals[2]),      # Beat 3 & (Third)
            (3.0, 3.45, scale_intervals[4]),      # Beat 4
            (3.5, 3.95, scale_intervals[4] - 12)  # Beat 4 & (Fifth, lower octave)
        ]
        
        for start_beat, end_beat, pitch_offset in pattern:
            pitch = base_pitch + pitch_offset
            start_t = bar_offset + (start_beat * beat_sec)
            end_t = bar_offset + (end_beat * beat_sec)
            
            add_note(take_sub, start_t, end_t, pitch, velocity_base)
            add_note(take_wide, start_t, end_t, pitch, velocity_base - 10)
            note_count += 1

    # Force MIDI UI update
    RPR.RPR_MIDI_Sort(take_sub)
    RPR.RPR_MIDI_Sort(take_wide)

    return f"Created Split Bass Bus with {note_count} notes over {bars} bars at {bpm} BPM. A stock Spectrum Analyzer has been placed on the parent folder to monitor mono compatibility."
