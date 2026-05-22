def create_pattern(
    project_name: str = "MetalcoreBass",
    track_name: str = "Rhythm Locked Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly lowered from 127 to avoid harsh pick attack
    **kwargs,
) -> str:
    """
    Create a kick-locked, syncopated rock/metal bassline with octave jumps.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (defines the key context, though primarily riding the root).
        bars: Number of bars to generate (4 or 8 recommended).
        velocity_base: Base MIDI velocity (0-127), deliberately kept ~110.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Note map to calculate base pitch (C1 octave = 24)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 24 # Start in the C1 octave range

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Take ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define a syncopated 16th note metalcore/rock kick pattern.
    # 1 = hit, 0 = rest
    # Pattern: 1, 1-a, 2-&, 3, 3-a, 4-e, 4-&
    rhythm_grid = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0]
    
    notes_added = 0
    step_sec = sec_per_beat / 4.0 # Length of a 16th note in seconds

    # Generate the MIDI notes
    for b in range(bars):
        # Every 4th bar is a variation phrase with octave jumps matching a guitar riff
        is_variation_bar = ((b % 4) == 3)
        
        for step, hit in enumerate(rhythm_grid):
            if hit == 1:
                # Calculate timing
                start_time = (b * bar_length_sec) + (step * step_sec)
                
                # Default duration: staccato 16th note, slightly separated
                duration = step_sec * 0.85 
                
                # Determine Pitch
                pitch = root_pitch
                # Apply the tutorial's "octave jump" on the 3rd and 4th beats of variation bars
                if is_variation_bar and step >= 8:
                    pitch = root_pitch + 12
                    duration = step_sec * 1.5 # Hold out octave accents slightly longer

                end_time = start_time + duration
                
                # Convert project time to PPQ (Pulses Per Quarter Note)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Insert Note
                # chan 0, pitch, velocity_base (110 avoids harsh pick transient), noSort=True
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Stock Bass Placeholder) ===
    # Add a stock synth acting as our bass tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a bassier tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 1.0) # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5) # Square wave mix
    
    # Add EQ to roll off harsh high end (simulating the low-pass effect or cab sim)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 (High Shelf -> change to Low Pass)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 1)     # Set band 4 type to Low Pass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 13, 2500)  # Filter cutoff at 2.5kHz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 14, -12)   # Gain reduction (just in case)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM. Velocity capped at {velocity_base} with 12th-fret octave jump variations."
