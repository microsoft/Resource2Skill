def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Velocity-Humanized MIDI Chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    scale_degrees = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Start at C3 (MIDI 48)

    # Function to get pitch safe-wrapping the scale
    def get_pitch_in_scale(degree_index):
        octave_shift = degree_index // len(scale_degrees)
        scale_note = scale_degrees[degree_index % len(scale_degrees)]
        return root_midi + (octave_shift * 12) + scale_note

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (ReaSynth as Piano Placeholder) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more "piano-like" plucky envelope
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Saw shape down
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0) # Pulse shape down
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0) # Attack time short
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3) # Decay time
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.2) # Sustain level low
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4) # Release time

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Humanized Chord Progression ===
    # Progression degrees (0-indexed): I, V, vi, IV
    progression = [0, 4, 5, 3] 
    
    notes_added = 0
    for bar in range(bars):
        # Repeat progression if bars > 4
        chord_root_idx = progression[bar % len(progression)]
        
        # Chord notes (Root, 3rd, 5th)
        chord_degrees = [chord_root_idx, chord_root_idx + 2, chord_root_idx + 4]
        
        # Rhythm Pattern within the bar (Beat times: [start_beat, length_beats])
        # A syncopated comping rhythm demonstrating velocity changes
        rhythm_hits = [
            (0.0, 1.4), # Downbeat: Strong
            (1.5, 0.4), # Syncopated offbeat: Weak
            (2.0, 1.9)  # Beat 3: Medium
        ]
        
        # Velocity profile corresponding to the rhythm hits
        vel_profile = [
            velocity_base,           # Accent downbeat
            int(velocity_base * 0.7), # Soften offbeat
            int(velocity_base * 0.85) # Medium sustain
        ]

        for hit_idx, (start_b, len_b) in enumerate(rhythm_hits):
            start_time = (bar * bar_length_sec) + (start_b * beat_length_sec)
            end_time = start_time + (len_b * beat_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            base_hit_vel = vel_profile[hit_idx]
            
            for voice_idx, degree in enumerate(chord_degrees):
                pitch = get_pitch_in_scale(degree)
                
                # Humanize: Inner voices (3rd, 5th) are played slightly softer than the root
                voice_vel_adjustment = 0 if voice_idx == 0 else -10
                final_vel = max(1, min(127, base_hit_vel + voice_vel_adjustment))
                
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, pitch, final_vel, True
                )
                notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} dynamically varied notes over {bars} bars at {bpm} BPM in {key} {scale}"
