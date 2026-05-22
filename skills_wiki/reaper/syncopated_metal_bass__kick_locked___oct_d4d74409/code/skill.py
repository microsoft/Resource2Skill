def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Djent Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Syncopated Metal Bass pattern locked to a theoretical kick groove, 
    featuring octave jumps and velocity throttling.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Determines the pedal note.
        scale: Scale type (unused here, as it relies primarily on roots and octaves).
        bars: Number of bars to generate (will repeat the 2-bar core loop).
        velocity_base: Base MIDI velocity (0-127). Kept lower than 127 to reduce VST string noise.
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
    
    # Resolve the root note to a low metal bass tuning range (e.g., C1 = MIDI 24)
    root_pc = NOTE_MAP.get(key.upper(), 0)
    root_note = 24 + root_pc 
    octave_note = root_note + 12

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
    
    # === Step 4: Generate Syncopated "Djent" MIDI Pattern ===
    # '1' = pedal root, '2' = octave jump, '0' = rest
    # This represents a complex 16th-note double kick groove
    core_rhythm = [
        # Bar 1
        '1', '0', '1', '1',  '0', '1', '0', '1',  '1', '0', '0', '0',  '1', '0', '1', '1',
        # Bar 2
        '1', '0', '1', '1',  '0', '1', '0', '1',  '1', '0', '0', '0',  '2', '0', '1', '2'
    ]
    
    ppq = 960 # REAPER default pulses per quarter note
    notes_added = 0
    
    # Repeat the 2-bar core rhythm to fill the requested number of bars
    for bar in range(bars):
        # We modulo 2 because our core pattern is 2 bars long
        pattern_offset = (bar % 2) * 16 
        current_bar_rhythm = core_rhythm[pattern_offset : pattern_offset + 16]
        
        for step, hit in enumerate(current_bar_rhythm):
            if hit == '0':
                continue
                
            # Assign pitch and nuanced velocity based on the hit type
            pitch = root_note if hit == '1' else octave_note
            velocity = velocity_base if hit == '1' else min(127, velocity_base + 8)
            
            # Calculate timing in quarter notes
            start_pos_qdr = (bar * beats_per_bar) + (step * 0.25)
            # Make the note length 0.20 quarter notes (slightly shorter than a 0.25 16th note) for a staccato chug
            end_pos_qdr = start_pos_qdr + 0.20 
            
            start_ppq = int(start_pos_qdr * ppq)
            end_ppq = int(end_pos_qdr * ppq)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity, False)
            notes_added += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", "Locked Bass MIDI", True)
    
    return f"Created '{track_name}' with {notes_added} locked bass notes over {bars} bars at {bpm} BPM."
