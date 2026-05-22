def create_pattern(
    project_name: str = "ModernMetalBass",
    track_name: str = "MIDI Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Modern Metal/Djent Bass sequence in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Down-tuned metal usually uses low roots.
        scale: Scale type (not strictly used here as it's a pedal tone riff, but accepted).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for sustained notes (0-127). Chugs will be louder.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated bassline.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # Standard metal bass programming relies on a low root. 
    # C1 (MIDI 24) is a common register for Drop C tunings.
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add placeholder synth (User should replace with a Bass VST like DjinnBass)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tune ReaSynth down slightly for bass frequencies and make it a bit more aggressive (mix in square/saw)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Tuning down
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.3) # Add Square
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.4) # Add Saw

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item_pos = 0.0
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define and Insert MIDI Notes ===
    # A standard 2-bar metalcore/djent pattern.
    # Format: (start_beat, duration_in_beats, pitch_offset, velocity)
    # Notice: Sustains have lower velocity (velocity_base), staccato chugs are spiked (+17).
    chug_vel = min(127, velocity_base + 17)
    
    two_bar_pattern = [
        # --- Bar 1: Syncopated double kick matching ---
        (0.0,  1.0,  0, velocity_base), # Beat 1: Smooth sustain
        (1.25, 0.25, 0, chug_vel),      # Syncopated 16th staccato
        (1.5,  0.25, 0, chug_vel),      # Syncopated 16th staccato
        (2.0,  0.5,  0, velocity_base), # Beat 3: Smooth sustain
        (2.75, 0.25, 0, chug_vel),
        (3.0,  0.25, 0, chug_vel),
        (3.5,  0.5,  0, velocity_base),
        
        # --- Bar 2: Turnaround with octave jump ---
        (4.0,  0.5,  0, velocity_base),
        (4.75, 0.25, 0, chug_vel),
        (5.0,  0.25, 0, chug_vel),
        (5.25, 0.25, 0, chug_vel),
        # Fretboard Fill: Jump up 12 frets (1 octave) matching guitar flourish
        (6.0,  0.25, 12, velocity_base + 5), 
        (6.5,  0.25, 12, velocity_base + 5),
        (7.0,  0.25, 12, velocity_base + 5),
        (7.5,  0.25, 12, velocity_base + 5),
    ]

    note_count = 0
    # Loop the 2-bar pattern across the requested number of bars
    for bar_offset in range(0, bars, 2):
        for beat, length, pitch_offset, vel in two_bar_pattern:
            start_beat = beat + (bar_offset * beats_per_bar)
            
            # Stop if we've filled the requested number of bars
            if start_beat >= bars * beats_per_bar:
                break
                
            start_time = item_pos + (start_beat * (60.0 / bpm))
            end_time = item_pos + ((start_beat + length) * (60.0 / bpm))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = int(root_pitch + pitch_offset)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(vel), False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} metal bass notes over {bars} bars at {bpm} BPM (Root: {key}1). Note: Replace ReaSynth with a Bass VST for accurate tonal velocity switching."
