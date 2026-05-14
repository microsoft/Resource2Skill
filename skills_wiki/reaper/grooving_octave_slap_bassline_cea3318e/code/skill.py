def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Groove Bass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a humanized, syncopated octave-slap bassline groove in REAPER.
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

    # === Step 1: Set Tempo ===
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

    # === Step 4: Define the Groove Pattern ===
    # Each tuple: (Quarter Note Position, Duration in QN, Velocity, Octave Shift, Timing Offset in QN)
    # The tutorial emphasizes: Slaps are an octave up, very short, with timing offsets (humanization)
    rhythm_pattern = [
        (0.00, 0.50, 110, 0,  0.000),  # Beat 1: Low Root, on grid
        (0.75, 0.15, 127, 1, -0.015),  # Beat 1 'a': High Slap, short, slightly rushed
        (1.50, 0.25,  95, 0,  0.010),  # Beat 2 'and': Low Root, slightly late/laid back
        (2.00, 0.50, 105, 0,  0.000),  # Beat 3: Low Root, on grid
        (2.75, 0.15, 120, 1,  0.020),  # Beat 3 'a': High Slap, short, slightly late (dragged)
        (3.50, 0.25,  90, 0, -0.010),  # Beat 4 'and': Low Root, slightly rushed
    ]

    scale_degrees = SCALES.get(scale.lower(), SCALES["minor"])
    # Base octave 1 for bass (e.g. E1 = 28)
    base_note = 24 + NOTE_MAP.get(key, 0) 

    # Generate notes across the bars
    for bar in range(bars):
        # Simple chord progression to keep it interesting: i -> iv -> i -> iv
        # Landing on the root tone of the chord as advised in the tutorial
        is_iv_chord = (bar % 2 != 0)
        degree_idx = 3 if is_iv_chord and len(scale_degrees) > 3 else 0
        chord_root_pitch = base_note + scale_degrees[degree_idx]

        for qn_pos, dur_qn, vel, octave_shift, offset_qn in rhythm_pattern:
            # Calculate absolute quarter note position
            absolute_qn_start = (bar * beats_per_bar) + qn_pos + offset_qn
            absolute_qn_end = absolute_qn_start + dur_qn
            
            # Convert to seconds
            start_sec = (absolute_qn_start * 60.0) / bpm
            end_sec = (absolute_qn_end * 60.0) / bpm
            
            # Convert to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Determine pitch (adding 12 for octave slaps)
            pitch = chord_root_pitch + (octave_shift * 12)
            
            # Scale velocity safely
            scaled_vel = max(1, min(127, int(vel * (velocity_base / 100.0))))
            
            # Insert note (take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, scaled_vel, True)

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument & FX ===
    # Add native synth to give it a plucky bass tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a bass feel: 
    # Param 0 = Volume, 1 = Tuning, 2 = Square mix, 3 = Saw mix, 5 = Attack, 6 = Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5)  # Square wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.8)  # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.0)  # Fast attack (punchy)
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.3)  # Short decay

    # Add ReaEQ to roll off harsh high frequencies (creating a rounder bass tone)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 (High Shelf -> Low Pass)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 5) # Set band 4 to Low Pass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 13, 1500.0) # Cutoff frequency (Hz)
    
    return f"Created '{track_name}' with {len(rhythm_pattern) * bars} humanized slap bass notes over {bars} bars at {bpm} BPM."
