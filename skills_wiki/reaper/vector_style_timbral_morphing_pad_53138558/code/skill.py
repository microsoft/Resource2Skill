def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Morphing Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Vector-Style Timbral Morphing Pad in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the generated structure.
    """
    import math
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    base_note = NOTE_MAP.get(key, 0) + 48 # Anchor at C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_chord_notes(root_degree, intervals, base, num_notes=4):
        """Generates extended diatonic chords by stacking thirds"""
        notes = []
        for i in range(num_notes):
            deg = (root_degree + i * 2) % len(intervals)
            oct_shift = (root_degree + i * 2) // len(intervals)
            pitch = base + intervals[deg] + (oct_shift * 12)
            notes.append(min(127, max(0, pitch)))
        return notes

    # Progressions (i-VI-III-VII for minor, I-vi-IV-V for major)
    progression = [0, 5, 2, 6] if scale == "minor" else [0, 5, 3, 4]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Parent Folder ===
    start_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    parent_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "D_VOL", 0.8) # Provide headroom
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaVerbate", False, -1)

    # === Synth Layer Configurations ===
    synths = [
        {"name": "Layer 1 (Lows)", "pan": -0.3, "oct": -1, "phase": 0.0, "fx": None},
        {"name": "Layer 2 (Sat)",  "pan": 0.0,  "oct": 0,  "phase": 2.0 * math.pi / 3.0, "fx": "JS: Saturation"},
        {"name": "Layer 3 (Cho)",  "pan": 0.3,  "oct": 1,  "phase": 4.0 * math.pi / 3.0, "fx": "JS: Chorus"}
    ]

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Step 3: Create Child Tracks, MIDI, and Modulation ===
    for i, s_cfg in enumerate(synths):
        idx = start_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        child = RPR.RPR_GetTrack(0, idx)
        
        RPR.RPR_GetSetMediaTrackInfo_String(child, "P_NAME", f"{track_name} - {s_cfg['name']}", True)
        RPR.RPR_SetMediaTrackInfo_Value(child, "D_PAN", s_cfg["pan"])
        
        # Close folder on the last track
        if i == len(synths) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(child, "I_FOLDERDEPTH", -1)
        else:
            RPR.RPR_SetMediaTrackInfo_Value(child, "I_FOLDERDEPTH", 0)

        # 3a. Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(child)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Generate Chords
        for bar in range(bars):
            deg = progression[bar % len(progression)]
            notes = get_chord_notes(deg, scale_intervals, base_note, 4)
            
            start_time = bar * bar_length_sec
            end_time = (bar + 1) * bar_length_sec
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            for pitch in notes:
                shifted_pitch = min(127, max(0, pitch + (s_cfg["oct"] * 12)))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, shifted_pitch, velocity_base, True)
                
        RPR.RPR_MIDI_Sort(take)

        # 3b. Add FX Chain
        synth_fx_idx = RPR.RPR_TrackFX_AddByName(child, "ReaSynth", False, -1)
        if s_cfg["fx"]:
            RPR.RPR_TrackFX_AddByName(child, s_cfg["fx"], False, -1)

        # 3c. Generate LFO Volume Automation (Simulating Parameter Modulation)
        # Parameter 0 in ReaSynth is Volume. We get its envelope.
        env = RPR.RPR_GetFXEnvelope(child, synth_fx_idx, 0, True)
        
        # LFO Math: 1 full cycle every 2 bars
        lfo_freq_hz = 1.0 / (bar_length_sec * 2.0)
        step_sec = (60.0 / bpm) / 4.0 # 16th note resolution for the drawing points
        
        t = 0.0
        while t <= total_length_sec + step_sec:
            # Cosine ensures phase=0 starts at peak amplitude
            osc_val = (math.cos(2 * math.pi * lfo_freq_hz * t - s_cfg["phase"]) + 1.0) / 2.0
            # Scale to a musical range (e.g., 0.0 to 0.6)
            env_val = osc_val * 0.6
            RPR.RPR_InsertEnvelopePoint(env, t, env_val, 0, 0, False, True)
            t += step_sec
            
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' morphing pad structure with 3 offset synth layers over {bars} bars at {bpm} BPM."
