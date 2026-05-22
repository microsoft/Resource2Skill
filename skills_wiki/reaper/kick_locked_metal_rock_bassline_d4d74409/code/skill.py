def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Locked Bass",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Lowered from 127 to tame harsh string attack
    **kwargs,
) -> str:
    """
    Create a 'Kick-Locked Metal/Rock Bassline' in the current REAPER project.
    Generates both a reference Kick track and a Bass track that lock together perfectly.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created bass track.
        bpm: Tempo in BPM (130-160 typical for this style).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (primarily uses root and octave).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). 110 recommended for VST basses.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and notes.
    """
    import reaper_python as RPR

    # Note map to calculate MIDI pitches
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key, 0)
    
    # Bass typically sits in octave 1 for modern metal/rock (e.g., Drop C = C1 = MIDI 24)
    bass_root_midi = root_val + 24 
    kick_midi = 36 # General MIDI standard for Kick Drum 1
    
    # 2-bar syncopated metal/rock rhythm pattern mapped in 16th notes
    # Tuple: (start_16th_position, duration_in_16ths, octave_shift_multiplier)
    rhythm_pattern = [
        # Bar 1
        (0,  1.5, 0),  # Beat 1
        (2,  1.5, 0),  # Beat 1 &
        (6,  1.5, 0),  # Beat 2 &
        (8,  1.5, 0),  # Beat 3
        (12, 1.5, 1),  # Beat 4 - OCTAVE JUMP!
        (14, 1.5, 0),  # Beat 4 &
        # Bar 2
        (16 + 0,  1.5,  0), 
        (16 + 2,  1.5,  0), 
        (16 + 6,  1.5,  0), 
        (16 + 8,  1.5,  0), 
        (16 + 11, 0.75, 1), # Fast syncopated octave jump 
        (16 + 12, 1.5,  0), 
        (16 + 15, 0.75, 0), # Lead-in to next downbeat
    ]
    pattern_length_16ths = 32
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Calculate absolute timings
    beat_len_sec = 60.0 / bpm
    sixteenth_len_sec = beat_len_sec / 4.0
    bar_len_sec = beat_len_sec * 4.0
    
    # === Step 2: Create Tracks ===
    track_count = RPR.RPR_CountTracks(0)
    
    # Create Kick Reference Track
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    kick_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Reference Kick", True)
    
    # Create Bass Track
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", track_name, True)
    
    # === Step 3: Create MIDI Items ===
    total_length_sec = bars * bar_len_sec
    
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # === Step 4: Populate MIDI Notes ===
    notes_added = 0
    # Calculate how many 2-bar loops we need to iterate over
    num_2bar_loops = (bars // 2) + (1 if bars % 2 != 0 else 0)
    
    for loop in range(num_2bar_loops):
        loop_offset_16ths = loop * pattern_length_16ths
        
        for start_16th, dur_16ths, oct_shift in rhythm_pattern:
            abs_start_16th = loop_offset_16ths + start_16th
            
            # Stop if we exceed the requested number of bars
            if abs_start_16th >= bars * 16:
                break
                
            start_time = abs_start_16th * sixteenth_len_sec
            end_time = start_time + (dur_16ths * sixteenth_len_sec)
            
            # Convert project time to PPQ for the MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_time)
            
            # Insert Kick Note (Max Velocity)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, kick_midi, 127, False)
            
            # Insert Bass Note (Controlled Velocity + Octave Shift)
            bass_note = bass_root_midi + (oct_shift * 12)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_note, velocity_base, False)
            
            notes_added += 1

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(kick_take)
    RPR.RPR_MIDI_Sort(bass_take)
    
    # Add a basic synth to bass for immediate feedback (User will likely replace with a VST)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    return f"Created Kick and '{track_name}' tracks. Locked {notes_added} bass notes over {bars} bars at {bpm} BPM with octave jumps."
