def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sequenced Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 127,
    **kwargs,
) -> str:
    """
    Creates a generative-style 16th-note rolling electronic bassline with a deep analog synth tone.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity scaling (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    if bpm > 0:
        RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Music theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    # Base octave for deep bass (C1 = 24)
    base_note = NOTE_MAP.get(key.upper(), 0) + 24 
    
    # 1-bar rhythmic sequence (16th note grid)
    # deg: scale degree offset, oct: octave offset, vel: dynamic accent
    pattern = [
        {"pos_beats": 0.00, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 110},
        {"pos_beats": 0.25, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 0.50, "dur_beats": 0.20, "deg": 0, "oct": 1, "vel": 100}, # Octave jump
        {"pos_beats": 0.75, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 1.00, "dur_beats": 0.20, "deg": 2, "oct": 0, "vel": 100}, # Minor 3rd
        {"pos_beats": 1.25, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 1.50, "dur_beats": 0.20, "deg": 3, "oct": 0, "vel": 90},  # 4th
        {"pos_beats": 1.75, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 2.00, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 110},
        {"pos_beats": 2.25, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 2.50, "dur_beats": 0.20, "deg": 0, "oct": 1, "vel": 100}, # Octave jump
        {"pos_beats": 2.75, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 3.00, "dur_beats": 0.20, "deg": -1, "oct": 0, "vel": 100}, # Minor 7th below
        {"pos_beats": 3.25, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
        {"pos_beats": 3.50, "dur_beats": 0.20, "deg": -3, "oct": 0, "vel": 90},  # 5th below
        {"pos_beats": 3.75, "dur_beats": 0.20, "deg": 0, "oct": 0, "vel": 70},
    ]

    note_count = 0
    for bar in range(bars):
        bar_start_beats = bar * beats_per_bar
        for note_data in pattern:
            # Calculate pitch supporting negative scale degrees
            degree = note_data["deg"]
            octave_offset = note_data["oct"]
            
            octave = degree // len(scale_intervals) + octave_offset
            idx = degree % len(scale_intervals)
            pitch = base_note + (octave * 12) + scale_intervals[idx]
            pitch = max(0, min(127, pitch))
            
            # Scale velocity based on the base parameter
            vel = int((note_data["vel"] / 127.0) * velocity_base)
            vel = max(1, min(127, vel))
            
            # Calculate timings
            pos_beats_total = bar_start_beats + note_data["pos_beats"]
            dur_beats = note_data["dur_beats"]
            
            start_time = (60.0 / bpm) * pos_beats_total
            end_time = start_time + ((60.0 / bpm) * dur_beats)
            
            # Insert MIDI note
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time), 
                                    0, pitch, vel, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Deep Phat Synth) ===
    # 1. Synthesizer
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.4) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.6) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.5) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.0) # Tri mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.8) # Extra Sine (Sub Bass)

    # 2. EQ / Filtering
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: Low Shelf boost to emphasize fundamental
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 80.0)  # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 4.0)   # Gain (dB)
    # Band 4: Low Pass Filter to remove harsh highs and make it "Deep"
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 1200.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 14, 1.5)    # Bandwidth/Resonance
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 15, 8.0)    # Type (8 = Low Pass)

    # 3. Compression (Punch)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -20.0) # Threshold (dB)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 10.0)  # Attack (ms) allows transient through
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 50.0)  # Release (ms) resets for next 16th note

    return f"Created '{track_name}' with {note_count} sequencer notes over {bars} bars at {bpm} BPM."
