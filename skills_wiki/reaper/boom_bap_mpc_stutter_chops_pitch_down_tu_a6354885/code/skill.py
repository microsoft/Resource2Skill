def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "MPC_Chops",
    bpm: int = 85,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Boom-Bap MPC Stutter Chop loop with a pitch-shifted turnaround.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chops track.
        bpm: Tempo in BPM (85 is ideal for boom-bap).
        key: Root note (e.g., "C").
        scale: Scale type ("minor" is recommended).
        bars: Number of bars to generate (4 is recommended for the turnaround).
        velocity_base: Base MIDI velocity for the chops (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and elements.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Calculate scale pitches
    root_val = NOTE_MAP.get(key, 0)
    # Start at octave 4 (MIDI note 48 for C3/C4 depending on standard, 60 is middle C)
    root_pitch = root_val + 60 
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_chord_pitches(degree, num_notes=4):
        """Generates a 7th chord based on scale degree."""
        pitches = []
        for i in range(num_notes):
            idx = degree + i * 2
            octave = idx // len(scale_intervals)
            rem = idx % len(scale_intervals)
            pitches.append(root_pitch + octave * 12 + scale_intervals[rem])
        return pitches

    # === Step 2: Create Tracks ===
    track_count = RPR.RPR_CountTracks(0)
    
    # Track 1: Lo-Fi Chops
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    tr_chops = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_chops, "P_NAME", track_name, True)
    
    # Track 2: Boom Bap Drums
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    tr_drums = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_drums, "P_NAME", "Boom Bap Drums (GM)", True)

    # === Step 3: Create Media Items & Takes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    it_chops = RPR.RPR_AddMediaItemToTrack(tr_chops)
    RPR.RPR_SetMediaItemInfo_Value(it_chops, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(it_chops, "D_LENGTH", item_length)
    take_chops = RPR.RPR_AddTakeToMediaItem(it_chops)

    it_drums = RPR.RPR_AddMediaItemToTrack(tr_drums)
    RPR.RPR_SetMediaItemInfo_Value(it_drums, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(it_drums, "D_LENGTH", item_length)
    take_drums = RPR.RPR_AddTakeToMediaItem(it_drums)

    def add_note_by_beat(take, start_beat, length_beats, pitch, vel):
        """Helper to insert MIDI notes using musical beats."""
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 4: Sequence MPC Chops ===
    chord_main = get_chord_pitches(0) # Tonic 7th chord
    chord_turnaround = get_chord_pitches(3) # Subdominant 7th chord

    for b in range(bars):
        bar_start = b * 4
        is_turnaround = (b % 4 == 3) # Every 4th bar is a turnaround

        if not is_turnaround:
            # Main Groove: Syncopated stutter chops (like hitting pads)
            chop_rhythm = [
                (0.0, 1.0),   # Beat 1 (downbeat)
                (1.0, 0.5),   # Beat 2 (8th note)
                (1.5, 0.5),   # Beat 2 "and" (8th note)
                (2.5, 1.0),   # Beat 3 "and" (syncopated stab)
                (3.5, 0.5)    # Beat 4 "and" (lead in)
            ]
            for st, length in chop_rhythm:
                for p in chord_main:
                    # Length is slightly shortened (* 0.9) to emulate sample cutoff
                    add_note_by_beat(take_chops, bar_start + st, length * 0.9, p, velocity_base)
        else:
            # Turnaround: Faster 1/4 note stutters, pitched down an octave (-12)
            turnaround_rhythm = [
                (0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (1.5, 0.5),
                (2.0, 0.5), (2.75, 0.25), (3.0, 0.5), (3.5, 0.5)
            ]
            for st, length in turnaround_rhythm:
                for p in chord_turnaround:
                    add_note_by_beat(take_chops, bar_start + st, length * 0.8, p - 12, velocity_base - 10)

    # === Step 5: Sequence Swung Boom-Bap Drums (GM Map) ===
    swing_amt = 0.08 # Delays off-beats to create bounce

    for b in range(bars):
        bar_start = b * 4
        
        # Kick (MIDI 36)
        add_note_by_beat(take_drums, bar_start + 0.0, 0.25, 36, 110)
        add_note_by_beat(take_drums, bar_start + 1.5 + swing_amt, 0.25, 36, 90)
        add_note_by_beat(take_drums, bar_start + 2.5 + swing_amt, 0.25, 36, 105)
        if b % 2 == 1: # Ghost kick variation every 2nd bar
            add_note_by_beat(take_drums, bar_start + 3.5 + swing_amt, 0.25, 36, 75)
            
        # Snare (MIDI 38)
        add_note_by_beat(take_drums, bar_start + 1.0, 0.25, 38, 115)
        add_note_by_beat(take_drums, bar_start + 3.0, 0.25, 38, 120)
        
        # Hi-Hats (MIDI 42) - 8th notes with alternating velocities
        for i in range(8):
            st = i * 0.5
            is_offbeat = (i % 2 != 0)
            timing = st + swing_amt if is_offbeat else st
            vel = 70 if is_offbeat else 95
            add_note_by_beat(take_drums, bar_start + timing, 0.125, 42, vel)

    RPR.RPR_MIDI_Sort(take_chops)
    RPR.RPR_MIDI_Sort(take_drums)

    # === Step 6: Add Sound Design FX to Chops ===
    # 1. Synthesize an Organ/Vintage Keys tone
    fx_synth = RPR.RPR_TrackFX_AddByName(tr_chops, "ReaSynth", False, 1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_synth, 0, 0.3)  # Volume slightly down
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_synth, 6, 0.8)  # Add Square Wave
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_synth, 7, 0.4)  # Add Saw Wave
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_synth, 2, 0.05) # Soft Attack
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_synth, 5, 0.1)  # Short Release (stutter effect)

    # 2. EQ to emulate vinyl sample tone
    RPR.RPR_TrackFX_AddByName(tr_chops, "ReaEQ", False, 1)
    
    # 3. Compressor to emulate hardware sampler pump
    fx_comp = RPR.RPR_TrackFX_AddByName(tr_chops, "ReaComp", False, 1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_comp, 0, 0.3) # Lower threshold
    RPR.RPR_TrackFX_SetParamNormalized(tr_chops, fx_comp, 1, 0.5) # Higher ratio

    return f"Created '{track_name}' and 'Boom Bap Drums' tracks featuring a {bars}-bar MPC stutter loop with pitch-shifted turnaround at {bpm} BPM in {key} {scale}."
