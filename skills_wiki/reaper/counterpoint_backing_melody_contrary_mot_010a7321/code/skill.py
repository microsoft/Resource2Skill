def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Counterpoint Backing",
    bpm: int = 95,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Lead Melody and a Counterpoint Backing Melody utilizing contrary motion,
    rhythmic contrast, and strategic rests.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created backing track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    root_val = NOTE_MAP.get(key, 9) # Default A
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_pitch(degree: int, octave: int) -> int:
        """Convert a 0-indexed scale degree into a MIDI pitch number."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        note_val = root_val + scale_intervals[scale_idx] + ((octave + octave_shift + 1) * 12)
        return max(0, min(127, note_val))

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Track 1: Lead Melody
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    lead_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", "Lead Melody", True)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)

    # Track 2: Backing Melody
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    backing_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(backing_track, "P_NAME", track_name, True)
    RPR.RPR_TrackFX_AddByName(backing_track, "ReaSynth", False, -1)
    
    # Push the backing melody lower in the mix (-6dB roughly equals 0.5 amplitude)
    RPR.RPR_SetMediaTrackInfo_Value(backing_track, "D_VOL", 0.5)

    # === Step 3: Create MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    lead_item = RPR.RPR_AddMediaItemToTrack(lead_track)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_LENGTH", item_length)
    lead_take = RPR.RPR_AddTakeToMediaItem(lead_item)

    backing_item = RPR.RPR_AddMediaItemToTrack(backing_track)
    RPR.RPR_SetMediaItemInfo_Value(backing_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(backing_item, "D_LENGTH", item_length)
    backing_take = RPR.RPR_AddTakeToMediaItem(backing_item)

    # Helper function to insert notes
    def insert_note(take, start_beat, length_beats, degree, octave=5, vel=100):
        pitch = get_pitch(degree, octave)
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # === Step 4: Populate MIDI with Counterpoint Logic ===
    # We iterate in 2-bar phrases (8 beats)
    for b in range(0, bars, 2):
        
        # --- Bar 1 ---
        if b < bars:
            start_b = b * 4
            # LEAD: Moves Down (Degree 2 -> 0), then Up (Degree 0 -> 1 with long duration)
            insert_note(lead_take, start_b + 0, 1.0, 2, 5, velocity_base)
            insert_note(lead_take, start_b + 1, 1.0, 0, 5, velocity_base)
            insert_note(lead_take, start_b + 2, 2.0, 1, 5, velocity_base)

            # BACKING: Contrary to Lead. Moves Up (Degree 0 -> 1). 
            # Then rhythmic counter (4 rapid 8th notes moving down) during lead's long note
            insert_note(backing_take, start_b + 0, 1.0, 0, 5, velocity_base - 10)
            insert_note(backing_take, start_b + 1, 1.0, 1, 5, velocity_base - 10)
            
            insert_note(backing_take, start_b + 2.0, 0.5, 4, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 2.5, 0.5, 3, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.0, 0.5, 2, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.5, 0.5, 1, 5, velocity_base - 15)

        # --- Bar 2 ---
        if b + 1 < bars:
            start_b = (b + 1) * 4
            # LEAD: Moves Up (Degree 4), then Down (Degree 0) - Using long, expressive 2-beat notes
            insert_note(lead_take, start_b + 0, 2.0, 4, 5, velocity_base)
            insert_note(lead_take, start_b + 2, 2.0, 0, 5, velocity_base)

            # BACKING: Uses RESTS for the first 2 beats to give the Lead space.
            # Then rapid 8th notes moving UP (Contrary to Lead's downward motion)
            insert_note(backing_take, start_b + 2.0, 0.5, 0, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 2.5, 0.5, 1, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.0, 0.5, 2, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.5, 0.5, 3, 5, velocity_base - 15)

    # Sort MIDI items to ensure they behave correctly in the editor
    RPR.RPR_MIDI_Sort(lead_take)
    RPR.RPR_MIDI_Sort(backing_take)

    return f"Created 'Lead Melody' and '{track_name}' showcasing Counterpoint over {bars} bars in {key} {scale} at {bpm} BPM."
