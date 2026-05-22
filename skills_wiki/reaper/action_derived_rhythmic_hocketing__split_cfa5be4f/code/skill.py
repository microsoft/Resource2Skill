def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Hocket_Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Action-Derived Rhythmic Hocketing pattern in REAPER.
    Simulates the "Split and put item above" custom action by generating
    interlocking, alternating chords across two contrasting tracks.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # --- Theory Lookup Tables ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 48 # Start at octave 4 (C3 in REAPER standard)

    # Standard progression: I - VI - IV - V (1-6-4-5)
    progression_degrees = [0, 5, 3, 4] 

    # --- Project Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar

    # --- Create Track 1 (Base Layer) ---
    track_idx_1 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_1, True)
    track_1 = RPR.RPR_GetTrack(0, track_idx_1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_1, "P_NAME", f"{track_name}_Base", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_1, "D_PAN", -0.5) # Pan Left
    RPR.RPR_TrackFX_AddByName(track_1, "ReaSynth", False, -1)

    # --- Create Track 2 ("Moved Up" Layer) ---
    track_idx_2 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_2, True)
    track_2 = RPR.RPR_GetTrack(0, track_idx_2)
    RPR.RPR_GetSetMediaTrackInfo_String(track_2, "P_NAME", f"{track_name}_MovedUp", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_2, "D_PAN", 0.5) # Pan Right
    fx_idx = RPR.RPR_TrackFX_AddByName(track_2, "ReaSynth", False, -1)
    # Pitch ReaSynth up an octave to simulate distinct processing on the "above" track
    RPR.RPR_TrackFX_SetParam(track_2, fx_idx, 0, 0.5 + (12.0/240.0)) # Tuning parameter (rough approximation for +12 st)

    # --- Generate MIDI Items ---
    total_length_sec = bar_length_sec * bars
    
    item_1 = RPR.RPR_AddMediaItemToTrack(track_1)
    RPR.RPR_SetMediaItemInfo_Value(item_1, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_1, "D_LENGTH", total_length_sec)
    take_1 = RPR.RPR_AddTakeToMediaItem(item_1)

    item_2 = RPR.RPR_AddMediaItemToTrack(track_2)
    RPR.RPR_SetMediaItemInfo_Value(item_2, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_2, "D_LENGTH", total_length_sec)
    take_2 = RPR.RPR_AddTakeToMediaItem(item_2)

    # --- Populate MIDI Notes (Hocketing Pattern) ---
    ppq = 960 # Standard REAPER PPQ
    note_count = 0

    for bar in range(bars):
        # Change chord every bar based on progression
        degree = progression_degrees[bar % len(progression_degrees)]
        
        # Build a basic triad
        chord = [
            root_pitch + scale_intervals[degree % 7] + (12 * (degree // 7)),
            root_pitch + scale_intervals[(degree + 2) % 7] + (12 * ((degree + 2) // 7)),
            root_pitch + scale_intervals[(degree + 4) % 7] + (12 * ((degree + 4) // 7))
        ]

        # Simulate the "Split and Move Up" action every beat
        for beat in range(beats_per_bar):
            start_time = (bar * beats_per_bar + beat) * beat_length_sec
            end_time = start_time + (beat_length_sec * 0.8) # Slight gap for rhythmic gating
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_1, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_1, end_time)

            # Alternate tracks: Even beats on Track 1, Odd beats on Track 2
            target_take = take_1 if beat % 2 == 0 else take_2
            
            for note in chord:
                RPR.RPR_MIDI_InsertNote(
                    target_take, 
                    False,          # selected
                    False,          # muted
                    start_ppq,      # start_ppq
                    end_ppq,        # end_ppq
                    0,              # channel
                    note,           # pitch
                    velocity_base,  # velocity
                    False           # noSort
                )
                note_count += 1

    # Force sort MIDI events
    RPR.RPR_MIDI_Sort(take_1)
    RPR.RPR_MIDI_Sort(take_2)

    return f"Created interlocking hocketed tracks ('{track_name}_Base' and '{track_name}_MovedUp') with {note_count} notes over {bars} bars at {bpm} BPM."
