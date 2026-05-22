def create_pattern(
    project_name: str = "HeavyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Specifically lowered from 127 per tutorial
    **kwargs,
) -> str:
    """
    Create a Rock/Metal Kick-Locked Bass pattern in the current REAPER project.
    """
    import reaper_python as RPR
    
    # === Step 1: Initialize Theory & Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Root note mapped to the 2nd octave (e.g., Drop C tuning equivalent range)
    root_midi = 36 + NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Add FX Chain for Heavy Bass (Stock Placeholder) ===
    # Add a synth to act as the bass
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.0)    # Volume (lower to avoid clipping)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.5)    # Square mix (adds grit)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.5)    # Saw mix (adds bite)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 0.1)    # Attack tight
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 5, 0.1)    # Decay short for chugs
    
    # Add compression to flatten the dynamic range (essential for modern metal bass)
    fx_comp = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 0, -20.0)   # Threshold
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 1, 8.0)     # Ratio 8:1
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 2, 2.0)     # Attack 2ms
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 3, 50.0)    # Release 50ms
    
    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Enable MIDI item to accept inserted notes
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 5: Define Rhythmic Pattern & Insert Notes ===
    # A typical metalcore syncopated "kick" pattern (positions in beats)
    # Format: (beat_position, duration_in_beats, is_octave_jump)
    base_pattern = [
        (0.0,  0.25, False), # Chug
        (0.5,  0.25, False), # Chug
        (1.25, 0.25, False), # Syncopated hit
        (1.5,  0.25, False), # Syncopated hit
        (2.0,  0.50, False), # Held note (let ring)
        (2.75, 0.25, False), # Pickup
        (3.0,  0.25, False), # Hit
        (3.5,  0.25, False)  # Hit
    ]
    
    # Define an alternate bar with the "12th fret" octave jump variation mentioned in tutorial
    fill_pattern = [
        (0.0,  0.25, False), 
        (0.5,  0.25, False), 
        (1.25, 0.25, False), 
        (1.5,  0.25, False), 
        (2.0,  0.50, False), 
        (3.0,  0.25, True),  # OCTAVE JUMP!
        (3.5,  0.25, True)   # OCTAVE JUMP!
    ]

    total_notes = 0
    
    # Generate notes across all requested bars
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        # Use fill pattern on every 2nd bar (e.g., bar index 1, 3, 5)
        current_pattern = fill_pattern if (bar % 2 == 1) else base_pattern
        
        for pos_beats, dur_beats, octave_jump in current_pattern:
            # Calculate absolute time in seconds
            note_start_sec = bar_start_time + (pos_beats * (60.0 / bpm))
            note_end_sec = note_start_sec + (dur_beats * (60.0 / bpm))
            
            # Convert time to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
            
            # Pitch logic: Root note, or Root + 12 for octave jumps
            pitch = root_midi + 12 if octave_jump else root_midi
            
            # Add note (not sorted immediately for performance)
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, int(pitch), int(velocity_base), True
            )
            total_notes += 1

    # Finalize MIDI by sorting the inserted notes
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes} kick-locked notes (velocity {velocity_base}) over {bars} bars at {bpm} BPM in {key}."
