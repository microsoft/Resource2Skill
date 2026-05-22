def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Funky Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a humanized slap bass groove in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., E, A, C).
        scale: Scale type (e.g., minor, dorian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the generated bassline.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Fallback to minor if scale is not in dictionary
    selected_scale = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Calculate base MIDI note (targeting E1 to D#2 range for bass)
    base_midi = 24 + NOTE_MAP.get(key.upper(), 4) # 24 is C1. E is 28 (E1)
    if base_midi < 28:
        base_midi += 12 # Keep it from getting impossibly low and muddy

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Synth for Plucky Bass Sound ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a bass pluck:
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)    # Tuning (0)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.7)    # Square mix (thick bass)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)    # Saw mix (bite)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0)    # Attack (Instant)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.2)    # Decay (Short)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.1)    # Sustain (Low)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.15)   # Release (Short)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate the Humanized Pattern ===
    # Pattern data structure: (beat_position, scale_degree, octave_shift, length_in_beats, relative_velocity)
    # This is a 2-bar looping funky slap pattern.
    pattern = [
        # --- Bar 1 ---
        (0.00,  0, 0, 0.50,  1.00),  # Beat 1: Root foundation
        (1.50,  0, 0, 0.25,  0.80),  # Beat 2 &: Syncopated Root setup
        (2.25,  0, 1, 0.125, 1.25),  # Beat 3 e: Octave SLAP! (very short, very loud)
        (2.75,  0, 0, 0.25,  0.60),  # Beat 3 a: Low ghost note
        (3.00,  0, 0, 0.50,  0.95),  # Beat 4: Root anchor
        (3.75,  4, 0, 0.25,  0.85),  # Beat 4 a: 5th walkup passing tone
        
        # --- Bar 2 ---
        (4.00,  0, 0, 0.50,  1.00),  # Beat 1: Root foundation
        (5.50,  0, 0, 0.25,  0.80),  # Beat 2 &: Syncopated Root
        (6.25,  0, 1, 0.125, 1.25),  # Beat 3 e: Octave SLAP!
        (6.75,  6, 0, 0.25,  0.85),  # Beat 3 a: Flat 7th walkup
        (7.00,  4, 0, 0.50,  0.95),  # Beat 4: 5th anchor
        (7.75,  6, -1, 0.25, 0.90)   # Beat 4 a: Low flat 7th turnaround back to root
    ]

    note_count = 0
    # Loop over the requested number of bars in 2-bar chunks
    for bar_pair in range(0, bars, 2):
        bar_offset_beats = bar_pair * 4.0
        
        for note_def in pattern:
            beat_pos, degree, oct_shift, length_beats, rel_vel = note_def
            
            # Bound check: skip notes that would generate past requested bars
            if (bar_offset_beats + beat_pos) >= (bars * 4.0):
                continue
                
            # --- HUMANIZATION (Imitating Reality) ---
            # Random timing offset between -0.02 and +0.02 beats (approx +/- 10ms at 120bpm)
            timing_offset = random.uniform(-0.02, 0.02)
            
            # Apply offset to start, but keep length intact
            start_beat = max(0.0, bar_offset_beats + beat_pos + timing_offset)
            end_beat = start_beat + length_beats
            
            # Convert beats to time in seconds, then to PPQ (Pulses Per Quarter Note)
            start_time = start_beat * (60.0 / bpm)
            end_time = end_beat * (60.0 / bpm)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Calculate Pitch
            # Handle degree wrapping just in case it goes above scale length
            octave_calc = oct_shift + (degree // len(selected_scale))
            scale_idx = degree % len(selected_scale)
            pitch = base_midi + selected_scale[scale_idx] + (octave_calc * 12)
            
            # Ensure pitch is in valid MIDI range
            pitch = max(0, min(127, int(pitch)))
            
            # Humanize Velocity
            vel_variance = random.randint(-5, 5)
            final_vel = int((velocity_base * rel_vel) + vel_variance)
            final_vel = max(1, min(127, final_vel)) # Clamp 1-127
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, True)
            note_count += 1

    # Sort MIDI events after inserting all (True flag above = noSort to save CPU, so sort once here)
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} humanized slap bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
