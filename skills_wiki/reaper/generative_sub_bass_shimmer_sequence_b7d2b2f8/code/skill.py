def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Shimmer Sub",
    bpm: int = 100,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a generative, shimmering sub-bass pattern by simulating a drum sequencer 
    triggering a synth, processed through pitch-shifted reverb.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (unused strictly here as we map drum intervals).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # Use a fixed seed for reproducible generative results
    random.seed(42)

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_offset = NOTE_MAP.get(key, 0)
    
    # Base octave for Sub Bass (e.g., C1 = 24)
    base_note = 24 + root_offset

    # === Step 1: Setup Tempo & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item & Algorithmic Pattern ===
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    start_time = 0.0
    end_time = (60.0 / bpm) * total_beats
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
    take = RPR.RPR_GetActiveTake(item)

    notes_to_add = []
    steps_per_bar = 16 # 16th notes
    total_steps = steps_per_bar * bars
    
    for step in range(total_steps):
        # Emulate Beat Map Drum Logic triggering a Synth
        # Kick -> Root Note
        if step % 8 == 0 or (step % 8 == 3 and random.random() > 0.5):
            notes_to_add.append((step, 0))
        # Snare -> Major 2nd (+2 st)
        if step % 16 == 4 or step % 16 == 12:
            notes_to_add.append((step, 1))
        # Closed Hat -> Tritone (+6 st)
        if step % 2 == 1 and random.random() > 0.6:
            notes_to_add.append((step, 2))
        # Open Hat -> Minor 7th (+10 st)
        if step % 4 == 2 and random.random() > 0.8:
            notes_to_add.append((step, 3))

    # Insert MIDI notes
    intervals = [0, 2, 6, 10] # Root, M2, #4, m7
    
    for step, p_idx in notes_to_add:
        start_beat = step * 0.25 # 16th note step
        end_beat = start_beat + 0.1 # Staccato triggers
        
        note_start_time = start_beat * (60.0 / bpm)
        note_end_time = end_beat * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
        
        pitch = base_note + intervals[p_idx]
        vel = velocity_base + random.randint(-15, 15)
        vel = max(1, min(127, vel))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Sound Design FX Chain ===
    
    # 1. Sub Bass (ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if synth_idx >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.0) # Square Mix = 0 (Pure Sine)
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.0) # Saw Mix = 0
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.0) # Triangle Mix = 0
        RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.0) # Fast Attack

    # 2. Pitch Shifter (+1 Octave Shimmer source)
    pitch_idx = RPR.RPR_TrackFX_AddByName(track, "superpitch", False, -1)
    if pitch_idx >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, pitch_idx, 0, 1.0) # Pitch = +1200 cents
        RPR.RPR_TrackFX_SetParamNormalized(track, pitch_idx, 3, 0.9) # Wet Mix 
        RPR.RPR_TrackFX_SetParamNormalized(track, pitch_idx, 4, 0.95) # Dry Mix 

    # 3. Massive Reverb (Smear the pitched signal)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    if verb_idx >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 2, 0.95) # Massive Room Size
        RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 3, 0.1)  # Low Dampening
        RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.9)  # Wet Mix
        RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 0.95) # Dry Mix

    return f"Created '{track_name}' generative shimmer sequence over {bars} bars at {bpm} BPM in {key}"
