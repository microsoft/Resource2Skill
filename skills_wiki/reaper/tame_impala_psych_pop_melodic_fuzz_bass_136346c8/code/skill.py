def create_pattern(
    project_name: str = "PsychPop",
    track_name: str = "Psych Fuzz Bass",
    bpm: int = 100,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Tame Impala-style Melodic Fuzz Bass in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (defaults to 100 per tutorial).
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

    # Base setup
    root_pitch = NOTE_MAP.get(key, 0) + 36  # C2 as anchor
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Calculate key scale degrees for the groove
    pitch_root = root_pitch
    pitch_octave = root_pitch + 12
    pitch_fifth = root_pitch + scale_intervals[min(4, len(scale_intervals)-1)]
    # Use 7th for passing note (index 6 if standard 7-note scale, otherwise fallback to 5th)
    pitch_seventh = root_pitch + scale_intervals[min(6, len(scale_intervals)-1)] if len(scale_intervals) > 6 else pitch_fifth

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function for inserting notes
    def insert_note(start_beat, length_beats, pitch, velocity):
        # Convert beats to time, then time to PPQ
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    # === Step 4: Program the Groove ===
    # 1-bar looping syncopated melodic bass groove
    for bar in range(bars):
        b_offset = bar * 4.0
        
        # Beat 1: Solid downbeat Root
        insert_note(b_offset + 0.0, 0.75, pitch_root, velocity_base)
        
        # Beat 1.75: Funky 16th note syncopated octave leap
        insert_note(b_offset + 0.75, 0.25, pitch_octave, velocity_base - 10)
        
        # Beat 2.5: 8th note Fifth (syncopated)
        insert_note(b_offset + 1.5, 0.5, pitch_fifth, velocity_base - 5)
        
        # Beat 3.0: Back to Root
        insert_note(b_offset + 2.0, 0.5, pitch_root, velocity_base)
        
        # Beat 3.5: Passing 7th note
        insert_note(b_offset + 2.5, 0.5, pitch_seventh, velocity_base - 15)
        
        # Beat 4.0: Resolving Fifth leading into next bar
        insert_note(b_offset + 3.0, 1.0, pitch_fifth, velocity_base - 5)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design & FX Chain ===
    
    # 1. The Core Synth (ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.3) # Volume (keep low before fuzz)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.7) # Mix in Square Wave for body
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5) # Mix in Saw Wave for buzz
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.1) # Slight portamento/glide
    
    # 2. The Guitar Fuzz Pedal Emulation (JS: Distortion)
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 20.0) # Gain (Drive it hard into clipping)
    RPR.RPR_TrackFX_SetParam(track, dist_idx, 1, 1.0)  # Hard clip (Fuzz characteristic)
    
    # 3. Tone Shaping EQ (ReaEQ) - Cut some harsh highs from the fuzz
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 3) # Band 1 Type: High Cut / Low Pass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 4000.0) # Freq cutoff at 4kHz
    
    # 4. Analog Chorus (JS: Chorus) - To replicate the layered width mentioned in tutorial
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 0, 15.0) # Delay length
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 1, 0.8)  # Rate (Slow, psychy wow)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 2, 2.5)  # Depth
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 3, -12.0) # Wet mix (Keep it subtle so low-end stays tight)

    return f"Created '{track_name}' with a melodic Fuzz Bass line over {bars} bars at {bpm} BPM in {key} {scale}."
