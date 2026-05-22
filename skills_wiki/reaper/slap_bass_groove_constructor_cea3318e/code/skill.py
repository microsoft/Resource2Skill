def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass Groove",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a highly syncopated Slap Bass Groove in the current REAPER project.
    Features octave pops, ghost notes, walk-ups, and timing humanization.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    
    # Music theory setup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 4)
    # Standard bass guitar range usually centers around E1 (28) to E2 (40).
    base_midi_note = 36 + root_pitch 
    if base_midi_note < 36:
        base_midi_note += 12

    # Adjust the third based on the requested scale
    is_major = "major" in scale.lower() and "pentatonic" not in scale.lower()
    third_offset = 4 if is_major else 3

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
    
    # The 2-bar groove definition matrix
    # Format: (beat_pos, pitch_offset_semitones, velocity_modifier, duration_beats, timing_offset_beats)
    groove_pattern = [
        # --- Bar 1 ---
        (0.00, 0,             15,  0.25,  0.00),   # Downbeat root
        (0.75, -2,           -15,  0.15,  0.01),   # 16th syncopation, pushed late (ghost)
        (1.00, 0,             0,   0.15,  0.00),   # Beat 2 root
        (1.25, 12,            27,  0.10, -0.01),   # POP! (octave higher), slightly rushed
        (1.75, 7,            -5,   0.15,  0.01),   # 5th
        (2.00, 0,             10,  0.20,  0.00),   # Beat 3 downbeat
        (2.75, third_offset, -5,   0.15,  0.02),   # 3rd interval
        (3.00, 12,            20,  0.10, -0.01),   # POP! on beat 4
        (3.50, -2,           -15,  0.15,  0.00),   # Walk-up start (b7)
        (3.75, -1,           -10,  0.15,  0.01),   # Walk-up passing tone (natural 7)
        
        # --- Bar 2 ---
        (4.00, 0,             15,  0.20,  0.00),   # Downbeat root
        (4.75, 10,           -5,   0.15,  0.01),   # High b7
        (5.00, 12,            27,  0.10, -0.01),   # POP!
        (5.25, 0,            -15,  0.15,  0.00),   # Ghost root note
        (5.75, 5,            -5,   0.15,  0.01),   # 4th interval
        (6.00, 7,             10,  0.20,  0.00),   # 5th on downbeat
        (6.75, 5,            -10,  0.15,  0.01),   # 4th back down
        (7.00, third_offset, -5,   0.15,  0.00),   # 3rd interval
        (7.25, 0,             0,   0.15,  0.01),   # Root ghost
        (7.50, -2,           -15,  0.15,  0.00),   # Walk-up start (b7)
        (7.75, -1,           -5,   0.15,  0.01),   # Walk-up passing tone
    ]
    
    note_count = 0
    # Loop the 2-bar pattern to fill the requested number of bars
    for bar in range(0, bars, 2):
        for beat_pos, pitch_offset, vel_mod, dur_beats, time_offset in groove_pattern:
            # Prevent drawing notes past the requested total bars
            if bar * beats_per_bar + beat_pos >= bars * beats_per_bar:
                continue
                
            absolute_beat = (bar * beats_per_bar) + beat_pos + time_offset
            start_time_sec = absolute_beat * (60.0 / bpm)
            end_time_sec = start_time_sec + (dur_beats * (60.0 / bpm))
            
            # Convert project time to PPQ for safe MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            pitch = base_midi_note + pitch_offset
            vel = max(1, min(127, velocity_base + vel_mod))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                                    start_ppq, end_ppq, 
                                    0, pitch, vel, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add Sound Design (Plucky Bass Synth & Slap EQ) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth parameter setup for a staccato/slap tone
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.40) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.25) # Square Mix (for fret buzz)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.00) # Saw Mix 
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.90) # Triangle Mix (deep sub fundamental)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.00) # Attack (instant)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.15) # Decay (fast pluck)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.05) # Sustain (very low)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.05) # Release (tight)
    
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Scoop the mids to make room for kick, boost the highs to emphasize the "pop" transients
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 0, 0.60) # Band 1 Gain (Low end boost)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 3, 0.35) # Band 2 Gain (Scoop mud around 400Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 9, 0.65) # Band 4 Gain (High shelf boost for pops)
    
    return f"Created '{track_name}' with {note_count} highly syncopated slap notes over {bars} bars at {bpm} BPM in {key} {scale}."
