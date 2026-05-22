def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Legato Bass",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Legato Bass Slide Finesse pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

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

    # Resolve pitches
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = NOTE_MAP.get(key.capitalize(), 0) + 36  # Base C2 (MIDI 36)
    
    # Extract scale degrees (safely wrapping octaves if needed)
    root = root_midi
    third = root_midi + scale_intervals[2 % len(scale_intervals)]
    fifth = root_midi + scale_intervals[4 % len(scale_intervals)]
    
    keyswitch_note = 24  # C0 (Standard for VST Legato toggle)

    # Define the note pattern [start_beat, end_beat, pitch, velocity]
    # Note how the end_beats overlap the subsequent start_beats to trigger legato.
    note_events = [
        # 1. The MODO Bass Legato Keyswitch (Hold across the whole phrase)
        (0.0, beats_per_bar * bars, keyswitch_note, 127),
        
        # 2. Pluck Root
        (0.0, 1.25, root, velocity_base),
        
        # 3. Slide Up to Fifth (overlaps Root by 0.25 beats)
        (1.0, 2.25, fifth, velocity_base - 5),
        
        # 4. The Tutorial's "Finesse Trick" for sliding DOWN 
        # A tiny ghost note overlapping the end of the previous note
        (2.125, 2.25, third, int(velocity_base * 0.5)), 
        
        # 5. Main Third (Slide target)
        (2.25, 3.25, third, velocity_base - 10),
        
        # 6. Slide back to Root
        (3.0, 4.0, root, velocity_base - 10)
    ]

    # Convert beats to PPQ and insert notes
    for start_beat, end_beat, pitch, vel in note_events:
        # Loop this 1-bar pattern across the generated item
        for bar in range(bars):
            # Calculate time in seconds
            start_sec = (start_beat + (bar * beats_per_bar)) * (60.0 / bpm)
            end_sec = (end_beat + (bar * beats_per_bar)) * (60.0 / bpm)
            
            # Bound the end_sec to item length
            if start_sec >= item_length:
                continue
            end_sec = min(end_sec, item_length)
            
            # Convert to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, int(pitch), int(vel), True
            )

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (ReaSynth Emulation) ===
    # Adding ReaSynth to demonstrate the slide effect without requiring 3rd party VSTs
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth Param 6 is Portamento. We turn it up to create the glide
    # that happens when MIDI notes overlap.
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.4)
    # Turn down the mix levels slightly to sound a bit more bass-like
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3) # Release

    return f"Created '{track_name}' with Legato overlapping notes and downward finesse trick over {bars} bars at {bpm} BPM"
