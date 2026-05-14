def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Modern Metal Bassline featuring kick-synced rhythms,
    staccato 16th-note bursts, and octave jumps, with limited velocity
    to reduce string clank.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). Defaults to 110 to tame harshness.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Note map to calculate the Drop-tuned root note
    # We will anchor the bass to octave 1 (MIDI note 24 = C1)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = 24 + NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else "C", 0)

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
    
    # Create the MIDI item spanning the requested bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Program Rhythmic Pattern ===
    # 1 QN = 960 PPQ, 16th note = 240 PPQ
    PPQ_16TH = 240
    
    # 16th-note rhythm grid representing a 2-bar metalcore kick pattern
    # 1 = Root Note (0), 2 = Octave Jump (+12), 0 = Rest
    # This simulates a typical "djent" double-kick syncopation
    two_bar_pattern = [
        # Bar 1
        1, 1, 0, 1,  0, 1, 0, 1,  # Beat 1 & 2: chugs
        1, 1, 1, 0,  1, 0, 0, 0,  # Beat 3 & 4: burst and stop
        # Bar 2
        1, 1, 0, 1,  0, 1, 0, 1,  # Beat 1 & 2: chugs
        1, 1, 1, 0,  2, 0, 2, 0   # Beat 3 & 4: burst and OCTAVE JUMPS
    ]
    
    pattern_length_16ths = len(two_bar_pattern) # 32 (2 bars)
    total_16ths = bars * 16
    
    for i in range(total_16ths):
        step = two_bar_pattern[i % pattern_length_16ths]
        if step > 0:
            # Determine Pitch (Step 1 -> Root, Step 2 -> Octave)
            pitch = root_pitch if step == 1 else root_pitch + 12
            
            # Start and End position in PPQ
            start_ppq = i * PPQ_16TH
            # Create a tight, staccato length (e.g. 120 PPQ = 32nd note duration) 
            # to leave room between fast hits
            end_ppq = start_ppq + (140 if step == 1 else 200) 
            
            # Insert the note
            # Notice velocity is strictly passed as velocity_base (110) 
            # to implement the tutorial's tonal rule.
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity_base, True
            )

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 5: Basic Synthesizer (Placeholder for Bass VST) ===
    # We add a basic synth so the track produces audio out of the box,
    # tuned down slightly to act as a placeholder for a heavy bass sim.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth tuning (useful for deeper bass simulation)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.3) # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) # Tuning (offset)
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.1) # Extra attack for punch

    return f"Created '{track_name}' with kick-synced 16th notes over {bars} bars at {bpm} BPM (Velocity strictly capped at {velocity_base})."
