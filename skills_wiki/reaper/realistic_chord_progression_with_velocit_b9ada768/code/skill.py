def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Create a Realistic Chord Progression with Velocity Humanization.

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
        Status string describing the created track and chords.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    if hasattr(RPR, "RPR_SetCurrentBPM"):
        RPR.RPR_SetCurrentBPM(0, bpm, False)
    else:
        RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, bpm, 0, 0, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # === Step 4: Music Theory & Ramping Setup ===
    root_note = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_note_in_scale(root_midi, intervals, degree):
        octave = degree // len(intervals)
        scale_degree = degree % len(intervals)
        return root_midi + (octave * 12) + intervals[scale_degree]

    base_octave_midi = 48 # C3
    # Chord Voicing: Bass (Root -1 oct), Root, 3rd, 5th
    chord_degrees = [-7, 0, 2, 4]
    notes_to_play = [get_note_in_scale(root_note + base_octave_midi, scale_intervals, d) for d in chord_degrees]
    
    total_chords = bars * beats_per_bar
    
    # Ramp bounds for the macro crescendo
    vel_ramp_start = max(1, velocity_base - 30)
    vel_ramp_end = min(127, velocity_base + 30)
    
    # Deterministic arrays for organic micro-fluctuations
    humanize_offsets = [3, -2, 4, -3, 1, -4, 2, -1]
    # Anchoring dynamics: Bass is strongest, 3rd is softest
    chord_voice_offsets = [0, -8, -12, -4]
    
    # === Step 5: Insert Notes with Dynamic Velocities ===
    for i in range(total_chords):
        # 1. Macro velocity ramp interpolation (simulating "click and drag" in velocity lane)
        if total_chords > 1:
            base_vel = int(vel_ramp_start + (vel_ramp_end - vel_ramp_start) * (i / (total_chords - 1)))
        else:
            base_vel = velocity_base
            
        # 2. Micro humanization offset
        human_offset = humanize_offsets[i % len(humanize_offsets)]
        
        # Timing (quarter notes with a staccato gap for articulation clarity)
        start_qn = i
        end_qn = i + 0.85
        
        start_time_sec = start_qn * (60.0 / bpm)
        end_time_sec = end_qn * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
        
        for j, pitch in enumerate(notes_to_play):
            # 3. Micro voicing offset
            voice_offset = chord_voice_offsets[j % len(chord_voice_offsets)]
            final_vel = base_vel + human_offset + voice_offset
            final_vel = max(1, min(127, final_vel)) # Clamp to valid MIDI range
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(final_vel), False)
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add Stock FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    return f"Created '{track_name}' with {total_chords} humanized chords over {bars} bars at {bpm} BPM."
