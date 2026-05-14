def create_pattern(
    project_name: str = "Trap_Project",
    track_name: str = "Trap_Groove",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Half-Time Trap Drum & 808 Foundation in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM (130-150 recommended for this style).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (must be even, ideally 4 or 8).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # Determine 808 root note (around C2 / MIDI 36 for sub bass)
    root_pitch = NOTE_MAP.get(key, 0) + 36
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    turnaround_pitch = root_pitch + scale_intervals[4] # 5th degree of the scale

    # Set BPM
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper: Create track with MIDI item
    def create_midi_track(name, num_bars):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Calculate item length in seconds
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_length_sec * num_bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # Helper: Add MIDI note based on Quarter Notes (Beats)
    def add_note(take, start_qn, end_qn, pitch, vel):
        start_time = start_qn * (60.0 / bpm)
        end_time = end_qn * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        # MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(vel), False)

    # 1. Create Tracks & Items
    kick_track, kick_take = create_midi_track(f"{track_name}_Kick", bars)
    snare_track, snare_take = create_midi_track(f"{track_name}_Snare", bars)
    hat_track, hat_take = create_midi_track(f"{track_name}_Hats", bars)
    bass_track, bass_take = create_midi_track(f"{track_name}_808", bars)

    # Add native synth to 808 track to guarantee sound
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)

    # 2. Program the Patterns
    for b in range(bars):
        bar_start_qn = b * 4.0
        
        # --- SNARE (Half-time: lands exactly on beat 3) ---
        add_note(snare_take, bar_start_qn + 2.0, bar_start_qn + 2.25, 38, velocity_base)
        
        # --- HI-HATS (Continuous 8th notes with bounce and rolls) ---
        for h in range(8):
            hat_qn = bar_start_qn + (h * 0.5)
            # Dynamic velocity: downbeats hit harder than upbeats
            hat_vel = velocity_base if h % 2 == 0 else velocity_base * 0.75
            
            # Add a 32nd note roll at the end of every 2nd bar
            if b % 2 == 1 and h == 7:
                roll_vel = velocity_base * 0.8
                add_note(hat_take, hat_qn, hat_qn + 0.125, 42, roll_vel)
                add_note(hat_take, hat_qn + 0.125, hat_qn + 0.25, 42, roll_vel)
                add_note(hat_take, hat_qn + 0.25, hat_qn + 0.375, 42, roll_vel)
                add_note(hat_take, hat_qn + 0.375, hat_qn + 0.5, 42, roll_vel)
            else:
                add_note(hat_take, hat_qn, hat_qn + 0.25, 42, hat_vel)

        # --- KICK & 808 (Syncopated interactions) ---
        # Pattern A (Bars 1, 3, etc.) vs Pattern B (Bars 2, 4, etc.)
        kick_rhythms = [0.0, 1.5, 3.5] if b % 2 == 0 else [0.0, 1.5, 2.5]
        
        for i, kick_qn_offset in enumerate(kick_rhythms):
            abs_qn = bar_start_qn + kick_qn_offset
            
            # Kick (GM Note 36)
            add_note(kick_take, abs_qn, abs_qn + 0.25, 36, velocity_base + 10)
            
            # 808 Sub Bass
            # Note length: holds until the next kick, or a standard 1.5 beats
            note_len = 1.5 if i < len(kick_rhythms)-1 else 0.5
            
            # Harmonic turnaround on the very last note of the total phrase
            current_pitch = root_pitch
            if b == bars - 1 and i == len(kick_rhythms) - 1:
                current_pitch = turnaround_pitch
                
            add_note(bass_take, abs_qn, abs_qn + note_len, current_pitch, velocity_base)

    # 3. Finalize and Sort MIDI items
    for take in [kick_take, snare_take, hat_take, bass_take]:
        RPR.RPR_MIDI_Sort(take)
    
    RPR.RPR_UpdateTimeline()

    return f"Created Half-Time Trap Groove '{track_name}' across 4 separate tracks over {bars} bars at {bpm} BPM in {key} {scale}."
