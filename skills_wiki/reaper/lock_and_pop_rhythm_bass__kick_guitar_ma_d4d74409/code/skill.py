def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Locked Rhythm Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly 110 to avoid 127 top-end harshness as per tutorial
    **kwargs,
) -> str:
    """
    Create a kick-matching rhythm bassline with velocity control and octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (set to 110 to tame harsh sample layers).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Note map starting at Octave 2 (Standard low tuning range for rock/metal bass)
    # Using Octave 2 for aggressive sub/mid bass energy
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
    
    # Get the root note for our pedal bassline
    root_pitch = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 24)

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
    
    # A heavy syncopated rhythm mimicking a kick drum pattern
    # Format: (start_beat, duration_in_beats)
    rhythm_pattern = [
        (0.0, 0.25),   # Beat 1
        (0.75, 0.25),  # The "ah" of 1
        (1.5, 0.25),   # The "and" of 2
        (2.0, 0.25),   # Beat 3
        (2.5, 0.25),   # The "and" of 3
        (2.75, 0.25),  # The "ah" of 3
        (3.5, 0.5)     # The "and" of 4 (Held slightly longer)
    ]
    
    note_count = 0
    # === Step 4: Generate MIDI Notes ===
    for b in range(bars):
        for i, (pos_beats, dur_beats) in enumerate(rhythm_pattern):
            start_qn = (b * beats_per_bar) + pos_beats
            end_qn = start_qn + dur_beats
            
            # Convert beats (QN) to project time, then to PPQ for MIDI insertion
            start_proj_time = start_qn * (60.0 / bpm)
            end_proj_time = end_qn * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_proj_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_proj_time)
            
            # Technique: Jump an octave at the end of the phrase (e.g. end of every 2nd bar)
            # Mimics sliding to the 12th fret with the guitar
            is_end_of_phrase = (b % 2 == 1) and (i == len(rhythm_pattern) - 1)
            pitch = root_pitch + 12 if is_end_of_phrase else root_pitch
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity_base, True
            )
            note_count += 1

    # Sort MIDI after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add VST Placeholder & Processing ===
    # Add ReaSynth as a placeholder for the Bass VST
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tune ReaSynth to sound like a gritty bass DI (Saw/Square blend)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)    # Volume slightly down
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5)    # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5)    # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.1)    # Fast attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.2)    # Decay
    
    return f"Created '{track_name}' with {note_count} syncopated pedal notes over {bars} bars at {bpm} BPM (Velocity capped at {velocity_base})."
