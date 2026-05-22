def create_pattern(
    project_name: str = "MultiTrackOrchestration",
    track_name: str = "Arrangement",
    bpm: int = 125,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track pop-rock arrangement (Drums, Bass, Rhythm Gtr, Lead Gtr)
    demonstrating multi-track MIDI composition.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (unused, as we create 4 specific tracks).
        bpm: Tempo in BPM.
        key: Root note (e.g., "A", "C#").
        scale: Scale type ("minor" or "major").
        bars: Number of bars to generate (generates a looping progression).
        velocity_base: Base MIDI velocity.
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
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Default to minor if an unsupported scale is passed for this specific pattern
    safe_scale = scale if scale in SCALES else "minor"
    scale_intervals = SCALES[safe_scale]
    root_midi = NOTE_MAP.get(key, 9) # Default to A

    # Progression logic
    if safe_scale == "major":
        progression = [0, 4, 5, 3] # I - V - vi - IV
    else:
        progression = [0, 5, 2, 6] # i - VI - III - VII

    # Setup Timing
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    cursor_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    item_length = bar_sec * bars

    # Helper: Add Track + Item
    def create_layer(name, add_synth=True):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        if add_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        return take

    # Helper: Add Note
    def add_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # 1. Create Tracks and Takes
    take_drums = create_layer("Drums", add_synth=False)
    take_bass = create_layer("Bass", add_synth=True)
    take_rhythm = create_layer("Rhythm Gtr", add_synth=True)
    take_lead = create_layer("Lead Gtr", add_synth=True)

    # 2. Generate Musical Data
    for b in range(bars):
        bar_start = cursor_pos + (b * bar_sec)
        
        # --- DRUMS ---
        # Kick (MIDI 36)
        add_note(take_drums, bar_start, bar_start + beat_sec*0.5, 36, velocity_base + 10)
        add_note(take_drums, bar_start + beat_sec*2.0, bar_start + beat_sec*2.5, 36, velocity_base)
        add_note(take_drums, bar_start + beat_sec*2.5, bar_start + beat_sec*3.0, 36, velocity_base - 10)
        
        # Snare (MIDI 38)
        add_note(take_drums, bar_start + beat_sec*1.0, bar_start + beat_sec*1.5, 38, velocity_base + 10)
        add_note(take_drums, bar_start + beat_sec*3.0, bar_start + beat_sec*3.5, 38, velocity_base + 10)
        
        # Hi-Hats (MIDI 42)
        for h in range(8):
            h_start = bar_start + (h * beat_sec * 0.5)
            h_vel = velocity_base - 10 if h % 2 == 0 else velocity_base - 30
            add_note(take_drums, h_start, h_start + (beat_sec*0.25), 42, h_vel)
            
        # Crash (MIDI 49) on the first beat of the loop
        if b == 0:
            add_note(take_drums, bar_start, bar_start + beat_sec, 49, velocity_base + 20)

        # --- HARMONY (Bass, Rhythm, Lead) ---
        degree = progression[b % len(progression)]
        scale_root = scale_intervals[degree]
        
        # Calculate Triad intervals for the current chord
        third_idx = (degree + 2) % len(scale_intervals)
        fifth_idx = (degree + 4) % len(scale_intervals)
        
        scale_third = scale_intervals[third_idx] + (12 if third_idx < degree else 0)
        scale_fifth = scale_intervals[fifth_idx] + (12 if fifth_idx < degree else 0)

        # Bass (Octave 2) - Driving 8th notes
        bass_pitch = root_midi + 24 + scale_root
        for i in range(8):
            n_start = bar_start + (i * beat_sec * 0.5)
            n_end = n_start + (beat_sec * 0.45) # Staccato gap
            add_note(take_bass, n_start, n_end, bass_pitch, velocity_base)

        # Rhythm Guitar (Octave 3) - Whole Note Power Chords (Root, 5th, Octave)
        rhythm_p1 = root_midi + 36 + scale_root
        rhythm_p2 = rhythm_p1 + 7  # Perfect Fifth
        rhythm_p3 = rhythm_p1 + 12 # Octave
        r_end = bar_start + (bar_sec * 0.98)
        add_note(take_rhythm, bar_start, r_end, rhythm_p1, velocity_base - 10)
        add_note(take_rhythm, bar_start, r_end, rhythm_p2, velocity_base - 10)
        add_note(take_rhythm, bar_start, r_end, rhythm_p3, velocity_base - 10)

        # Lead Guitar (Octave 4) - 8th Note Arpeggio (Root, 3rd, 5th, 3rd)
        arp_pitches = [
            root_midi + 48 + scale_root,
            root_midi + 48 + scale_third,
            root_midi + 48 + scale_fifth,
            root_midi + 48 + scale_third
        ]
        
        for i in range(8):
            n_start = bar_start + (i * beat_sec * 0.5)
            n_end = n_start + (beat_sec * 0.45)
            add_note(take_lead, n_start, n_end, arp_pitches[i % 4], velocity_base - 15)

    # Sort MIDI data for all takes
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_rhythm)
    RPR.RPR_MIDI_Sort(take_lead)
    
    RPR.RPR_UpdateArrange()

    return f"Created 4-track orchestration (Drums, Bass, Rhythm, Lead) over {bars} bars in {key} {safe_scale} at {bpm} BPM."
