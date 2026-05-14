def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Moving Bassline",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a humanized, moving slap-bass groove in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Baseline velocity (slap notes will be forced higher).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # Validate inputs
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Base octave for Bass (E1 = MIDI 28)
    base_midi_note = 24 + root_val 
    if base_midi_note < 28:
        base_midi_note += 12 # Keep it out of the sub-mud range

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

    # === Step 4: Define the Groove Pattern ===
    # Format: (Beat_position, Length_in_beats, Scale_Degree_Index, Octave_Offset, Base_Velocity, Is_Slap)
    groove_pattern = [
        (0.0,  0.5,   0, 0, -10, False), # Beat 1 downbeat
        (0.75, 0.25,  0, 0, -15, False), # 16th pickup
        (1.5,  0.125, 0, 1, 30,  True),  # Beat 2 offbeat SLAP (Octave up, short duration)
        (2.0,  0.5,   0, 0, -5,  False), # Beat 3 downbeat
        (2.75, 0.25,  0, 0, -10, False), # 16th pickup
        (3.5,  0.125, 0, 1, 37,  True),  # Beat 4 offbeat SLAP
        (3.75, 0.125, 4, 0, -20, False), # 16th ghost note passing to root (uses 5th of scale)
    ]

    # === Step 5: Generate and Humanize Notes ===
    note_count = 0
    qn_duration = 60.0 / bpm

    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        for p_beat, p_len, p_deg, p_oct, p_vel_mod, is_slap in groove_pattern:
            # 5a. Pitch Calculation
            # Wrap scale degree and calculate octave bumps if degree exceeds scale length
            octave_shift = p_oct + (p_deg // len(scale_intervals))
            scale_idx = p_deg % len(scale_intervals)
            pitch = base_midi_note + scale_intervals[scale_idx] + (octave_shift * 12)
            
            # 5b. Humanized Timing
            beat_pos = bar_start_beat + p_beat
            # Slaps tend to be rushed slightly, normal notes fall in the pocket
            timing_offset = random.uniform(-0.02, 0.01) if not is_slap else random.uniform(-0.03, 0.0)
            
            start_time = (beat_pos + timing_offset) * qn_duration
            end_time = start_time + (p_len * qn_duration)
            
            # Convert time to PPQ (Pulses Per Quarter Note)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # 5c. Humanized Velocity
            target_vel = velocity_base + p_vel_mod
            if is_slap:
                target_vel = 120 # Force slap notes to be extremely hard
            
            vel_fluctuation = int(random.uniform(-5, 5))
            final_vel = max(1, min(127, target_vel + vel_fluctuation))

            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add Sound Design (Synth & FX Chain) ===
    # 1. Add ReaSynth to act as our bass
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth to a mix of Saw and Square for harmonics
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3) # Decay

    # 2. Add ReaEQ to roll off harsh high end, keeping it focused
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4: Lowpass filter
    RPR.RPR_TrackFX_SetParam(track, 1, 0, 3) # Set band 1 type to Lowpass
    RPR.RPR_TrackFX_SetParam(track, 1, 1, 2500) # Cutoff frequency
    
    # 3. Add ReaComp to glue the high-velocity slaps and low-velocity sustains
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 2, 0, -18.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, 2, 1, 4.0)   # Ratio 4:1
    RPR.RPR_TrackFX_SetParam(track, 2, 3, 5.0)   # Attack 5ms
    RPR.RPR_TrackFX_SetParam(track, 2, 4, 100.0) # Release 100ms

    return f"Created '{track_name}' with {note_count} moving bass notes (with slap accents) over {bars} bars at {bpm} BPM in {key} {scale}."
