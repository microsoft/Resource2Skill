def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "3D_Space",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 3D Frequency Positioning arrangement (Bass, Chords, Lead) in distinct octaves.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
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

    # Set Project BPM
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Establish Root (C1 octave base ~ 32.7 Hz)
    # If the user passes 'D#' or 'E', this naturally hits the sub-bass "Sweet Spot" 
    root_midi = 24 + NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # 1-4-6-5 progression based on scale degrees (0-indexed)
    progression = [0, 3, 5, 4] 
    
    beats_per_bar = 4
    bar_sec = (60.0 / bpm) * beats_per_bar
    beat_sec = 60.0 / bpm

    def get_note(degree: int, octave_offset: int = 0) -> int:
        """Calculates exact MIDI pitch wrapped to scale and requested octave."""
        deg = degree % len(scale_intervals)
        octs = (degree // len(scale_intervals)) + octave_offset
        return root_midi + (octs * 12) + scale_intervals[deg]

    def insert_midi_note(take, start_sec: float, end_sec: float, pitch: int, vel: int):
        """Converts seconds to PPQ and inserts the MIDI note securely."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # ==========================================
    # 1. SUB-BASS (Height: Low | Width: Center | Depth: Forward)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    sub_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(sub_track, "P_NAME", f"{track_name}_SubBass", True)
    RPR.RPR_SetMediaTrackInfo_Value(sub_track, "D_VOL", 0.6) # Loud / Forward
    RPR.RPR_SetMediaTrackInfo_Value(sub_track, "D_PAN", 0.0) # Center
    
    sub_item = RPR.RPR_AddMediaItemToTrack(sub_track)
    RPR.RPR_SetMediaItemInfo_Value(sub_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(sub_item, "D_LENGTH", bar_sec * bars)
    sub_take = RPR.RPR_AddTakeToMediaItem(sub_item)
    RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)

    for i in range(bars):
        deg = progression[i % len(progression)]
        note = get_note(deg, octave_offset=0) # Octave 1
        insert_midi_note(sub_take, i * bar_sec, (i * bar_sec) + bar_sec, note, velocity_base)
    RPR.RPR_MIDI_Sort(sub_take)

    # ==========================================
    # 2. CHORDS (Height: Mid | Width: Left | Depth: Back)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name}_Chords", True)
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "D_VOL", 0.25) # Quiet / Pushed back
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "D_PAN", -0.4) # Wide Left
    
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", bar_sec * bars)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)

    for i in range(bars):
        deg = progression[i % len(progression)]
        # Triad built dynamically (Root, 3rd, 5th) in Octave 3 (+2 from bass)
        r = get_note(deg, octave_offset=2)
        t = get_note(deg + 2, octave_offset=2)
        f = get_note(deg + 4, octave_offset=2)
        
        # 3-3-2 Syncopation Rhythm
        insert_midi_note(chord_take, i*bar_sec, i*bar_sec + beat_sec*1.5 - 0.05, r, velocity_base - 10)
        insert_midi_note(chord_take, i*bar_sec, i*bar_sec + beat_sec*1.5 - 0.05, t, velocity_base - 10)
        insert_midi_note(chord_take, i*bar_sec, i*bar_sec + beat_sec*1.5 - 0.05, f, velocity_base - 10)
        
        insert_midi_note(chord_take, i*bar_sec + beat_sec*1.5, i*bar_sec + beat_sec*3.0 - 0.05, r, velocity_base - 15)
        insert_midi_note(chord_take, i*bar_sec + beat_sec*1.5, i*bar_sec + beat_sec*3.0 - 0.05, t, velocity_base - 15)
        insert_midi_note(chord_take, i*bar_sec + beat_sec*1.5, i*bar_sec + beat_sec*3.0 - 0.05, f, velocity_base - 15)
        
        insert_midi_note(chord_take, i*bar_sec + beat_sec*3.0, i*bar_sec + beat_sec*4.0 - 0.05, r, velocity_base - 20)
        insert_midi_note(chord_take, i*bar_sec + beat_sec*3.0, i*bar_sec + beat_sec*4.0 - 0.05, t, velocity_base - 20)
        insert_midi_note(chord_take, i*bar_sec + beat_sec*3.0, i*bar_sec + beat_sec*4.0 - 0.05, f, velocity_base - 20)
    RPR.RPR_MIDI_Sort(chord_take)

    # ==========================================
    # 3. LEAD (Height: High | Width: Right | Depth: Mid)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    lead_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", f"{track_name}_Lead", True)
    RPR.RPR_SetMediaTrackInfo_Value(lead_track, "D_VOL", 0.4) # Medium volume
    RPR.RPR_SetMediaTrackInfo_Value(lead_track, "D_PAN", 0.4) # Wide Right
    
    lead_item = RPR.RPR_AddMediaItemToTrack(lead_track)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_LENGTH", bar_sec * bars)
    lead_take = RPR.RPR_AddTakeToMediaItem(lead_item)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)

    for i in range(bars):
        deg = progression[i % len(progression)]
        # Sparse lead notes placed in Octave 5 (+4 from bass)
        note1 = get_note(deg, octave_offset=4)
        note2 = get_note(deg + 4, octave_offset=4)
        note3 = get_note(deg + 2, octave_offset=5) # Up one more octave
        
        insert_midi_note(lead_take, i*bar_sec, i*bar_sec + beat_sec*0.5, note1, velocity_base)
        insert_midi_note(lead_take, i*bar_sec + beat_sec*1.5, i*bar_sec + beat_sec*2.0, note2, velocity_base - 5)
        insert_midi_note(lead_take, i*bar_sec + beat_sec*3.0, i*bar_sec + beat_sec*3.5, note3, velocity_base)
    RPR.RPR_MIDI_Sort(lead_take)

    return f"Created 3-part 3D arrangement (Sub, Chords, Lead) in {key} {scale} at {bpm} BPM."
