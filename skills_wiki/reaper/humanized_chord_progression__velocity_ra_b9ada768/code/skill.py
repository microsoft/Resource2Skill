def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 70,
    **kwargs,
) -> str:
    """
    Create a Humanized Chord Progression with velocity ramping in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (defaults to 4).
        velocity_base: Base starting MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR
    import math

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Get base pitch (Octave 3)
    root_pitch = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 0) + 48
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # Define a common 4-chord progression based on scale degrees (0-indexed)
    # Major: I - V - vi - IV (0, 4, 5, 3)
    # Minor: i - VI - III - VII (0, 5, 2, 6)
    if scale == "major":
        progression_degrees = [0, 4, 5, 3] 
    else:
        progression_degrees = [0, 5, 2, 6]

    def get_pitch_in_scale(degree_index):
        octave_offset = (degree_index // 7) * 12
        scale_degree = degree_index % 7
        return root_pitch + octave_offset + scale_intervals[scale_degree]

    # === Step 1: Initialize Project & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Create new track additively
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add FX (Stock Instrument Fallback) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower volume slightly to avoid clipping on chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Create MIDI Item & Take ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    total_length_sec = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert "Humanized" MIDI Notes ===
    # We will loop through the progression, placing one chord per bar.
    # Velocity will gradually crescendo (ramp up) over the progression.
    end_velocity_target = min(127, velocity_base + 40) # Ramp up by 40
    
    note_count = 0
    
    for bar_idx in range(bars):
        # Determine which chord in the progression we are on
        prog_idx = bar_idx % len(progression_degrees)
        root_degree = progression_degrees[prog_idx]
        
        # Build triad (root, 3rd, 5th)
        chord_degrees = [root_degree, root_degree + 2, root_degree + 4]
        
        # Calculate timing for this bar (whole notes)
        start_time = bar_idx * bar_length_sec
        end_time = start_time + bar_length_sec
        
        # Convert absolute time to PPQ (pulses per quarter note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Calculate overall velocity swell for this bar (linear interpolation)
        progress = bar_idx / max(1, (bars - 1))
        bar_base_vel = velocity_base + (end_velocity_target - velocity_base) * progress
        
        # Insert notes with internal chord voicing humanization
        for i, degree in enumerate(chord_degrees):
            pitch = get_pitch_in_scale(degree)
            
            # Voicing humanization:
            # Root is strongest, 3rd is quietest (-15%), 5th is mid (-5%)
            if i == 0:
                note_vel = bar_base_vel
            elif i == 1:
                note_vel = bar_base_vel * 0.85
            else:
                note_vel = bar_base_vel * 0.95
                
            # Clamp velocity
            note_vel = max(1, min(127, int(note_vel)))
            
            # Insert note
            # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), note_vel, True)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    # Update timeline/UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} humanized chord notes over {bars} bars at {bpm} BPM."
