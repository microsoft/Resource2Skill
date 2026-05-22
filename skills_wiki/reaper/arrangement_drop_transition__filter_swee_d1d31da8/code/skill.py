def create_pattern(
    project_name: str = "Arrangement Transition",
    track_name: str = "Beat Structure",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Arrangement Drop Transition (Filter Sweep & Riser) in REAPER.
    Generates a sparse verse, a 1-bar tension build with filter sweep and riser, 
    and drops into a full chorus.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_val = NOTE_MAP.get(key, 9)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Helper to get MIDI pitch for a scale degree (0-indexed)
    def get_pitch(degree, octave):
        octave_shift = degree // 7
        interval = scale_intervals[degree % 7]
        return root_val + interval + ((octave + octave_shift) * 12)

    # === Step 1: Set Tempo & Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_sec = (60.0 / bpm) * beats_per_bar

    def add_note(take, start_time, end_time, pitch, vel, chan=0):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)

    # === Step 2: Track 1 - Chords & Filter Sweep ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", "Chords (Filter Target)", True)
    
    # Add Synth & EQ
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track_chords, "ReaEQ", False, -1)
    
    # Create MIDI Item for Chords
    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bar_sec * 8)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    # Progression: i - VI - III - VII
    progression = [0, 5, 2, 6] 
    
    for b in range(8):
        chord_degree = progression[b % 4]
        start_t = b * bar_sec
        end_t = start_t + bar_sec
        # Add triad
        add_note(take_chords, start_t, end_t, get_pitch(chord_degree, 4), velocity_base - 10)
        add_note(take_chords, start_t, end_t, get_pitch(chord_degree + 2, 4), velocity_base - 15)
        add_note(take_chords, start_t, end_t, get_pitch(chord_degree + 4, 4), velocity_base - 15)
    
    RPR.RPR_MIDI_Sort(take_chords)

    # Automate EQ High Shelf (Band 4 Gain - Param 10) for the transition
    env_eq = RPR.RPR_GetFXEnvelope(track_chords, eq_idx, 10, True)
    build_start = 3 * bar_sec
    drop_time = 4 * bar_sec
    
    # Sweep High Shelf Gain down to muffle sound, then snap back at drop
    RPR.RPR_InsertEnvelopePoint(env_eq, build_start, 0.5, 0, 0, False, True) # 0dB (Normal)
    RPR.RPR_InsertEnvelopePoint(env_eq, drop_time - 0.05, 0.1, 2, 0, False, True) # ~ -18dB (Muffled, curve 2)
    RPR.RPR_InsertEnvelopePoint(env_eq, drop_time, 0.5, 0, 0, False, True) # 0dB (Snap to open)
    RPR.RPR_Envelope_SortPoints(env_eq)


    # === Step 3: Track 2 - The Riser Transition ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_riser = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_riser, "P_NAME", "Tension Riser", True)
    
    synth_idx = RPR.RPR_TrackFX_AddByName(track_riser, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_riser, "ReaVerbate", False, -1) # Add massive space
    
    item_riser = RPR.RPR_AddMediaItemToTrack(track_riser)
    RPR.RPR_SetMediaItemInfo_Value(item_riser, "D_POSITION", build_start)
    RPR.RPR_SetMediaItemInfo_Value(item_riser, "D_LENGTH", bar_sec)
    take_riser = RPR.RPR_AddTakeToMediaItem(item_riser)
    
    # 1 Bar sustained note for the riser
    add_note(take_riser, build_start, drop_time, root_val + 48, velocity_base)
    RPR.RPR_MIDI_Sort(take_riser)
    
    # Fade in volume using item properties for a smooth swell
    RPR.RPR_SetMediaItemInfo_Value(item_riser, "D_FADEINLEN", bar_sec)
    RPR.RPR_SetMediaItemInfo_Value(item_riser, "C_FADEINSHAPE", 1) # Square-like sweep

    # Automate Pitch/Tuning (Param 1) to create siren rise effect
    env_tune = RPR.RPR_GetFXEnvelope(track_riser, synth_idx, 1, True)
    RPR.RPR_InsertEnvelopePoint(env_tune, build_start, 0.5, 0, 0, False, True) # Normal pitch
    RPR.RPR_InsertEnvelopePoint(env_tune, drop_time, 1.0, 2, 0, False, True) # +2 Octaves pitch
    RPR.RPR_Envelope_SortPoints(env_tune)


    # === Step 4: Track 3 - Dynamic Drums (GM MIDI) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    track_drums = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", "Drums (Arranged)", True)
    
    item_drums = RPR.RPR_AddMediaItemToTrack(track_drums)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_LENGTH", bar_sec * 8)
    take_drums = RPR.RPR_AddTakeToMediaItem(item_drums)

    kick = 36
    snare = 38
    hat = 42
    drum_ch = 9 # MIDI Channel 10
    beat_sec = bar_sec / 4

    # Verse (Bars 1-3): Sparse
    for b in range(3):
        t = b * bar_sec
        add_note(take_drums, t, t + 0.1, kick, velocity_base, drum_ch)
        add_note(take_drums, t + beat_sec*2, t + beat_sec*2 + 0.1, snare, velocity_base-10, drum_ch)

    # Build-up (Bar 4): Drum roll
    t_build = 3 * bar_sec
    for beat in range(4):
        # 4-to-the-floor kicks building tension
        add_note(take_drums, t_build + (beat * beat_sec), t_build + (beat * beat_sec) + 0.1, kick, velocity_base + (beat*5), drum_ch)
    # Snare fill at the end of the bar
    for sixteenth in range(4):
        t_fill = t_build + (3 * beat_sec) + (sixteenth * (beat_sec / 4))
        add_note(take_drums, t_fill, t_fill + 0.05, snare, velocity_base + (sixteenth*5), drum_ch)

    # Chorus / Drop (Bars 5-8): Full Energy
    for b in range(4, 8):
        t = b * bar_sec
        add_note(take_drums, t, t + 0.1, kick, velocity_base + 10, drum_ch)
        add_note(take_drums, t + beat_sec*1.5, t + beat_sec*1.5 + 0.1, kick, velocity_base + 5, drum_ch)
        add_note(take_drums, t + beat_sec*2, t + beat_sec*2 + 0.1, snare, velocity_base + 10, drum_ch)
        
        # Consistent 8th note hi-hats
        for h in range(8):
            t_hat = t + (h * (beat_sec / 2))
            add_note(take_drums, t_hat, t_hat + 0.05, hat, velocity_base - (10 if h%2==1 else 0), drum_ch)

    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created Filter Sweep Transition & Drop spanning {bars} bars at {bpm} BPM. Riser peaks at Bar 4, drops at Bar 5."
