def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Arrangement",
    bpm: int = 140,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Track Driving Rock Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Helper Functions ===
    def rpr_color(r, g, b):
        return RPR.RPR_ColorToNative(r, g, b) | 0x1000000

    def insert_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        
    def create_track(name, color_int, pan=0.0):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetTrackColor(track, color_int)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)
        return track
        
    def create_midi_item(track, start_time, length):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take
        
    def get_diatonic_triad(scale_ints, root_degree):
        notes = []
        for offset in [0, 2, 4]:
            idx = root_degree + offset
            octave = idx // 7
            note = scale_ints[idx % 7] + (12 * octave)
            notes.append(note)
        return notes

    # === Structural Timing Math ===
    qn_duration = 60.0 / bpm
    bar_duration = qn_duration * 4
    item_length = bar_duration * bars
    eighth_dur = qn_duration / 2
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Standard rock progression: i, VI, VII, v (0, 5, 6, 4)
    progression = [0, 5, 6, 4]
    prefix = f"{track_name} - "

    # --- TRACK 1: DRUMS ---
    drum_track = create_track(f"{prefix}Drums", rpr_color(75, 0, 130))
    drum_take = create_midi_item(drum_track, 0.0, item_length)
    
    for bar in range(bars):
        bar_start = bar * bar_duration
        for eighth in range(8):
            t_start = bar_start + eighth * eighth_dur
            t_end = t_start + eighth_dur * 0.9 
            
            # 8th note Hi-Hats
            vel_hh = velocity_base if eighth % 2 == 0 else velocity_base - 20
            insert_note(drum_take, t_start, t_end, 42, vel_hh)
            
            # Backbeat Snare
            if eighth in [2, 6]:
                insert_note(drum_take, t_start, t_end, 38, velocity_base + 10)
                
            # Syncopated Kick
            if eighth in [0, 3, 5]:
                insert_note(drum_take, t_start, t_end, 36, velocity_base + 15)
                
    RPR.RPR_MIDI_Sort(drum_take)

    # --- TRACK 2: BASS ---
    bass_track = create_track(f"{prefix}Bass", rpr_color(128, 0, 128))
    bass_take = create_midi_item(bass_track, 0.0, item_length)
    bass_base_midi = 24 + root_val  # Deep low octave
    
    for bar in range(bars):
        bar_start = bar * bar_duration
        degree = progression[bar % len(progression)]
        root_offset = scale_intervals[degree % 7] + 12 * (degree // 7)
        bass_pitch = bass_base_midi + root_offset
        
        for eighth in range(8):
            t_start = bar_start + eighth * eighth_dur
            t_end = t_start + eighth_dur * 0.8  # Staccato driving feel
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 10
            insert_note(bass_take, t_start, t_end, bass_pitch, vel)
            
    RPR.RPR_MIDI_Sort(bass_take)
    fx_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 6, 1.0) # Square wave
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 5, 0.1) # Fast release

    # --- TRACK 3: RHYTHM GUITAR ---
    rgtr_track = create_track(f"{prefix}Rhythm Gtr", rpr_color(255, 165, 0), pan=-0.7)
    rgtr_take = create_midi_item(rgtr_track, 0.0, item_length)
    rgtr_base_midi = 48 + root_val  # Mid-low octave
    
    for bar in range(bars):
        bar_start = bar * bar_duration
        t_end = bar_start + bar_duration * 0.95
        degree = progression[bar % len(progression)]
        triad_offsets = get_diatonic_triad(scale_intervals, degree)
        
        for offset in triad_offsets:
            pitch = rgtr_base_midi + offset
            insert_note(rgtr_take, bar_start, t_end, pitch, velocity_base)
            
    RPR.RPR_MIDI_Sort(rgtr_take)
    fx_idx = RPR.RPR_TrackFX_AddByName(rgtr_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(rgtr_track, fx_idx, 7, 1.0) # Sawtooth wave
    RPR.RPR_TrackFX_SetParam(rgtr_track, fx_idx, 2, 0.05) # Slower attack for chords

    # --- TRACK 4: LEAD GUITAR ---
    lgtr_track = create_track(f"{prefix}Lead Gtr", rpr_color(0, 200, 255), pan=0.7)
    lgtr_take = create_midi_item(lgtr_track, 0.0, item_length)
    lgtr_base_midi = 60 + root_val  # Upper mid octave
    
    for bar in range(bars):
        bar_start = bar * bar_duration
        degree = progression[bar % len(progression)]
        triad_offsets = get_diatonic_triad(scale_intervals, degree)
        
        # Arpeggio motion: Root, 3rd, 5th, 3rd, Root, 3rd, 5th, 3rd
        arp_pattern = [0, 1, 2, 1, 0, 1, 2, 1]
        
        for eighth in range(8):
            t_start = bar_start + eighth * eighth_dur
            t_end = t_start + eighth_dur * 0.9
            
            note_idx = arp_pattern[eighth]
            pitch = lgtr_base_midi + triad_offsets[note_idx]
            
            vel = velocity_base + (5 if eighth % 4 == 0 else 0)
            insert_note(lgtr_take, t_start, t_end, pitch, vel)
            
    RPR.RPR_MIDI_Sort(lgtr_take)
    fx_idx = RPR.RPR_TrackFX_AddByName(lgtr_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(lgtr_track, fx_idx, 8, 1.0) # Triangle wave
    RPR.RPR_TrackFX_SetParam(lgtr_track, fx_idx, 6, 0.3) # Subtle square mix

    return f"Created multi-track arrangement '{track_name}' (4 tracks) over {bars} bars at {bpm} BPM in {key} {scale}."
