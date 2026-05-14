def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Reese Bass (Stock)",
    bpm: int = 140,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a continuous, evolving Reese Bass pattern with a custom stock FX synthesis chain.
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

    if key not in NOTE_MAP or scale not in SCALES:
        return "Error: Invalid key or scale provided."

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Build the Reese Synthesis FX Chain ===
    
    # 1. ReaSynth (Raw Sawtooth Wave)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.3)  # Portamento (glide for legato)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 1.0)  # Saw mix (The core of the Reese)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.0)  # Triangle mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.1)  # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 10, 0.4) # Release

    # 2. JS: Chorus (Emulates Serum's 'Unison' by creating detuned copies)
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus_idx, 0, 0.5) # Delay length
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 1, 4.0)           # Voices (Unison count)
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus_idx, 2, 0.4) # Rate (Wobble speed)
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus_idx, 3, 0.6) # Depth (Detune amount)
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus_idx, 4, 0.8) # Wet mix

    # 3. JS: Distortion (Emulates the Tube Distortion step)
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, dist_idx, 0, 0.6)   # Drive (approx 60% as in tutorial)
    RPR.RPR_TrackFX_SetParamNormalized(track, dist_idx, 1, 0.5)   # Gain

    # 4. JS: 4-Pole Filter (Emulates the MG Low 12 Filter)
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: 4-Pole Filter", False, -1)
    RPR.RPR_TrackFX_SetParam(track, filter_idx, 0, 350.0)         # Cutoff Freq (Hz) - keeps it dark
    RPR.RPR_TrackFX_SetParamNormalized(track, filter_idx, 1, 0.2) # Resonance (20% as in tutorial)

    # === Step 4: Create Legato MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "B_STARTOFFS", 0.0)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_PLAYRATE", 1.0)
    
    # Calculate scale notes
    root_midi = NOTE_MAP[key] + 24 # Octave 1/2 for deep bass
    scale_intervals = SCALES[scale]
    
    # Standard dark Reese progression degrees: i - VI - iv - V
    progression_degrees = [0, 5, 3, 4] 
    
    note_count = 0
    for i in range(bars):
        degree_idx = progression_degrees[i % len(progression_degrees)]
        
        # Calculate pitch and keep it in bounds (wrap octave if needed)
        octave_shift = 0
        if degree_idx >= len(scale_intervals):
            octave_shift = 12
            degree_idx = degree_idx % len(scale_intervals)
            
        pitch = root_midi + scale_intervals[degree_idx] + octave_shift
        
        # Exact timing (QN = Quarter Notes)
        start_qn = i * beats_per_bar
        # Slightly overlap notes (+0.1 QN) to ensure portamento/legato triggers smoothly
        end_qn = start_qn + beats_per_bar + 0.1 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(
            take, 
            False,   # selected
            False,   # muted
            start_ppq, 
            end_ppq, 
            0,       # channel
            pitch, 
            velocity_base, 
            False    # noSort
        )
        note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} legato bass notes over {bars} bars at {bpm} BPM, using a custom Sawtooth + Unison + Distortion FX chain."
