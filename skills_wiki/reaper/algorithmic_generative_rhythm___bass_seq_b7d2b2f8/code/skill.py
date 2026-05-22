def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic Sequence",
    bpm: int = 120,
    key: str = "C",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an algorithmic generative Bassline and Drum groove.
    Replicates the workflow of procedural sequencer plugins natively in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "F#").
        scale: Scale type (e.g., "pentatonic_minor", "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string detailing the generated items.
    """
    import reaper_python as RPR
    import random

    # Fixed seed for reproducible output based on inputs
    random.seed(bpm + bars)

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Format inputs
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    root_note = NOTE_MAP.get(key, 0) + 36 # Octave 2 for bass
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    
    beats_per_bar = 4
    quarter_len = 60.0 / bpm
    bar_length_sec = quarter_len * beats_per_bar
    item_length = bar_length_sec * bars
    grid_size = 0.25 # 16th notes in beats

    pattern_length_steps = 16 # 1 bar looping generator
    note_count = 0

    # ==========================================
    # TRACK 1: GENERATIVE BASSLINE (ReaSynth)
    # ==========================================
    track_idx_bass = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_bass, True)
    track_bass = RPR.RPR_GetTrack(0, track_idx_bass)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name} - Bass", True)

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", item_length)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)
    
    bass_notes = []
    
    # Procedural generation logic for 1 bar
    for step in range(pattern_length_steps):
        beat_pos = step * grid_size
        is_downbeat = (step % 4 == 0)
        is_upbeat = (step % 4 == 2)
        
        # Probabilities for rhythmic placement
        prob = 0.9 if is_downbeat else (0.6 if is_upbeat else 0.3)
            
        if random.random() < prob:
            # Pitch generation constraint
            if step == 0:
                pitch = root_note # Always anchor the 1st beat
            else:
                if random.random() < 0.5:
                    pitch = root_note
                else:
                    interval = random.choice(scale_intervals)
                    octave_jump = random.choice([0, 0, 12]) # Occasional octave jump
                    pitch = root_note + interval + octave_jump
            
            vel = velocity_base if not is_downbeat else min(127, velocity_base + 15)
            vel = max(1, min(127, vel + random.randint(-10, 10))) # Humanize
            
            length_beats = grid_size * random.uniform(0.5, 0.8) # Staccato synth
            bass_notes.append((beat_pos, pitch, vel, length_beats))
            
    # Print generated bass to MIDI item
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        for beat_pos, pitch, velocity, length_beats in bass_notes:
            start_time_sec = (bar_offset_beats + beat_pos) * quarter_len
            end_time_sec = start_time_sec + (length_beats * quarter_len)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, end_time_sec)
            
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take_bass)

    # Add ReaSynth for immediate bass playback
    fx_idx = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_idx, 2, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_idx, 3, 0.8) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_idx, 5, 0.0) # Attack (Fast)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_idx, 6, 0.2) # Decay

    # ==========================================
    # TRACK 2: GENERATIVE DRUMS (GM Mapping)
    # ==========================================
    track_idx_drums = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_drums, True)
    track_drums = RPR.RPR_GetTrack(0, track_idx_drums)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", f"{track_name} - Drums", True)

    item_drums = RPR.RPR_AddMediaItemToTrack(track_drums)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_LENGTH", item_length)
    take_drums = RPR.RPR_AddTakeToMediaItem(item_drums)
    
    drum_notes = []
    
    for step in range(pattern_length_steps):
        beat_pos = step * grid_size
        
        # Generative Kick (MIDI 36)
        if step == 0:
            drum_notes.append((beat_pos, 36, 110))
        elif step == 8 and random.random() < 0.8:
            drum_notes.append((beat_pos, 36, 100))
        elif step not in [4, 12] and random.random() < 0.15:
            drum_notes.append((beat_pos, 36, 80)) # Syncopated ghost kick
                
        # Generative Snare (MIDI 38)
        if step in [4, 12]:
            drum_notes.append((beat_pos, 38, 115))
        elif random.random() < 0.1:
            drum_notes.append((beat_pos, 38, random.randint(40, 60))) # Ghost note
                
        # Generative Hi-hat (MIDI 42)
        if random.random() < 0.8:
            vel = 100 if step % 4 == 0 else 70 + random.randint(-15, 15)
            drum_notes.append((beat_pos, 42, vel))

    # Print generated drums to MIDI item
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        for beat_pos, pitch, velocity in drum_notes:
            start_time_sec = (bar_offset_beats + beat_pos) * quarter_len
            end_time_sec = start_time_sec + (grid_size * 0.5 * quarter_len)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, end_time_sec)
            
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 0, pitch, int(velocity), False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created algorithmic pattern with {note_count} MIDI events over {bars} bars (Bass + Drums) at {bpm} BPM."
