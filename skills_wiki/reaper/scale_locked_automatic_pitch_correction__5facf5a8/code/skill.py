def create_pattern(
    project_name: str = "TuningDemo",
    track_name: str = "Tuned Synth Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    attack_ms: float = 0.0,  # 0.0 for robotic/T-Pain effect, 100.0 for natural
    **kwargs,
) -> str:
    """
    Creates a track with a pitch-bending synthesizer fed into ReaTune, configured 
    to automatically snap pitches back to the specified key and scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        attack_ms: Attack time for pitch correction (ms).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import math
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

    # Validate key/scale
    root_idx = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    scale_indices = [(root_idx + interval) % 12 for interval in scale_intervals]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item with a Sustained Note and Pitch Bend ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_ppq = 0
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    # Calculate root note in the 4th octave (e.g., Middle C = 60)
    note_val = 60 + root_idx
    
    # Insert one long continuous note
    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val, 100, False)

    # Insert Pitch Bend sweep to simulate an out-of-tune / gliding performance
    # This sweep will go up and down continuously over the bars
    num_points = bars * 32
    for i in range(num_points):
        fraction = i / (num_points - 1)
        # Create a sine wave oscillation for the pitch bend
        # This will sweep up to +max and down to -max
        cycles = bars / 2.0  # complete one up/down cycle every 2 bars
        sine_val = math.sin(fraction * cycles * 2 * math.pi)
        
        pb_center = 8192
        pb_amplitude = 8191 # Max pitch bend
        pb_val = int(pb_center + (sine_val * pb_amplitude))
        
        # Clamp just in case
        pb_val = max(0, min(16383, pb_val))
        
        msb = pb_val // 128
        lsb = pb_val % 128
        
        pos_ppq = start_ppq + (end_ppq - start_ppq) * fraction
        
        # 224 (0xE0) is the MIDI status byte for Pitch Bend on Channel 1
        RPR.RPR_MIDI_InsertCC(take, False, False, pos_ppq, 224, 0, lsb, msb)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments & FX ===
    
    # 1. Add ReaSynth to generate the raw, bending audio
    synth_fx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Add ReaTune to correct the bending audio back into the scale
    tune_fx = RPR.RPR_TrackFX_AddByName(track, "ReaTune", False, -1)

    # === Step 5: Configure ReaTune Dynamically ===
    num_params = RPR.RPR_TrackFX_GetNumParams(track, tune_fx)
    
    notes_chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    for i in range(num_params):
        _, _, _, _, param_name, _ = RPR.RPR_TrackFX_GetParamName(track, tune_fx, i, "", 256)
        p_lower = param_name.lower().strip()

        # Enable Automatic Pitch Correction
        if "automatic" in p_lower or "auto" in p_lower:
            RPR.RPR_TrackFX_SetParamNormalized(track, tune_fx, i, 1.0)

        # Set Attack Time (assuming parameter max is roughly 250ms)
        # Using 0.0 results in robotic hard-tuning, higher values are smoother
        if "attack" in p_lower:
            normalized_attack = max(0.0, min(attack_ms / 250.0, 1.0))
            RPR.RPR_TrackFX_SetParamNormalized(track, tune_fx, i, normalized_attack)

        # Configure Scale / Key filtering
        # ReaTune exposes its note checkboxes as parameters named "C", "C#", etc.
        for j, note in enumerate(notes_chromatic):
            if p_lower == note.lower() or p_lower == f"enable {note.lower()}":
                # If this note is in our target scale, set param to 1.0, otherwise 0.0
                is_in_scale = 1.0 if j in scale_indices else 0.0
                RPR.RPR_TrackFX_SetParamNormalized(track, tune_fx, i, is_in_scale)

    style = "Robotic (T-Pain)" if attack_ms < 10.0 else "Natural"
    return f"Created '{track_name}' demonstrating {style} Pitch Correction locked to {key} {scale} over {bars} bars."
