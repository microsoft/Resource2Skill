def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groove Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a Grooving Slap Bassline with two articulations (Mellow Foundation + Slap Octaves).
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, C#, D, E).
        scale: Scale type (e.g., minor, major, dorian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for the foundation.
        
    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    import random

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

    # Validate inputs
    root_pitch_class = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Base octave for Bass is usually Octave 2 (MIDI note 36 for C2)
    base_midi_note = 36 + root_pitch_class
    # Drop down an octave if the note is too high (e.g., A, B) to keep sub energy
    if base_midi_note > 43: 
        base_midi_note -= 12

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Timing calculations
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # --- Create Track 1: Foundation (Finger/Mellow Bass) ---
    idx_fnd = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_fnd, True)
    track_fnd = RPR.RPR_GetTrack(0, idx_fnd)
    RPR.RPR_GetSetMediaTrackInfo_String(track_fnd, "P_NAME", f"{track_name} - Foundation", True)
    
    # Add Item & Take for Foundation
    item_fnd = RPR.RPR_AddMediaItemToTrack(track_fnd)
    RPR.RPR_SetMediaItemInfo_Value(item_fnd, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_fnd, "D_LENGTH", total_length_sec)
    take_fnd = RPR.RPR_AddTakeToMediaItem(item_fnd)
    
    # Foundation FX (ReaSynth + ReaEQ Lowpass)
    fx_synth1 = RPR.RPR_TrackFX_AddByName(track_fnd, "ReaSynth", False, -1)
    fx_eq1 = RPR.RPR_TrackFX_AddByName(track_fnd, "ReaEQ", False, -1)

    # --- Create Track 2: Slap (Aggressive Octave Bass) ---
    idx_slap = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_slap, True)
    track_slap = RPR.RPR_GetTrack(0, idx_slap)
    RPR.RPR_GetSetMediaTrackInfo_String(track_slap, "P_NAME", f"{track_name} - Slap Articulation", True)
    
    # Add Item & Take for Slap
    item_slap = RPR.RPR_AddMediaItemToTrack(track_slap)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_LENGTH", total_length_sec)
    take_slap = RPR.RPR_AddTakeToMediaItem(item_slap)
    
    # Slap FX (ReaSynth + ReaEQ Brightness boost)
    fx_synth2 = RPR.RPR_TrackFX_AddByName(track_slap, "ReaSynth", False, -1)
    fx_eq2 = RPR.RPR_TrackFX_AddByName(track_slap, "ReaEQ", False, -1)
    
    # --- Rhythm & Note Generation Loop ---
    notes_added = 0
    
    for b in range(bars):
        bar_offset_beats = b * beats_per_bar
        
        # We will use the scale to pick passing notes (e.g. scale degree 3, 5, 7)
        # Note indices wrap around safely using modulo
        def get_scale_note(degree_idx, octave_offset=0):
            degree_idx = degree_idx % len(scale_intervals)
            return base_midi_note + scale_intervals[degree_idx] + (octave_offset * 12)

        # -- Define the Groovy Pattern --
        # Structure: (Take, Start_Beat, Length_Beats, Scale_Degree, Octave, Base_Vel, Is_Staccato)
        pattern = [
            # Beat 1: Strong downbeat root
            (take_fnd, 0.0, 0.5, 0, 0, velocity_base, False),
            
            # Beat 1 "a" (1.75): Syncopated slap octave
            (take_slap, 0.75, 0.15, 0, 1, 120, True),
            
            # Beat 2 "+" (2.5): Passing note (3rd or 4th degree)
            (take_fnd, 1.5, 0.25, 2, 0, velocity_base - 5, False),
            
            # Beat 3: Solid root again (split length from standard quarter)
            (take_fnd, 2.0, 0.25, 0, 0, velocity_base + 5, False),
            
            # Beat 3 "e" (3.25): Double-pluck foundation
            (take_fnd, 2.25, 0.25, 0, 0, velocity_base - 10, False),
            
            # Beat 4: Slap octave syncopation
            (take_slap, 2.75, 0.15, 0, 1, 127, True),
            
            # Beat 4 "+": Walk up or ghost note to lead back to next bar
            (take_fnd, 3.5, 0.25, 4, 0, velocity_base - 5, False),
        ]
        
        # Add variation on the 4th bar (turnaround)
        if b % 4 == 3:
            pattern.append((take_slap, 3.75, 0.15, 3, 1, 110, True))

        for tk, st_beat, len_beat, sc_deg, oct_off, vel, is_stacc in pattern:
            # 1. Calculate ideal times
            start_sec = (bar_offset_beats + st_beat) * beat_length_sec
            end_sec = start_sec + (len_beat * beat_length_sec)
            
            # 2. Humanization: "Always imitate reality" (Slight timing & velocity offsets)
            time_offset = random.uniform(-0.015, 0.015) # +/- 15ms
            start_sec = max(0.0, start_sec + time_offset)
            end_sec = max(start_sec + 0.05, end_sec + time_offset) # Ensure minimum length
            
            human_vel = int(vel + random.uniform(-6, 6))
            human_vel = max(1, min(127, human_vel))
            
            pitch = get_scale_note(sc_deg, oct_off)
            
            # 3. Convert time to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(tk, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(tk, end_sec)
            
            # 4. Insert Note
            RPR.RPR_MIDI_InsertNote(tk, False, False, start_ppq, end_ppq, 0, pitch, human_vel, True)
            notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take_fnd)
    RPR.RPR_MIDI_Sort(take_slap)

    return f"Created Grooving Bassline across 2 tracks ('{track_name} - Foundation/Slap') with {notes_added} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
