def create_pattern(
    project_name: str = "LatinJazz",
    track_name: str = "Cubop",
    bpm: int = 160,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a foundational Cubop / Latin Jazz pattern (2-3 Clave + Syncopated Chords) 
    in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM (140-180 recommended for Cubop).
        key: Root note (e.g., "C", "F#").
        scale: Scale type ("minor" or "major").
        bars: Number of bars to generate (should be even, as clave is a 2-bar pattern).
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # --- Music Theory & Scale Definitions ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    root_note = NOTE_MAP.get(key.capitalize(), 0) + 48 # Start at C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Define a 7th chord based on the scale (Root, 3rd, 5th, 7th)
    # Using modulo to safely wrap around the octave
    chord_degrees = [0, 2, 4, 6] # 1st, 3rd, 5th, 7th notes of the scale
    chord_pitches = []
    for degree in chord_degrees:
        octave_shift = (degree // 7) * 12
        interval = scale_intervals[degree % 7]
        chord_pitches.append(root_note + interval + octave_shift)

    # --- Environment Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    qn_sec = 60.0 / bpm # Length of one quarter note in seconds
    bar_sec = qn_sec * beats_per_bar
    total_length_sec = bar_sec * bars

    # Ensure we generate an even number of bars to complete the clave cycles
    if bars % 2 != 0:
        bars += 1
        total_length_sec = bar_sec * bars

    # --- Helper: Add MIDI Note ---
    def add_midi_note(take, pitch, start_qn, length_qn, velocity):
        start_pos = start_qn * qn_sec
        end_pos = start_pos + (length_qn * qn_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                start_pos, end_pos, 
                                0, pitch, velocity, False)

    # ==========================================
    # TRACK 1: PERCUSSION (2-3 SON CLAVE)
    # ==========================================
    track_idx_clave = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_clave, True)
    clave_track = RPR.RPR_GetTrack(0, track_idx_clave)
    RPR.RPR_GetSetMediaTrackInfo_String(clave_track, "P_NAME", f"{track_name} - Clave", True)
    RPR.RPR_SetMediaTrackInfo_Value(clave_track, "D_PAN", 0.3) # Pan right

    # Add ReaSynth for percussive block sound
    clave_fx = RPR.RPR_TrackFX_AddByName(clave_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(clave_track, clave_fx, 1, 0.0) # Attack = 0
    RPR.RPR_TrackFX_SetParam(clave_track, clave_fx, 2, 0.05) # Decay = short
    RPR.RPR_TrackFX_SetParam(clave_track, clave_fx, 3, 0.0) # Sustain = 0
    RPR.RPR_TrackFX_SetParam(clave_track, clave_fx, 4, 0.0) # Release = 0
    RPR.RPR_TrackFX_SetParam(clave_track, clave_fx, 0, 0.0) # Volume mixed down slightly

    clave_item = RPR.RPR_AddMediaItemToTrack(clave_track)
    RPR.RPR_SetMediaItemInfo_Value(clave_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(clave_item, "D_LENGTH", total_length_sec)
    clave_take = RPR.RPR_AddTakeToMediaItem(clave_item)

    # Generate 2-3 Son Clave pattern
    clave_pitch = 76 # E5 (high, cutting tone)
    for i in range(0, bars, 2):
        bar_offset = i * beats_per_bar
        # Bar 1 (2-side)
        add_midi_note(clave_take, clave_pitch, bar_offset + 1.0, 0.25, velocity_base + 10)
        add_midi_note(clave_take, clave_pitch, bar_offset + 2.0, 0.25, velocity_base + 10)
        # Bar 2 (3-side)
        add_midi_note(clave_take, clave_pitch, bar_offset + 4.0, 0.25, velocity_base + 15)
        add_midi_note(clave_take, clave_pitch, bar_offset + 5.5, 0.25, velocity_base)
        add_midi_note(clave_take, clave_pitch, bar_offset + 7.0, 0.25, velocity_base + 10)

    RPR.RPR_MIDI_Sort(clave_take)

    # ==========================================
    # TRACK 2: JAZZ PIANO (SYNCOPATED COMPING)
    # ==========================================
    track_idx_chords = track_idx_clave + 1
    RPR.RPR_InsertTrackAtIndex(track_idx_chords, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx_chords)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name} - Chords", True)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "D_PAN", -0.3) # Pan left

    # Add ReaSynth for electric piano/organ tone
    chords_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, chords_fx, 1, 0.02) # Soft attack
    RPR.RPR_TrackFX_SetParam(chords_track, chords_fx, 2, 0.5)  # Decay
    RPR.RPR_TrackFX_SetParam(chords_track, chords_fx, 3, 0.3)  # Sustain
    RPR.RPR_TrackFX_SetParam(chords_track, chords_fx, 4, 0.2)  # Release
    RPR.RPR_TrackFX_SetParam(chords_track, chords_fx, 6, 0.5)  # Saw mix
    RPR.RPR_TrackFX_SetParam(chords_track, chords_fx, 0, -0.1) # Vol down

    # Add lowpass filter (ReaEQ) to warm up the tone
    eq_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, eq_fx, 0, 1) # Set Band 1 to Low Shelf/Pass
    RPR.RPR_TrackFX_SetParam(chords_track, eq_fx, 1, 800.0) # Cutoff frequency

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # Generate syncopated comping pattern interlocking with clave
    # Hits on: Bar 1 -> 1, 2&, 4. Bar 2 -> 2&, 4.
    for i in range(0, bars, 2):
        bar_offset = i * beats_per_bar
        
        comp_rhythm = [
            (0.0, 1.0),   # Downbeat of 1
            (1.5, 1.0),   # Anticipation of 3 ("and" of 2)
            (3.0, 0.75),  # Beat 4
            (5.5, 1.0),   # Anticipation of 3 ("and" of 2) in 2nd bar
            (7.0, 0.75)   # Beat 4 in 2nd bar
        ]
        
        for qn_start, qn_len in comp_rhythm:
            # Randomize velocity slightly for human feel
            vel = max(10, min(127, velocity_base - 10 + (int(qn_start * 10) % 20)))
            for pitch in chord_pitches:
                add_midi_note(chords_take, pitch, bar_offset + qn_start, qn_len, vel)

    RPR.RPR_MIDI_Sort(chords_take)

    return f"Created Latin Jazz pattern (Clave & Comping) over {bars} bars at {bpm} BPM in {key} {scale}."
