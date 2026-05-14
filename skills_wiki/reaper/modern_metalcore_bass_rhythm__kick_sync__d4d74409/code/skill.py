def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metalcore Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110, # Explicitly 110 based on the tutorial to prevent sample harshness
    **kwargs,
) -> str:
    """
    Create a Modern Metalcore Bass Rhythm with kick-locked syncopation and octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C' for Drop C tuning).
        scale: Scale type.
        bars: Number of bars to generate (pattern loops every 4 bars).
        velocity_base: Base MIDI velocity (0-127). Default 110 for virtual bass realism.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

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
    
    # Establish root pitch (C1 = 24 in standard MIDI, typical for modern drop tunings)
    root_midi = 24 + NOTE_MAP.get(key, 0)
    
    # Define a syncopated 16th/8th note "machine gun" kick pattern
    # Tuples of (start_beat, duration_in_beats, octave_jump_flag)
    standard_riff = [
        (0.00, 0.25, False), (0.25, 0.25, False), # two 16ths
        (1.00, 0.25, False), (1.50, 0.25, False), # off-beat 16ths
        (2.00, 0.50, False),                      # held 8th
        (3.00, 0.25, False), (3.25, 0.25, False), # 16th burst
        (3.50, 0.25, False), (3.75, 0.25, False)
    ]
    
    # Define the 4th bar variation with the 12th fret octave jumps
    variation_riff = [
        (0.00, 0.25, False), (0.25, 0.25, False),
        (1.00, 0.25, False), (1.50, 0.25, False),
        (2.00, 0.25, True),  (2.50, 0.25, True),  # Octave pop! (e.g. following a guitar fill)
        (3.00, 0.25, True),  (3.50, 0.25, True)   
    ]

    total_notes_added = 0

    # === Step 4: Insert MIDI Notes ===
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        
        # Use variation riff on the 4th bar of every 4-bar cycle
        if (bar + 1) % 4 == 0:
            current_riff = variation_riff
        else:
            current_riff = standard_riff
            
        for beat_pos, duration, is_octave in current_riff:
            # Calculate absolute times
            start_time = bar_start_time + (beat_pos * 60.0 / bpm)
            # Make the note slightly staccato (multiply duration by 0.85) to leave gaps between chugs
            end_time = start_time + ((duration * 0.85) * 60.0 / bpm)
            
            # Convert time to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Calculate pitch
            pitch = root_midi + 12 if is_octave else root_midi
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take, 
                False, # selected
                False, # muted
                start_ppq, 
                end_ppq, 
                0,     # channel
                pitch, 
                velocity_base, 
                -1     # no custom param
            )
            total_notes_added += 1

    # Force MIDI item update
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    # Create a basic synth fallback just so it makes noise out-of-the-box, 
    # though the user should replace this with a dedicated Bass VSTi.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth to sound a bit more like a bass
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, 1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Square mix

    return f"Created '{track_name}' with {total_notes_added} kick-locked notes over {bars} bars at {bpm} BPM. Velocity scaled to {velocity_base}."
