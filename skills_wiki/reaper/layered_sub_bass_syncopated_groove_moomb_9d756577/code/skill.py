def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Layered Sub Bass",
    bpm: int = 95,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a syncopated, layered sub-bass synth pattern mirroring the tutorial's technique.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (90-100 recommended for this style).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
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
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    base_octave = 24  # C1 for deep bass

    def get_midi_note(degree: int, octave_offset: int = 0) -> int:
        deg = degree % len(scale_intervals)
        octs = (degree // len(scale_intervals)) + octave_offset
        return base_octave + root_val + scale_intervals[deg] + (octs * 12)

    # === Step 1: Initialize Tempo & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 2: Add FX Chain (Sound Design) ===
    # Add ReaSynth (Layered Character + Sub)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 0: Volume (approx -10dB to allow headroom)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.3)
    # Envelope: Fast attack, tight decay, low sustain, fast release (emulates chopped sample)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.1)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.2)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.05)  # Release
    # Waveforms: Sawtooth for character, Extra Sine for sub
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.8)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.0)   # Triangle mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 10, 1.0)  # Extra Sine (Sub) mix

    # Add ReaVerbate for subtle space (as shown in tutorial)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.08)  # Wet very low
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 1.0)   # Dry full
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.5)   # Room size 50%
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 3, 0.5)   # Dampening 50%

    # === Step 3: Create MIDI Item & Sequence ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Define syncopated rhythm pattern (16th note grid)
    # Tuple: (start_16th, length_16ths, scale_degree, octave_offset, vel_offset)
    groove_pattern = [
        (0,  1.5, 0, 0, 0),    # 1.1.00 - Root
        (3,  1.0, 0, -1, -20), # 1.1.75 - Root octave down (syncopated)
        (6,  1.5, 0, 0, 0),    # 1.2.50 - Root (syncopated)
        (10, 1.0, 4, 0, -10),  # 1.3.50 - Perfect 5th (syncopated)
        (12, 1.5, 0, 0, 0)     # 1.4.00 - Root
    ]
    
    notes_created = 0
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        # Add a variation in the 4th bar
        is_turnaround = (bar % 4 == 3)
        
        for p in groove_pattern:
            start_16th, length_16ths, degree, oct_offset, vel_offset = p
            
            # Turnaround variation: Walk down on the last beat
            if is_turnaround and start_16th == 12:
                degree = 2 # 3rd scale degree
                oct_offset = -1
                length_16ths = 1.0
                
            start_time = bar_start_time + (start_16th * (60.0 / bpm) * 0.25)
            end_time = start_time + (length_16ths * (60.0 / bpm) * 0.25)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = get_midi_note(degree, oct_offset)
            vel = max(1, min(127, velocity_base + vel_offset))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_created += 1
            
            # Add final turnaround note if applicable
            if is_turnaround and start_16th == 12:
                end_time_2 = end_time + (1.0 * (60.0 / bpm) * 0.25)
                end_ppq_2 = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_2)
                pitch_2 = get_midi_note(1, oct_offset) # 2nd scale degree
                RPR.RPR_MIDI_InsertNote(take, False, False, end_ppq, end_ppq_2, 0, pitch_2, vel-10, False)
                notes_created += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} syncopated bass notes over {bars} bars at {bpm} BPM."
