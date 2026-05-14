def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Phase-Safe Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    split_freq: float = 120.0,
    **kwargs,
) -> str:
    """
    Create a Phase-Safe Stereo Bass crossover in the current REAPER project.
    Generates a parent folder with a Mono Sub track and a wide Stereo Top track.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        split_freq: The crossover frequency (Hz) where the bass becomes mono.
        **kwargs: Additional overrides.

    Returns:
        Status string.
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Setup pitch
    root_midi = NOTE_MAP.get(key, 4) + 24 # Deep bass register (e.g., E1)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    turnaround_idx = min(4, len(scale_intervals) - 1)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track Routing Structure ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # 2a. Parent Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    parent_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1) # Start folder

    # 2b. Child 1: Low Track (Mono)
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    low_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(low_track, "P_NAME", f"{track_name} Sub (Mono)", True)
    RPR.RPR_SetMediaTrackInfo_Value(low_track, "I_FOLDERDEPTH", 0)

    # 2c. Child 2: High Track (Stereo)
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    high_track = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(high_track, "P_NAME", f"{track_name} Top (Stereo)", True)
    RPR.RPR_SetMediaTrackInfo_Value(high_track, "I_FOLDERDEPTH", -1) # End folder

    # === Step 3: Generate MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Syncopated 16th note driving bass rhythm
    rhythm_pattern = [1, 0, 1, 1,  0, 1, 0, 1,  1, 1, 0, 1,  0, 1, 1, 0]
    note_len_sec = (60.0 / bpm) * 0.25 

    for track in [low_track, high_track]:
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for bar in range(bars):
            base_note = root_midi
            if bar % 4 == 3: # Modulate on the 4th bar turnaround
                base_note = root_midi + scale_intervals[turnaround_idx]
                
            for i, hit in enumerate(rhythm_pattern):
                if hit:
                    # Octave jumping for groove
                    note = base_note if (i % 4 == 0) else base_note + 12
                    
                    start_sec = (bar * bar_length_sec) + (i * note_len_sec)
                    end_sec = start_sec + (note_len_sec * 0.8) # Staccato envelope
                    
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                    
                    RPR.RPR_MIDI_InsertNote(
                        take, False, False,
                        start_ppq, end_ppq,
                        0, note, velocity_base, False
                    )
        RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design & Crossover FX ===

    # 4a. LOW TRACK: Sub Sine + Lowpass + Mono Force
    fx_synth_low = RPR.RPR_TrackFX_AddByName(low_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(low_track, fx_synth_low, 0, 1.0) # Volume
    RPR.RPR_TrackFX_SetParam(low_track, fx_synth_low, 1, 0.0) # Pure sine wave

    fx_eq_low = RPR.RPR_TrackFX_AddByName(low_track, "ReaEQ", False, -1)
    # Cut highs starting slightly above the crossover to isolate the sub
    RPR.RPR_TrackFX_SetParam(low_track, fx_eq_low, 3, split_freq)      # Band 2 Freq
    RPR.RPR_TrackFX_SetParam(low_track, fx_eq_low, 4, -120.0)          # Band 2 Gain (Cut)
    RPR.RPR_TrackFX_SetParam(low_track, fx_eq_low, 6, split_freq*1.5)  # Band 3 Freq
    RPR.RPR_TrackFX_SetParam(low_track, fx_eq_low, 7, -120.0)          # Band 3 Gain (Cut)
    RPR.RPR_TrackFX_SetParam(low_track, fx_eq_low, 9, split_freq*2.0)  # Band 4 Freq
    RPR.RPR_TrackFX_SetParam(low_track, fx_eq_low, 10, -120.0)         # Band 4 Gain (Cut)

    fx_mono = RPR.RPR_TrackFX_AddByName(low_track, "JS: Stereo Field", False, -1)
    if fx_mono >= 0:
        RPR.RPR_TrackFX_SetParam(low_track, fx_mono, 0, 0.0) # Width = 0% (Strict Mono)

    # 4b. HIGH TRACK: Buzzy Saw + Wide Stereo + Highpass
    fx_synth_high = RPR.RPR_TrackFX_AddByName(high_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(high_track, fx_synth_high, 0, 0.4) # Volume
    RPR.RPR_TrackFX_SetParam(high_track, fx_synth_high, 1, 1.0) # Sawtooth for harmonics
    RPR.RPR_TrackFX_SetParam(high_track, fx_synth_high, 2, 0.5) # Pulse Width

    fx_chorus = RPR.RPR_TrackFX_AddByName(high_track, "JS: Chorus", False, -1)
    # Default settings naturally create a wide, phasey stereo image

    fx_eq_high = RPR.RPR_TrackFX_AddByName(high_track, "ReaEQ", False, -1)
    # Highpass by dropping the low shelf
    RPR.RPR_TrackFX_SetParam(high_track, fx_eq_high, 0, split_freq) # Band 1 Freq
    RPR.RPR_TrackFX_SetParam(high_track, fx_eq_high, 1, -120.0)     # Band 1 Gain (Cut)

    return f"Created Phase-Safe crossover '{track_name}' (Mono < {split_freq}Hz, Stereo > {split_freq}Hz) over {bars} bars."
