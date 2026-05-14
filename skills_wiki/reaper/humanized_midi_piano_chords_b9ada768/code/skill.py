def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    humanize_amt: int = 20,
    **kwargs,
) -> str:
    """
    Create a 'Humanized MIDI Piano Chords' sequence in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        humanize_amt: Maximum random ± offset applied to velocity to simulate human playing.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Stock Instrument (ReaSynth as Piano Placeholder) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth parameters for a softer, plucky piano-like envelope
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)  # Attack: 0
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3)  # Decay: ~30%
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1)  # Sustain: low
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Release: moderate

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Humanized Chord Progression ===
    # Diatonic progression: I - vi - IV - V (represented as scale degrees, 0-indexed)
    progression = [
        [0, 2, 4], # I
        [5, 7, 2], # vi (last note wrapped to octave below if desired, but 2 maps up naturally)
        [3, 5, 0], # IV
        [4, 6, 1]  # V
    ]

    scale_intervals = SCALES.get(scale, SCALES["major"])
    root_midi = 60 + NOTE_MAP.get(key, 0) # Base octave C4
    
    notes_created = 0

    for bar in range(bars):
        chord_idx = bar % len(progression)
        chord_degrees = progression[chord_idx]

        # Calculate time positions (leaving a 10% gap at the end for realistic key release)
        start_time = bar * bar_length_sec
        end_time = start_time + (bar_length_sec * 0.9)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        for degree in chord_degrees:
            # Map scale degree to exact MIDI note pitch
            octave_shift = degree // len(scale_intervals)
            scale_idx = degree % len(scale_intervals)
            note_pitch = root_midi + scale_intervals[scale_idx] + (octave_shift * 12)

            # --- Core Technique: Velocity Humanization ---
            # Randomize velocity around the base to avoid the "machine gun" effect
            random_offset = random.randint(-humanize_amt, humanize_amt)
            vel = max(1, min(127, velocity_base + random_offset))

            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_pitch, vel, False)
            notes_created += 1

    # Finalize MIDI to ensure it displays correctly
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized velocity notes over {bars} bars at {bpm} BPM in {key} {scale}."
