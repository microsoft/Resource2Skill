def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Electro_Triad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Electronic Triad Setup (Drums, Bass, Pad) in the current REAPER project.
    Simulates the Massive X + Reason Rack + Reaktor workflow using native plugins.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "F#").
        scale: Scale type ("minor", "major", etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the creation.
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

    # Helper functions for harmonic computation
    def get_note_by_degree(base_str, scale_str, degree, octave):
        base_note = NOTE_MAP.get(base_str.capitalize(), 0)
        scale_intervals = SCALES.get(scale_str, SCALES["minor"])
        idx = degree % len(scale_intervals)
        octave_shift = degree // len(scale_intervals)
        # +1 because standard MIDI C4 is note 60 (0 + 5 * 12)
        return base_note + scale_intervals[idx] + (octave + octave_shift + 1) * 12

    def get_chord(base_str, scale_str, degree, octave=4):
        return [get_note_by_degree(base_str, scale_str, degree + i, octave) for i in [0, 2, 4]]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_length = bar_len * bars
    
    # Progressions: i - VI - III - VII
    progression = [0, 5, 2, 6] 

    def get_ppq(take, time_sec):
        return RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)

    # ==========================================
    # 1. DRUM TRACK (Offbeat Pattern Simulation)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)
    
    # Add 3 RS5K instances as placeholders for Kick, Snare, Hat
    for _ in range(3):
        RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
        
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    for b in range(bars):
        bar_start = b * bar_len
        for beat in range(4):
            beat_start = bar_start + (beat * beat_len)
            
            # Kick (C2 - 36) on every downbeat
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    get_ppq(drum_take, beat_start), get_ppq(drum_take, beat_start + 0.1), 
                                    0, 36, velocity_base, False)
            
            # Snare (D2 - 38) on beats 2 and 4
            if beat % 2 == 1:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                        get_ppq(drum_take, beat_start), get_ppq(drum_take, beat_start + 0.1), 
                                        0, 38, velocity_base, False)
                
            # Hi-Hat (F#2 - 42) on the offbeats
            hat_start = beat_start + (beat_len * 0.5)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    get_ppq(drum_take, hat_start), get_ppq(drum_take, hat_start + 0.1), 
                                    0, 42, int(velocity_base * 0.8), False)
    RPR.RPR_MIDI_Sort(drum_take)

    # ==========================================
    # 2. BASS TRACK (Reaktor Synth Simulation)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)
    
    # Configure ReaSynth as a Bass (Saw wave, tuned down)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 1.0) # Saw shape mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.2) # Short release
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    for b in range(bars):
        degree = progression[b % len(progression)]
        bass_note = get_note_by_degree(key, scale, degree, 2) # Octave 2
        bar_start = b * bar_len
        
        # 8th note rhythm
        for i in range(8):
            start_time = bar_start + i * (beat_len * 0.5)
            end_time = start_time + (beat_len * 0.4) # Slightly staccato
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, 
                                    get_ppq(bass_take, start_time), get_ppq(bass_take, end_time), 
                                    0, bass_note, velocity_base, False)
    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # 3. PAD TRACK (Massive X Simulation)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    pad_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", f"{track_name} Pad", True)
    
    # Configure ReaSynth as a Pad (Slow attack, long release)
    RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 5, 0.4) # Attack
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 6, 0.7) # Release
    
    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", total_length)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)
    
    for b in range(bars):
        degree = progression[b % len(progression)]
        chord_notes = get_chord(key, scale, degree, 4) # Octave 4
        
        start_time = b * bar_len
        end_time = start_time + bar_len
        
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(pad_take, False, False, 
                                    get_ppq(pad_take, start_time), get_ppq(pad_take, end_time), 
                                    0, note, int(velocity_base * 0.7), False)
    RPR.RPR_MIDI_Sort(pad_take)

    return f"Created Electronic Triad scaffold (Drums, Bass, Pad) in {key} {scale} over {bars} bars at {bpm} BPM."
