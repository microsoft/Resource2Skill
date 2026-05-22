def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Humanized Wide-Voiced Chord Progression in the current REAPER project.
    """
    import reaper_python as RPR
    import random

    # Music theory lookup tables
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Lower volume to prevent clipping

    # === Step 3: Add FX Chain (ReaSynth as placeholder) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Harmony Calculations
    base_note = NOTE_MAP.get(key.upper(), 0) + 60 # C4 = 60
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    def get_scale_note(degree):
        octave_shift = degree // len(scale_intervals)
        note_idx = degree % len(scale_intervals)
        return base_note + (octave_shift * 12) + scale_intervals[note_idx]

    # I - V - vi - IV progression
    progression = [0, 4, 5, 3]
    total_notes = 0
    
    # === Step 5: Generate Humanized MIDI ===
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # Calculate diatonic triad
        root = get_scale_note(degree)
        third = get_scale_note(degree + 2)
        fifth = get_scale_note(degree + 4)
        
        # Wide Voicing: Drop the root 1 and 2 octaves down
        notes = [root - 24, root - 12, root, third, fifth]
        
        # Generate quarter note chords
        for beat in range(4):
            start_time = (bar * beats_per_bar + beat) * (60.0 / bpm)
            end_time = start_time + (60.0 / bpm) * 0.85 # 85% gate length
            
            # Linear Velocity Ramp (Swell)
            progress = (bar * 4 + beat) / (bars * 4 - 1)
            target_vel = int(velocity_base * 0.4 + (velocity_base * 0.6 * progress))
            
            for pitch in notes:
                # Add micro-humanization to velocity and timing
                human_vel = max(1, min(127, target_vel + random.randint(-12, 12)))
                human_start = max(0.0, start_time + random.uniform(-0.015, 0.015))
                human_end = end_time + random.uniform(-0.015, 0.015)
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, human_start)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, human_end)
                
                # Insert note (noSort = True for performance, sorted at the end)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, human_vel, True)
                total_notes += 1

    # Apply all MIDI note insertions
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {total_notes} humanized wide-voiced notes over {bars} bars at {bpm} BPM."
