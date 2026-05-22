def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,  # Base max peak for the swell
    **kwargs,
) -> str:
    """
    Creates a 4-bar chord progression with an expressive velocity swell (humanization).
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, etc.).
        scale: Scale type (major, minor).
        bars: Number of bars.
        velocity_base: Maximum velocity reached during the swell.
    """
    import reaper_python as RPR

    # --- Music Theory Lookup Tables ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    # Fallback to major if scale is unsupported in this simple list
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.upper(), 0)

    # Pre-compute a full range of scale notes (MIDI 0-127)
    scale_notes = []
    for oct in range(11):
        for interval in scale_intervals:
            note = (oct * 12) + root_val + interval
            if 0 <= note <= 127:
                scale_notes.append(note)

    # Progression: vi - IV - I - V (0-indexed scale degrees: 5, 3, 0, 4)
    # If minor, this translates to i - VI - III - VII
    progression_degrees = [5, 3, 0, 4] 
    
    # --- Step 1: Initialize Project & Track ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Step 2: Add Instrument (ReaSynth as Piano placeholder) ---
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Soften the attack (param 0) and extend release (param 3) for a piano-like feel
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.05) 
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.6)

    # --- Step 3: Create MIDI Item ---
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = sec_per_beat * beats_per_bar * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # --- Step 4: Populate MIDI with Velocity Swell ---
    # We will place 2 chords per bar (half notes). Total 8 chords.
    total_chords = bars * 2
    
    # Replicate the "click and drag" velocity curve shown in the video:
    # Swell up to velocity_base, then back down.
    # [60, 75, 90, 105, 110, 95, 80, 65]
    peak_index = total_chords // 2
    velocities = []
    min_vel = max(30, int(velocity_base * 0.5))
    
    for i in range(total_chords):
        if i <= peak_index:
            # Ramping up
            progress = i / peak_index
            vel = min_vel + int((velocity_base - min_vel) * progress)
        else:
            # Ramping down
            progress = (i - peak_index) / (total_chords - 1 - peak_index)
            vel = velocity_base - int((velocity_base - min_vel) * progress)
        velocities.append(min(127, max(1, vel)))

    # Draw the chords
    note_count = 0
    for i in range(total_chords):
        # 1. Determine timing
        start_time = i * (sec_per_beat * 2)  # Every 2 beats
        # Leave a tiny gap (0.1 sec) so chords don't perfectly touch (humanization)
        end_time = start_time + (sec_per_beat * 2) - 0.05 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # 2. Determine chord voicing
        # Base octave around C3 / C4 (middle of the keyboard)
        base_degree_index = 21 # roughly octave 3 in our scale array
        chord_root_degree = progression_degrees[i % len(progression_degrees)]
        
        # Build triad (root, 3rd, 5th in the scale)
        triad_indexes = [
            base_degree_index + chord_root_degree,
            base_degree_index + chord_root_degree + 2,
            base_degree_index + chord_root_degree + 4
        ]
        
        # 3. Apply the automated velocity curve
        current_vel = velocities[i]
        
        # 4. Insert notes
        for idx in triad_indexes:
            pitch = scale_notes[idx]
            # Add slight micro-variation to velocity per note for extreme realism
            note_vel = min(127, max(1, current_vel + (idx % 3) - 1))
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, note_vel, True
            )
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} humanized MIDI notes (velocity swell {min_vel}->{velocity_base}) over {bars} bars at {bpm} BPM."
