def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass (Kick-Locked)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly lowered from 127 to remove string noise
    **kwargs,
) -> str:
    """
    Create a kick-locked metal bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc. - mostly irrelevant as we pedal the root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), intentionally lowered for tone control.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note map to find the root pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Metal bass tunings typically place the root very low (C1 or C2). 
    # MIDI note 24 is C1.
    root_pitch = NOTE_MAP.get(key, 0) + 24 
    
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

    # Core syncopated metal/djent rhythm representing a kick drum pattern.
    # List of tuples: (start_beat, length_in_beats)
    kick_rhythm_beats = [
        (0.0, 0.5),    # Downbeat
        (0.75, 0.25),  # 16th note syncopation ("a" of 1)
        (1.5, 0.5),    # Upbeat of 2
        (2.25, 0.25),  # 16th note 
        (2.5, 0.25),   # 8th note
        (3.0, 0.5)     # Downbeat of 4
    ]

    notes_created = 0

    # === Step 4: Generate MIDI Notes ===
    for bar in range(bars):
        for start_beat, length in kick_rhythm_beats:
            
            # Determine if we should do an octave jump for variation
            # We do this on the last beat of every 2nd bar (phrase turnaround)
            is_turnaround = (bar % 2 == 1) and (start_beat == 3.0)
            pitch = root_pitch + 12 if is_turnaround else root_pitch
            
            # Calculate actual timing in seconds, then convert to PPQ
            actual_start_beat = start_beat + (bar * beats_per_bar)
            start_time = actual_start_beat * (60.0 / bpm)
            end_time = (actual_start_beat + length) * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Stock FX Chain Placeholder ===
    # Since we can't guarantee DjinnBass is installed, we create a heavy sub-bass with ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Adjust ReaSynth for a more "bass guitar" fundamental tone (more Saw/Square, less Sine)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Sine vol down
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.7) # Square/Saw vol up
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5) # Triangle vol up
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1) # Faster attack

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM. Velocity clamped at {velocity_base} to reduce sampler string noise."
