def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Acid_Groove",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Acid Bass and Drum groove approximation in the current REAPER project.
    Approximates the third-party VST setup from the tutorial using stock ReaSynth and MIDI.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # Bass Track
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    bass_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_Bass_Synth", True)

    # Drum Track
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    drum_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums_MIDI", True)

    # === Step 3: Define Patterns ===
    # Bass sequence: (start_beat, end_beat, scale_degree, octave_shift)
    bass_seq = [
        (0.0, 0.25, 0, 0),
        (0.25, 0.5, 0, 1),  # Octave jump
        (0.75, 1.0, 2, 0),
        (1.0, 1.25, 0, 0),
        (1.5, 1.75, 3, 0),
        (2.0, 2.25, 0, 0),
        (2.5, 2.75, 4, 0),
        (3.0, 3.25, 6, 0),
        (3.5, 3.75, 0, 1),  # Octave jump
        (3.75, 4.0, 2, 0),
    ]

    # Drum sequence: (start_beat, end_beat, midi_pitch)
    drum_seq = [
        # Kick
        (0.0, 0.25, 36), (1.0, 1.25, 36), (2.0, 2.25, 36), (3.0, 3.25, 36),
        # Snare
        (1.0, 1.25, 38), (3.0, 3.25, 38),
        # Hi-Hat
        (0.5, 0.75, 42), (1.5, 1.75, 42), (2.5, 2.75, 42), (3.5, 3.75, 42)
    ]

    # === Step 4: Create MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, 0.0, item_length, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)
    
    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, item_length, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)
    
    def insert_note(take, start_beat, end_beat, pitch, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    bass_root_midi = 36 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    num_notes_in_scale = len(scale_intervals)

    for bar in range(bars):
        beat_offset = bar * beats_per_bar
        
        # Populate Bass
        for start, end, degree, oct_shift in bass_seq:
            octaves = degree // num_notes_in_scale
            idx = degree % num_notes_in_scale
            pitch = bass_root_midi + scale_intervals[idx] + (12 * (octaves + oct_shift))
            insert_note(bass_take, beat_offset + start, beat_offset + end, pitch, velocity_base)
            
        # Populate Drums
        for start, end, pitch in drum_seq:
            insert_note(drum_take, beat_offset + start, beat_offset + end, pitch, velocity_base)
            
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 5: Sound Design (Stock Approximation) ===
    # Set up ReaSynth on Bass track for an "acid" square wave tone
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Param 6 is Square wave mix, Param 9 is Sine wave mix, Param 3 is Decay, Param 4 is Sustain
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 1.0)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 9, 0.0)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.05)
    
    return f"Created Acid Groove approximation: 2 tracks ('{track_name}_Bass_Synth' and '{track_name}_Drums_MIDI') over {bars} bars at {bpm} BPM."
