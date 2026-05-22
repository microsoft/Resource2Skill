def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly 110 to reduce harshness as per tutorial
    **kwargs,
) -> str:
    """
    Create a Kick-Locked Modern Rock/Metal Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (used for reference, though mostly root notes).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (lowered to 110 to avoid string clank).
        **kwargs: Additional overrides.

    Returns:
        Status string indicating the result.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Calculate Root Pitch ===
    # Bass is usually plotted around C1 to C2. We'll use octave 2 (MIDI 24 for C1, 36 for C2).
    # Let's anchor around MIDI note 36 (C2)
    root_pitch = 36 + NOTE_MAP.get(key.capitalize(), 0)

    # === Step 3: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 5: Define Rhythmic Patterns (The Kick Rhythms) ===
    # Format: (beat_start, length_in_beats, octave_offset)
    
    # Standard rock/metal syncopated kick pattern
    pattern_standard = [
        (0.0, 0.5, 0),     # Beat 1 (8th note)
        (0.5, 0.5, 0),     # Beat 1.5 (8th note)
        (1.75, 0.25, 0),   # Beat 2.75 (16th note syncopation)
        (2.0, 0.5, 0),     # Beat 3 (8th note)
        (3.0, 0.25, 0),    # Beat 4 (16th note)
        (3.25, 0.25, 0)    # Beat 4.25 (16th note)
    ]
    
    # Turnaround pattern with +12 octave jumps on beat 4
    pattern_fill = [
        (0.0, 0.5, 0),     
        (0.5, 0.5, 0),     
        (1.75, 0.25, 0),   
        (2.0, 0.5, 0),     
        (3.0, 0.25, 12),   # Octave jump up (12th fret)
        (3.25, 0.25, 12),  # Octave jump up
        (3.5, 0.25, 12),   # Octave jump up
        (3.75, 0.25, 12)   # Octave jump up
    ]

    # === Step 6: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        # Use fill pattern every 2nd bar, otherwise standard pattern
        current_pattern = pattern_fill if (bar % 2 == 1) else pattern_standard
        
        for note in current_pattern:
            beat_start, length_beats, octave_offset = note
            
            # Calculate absolute time positions
            abs_beat_start = (bar * beats_per_bar) + beat_start
            abs_beat_end = abs_beat_start + length_beats
            
            start_time = abs_beat_start * (60.0 / bpm)
            end_time = abs_beat_end * (60.0 / bpm)
            
            # Convert time to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Staccato spacing: reduce end_ppq slightly so notes are "chopped"
            end_ppq -= 20 
            
            pitch = root_pitch + octave_offset
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(
                take, 
                False, # selected
                False, # muted
                start_ppq, 
                end_ppq, 
                0, # channel
                pitch, 
                velocity_base, 
                False # noSort
            )
            note_count += 1

    # Sort MIDI data after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 7: Sound Design FX Chain ===
    # 1. Add ReaSynth for the basic tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tune down slightly, mix in some square wave for bite
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.3) # Saw mix
    
    # 2. Add an Amp Simulator (JS Guitar/amp-model) for rock distortion
    amp_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Guitar/amp-model", False, -1)
    if amp_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, amp_idx, 0, 5.0) # Preamp drive
        RPR.RPR_TrackFX_SetParam(track, amp_idx, 5, 1.0) # Amp mode (on)

    # 3. Add EQ to boost the low end and cut harsh highs
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    if eq_idx >= 0:
        # Band 1: Low Shelf boost at ~80Hz
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0) # Type: Low Shelf
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 80.0) # Freq
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, 4.0) # Gain (dB)

    return f"Created '{track_name}' with {note_count} locked bass notes (velocity {velocity_base}) and octave fills over {bars} bars at {bpm} BPM."
