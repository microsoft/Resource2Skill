def create_pattern(
    project_name: str = "MixEQ",
    track_name: str = "InstrumentEQ",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Kick, Snare, and Lead track with fundamental instrument-specific EQ curves.
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

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.upper(), 0)
    
    def get_pitch(octave, degree):
        octave_shift = degree // len(scale_intervals)
        rem_degree = degree % len(scale_intervals)
        # C4 = 60
        return 12 + (octave + octave_shift) * 12 + root_val + scale_intervals[rem_degree]

    def insert_midi_item(track, start_time, length, notes):
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, start_time + length, False)
        take = RPR.RPR_GetActiveTake(item)
        
        for note in notes:
            start_beat, end_beat, pitch, vel = note
            n_start_time = start_time + (start_beat * (60.0 / bpm))
            n_end_time = start_time + (end_beat * (60.0 / bpm))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        
        RPR.RPR_MIDI_Sort(take)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    # === 1. KICK TRACK ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", f"{track_name}_Kick", True)

    synth_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    # Set to fast decay sine for kick thud
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 3, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 4, 0.0) # Sustain
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 6, 0.0) # Square 
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 7, 0.0) # Saw

    eq_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 0, 120.0) # Band 1 Freq
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 1, 3.5)   # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 3, 400.0) # Band 2 Freq
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 4, -5.0)  # Band 2 Gain
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 6, 3000.0)# Band 3 Freq
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 7, 5.0)   # Band 3 Gain

    # === 2. SNARE TRACK ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    snare_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(snare_track, "P_NAME", f"{track_name}_Snare", True)

    synth_idx = RPR.RPR_TrackFX_AddByName(snare_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 3, 0.05) # Very fast Decay
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 4, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 6, 0.5)  # Square
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 7, 0.5)  # Saw

    eq_idx = RPR.RPR_TrackFX_AddByName(snare_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 0, 150.0) # Band 1 Freq
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 1, 6.0)   # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 6, 3000.0)# Band 3 Freq
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 7, 5.0)   # Band 3 Gain
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 9, 7000.0)# Band 4 Freq
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 10, 4.0)  # Band 4 Gain

    # === 3. LEAD / VOCAL TRACK ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    lead_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", f"{track_name}_Lead", True)

    synth_idx = RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, synth_idx, 7, 1.0) # Saw wave for richness
    
    eq_idx = RPR.RPR_TrackFX_AddByName(lead_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 0, 100.0)  # Band 1 Freq (HPF sim)
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 1, -12.0)  # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 3, 350.0)  # Band 2 Freq
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 4, -3.0)   # Band 2 Gain
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 6, 3000.0) # Band 3 Freq
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 7, 3.0)    # Band 3 Gain
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 9, 5000.0) # Band 4 Freq
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 10, 4.0)   # Band 4 Gain

    # === GENERATE MIDI ARANGEMENT ===
    kick_notes = []
    snare_notes = []
    lead_notes = []
    
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        # Kick: 4-on-the-floor
        kick_notes.extend([
            (bar_offset + 0, bar_offset + 0.5, 36, velocity_base),
            (bar_offset + 1, bar_offset + 1.5, 36, velocity_base),
            (bar_offset + 2, bar_offset + 2.5, 36, velocity_base),
            (bar_offset + 3, bar_offset + 3.5, 36, velocity_base),
        ])
        # Snare: Beats 2 and 4 (indices 1 and 3)
        snare_notes.extend([
            (bar_offset + 1, bar_offset + 1.25, 48, velocity_base),
            (bar_offset + 3, bar_offset + 3.25, 48, velocity_base),
        ])
        # Lead: Syncopated melody
        lead_notes.extend([
            (bar_offset + 0.0, bar_offset + 0.5, get_pitch(4, 0), velocity_base),
            (bar_offset + 0.5, bar_offset + 1.0, get_pitch(4, 2), velocity_base),
            (bar_offset + 1.5, bar_offset + 2.0, get_pitch(4, 4), velocity_base),
            (bar_offset + 2.5, bar_offset + 3.0, get_pitch(4, 2), velocity_base),
            (bar_offset + 3.0, bar_offset + 3.5, get_pitch(4, 1), velocity_base),
        ])

    insert_midi_item(kick_track, 0.0, total_length, kick_notes)
    insert_midi_item(snare_track, 0.0, total_length, snare_notes)
    insert_midi_item(lead_track, 0.0, total_length, lead_notes)

    return f"Created 3 Tracks (Kick, Snare, Lead) demonstrating Fundamental Mix EQ over {bars} bars at {bpm} BPM in {key} {scale}."
