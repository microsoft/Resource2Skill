def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano/Synth Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Foundational MIDI Track & Channel Strip Setup in REAPER.
    
    Generates a 4-bar block chord progression with a pre-configured 
    synthesizer, EQ, and Compressor chain.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (4 is recommended for the progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Ensure valid key and scale
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    octave_base = 48 # C3
    root_midi = octave_base + root_val

    # Helper function to get a MIDI note for a specific scale degree (0-indexed)
    def get_scale_note(degree):
        octave_shift = degree // 7
        interval = scale_intervals[degree % 7]
        return root_midi + (octave_shift * 12) + interval

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Gain stage: Set track volume to -6dB (approx 0.5 in REAPER's amplitude scale)
    vol_amp = 10 ** (-6.0 / 20.0)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol_amp)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Define a basic progression: I - V - vi - IV (degrees 0, 4, 5, 3)
    progression = [0, 4, 5, 3]
    
    total_notes_inserted = 0
    
    # Insert chords
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # Build a triad (root, third, fifth relative to the scale degree)
        chord_degrees = [degree, degree + 2, degree + 4]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec - 0.05 # slight gap between chords
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for chord_degree in chord_degrees:
            pitch = get_scale_note(chord_degree)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), False)
            total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    
    # 1. Virtual Instrument (ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a softer, more pad/piano-like attack and decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.2)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4)   # Release

    # 2. Equalization (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Tame the high frequencies (simulating the Low-Pass from tutorial)
    # Band 4 (High Shelf) Gain is Param 10. Cut by -8dB.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, -8.0) 

    # 3. Compression (ReaComp)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Param 0: Threshold (-12 dB)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -12.0)
    # Param 1: Ratio (3.0 : 1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 3.0)
    # Param 2: Attack (10 ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 10.0)
    # Param 3: Release (100 ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 100.0)

    return f"Created '{track_name}' with {total_notes_inserted} notes (I-V-vi-IV progression) over {bars} bars at {bpm} BPM in {key} {scale}. Loaded ReaSynth + EQ + Comp."
