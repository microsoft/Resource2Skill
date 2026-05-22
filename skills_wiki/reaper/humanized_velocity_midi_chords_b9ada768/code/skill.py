def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Humanized Velocity MIDI Chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (generates 1 chord per bar).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10]
    }
    
    # Fallback to major if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    base_midi_note = 48 + NOTE_MAP.get(key.upper(), 0) # Start around C3 (Midi note 48)

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

    # === Step 4: Generate Chords & Humanize Velocity/Timing ===
    # A standard I - IV - V - I progression defined by scale degrees
    progression = [0, 3, 4, 0] 
    
    def get_scale_pitch(degree_index, octave_shift=0):
        # Calculate diatonic pitch based on scale degree
        octave = degree_index // len(scale_intervals)
        rem = degree_index % len(scale_intervals)
        return base_midi_note + scale_intervals[rem] + (octave * 12) + (octave_shift * 12)

    notes_created = 0
    
    for bar in range(bars):
        # Loop progression if bars > len(progression)
        chord_root_degree = progression[bar % len(progression)]
        
        # Triad degrees (root, 3rd, 5th)
        chord_degrees = [chord_root_degree, chord_root_degree + 2, chord_root_degree + 4]
        
        start_time = bar * bar_length_sec
        # Leave a tiny gap at the end of the bar for articulation
        end_time = start_time + (bar_length_sec * 0.95) 
        
        base_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        base_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for i, degree in enumerate(chord_degrees):
            pitch = get_scale_pitch(degree)
            
            # --- HUMANIZATION LOGIC ---
            # 1. Velocity weighting (root is strongest, 3rd is quietest, 5th is mid)
            if i == 0:
                vel = velocity_base + 5
            elif i == 1:
                vel = velocity_base - 15
            else:
                vel = velocity_base - 5
                
            # 2. Velocity random jitter
            vel += random.randint(-8, 8)
            vel = max(1, min(127, vel)) # Clamp between 1-127
            
            # 3. Timing jitter (Stagger notes slightly to avoid robotic simultaneous attack)
            # 960 PPQ is typical for a quarter note; 20 PPQ is a very subtle human micro-shift
            timing_jitter = random.randint(-15, 25) 
            start_ppq = base_start_ppq + timing_jitter
            end_ppq = base_end_ppq + timing_jitter
            
            # Insert the humanized note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX ===
    # Using ReaSynth as a fallback, configured to act somewhat like a plucked/piano string
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth to have a fast attack and decaying sustain (Pluck/Piano style)
    # Param 1: Attack (fast)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 1, 0.01)
    # Param 2: Decay (moderate)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.4)
    # Param 3: Sustain (low)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.1)
    # Param 4: Release (moderate)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.3)

    return f"Created '{track_name}' with {notes_created} humanized velocity chord notes over {bars} bars at {bpm} BPM in {key} {scale}."
