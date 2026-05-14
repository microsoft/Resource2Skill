def create_pattern(
    project_name: str = "DillaBeat",
    track_name: str = "Neo-Soul Beat",
    bpm: int = 82,
    key: str = "Eb",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul / Boom-Bap Sample Flip groove in the current REAPER project.
    
    Generates a muffled, jazzy 9th chord progression to simulate a sample loop, 
    and overlays a heavily swung boom-bap drum and percussion groove.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # === Step 1: Set Tempo & Calculate Theory ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    quarter_len = 60.0 / bpm
    item_length = quarter_len * 4 * bars
    
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_pitch = 48 + NOTE_MAP.get(key, 3) # Default around C3/Eb3

    def get_scale_degree_pitch(degree, root, intervals):
        octave = degree // len(intervals)
        idx = degree % len(intervals)
        return root + (octave * 12) + intervals[idx]

    def make_voicing(degrees):
        # Drop the first note (root) down an octave for bass coverage
        bass = get_scale_degree_pitch(degrees[0], root_pitch - 12, scale_intervals)
        upper = [get_scale_degree_pitch(d, root_pitch, scale_intervals) for d in degrees[1:]]
        return [bass] + upper

    # Diatonic I (9th) and IV (9th) chords
    chords = [
        make_voicing([0, 2, 4, 6, 8]), 
        make_voicing([3, 5, 7, 9, 11])
    ]

    # Swing Algorithm (MPC style ~58-60% swing)
    def get_swung_time(pos_q, q_len, swing_ratio=0.58):
        beat_num = int(pos_q)
        fraction = pos_q - beat_num
        if fraction == 0.5: # 8th note offbeat
            fraction = swing_ratio
        elif fraction == 0.25: # 16th note offbeat 1
            fraction = swing_ratio / 2.0
        elif fraction == 0.75: # 16th note offbeat 2
            fraction = swing_ratio + (1.0 - swing_ratio) / 2.0
        return (beat_num + fraction) * q_len

    def add_midi_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    start_track_idx = RPR.RPR_CountTracks(0)

    # === Step 2: Track 1 - Sample Loop (Rhodes/Electric Piano Vibe) ===
    RPR.RPR_InsertTrackAtIndex(start_track_idx, True)
    sample_track = RPR.RPR_GetTrack(0, start_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(sample_track, "P_NAME", f"{track_name} - Sample Loop", True)
    
    # Configure ReaSynth to output a warm, muffled Triangle wave
    RPR.RPR_TrackFX_AddByName(sample_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 0, 0.3)   # Volume
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 2, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 3, 0.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 4, 1.0)   # Triangle mix (warm, muffled tone)
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 5, 0.0)   # Sine mix
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 6, 0.05)  # Attack
    RPR.RPR_TrackFX_SetParam(sample_track, 0, 9, 0.4)   # Release

    sample_item = RPR.RPR_CreateNewMIDIItemInProj(sample_track, 0.0, item_length, False)
    sample_take = RPR.RPR_GetActiveTake(sample_item)

    for b in range(bars):
        bar_offset = b * 4.0
        start_time = bar_offset * quarter_len
        end_time = start_time + (4.0 * quarter_len) - 0.05
        
        # Change chord every 2 bars for a slow, sweeping loop feel
        chord = chords[(b // 2) % 2] 
        for pitch in chord:
            add_midi_note(sample_take, start_time, end_time, pitch, velocity_base - 20)
    RPR.RPR_MIDI_Sort(sample_take)

    # === Step 3: Track 2 - Boom Bap Drums ===
    RPR.RPR_InsertTrackAtIndex(start_track_idx + 1, True)
    drum_track = RPR.RPR_GetTrack(0, start_track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Drums", True)
    
    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, item_length, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)
    
    kick_pattern = [0.0, 1.5, 2.5]
    snare_pattern = [1.0, 3.0]
    hat_pattern = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    
    for b in range(bars):
        bar_offset = b * 4.0
        for pos in kick_pattern:
            start_time = (bar_offset * quarter_len) + get_swung_time(pos, quarter_len)
            add_midi_note(drum_take, start_time, start_time + 0.1, 36, velocity_base)
            
        for pos in snare_pattern:
            start_time = (bar_offset * quarter_len) + get_swung_time(pos, quarter_len)
            add_midi_note(drum_take, start_time, start_time + 0.1, 38, min(127, velocity_base + 10))
            
        for i, pos in enumerate(hat_pattern):
            start_time = (bar_offset * quarter_len) + get_swung_time(pos, quarter_len)
            vel = velocity_base - 10 if i % 2 == 0 else velocity_base - 30 # Accents on downbeats
            add_midi_note(drum_take, start_time, start_time + 0.05, 42, vel)
    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 4: Track 3 - Syncopated Percussion (Bongos) ===
    RPR.RPR_InsertTrackAtIndex(start_track_idx + 2, True)
    perc_track = RPR.RPR_GetTrack(0, start_track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(perc_track, "P_NAME", f"{track_name} - Percussion", True)
    
    perc_item = RPR.RPR_CreateNewMIDIItemInProj(perc_track, 0.0, item_length, False)
    perc_take = RPR.RPR_GetActiveTake(perc_item)
    
    bongo_high = [0.75, 2.75] # Syncopated 16ths
    bongo_low = [1.25, 3.25]
    
    for b in range(bars):
        bar_offset = b * 4.0
        for pos in bongo_high:
            start_time = (bar_offset * quarter_len) + get_swung_time(pos, quarter_len)
            add_midi_note(perc_take, start_time, start_time + 0.1, 60, velocity_base - 20)
        for pos in bongo_low:
            start_time = (bar_offset * quarter_len) + get_swung_time(pos, quarter_len)
            add_midi_note(perc_take, start_time, start_time + 0.1, 61, velocity_base - 15)
    RPR.RPR_MIDI_Sort(perc_take)

    return f"Created Neo-Soul Beat '{track_name}': 3 tracks (Sample, Drums, Perc) over {bars} bars at {bpm} BPM with Dilla Swing."
