def create_pattern(
    project_name: str = "FirstMetalSong",
    bpm: int = 160,
    key: str = "E",
    scale: str = "phrygian",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal Phrygian Chorus (1-6-4-5) with double bass and hard-panned guitars.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM (160 is typical for this half-time feel).
        key: Root note (default 'E').
        scale: Scale type (default 'phrygian').
        bars: Number of bars to generate (default 4).
        velocity_base: Base MIDI velocity (high for metal).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR
    
    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
                
    SCALES = {
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "minor":    [0, 2, 3, 5, 7, 8, 10],
        "major":    [0, 2, 4, 5, 7, 9, 11]
    }
    
    # 1-6-4-5 progression (0-indexed scale degrees: 1st, 6th, 4th, 5th)
    CHORD_DEGREES = [0, 5, 3, 4]
    
    if key not in NOTE_MAP:
        key = "E"
    if scale not in SCALES:
        scale = "phrygian"
        
    root_midi = NOTE_MAP[key]
    intervals = SCALES[scale]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    quarter_len = 60.0 / bpm
    bar_len = quarter_len * 4.0
    total_len = bar_len * bars

    # === Helper: Create Track & MIDI Item ===
    def create_midi_track(name, pan=0.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === Helper: Insert MIDI Note ===
    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        
    # Sort out MIDI sorting state after inserting notes
    def finish_midi(take):
        RPR.RPR_MIDI_Sort(take)

    # === Step 2: Create Drums ===
    track_drums, take_drums = create_midi_track("Drums (MIDI)", pan=0.0)
    # Basic GM Mapping
    KICK = 36
    SNARE = 38
    CRASH = 49
    
    sixteenth_len = quarter_len / 4.0
    
    for bar in range(bars):
        bar_start = bar * bar_len
        # Crash on beat 1
        insert_note(take_drums, bar_start, bar_start + quarter_len, CRASH, velocity_base)
        
        for beat in range(4):
            beat_start = bar_start + (beat * quarter_len)
            
            # Half-time snare on beat 3
            if beat == 2:
                insert_note(take_drums, beat_start, beat_start + sixteenth_len, SNARE, velocity_base + 5)
                
            # 16th note double kicks (continuous)
            for sixteenth in range(4):
                k_start = beat_start + (sixteenth * sixteenth_len)
                # Alternate velocity slightly for humanization
                vel = velocity_base if sixteenth % 2 == 0 else velocity_base - 10
                insert_note(take_drums, k_start, k_start + sixteenth_len * 0.8, KICK, vel)
                
    finish_midi(take_drums)

    # === Step 3: Create Guitars and Bass ===
    # Hard Panning is explicitly required by the tutorial
    track_gtr_l, take_gtr_l = create_midi_track("Rhythm Guitar L", pan=-1.0)
    track_gtr_r, take_gtr_r = create_midi_track("Rhythm Guitar R", pan=1.0)
    track_bass, take_bass = create_midi_track("Bass", pan=0.0)
    
    # Add Placeholder Stock FX
    RPR.RPR_TrackFX_AddByName(track_gtr_l, "JS: Guitar/distortion", False, -1)
    RPR.RPR_TrackFX_AddByName(track_gtr_r, "JS: Guitar/distortion", False, -1)
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    
    eighth_len = quarter_len / 2.0
    
    for bar in range(bars):
        bar_start = bar * bar_len
        # Progression 1-6-4-5 mapping
        degree_idx = CHORD_DEGREES[bar % len(CHORD_DEGREES)]
        interval_offset = intervals[degree_idx]
        
        # Calculate root note for the current chord (bump octaves to keep it mostly in guitar range)
        chord_root = root_midi + interval_offset + 12 
        # Power chord: Root + Perfect 5th (+7 semitones)
        chord_fifth = chord_root + 7
        
        # Bass plays 1 octave below guitar root
        bass_note = chord_root - 12
        
        for eighth in range(8):
            e_start = bar_start + (eighth * eighth_len)
            e_end = e_start + eighth_len * 0.9 # Slight gap for chugging articulation
            
            # Accent downbeats
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 15
            
            # Left Guitar
            insert_note(take_gtr_l, e_start, e_end, chord_root, vel)
            insert_note(take_gtr_l, e_start, e_end, chord_fifth, vel)
            
            # Right Guitar (Same notes, double tracked)
            insert_note(take_gtr_r, e_start, e_end, chord_root, vel)
            insert_note(take_gtr_r, e_start, e_end, chord_fifth, vel)
            
            # Bass
            insert_note(take_bass, e_start, e_end, bass_note, vel)
            
    finish_midi(take_gtr_l)
    finish_midi(take_gtr_r)
    finish_midi(take_bass)

    return f"Created Metal Phrygian Chorus: 4 tracks (Drums, Gtr L, Gtr R, Bass) over {bars} bars in {key} {scale} at {bpm} BPM."
