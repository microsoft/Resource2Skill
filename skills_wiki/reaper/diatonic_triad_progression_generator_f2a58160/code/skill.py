def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Diatonic Chords",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Diatonic Triad Progression in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: 
            progression (list): List of scale degrees (1-7) for the chords. Default [1, 5, 6, 4].
            octave (int): Base octave for the chords. Default 4.

    Returns:
        Status string detailing the track creation.
    """
    import reaper_python as RPR

    # --- Configuration & Theory Parameters ---
    progression = kwargs.get("progression", [1, 5, 6, 4]) # Standard pop progression (I-V-vi-IV)
    base_octave = kwargs.get("octave", 4)
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if scale not in SCALES:
        scale = "major"
    if key not in NOTE_MAP:
        key = "C"

    root_pitch_class = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # --- Step 1: Project Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Add new track at the end
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Lower volume slightly to prevent clipping (-6dB approx)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # --- Step 2: Add Sound Generator ---
    # We use ReaSynth to guarantee sound output without third-party VSTs
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the ReaSynth sound (lower square/saw mix, increase release)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.1) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5) # Release time

    # --- Step 3: Time & Item Calculation ---
    beats_per_bar = 4
    beat_duration_sec = 60.0 / bpm
    bar_duration_sec = beat_duration_sec * beats_per_bar
    total_duration_sec = bar_duration_sec * bars

    # Create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_duration_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # --- Step 4: Diatonic Chord Generation ---
    notes_added = 0
    chords_per_bar = 1
    duration_per_chord_sec = bar_duration_sec / chords_per_bar
    
    # Loop over the requested number of bars
    for bar in range(bars):
        # Loop the progression
        chord_degree = progression[bar % len(progression)] 
        scale_index = chord_degree - 1 # 0-indexed
        
        # Calculate time positions
        start_time = bar * bar_duration_sec
        end_time = start_time + duration_per_chord_sec
        
        # Convert time to PPQ (MIDI ticks)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Build the triad (Root, 3rd, 5th) in the diatonic scale
        for triad_interval in [0, 2, 4]:
            target_index = scale_index + triad_interval
            
            # Handle wrapping to the next octave if we exceed the 7-note scale
            octave_offset = target_index // 7
            wrapped_index = target_index % 7
            
            # Calculate final MIDI pitch
            note_pitch_class = (root_pitch_class + scale_intervals[wrapped_index]) % 12
            # Add an extra octave offset if the scale interval calculation wrapped past C
            pitch_wrap = 1 if (root_pitch_class + scale_intervals[wrapped_index]) >= 12 else 0
            
            midi_pitch = (base_octave + octave_offset + pitch_wrap) * 12 + note_pitch_class
            
            # Keep pitch within safe MIDI bounds (0-127)
            midi_pitch = max(0, min(127, midi_pitch))
            
            # Insert Note
            # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, False)
            notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    prog_str = "-".join(str(d) for d in progression)
    return f"Created '{track_name}' playing {prog_str} in {key} {scale}. {notes_added} notes across {bars} bars at {bpm} BPM."
