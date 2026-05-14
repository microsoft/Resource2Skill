def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a Groovy Octave Slap Bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # --- Music Theory Definitions ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_midi_root = 36 + NOTE_MAP.get(key.upper(), NOTE_MAP["E"]) # Default to E1 range
    
    def get_midi_pitch(degree, octave_offset=0):
        """Calculates exact MIDI pitch based on scale degree and octave."""
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        pitch = base_midi_root + scale_intervals[idx] + (octave * 12) + (octave_offset * 12)
        return max(0, min(127, pitch))

    # --- REAPER Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # --- Generate MIDI Item ---
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    sixteenth_length_sec = (60.0 / bpm) * 0.25
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Base Syncopated 16-step pattern (1 bar)
    # Tuple format: (16th_position, scale_degree, octave_jump, duration_16ths, is_slap_accent)
    groove_pattern = [
        (0.0,  0,  0, 2.0, False), # Beat 1: Root long
        (2.5,  0,  0, 1.0, False), # Beat 1.75: Root syncopated short
        (4.0,  0,  1, 0.8, True),  # Beat 2: Slap Octave pop!
        (7.0,  0,  0, 1.0, False), # Beat 2.75: Root syncopated
        (8.0,  0,  1, 0.8, True),  # Beat 3: Slap Octave pop!
        (10.5, 0,  0, 1.5, False), # Beat 3.75: Root syncopated
        (12.5, 2,  0, 1.0, False), # Beat 4.25: Step (minor 3rd)
        (14.0,-1,  0, 1.0, False), # Beat 4.75: Step (flat 7th from below) leading back
    ]

    total_notes = 0
    for bar in range(bars):
        for step in groove_pattern:
            pos_16ths, degree, oct_offset, len_16ths, is_slap = step
            
            # --- HUMANIZATION ---
            # Slight timing push/pull (not applied to the hard on-beat slaps)
            h_offset = random.uniform(-0.05, 0.1) if not is_slap else 0.0
            h_pos = max(0.0, pos_16ths + h_offset)
            h_len = max(0.2, len_16ths * random.uniform(0.85, 1.1))
            
            # Velocity dynamics
            if is_slap:
                vel = 127 # Max velocity for the slap string pop
            else:
                vel = int(velocity_base * random.uniform(0.9, 1.05))
                vel = max(1, min(126, vel))
            
            start_time = (bar * bar_length_sec) + (h_pos * sixteenth_length_sec)
            end_time = start_time + (h_len * sixteenth_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = get_midi_pitch(degree, oct_offset)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes += 1

    RPR.RPR_MIDI_Sort(take)
    
    # --- Sound Design: ReaSynth & ReaComp ---
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.4) # Vol down
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.8) # Add Square wave for rich mid-harmonics
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.0) # Instant attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.2) # Fast decay for plucky feel
    
    # Add ReaComp to tame the 127 velocity slaps and glue the groove
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 0, 0.3) # Threshold down
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 1, 0.6) # Ratio ~ 4:1
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 2, 0.1) # Fast Attack to catch slap peak
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 3, 0.3) # Fast Release
    
    RPR.RPR_UpdateTimeline()
    RPR.RPR_TrackList_AdjustWindows(False)
    
    return f"Created '{track_name}' with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}."
