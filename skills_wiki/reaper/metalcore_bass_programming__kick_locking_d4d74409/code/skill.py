def create_pattern(
    project_name: str = "Metalcore Groove",
    track_name: str = "Prog Metal Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Specifically lowered from 127 as per tutorial
    **kwargs,
) -> str:
    """
    Creates a tight, syncopated metalcore bassline locked to a kick rhythm,
    featuring root-riding, octave jumps, and controlled velocities.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qlen = 60.0 / bpm # Length of one quarter note in seconds
    item_length_sec = qlen * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate base pitch (Drop tuning octave, usually C1 or D1)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Place root in the first octave (MIDI 24 = C1)
    root_pitch = NOTE_MAP.get(key.upper() if len(key) == 1 else key.capitalize(), 0) + 24

    # Define a 2-bar syncopated metalcore pattern
    # Format: (beat_start, duration_in_beats, is_octave_jump)
    two_bar_pattern = [
        # Bar 1
        (0.0,  0.5,  False), # Downbeat, slightly held
        (1.5,  0.25, False), # 'and' of beat 2, staccato kick
        (2.0,  0.25, False), # beat 3 downbeat
        (2.5,  0.25, False), # 'and' of beat 3
        (3.0,  0.5,  True),  # beat 4 downbeat - OCTAVE JUMP ACCENT

        # Bar 2
        (4.0,  0.25, False), # Downbeat, staccato
        (4.25, 0.25, False), # 16th after downbeat
        (4.75, 0.25, False), # 16th before beat 2
        (5.5,  0.25, False), # 'and' of beat 2
        (6.5,  0.25, True),  # 'and' of beat 3 - OCTAVE JUMP ACCENT
        (7.0,  0.5,  False)  # beat 4 downbeat
    ]

    notes_created = 0
    # Loop the 2-bar pattern across the requested number of bars
    for bar_pair in range(0, bars, 2):
        offset_beats = bar_pair * beats_per_bar
        
        for beat_start, duration, is_octave in two_bar_pattern:
            # Check if this note falls outside the requested number of total bars
            if (offset_beats + beat_start) >= (bars * beats_per_bar):
                continue
                
            pitch = root_pitch + 12 if is_octave else root_pitch
            
            start_sec = (offset_beats + beat_start) * qlen
            end_sec = start_sec + (duration * qlen)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Use the tutorial's specific velocity tip (110 instead of 127)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Stock Bass FX ===
    # Using ReaSynth to emulate a thick, subby bass tone
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        # Mix Sawtooth and Square for a rich harmonically dense tone
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.7) # Sawtooth mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3) # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5) # Extra Sine (Sub)
        # Apply lowpass filter to remove digital fizziness, focusing on the low end
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.15) # Filter cutoff

    return f"Created '{track_name}' with {notes_created} syncopated metalcore bass notes over {bars} bars at {bpm} BPM in Drop {key} tuning."
