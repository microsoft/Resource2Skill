def create_pattern(
    project_name: str = "GrooveBassProject",
    track_name: str = "Slap Groove Bass",
    bpm: int = 115,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a syncopated, humanized slap-bass groove in REAPER.
    """
    import reaper_python as RPR
    import random

    # === Music Theory & Setup ===
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

    # Ensure valid scale, default to minor if not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_note = NOTE_MAP.get(key.upper(), 4) # Default to E
    base_midi = 24 + base_note # 24 is C1 (Bass register)

    # Chord progression (Scale degrees: 0=Root, 3=4th, 4=5th)
    # We'll use a classic i - i - iv - V progression
    progression_degrees = [0, 0, 3, 4] 

    # Rhythm Pattern Definition for a single bar
    # (QuarterNote_Pos, ScaleDegree_Offset, Octave, Duration_QN, Velocity)
    groove_pattern = [
        (0.00,  0, 0, 0.50, velocity_base),       # Beat 1: Root Downbeat
        (1.50,  0, 0, 0.25, velocity_base - 15),  # Beat 2&: Syncopated Root Ghost
        (2.00,  0, 1, 0.25, 127),                 # Beat 3: Slap (Octave up, max vel)
        (2.75,  0, 0, 0.25, velocity_base - 10),  # Beat 3e&: Approach Ghost Note
        (3.00,  4, 0, 0.50, velocity_base - 5),   # Beat 4: 5th degree passing tone
        (3.75,  0, 1, 0.25, 127)                  # Beat 4e&: Slap Approach
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4.0
    qn_per_bar = 4.0
    item_length_sec = (60.0 / bpm) * qn_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate MIDI Notes ===
    total_notes_added = 0
    
    for bar in range(bars):
        # Determine the root chord for this bar
        chord_root_degree = progression_degrees[bar % len(progression_degrees)]
        
        for note_def in groove_pattern:
            beat_pos, degree_offset, octave_offset, duration_qn, vel = note_def
            
            # Calculate Pitch
            target_degree = chord_root_degree + degree_offset
            octaves_up = target_degree // len(scale_intervals)
            scale_idx = target_degree % len(scale_intervals)
            
            pitch = base_midi + scale_intervals[scale_idx] + ((octaves_up + octave_offset) * 12)
            
            # Keep pitch within safe MIDI bounds
            pitch = max(0, min(127, pitch))
            
            # Calculate Timing (with Humanization Jitter)
            exact_start_qn = (bar * qn_per_bar) + beat_pos
            exact_end_qn = exact_start_qn + duration_qn
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, exact_start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, exact_end_qn)
            
            # Humanize timing (+/- 12 ticks) and velocity (+/- 6)
            jitter = random.randint(-12, 12)
            start_ppq = max(0, start_ppq + jitter)
            end_ppq = max(start_ppq + 10, end_ppq + jitter) # Ensure note has some length
            
            final_vel = max(1, min(127, vel + random.randint(-6, 6)))
            # Force max velocity to 127 for slaps
            if vel == 127: final_vel = 127 
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(final_vel), True)
            total_notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument ===
    # Add stock ReaSynth to make it audible. The filter naturally responds well to short, low notes.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Optional: Lower ReaSynth volume slightly to prevent clipping
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.4)

    RPR.RPR_UpdateTimeline()
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes_added} humanized groove notes over {bars} bars at {bpm} BPM in {key} {scale}."
