def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lush Emotional Chords",
    bpm: int = 110,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a lush, humanized, and strummed extended chord progression with thick bass.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C', 'B', 'F#').
        scale: Scale type (e.g., 'minor', 'major').
        bars: Number of bars to generate (defaults to 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the operation.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Data ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    # Center around Octave 4 (Middle C area) for the chord body
    root_midi = 60 + NOTE_MAP.get(key, 0)
    if root_midi > 65: 
        root_midi -= 12 # Keep voicing centered
        
    def get_midi_pitch(degree_zero_idx):
        """Convert a scale degree (0=root, 1=2nd) to an absolute MIDI pitch."""
        octave = degree_zero_idx // len(scale_intervals)
        idx = degree_zero_idx % len(scale_intervals)
        return root_midi + (octave * 12) + scale_intervals[idx]

    # === Step 1: Initialization & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item & Take ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Musical Generation Engine ===
    # Progression: i (0) -> VI (5) -> iv (3) -> V (4)
    progression_degrees = [0, 5, 3, 4]
    
    total_notes_created = 0
    strum_delay_sec = 0.025 # 25ms delay per note for the "Strumizer" effect
    
    for bar_idx in range(min(bars, len(progression_degrees))):
        base_degree = progression_degrees[bar_idx]
        start_sec = bar_idx * bar_length_sec
        # Slightly humanize the chord start time and length
        start_sec += random.uniform(-0.01, 0.02) 
        length_sec = bar_length_sec * random.uniform(0.92, 0.98) 
        
        # 1. Build an Extended Chord (stacking 4 notes = 7th chord)
        chord_degrees = [base_degree, base_degree + 2, base_degree + 4, base_degree + 6]
        pitches = []
        
        for i, deg in enumerate(chord_degrees):
            pitch = get_midi_pitch(deg)
            
            # THE SAUCE: Harmonic Minor Mode Switch
            # If we are in minor, and this is the V chord (degree 4), and this note is its 3rd (i==1)
            # Raise it 1 semitone to make it a Dominant chord (Major 3rd)
            if scale.lower() == "minor" and base_degree == 4 and i == 1:
                pitch += 1
                
            pitches.append(pitch)
            
        # 2. Voice Leading: Drop the highest extension down an octave (Close Voicing)
        if len(pitches) >= 4:
            pitches[-1] -= 12
            
        # 3. Thick Bass Layering: Duplicate root down 1 and 2 octaves
        root_pitch = get_midi_pitch(base_degree)
        pitches.append(root_pitch - 12)
        pitches.append(root_pitch - 24)
        
        # Sort from lowest to highest pitch for proper upward strumming
        pitches.sort()
        
        # 4. Write to MIDI Item with Strumming and Velocity Humanization
        for p_idx, p in enumerate(pitches):
            note_start = start_sec + (p_idx * strum_delay_sec)
            note_end = note_start + length_sec
            
            # Humanize velocity
            v = random.randint(velocity_base - 10, velocity_base + 10)
            
            # Keep the deep bass notes quieter so they don't muddy the mix
            if p_idx < 2:
                v = max(10, v - 20)
                
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(p), int(v), 1)
            total_notes_created += 1

        # 5. Filler Notes (Melody transitions at the end of the measure)
        if bar_idx in [1, 3]: # Add filler notes at end of bar 2 and 4
            filler_start = start_sec + (bar_length_sec * 0.75) # 3rd beat
            filler_pitch = get_midi_pitch(base_degree + 4) + 12 # Octave up 5th
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, filler_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, filler_start + 0.25)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(filler_pitch), velocity_base-15, 1)
            total_notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (FX Chain) ===
    # Add Synth Pad
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth for a pad sound (Mix Saw and Square, slightly softer attack)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.0) # Sine Mix down
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.5) # Square Mix 
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.8) # Saw Mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.05) # Attack (50ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 11, 0.4) # Release (400ms)

    # Add Reverb for Lushness
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.8) # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.3) # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.8) # Room Size
    
    # Lower track volume to compensate for thick frequencies
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    return f"Created '{track_name}' with {total_notes_created} humanized strummed notes over {bars} bars at {bpm} BPM."
