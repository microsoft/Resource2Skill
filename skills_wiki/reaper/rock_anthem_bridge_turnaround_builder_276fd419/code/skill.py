def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Bridge",
    bpm: int = 94,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a multi-track Rock Bridge (iv-v-III-v7) with driving 8th notes in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (will loop the 4-bar progression).
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
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10]
    }

    root_val = NOTE_MAP.get(key, 5) # Default F
    intervals = SCALES.get(scale, SCALES["minor"])
    
    # 0-indexed scale degrees for: iv, v, III, v7
    bridge_progression = [
        {"degree": 3, "num_notes": 3}, # Bar 1: subdominant triad
        {"degree": 4, "num_notes": 3}, # Bar 2: dominant triad
        {"degree": 2, "num_notes": 3}, # Bar 3: mediant triad
        {"degree": 4, "num_notes": 4}, # Bar 4: dominant 7th (turnaround)
    ]

    def get_diatonic_chord(root_deg, num_notes, octave):
        notes = []
        for i in range(num_notes):
            deg = root_deg + (i * 2) # Stack thirds
            oct_offset = deg // len(intervals)
            scale_idx = deg % len(intervals)
            pitch = root_val + intervals[scale_idx] + (octave + oct_offset) * 12
            notes.append(pitch)
        return notes

    # Set project tempo
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0.0, -1, -1, bpm, 4, 4, True)

    beats_per_bar = 4
    quarter_len = 60.0 / bpm
    bar_len = quarter_len * beats_per_bar
    total_len = bar_len * bars

    # Helper to create a track with an item and basic FX
    def setup_track(name_suffix, vol_db):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", f"{track_name} {name_suffix}", True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "D_VOL", 10**(vol_db/20.0))
        
        # Add basic synth
        fx_idx = RPR.RPR_TrackFX_AddByName(trk, "ReaSynth", False, -1)
        
        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(trk, 0.0, total_len, False)
        take = RPR.RPR_GetActiveTake(item)
        return trk, take, fx_idx

    # --- TRACK 1: ORGAN (Sustained Chords) ---
    trk_org, take_org, fx_org = setup_track("Organ", -6.0)
    # Tweak ReaSynth for an organ-like square tone
    RPR.RPR_TrackFX_SetParam(trk_org, fx_org, 2, 0.6) # Square mix

    # --- TRACK 2: BASS (Driving 8ths) ---
    trk_bas, take_bas, fx_bas = setup_track("Bass", -3.0)
    # Tweak ReaSynth for aggressive saw bass
    RPR.RPR_TrackFX_SetParam(trk_bas, fx_bas, 3, 0.9) # Saw mix
    
    # --- TRACK 3: GUITAR (Driving 8th Chords) ---
    trk_gtr, take_gtr, fx_gtr = setup_track("Guitar", -8.0)
    # Tweak ReaSynth for blended bright tone
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 2, 0.4) 
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 3, 0.5)

    # Generate MIDI Data
    eighth_len = quarter_len / 2.0
    
    for bar in range(bars):
        bar_start_time = bar * bar_len
        # Loop progression every 4 bars
        chord_def = bridge_progression[bar % 4] 
        
        chord_pitches_org = get_diatonic_chord(chord_def["degree"], chord_def["num_notes"], 5)
        chord_pitches_gtr = get_diatonic_chord(chord_def["degree"], chord_def["num_notes"], 4)
        bass_pitch = chord_pitches_org[0] - 24 # Drop 2 octaves

        # 1. Insert Organ Notes (Whole note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_org, bar_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_org, bar_start_time + bar_len)
        for pitch in chord_pitches_org:
            RPR.RPR_MIDI_InsertNote(take_org, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base * 0.8), False)

        # 2. Insert Bass & Guitar Notes (Driving 8th notes)
        for e in range(8): # 8 eighths in a 4/4 bar
            note_start_time = bar_start_time + (e * eighth_len)
            note_end_time = note_start_time + (eighth_len * 0.85) # 85% length for separation/drive
            
            # Bass
            b_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bas, note_start_time)
            b_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bas, note_end_time)
            # Add slight velocity humanization/accent on downbeats
            b_vel = velocity_base if e % 2 == 0 else int(velocity_base * 0.85)
            RPR.RPR_MIDI_InsertNote(take_bas, False, False, b_start_ppq, b_end_ppq, 0, bass_pitch, b_vel, False)

            # Guitar
            g_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_gtr, note_start_time)
            g_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_gtr, note_end_time)
            g_vel = int(velocity_base * 0.9) if e % 2 == 0 else int(velocity_base * 0.75)
            for pitch in chord_pitches_gtr:
                RPR.RPR_MIDI_InsertNote(take_gtr, False, False, g_start_ppq, g_end_ppq, 0, pitch, g_vel, False)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_org)
    RPR.RPR_MIDI_Sort(take_bas)
    RPR.RPR_MIDI_Sort(take_gtr)

    return f"Created multi-track '{track_name}' (Organ, Bass, Guitar) covering {bars} bars at {bpm} BPM in {key} {scale}."
