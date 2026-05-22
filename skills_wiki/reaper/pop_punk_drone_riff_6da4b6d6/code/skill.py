def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pop Punk Drone Riff",
    bpm: int = 160,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pop Punk Drone Riff in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (typically 150-180 for this genre).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

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

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Calculate Pitches and Pattern ===
    root_midi = NOTE_MAP.get(key, 0) + 48  # Base octave (e.g., C3 = 48)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    drone_pitch = root_midi

    # 1-bar rhythmic patterns (True = Melody note, False = Drone note)
    # The integer represents the scale degree index for the melody note.
    pattern_bar1 = [
        (False, 0), # 1 (Drone)
        (True, 4),  # & (Melody: 5th)
        (False, 0), # 2 (Drone)
        (False, 0), # & (Drone)
        (True, 2),  # 3 (Melody: 3rd)
        (False, 0), # & (Drone)
        (True, 3),  # 4 (Melody: 4th)
        (False, 0), # & (Drone)
    ]
    pattern_bar2 = [
        (False, 0), # 1 (Drone)
        (True, 5),  # & (Melody: 6th)
        (False, 0), # 2 (Drone)
        (False, 0), # & (Drone)
        (True, 4),  # 3 (Melody: 5th)
        (False, 0), # & (Drone)
        (True, 2),  # 4 (Melody: 3rd)
        (False, 0), # & (Drone)
    ]

    total_notes_inserted = 0

    for bar in range(bars):
        # Alternate between the two patterns for a 2-bar loop feel
        current_pattern = pattern_bar1 if bar % 2 == 0 else pattern_bar2
        bar_start_time = bar * bar_length_sec
        step_len = bar_length_sec / 8.0  # 8th note duration
        
        for i, (is_melody, deg_idx) in enumerate(current_pattern):
            start_time = bar_start_time + i * step_len
            
            if is_melody:
                # Melody is played an octave higher than the drone
                pitch = root_midi + 12 + scale_intervals[deg_idx % len(scale_intervals)]
                vel = min(127, velocity_base + 20)  # Accented
                note_dur = step_len * 0.9           # Slightly legato
            else:
                pitch = drone_pitch
                vel = max(1, velocity_base - 30)    # Palm muted (quieter)
                note_dur = step_len * 0.5           # Staccato to simulate mute
                
            end_time = start_time + note_dur
            
            # Convert physical time to REAPER PPQ (Pulses Per Quarter note)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes_inserted += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain for Tone ===
    # 1. ReaSynth: Sawtooth wave for a buzzy, distorted character
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 1.0)  # Mix sawtooth wave
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)  # Remove pulse wave

    # 2. ReaEQ: High pass filter to clean up low-end mud
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1 parameter 0 is type (0 = Low Shelf, 1 = High Pass in ReaEQ)
    # Note: RPR_TrackFX_SetParam uses normalized values usually, but we'll use a rough generic EQ setup
    # Or rely on the default bands and just set the gain down on band 1.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 100.0) # Band 1 Freq to ~100Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, -12.0) # Band 1 Gain down

    return f"Created '{track_name}' with {total_notes_inserted} notes over {bars} bars at {bpm} BPM in {key} {scale}"
