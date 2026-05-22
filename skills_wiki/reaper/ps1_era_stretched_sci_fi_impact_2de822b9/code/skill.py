def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "PS1_SciFi_Impact",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 120,
    **kwargs,
) -> str:
    """
    Create a PS1-Era Stretched Sci-Fi Impact in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the stretched impact will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Calculate Timing ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    # Calculate deep root note (Octave 1 range for heavy pitch-down effect)
    root_midi = SCALES[scale][0] + NOTE_MAP[key] + 24 
    
    # Dissonant, complex cluster mimicking layered metallic/explosion samples
    pitches = [
        root_midi,               # Bass fundamental 
        root_midi + 1,           # Minor 2nd (crunch/dissonance)
        root_midi + 7,           # Power fifth
        root_midi + 12           # Octave overtone
    ]
    
    for pitch in pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain for Sound Design & Stretch Artifacts ===
    
    # 1. ReaSynth (Raw generated wave)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.1) # Attack (slowed transient)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.9) # Release (artificially long stretch)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.6) # Square wave mix for harshness
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.4) # Saw wave mix

    # 2. ReaDelay (Simulates granular/windowing artifacts from older time stretch algorithms)
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 0, 0.01) # Ultra short time (~20ms) -> comb filtering
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 1, 0.7)  # Heavy feedback
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_idx, 2, 0.5)  # Wet mix

    # 3. ReaVerberate (Simulates the stretched, massive reverb tail)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerberate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.8)   # Wet mix (very high)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 0.4)   # Dry mix
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 2, 0.98)  # Room size (gargantuan)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 3, 0.85)  # Dampening (dark/muffled tail)

    # 4. ReaEQ (Simulates high-frequency loss associated with extreme sample slow-down)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 in ReaEQ is typically the High Shelf. We lower the gain substantially.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.1)    # High Shelf Gain cut

    return f"Created '{track_name}': A massive, stretched {bars}-bar sci-fi impact in {key} {scale} at {bpm} BPM."
