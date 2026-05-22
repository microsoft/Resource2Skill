def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Offbeat",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an offbeat electronic groove featuring a chorused synth stab
    and a 16th-note rolling bassline, mimicking the generative sequences
    from the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_pc = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Octave placement
    stab_base_pitch = 60 + root_pc # C4 range
    bass_pitch = 36 + root_pc      # C2 range
    
    # I-Chord definition
    chord_pitches = [
        stab_base_pitch + scale_intervals[0], 
        stab_base_pitch + scale_intervals[2], 
        stab_base_pitch + scale_intervals[4]
    ]

    # === Timing Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def insert_midi_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Track 1: Offbeat Chorused Stabs ===
    track_idx_1 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_1, True)
    track1 = RPR.RPR_GetTrack(0, track_idx_1)
    RPR.RPR_GetSetMediaTrackInfo_String(track1, "P_NAME", f"{track_name}_Stabs", True)
    
    # Stab FX
    RPR.RPR_TrackFX_AddByName(track1, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track1, "JS: Chorus", False, -1)

    item1 = RPR.RPR_AddMediaItemToTrack(track1)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", total_length_sec)
    take1 = RPR.RPR_AddTakeToMediaItem(item1)

    # === Track 2: 16th Note Rolling Bass ===
    track_idx_2 = track_idx_1 + 1
    RPR.RPR_InsertTrackAtIndex(track_idx_2, True)
    track2 = RPR.RPR_GetTrack(0, track_idx_2)
    RPR.RPR_GetSetMediaTrackInfo_String(track2, "P_NAME", f"{track_name}_Bass", True)

    # Bass FX (Plucky ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track2, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track2, synth_idx, 2, 0.8) # Square mix

    item2 = RPR.RPR_AddMediaItemToTrack(track2)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", total_length_sec)
    take2 = RPR.RPR_AddTakeToMediaItem(item2)

    # === Generate MIDI Pattern ===
    note_count = 0
    for bar in range(bars):
        for beat in range(beats_per_bar):
            base_time = (bar * bar_length_sec) + (beat * beat_length_sec)
            
            # 1. Stabs: Trigger exactly halfway through the beat (the 8th note offbeat)
            stab_start = base_time + (beat_length_sec * 0.5)
            stab_end = stab_start + (beat_length_sec * 0.25) # 16th note duration
            for pitch in chord_pitches:
                insert_midi_note(take1, stab_start, stab_end, pitch, velocity_base)
                note_count += 1
                
            # 2. Bass: Rolling 16ths pattern (rest on downbeat, play e, &, a)
            # Rhythmic subdivisions: 0.25 (e), 0.5 (&), 0.75 (a)
            bass_rhythm = [
                (0.25, int(velocity_base * 0.8)), # Ghost note
                (0.50, int(velocity_base * 1.0)), # Accent matching the stab
                (0.75, int(velocity_base * 0.8))  # Ghost note
            ]
            
            for frac, vel in bass_rhythm:
                b_start = base_time + (beat_length_sec * frac)
                b_end = b_start + (beat_length_sec * 0.2) # slightly staccato
                insert_midi_note(take2, b_start, b_end, bass_pitch, vel)
                note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take1)
    RPR.RPR_MIDI_Sort(take2)

    return f"Created '{track_name}' groove: 2 tracks, {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
