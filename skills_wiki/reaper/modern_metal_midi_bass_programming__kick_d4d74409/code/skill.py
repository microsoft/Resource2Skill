def create_pattern(
    project_name: str = "MetalCoreProject",
    track_name: str = "Modern Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a highly syncopated metal bass MIDI pattern that locks to the kick drum
    and incorporates fretboard-accurate octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (tutorial recommends 110 to avoid harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # Note map to determine the root pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Metal bass is tuned very low. We center around Octave 1 (MIDI 24 = C1).
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
    
    # Create the MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Define the Syncopated Metal Rhythm ===
    # Each tuple represents: (beat_start_offset, length_in_beats, pitch_offset)
    # This creates a typical djent/metalcore kick-following rhythm.
    base_pattern = [
        (0.0,  0.5,   0),  # Beat 1: 8th note chug
        (0.75, 0.25,  0),  # Beat 1.75: Staccato pop
        (1.25, 0.5,   0),  # Beat 2.25: 8th note chug
        (2.0,  0.5,   0),  # Beat 3: 8th note chug
        (2.75, 0.25, 12),  # Beat 3.75: Staccato OCTAVE JUMP (12th fret)
        (3.0,  0.25, 12),  # Beat 4: Staccato OCTAVE JUMP
        (3.5,  0.5,   0),  # Beat 4.5: Back to open root note
        # --- Bar 2 ---
        (4.0,  0.25,  0),  
        (4.5,  0.25,  0),     
        (5.0,  0.5,   0),      
        (6.0,  0.5,   0),      
        (6.75, 0.25, 12),  # Octave jump
        (7.0,  0.25, 12),  # Octave jump  
        (7.5,  0.5,   0)
    ]
    
    note_count = 0
    # Loop the 2-bar pattern to fill the requested number of bars
    for bar_pair in range(0, bars, 2):
        base_beat = bar_pair * beats_per_bar
        
        for event in base_pattern:
            beat_start = base_beat + event[0]
            beat_len = event[1]
            p_offset = event[2]
            
            # Stop if we exceed the requested bars
            if beat_start >= bars * beats_per_bar:
                break
                
            start_time = beat_start * (60.0 / bpm)
            
            # Make the note slightly shorter than the exact grid length for a tighter metal feel
            is_staccato = (beat_len <= 0.25)
            # Staccato = 50% of grid length. Sustained = 85% of grid length.
            duration_multiplier = 0.5 if is_staccato else 0.85
            actual_end_time = start_time + (beat_len * (60.0 / bpm) * duration_multiplier)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, actual_end_time)
            
            pitch = root_pitch + p_offset
            
            # Velocity logic from tutorial: Stay near 110, vary slightly.
            vel = velocity_base
            if p_offset > 0:
                vel -= 5 # Octave jumps are played slightly softer
            if is_staccato:
                vel += 2 # Short notes hit slightly harder for punch
                
            vel = max(1, min(127, int(vel))) # Clamp safely
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_GetSetMediaItemInfo_String(item, "P_NOTES", "Metal Bass Pattern", True)

    # === Step 5: Add Placeholder Synth (Sound Design) ===
    # Adds a basic stock synth to ensure the MIDI produces sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tune down slightly and increase Saw/Square mix for a buzzy, aggressive bass tone
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.4) # Square mix
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.8) # Saw mix

    return f"Created '{track_name}' with {note_count} metal bass notes over {bars} bars at {bpm} BPM."
