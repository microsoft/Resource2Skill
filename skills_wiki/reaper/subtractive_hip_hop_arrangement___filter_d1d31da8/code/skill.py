def create_pattern(
    project_name: str = "Arrangement",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 28,  # Ignored, strict 28-bar arrangement used
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete 28-bar Subtractive Hip-Hop Arrangement.
    Includes Intro, Chorus, Verse (with kick-drop), and a Filter Sweep Transition.
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
    }

    root_val = NOTE_MAP.get(key.upper(), 0) + 48 # Base Octave C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Initialize Project & Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks and Routing ===
    track_idx = RPR.RPR_CountTracks(0)
    for i in range(4):
        RPR.RPR_InsertTrackAtIndex(track_idx + i, True)

    track_bus = RPR.RPR_GetTrack(0, track_idx)
    track_keys = RPR.RPR_GetTrack(0, track_idx + 1)
    track_bass = RPR.RPR_GetTrack(0, track_idx + 2)
    track_drums = RPR.RPR_GetTrack(0, track_idx + 3)

    RPR.RPR_GetSetMediaTrackInfo_String(track_bus, "P_NAME", f"{project_name} Inst Bus", True)
    RPR.RPR_GetSetMediaTrackInfo_String(track_keys, "P_NAME", f"{project_name} Keys", True)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{project_name} Bass", True)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", f"{project_name} Drums", True)

    # Create Folder structure: Keys and Bass go to Inst Bus. Drums are independent.
    RPR.RPR_SetMediaTrackInfo_Value(track_bus, "I_FOLDERDEPTH", 1)
    RPR.RPR_SetMediaTrackInfo_Value(track_bass, "I_FOLDERDEPTH", -1)
    RPR.RPR_SetMediaTrackInfo_Value(track_drums, "I_FOLDERDEPTH", 0)

    # === Step 3: Add Basic Sound Generators ===
    # Keys Synth (Square wave with envelope)
    fx_keys = RPR.RPR_TrackFX_AddByName(track_keys, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_keys, fx_keys, 2, 0.5) # Square
    RPR.RPR_TrackFX_SetParam(track_keys, fx_keys, 5, 0.05) # Attack
    RPR.RPR_TrackFX_SetParam(track_keys, fx_keys, 6, 0.4) # Decay

    # Bass Synth (Deep Sine wave)
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)

    # === Step 4: MIDI Generation Helpers ===
    def create_midi_item(track, start_bar, num_bars):
        start_sec = (start_bar - 1) * 4.0 * (60.0 / bpm)
        end_sec = (start_bar - 1 + num_bars) * 4.0 * (60.0 / bpm)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_sec, end_sec, False)
        return RPR.RPR_GetActiveTake(item)

    def add_note_abs(take, abs_qn, len_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, abs_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, abs_qn + len_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    def generate_keys(take, start_b, num_b):
        chord_degrees = [0, 5, 2, 6] # i, VI, III, VII progression
        def get_pitch(octave, degree):
            oct_shift = degree // len(scale_intervals)
            rem = degree % len(scale_intervals)
            return root_val + (octave + oct_shift) * 12 + scale_intervals[rem]

        for bar_offset in range(num_b):
            abs_qn = (start_b - 1 + bar_offset) * 4.0
            degree = chord_degrees[bar_offset % 4]
            p1, p2, p3 = get_pitch(0, degree), get_pitch(0, degree + 2), get_pitch(0, degree + 4)
            add_note_abs(take, abs_qn, 4.0, p1, velocity_base - 20)
            add_note_abs(take, abs_qn, 4.0, p2, velocity_base - 20)
            add_note_abs(take, abs_qn, 4.0, p3, velocity_base - 20)
        RPR.RPR_MIDI_Sort(take)

    def generate_bass(take, start_b, num_b):
        chord_degrees = [0, 5, 2, 6]
        def get_pitch(octave, degree):
            oct_shift = degree // len(scale_intervals)
            rem = degree % len(scale_intervals)
            return root_val + (octave + oct_shift) * 12 + scale_intervals[rem]

        for bar_offset in range(num_b):
            abs_qn = (start_b - 1 + bar_offset) * 4.0
            degree = chord_degrees[bar_offset % 4]
            p1 = get_pitch(-1, degree) # Sub octave
            add_note_abs(take, abs_qn + 0.0, 1.5, p1, velocity_base)
            add_note_abs(take, abs_qn + 1.5, 0.5, p1, velocity_base - 10)
            add_note_abs(take, abs_qn + 2.0, 2.0, p1, velocity_base)
        RPR.RPR_MIDI_Sort(take)

    def generate_drums(take, start_b, num_b, drop_kick, delay_hats):
        kick_pitch, snare_pitch, hat_pitch = 36, 38, 42
        for bar_offset in range(num_b):
            abs_qn = (start_b - 1 + bar_offset) * 4.0
            
            # Kicks (Drop first 2 bars of verse to cut energy)
            if not (drop_kick and bar_offset < 2):
                add_note_abs(take, abs_qn + 0.0, 0.25, kick_pitch, velocity_base + 10)
                add_note_abs(take, abs_qn + 2.5, 0.25, kick_pitch, velocity_base)
                
            # Snares (Beat 2 and 4)
            add_note_abs(take, abs_qn + 1.0, 0.25, snare_pitch, velocity_base)
            add_note_abs(take, abs_qn + 3.0, 0.25, snare_pitch, velocity_base)
            
            # Hats (Delay entrance in verse to build anticipation)
            if not (delay_hats and bar_offset < 2):
                for i in range(8):
                    vel = velocity_base - 10 if i % 2 == 0 else velocity_base - 30
                    add_note_abs(take, abs_qn + i * 0.5, 0.25, hat_pitch, vel)
        RPR.RPR_MIDI_Sort(take)

    # === Step 5: Build The Subtractive Arrangement ===
    
    # 1. Intro (Bars 1-4) - Melodies only
    tk_keys = create_midi_item(track_keys, 1, 4)
    generate_keys(tk_keys, 1, 4)
    
    # 2. Chorus 1 (Bars 5-12) - Full Energy
    tk_keys = create_midi_item(track_keys, 5, 8)
    generate_keys(tk_keys, 5, 8)
    tk_bass = create_midi_item(track_bass, 5, 8)
    generate_bass(tk_bass, 5, 8)
    tk_drums = create_midi_item(track_drums, 5, 8)
    generate_drums(tk_drums, 5, 8, drop_kick=False, delay_hats=False)
    
    # 3. Verse 1 (Bars 13-20) - Subtractive Energy (No early kicks, delayed hats)
    tk_keys = create_midi_item(track_keys, 13, 8)
    generate_keys(tk_keys, 13, 8)
    tk_bass = create_midi_item(track_bass, 13, 8)
    generate_bass(tk_bass, 13, 8)
    tk_drums = create_midi_item(track_drums, 13, 8)
    generate_drums(tk_drums, 13, 8, drop_kick=True, delay_hats=True)
    
    # 4. Chorus 2 (Bars 21-28) - Full Energy Drop
    tk_keys = create_midi_item(track_keys, 21, 8)
    generate_keys(tk_keys, 21, 8)
    tk_bass = create_midi_item(track_bass, 21, 8)
    generate_bass(tk_bass, 21, 8)
    tk_drums = create_midi_item(track_drums, 21, 8)
    generate_drums(tk_drums, 21, 8, drop_kick=False, delay_hats=False)

    # === Step 6: Filter Sweep Transition (Bars 19 to 21) ===
    # Add JS Filter to the Instrument Bus (affects Keys and Bass, leaves Drums alone)
    fx_idx = RPR.RPR_TrackFX_AddByName(track_bus, "JS: Filters/resonancedlowpass", False, -1)
    env = RPR.RPR_GetFXEnvelope(track_bus, fx_idx, 0, True) # 0 = Frequency
    
    # Calculate sweep timing in seconds
    t_start = (19 - 1) * 4.0 * (60.0 / bpm)     # Sweep down starts at Bar 19
    t_bottom = (21 - 1) * 4.0 * (60.0 / bpm) - 0.1 # Lowest point 100ms before Chorus
    t_snap = (21 - 1) * 4.0 * (60.0 / bpm)      # Snaps wide open exactly on Bar 21 (Drop)
    
    # Insert envelope points (value 1.0 = open, 0.15 = muffled)
    RPR.RPR_InsertEnvelopePoint(env, 0, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, t_start, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, t_bottom, 0.15, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, t_snap, 1.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created 28-bar Subtractive Arrangement '{project_name}' (Intro, Chorus, Verse, Drop) at {bpm} BPM in {key} {scale}"
