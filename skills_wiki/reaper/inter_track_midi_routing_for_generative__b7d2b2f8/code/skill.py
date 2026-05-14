def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative_Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an inter-track MIDI routing setup and generates an algorithmic bassline.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, F#).
        scale: Scale type (e.g., minor, dorian, pentatonic_minor).
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

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 1: Create the Target Synthesizer Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_synth = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_synth, "P_NAME", f"{track_name}_Target_Synth", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_synth, "D_VOL", 0.5) # Attenuate volume to avoid clipping

    # Add a stock synth to act as the bass receiver
    RPR.RPR_TrackFX_AddByName(track_synth, "ReaSynth", False, -1)


    # === Step 2: Create the MIDI Generator Track ===
    track_idx_midi = track_idx + 1
    RPR.RPR_InsertTrackAtIndex(track_idx_midi, True)
    track_midi = RPR.RPR_GetTrack(0, track_idx_midi)
    RPR.RPR_GetSetMediaTrackInfo_String(track_midi, "P_NAME", f"{track_name}_MIDI_Gen", True)


    # === Step 3: Configure Inter-Track MIDI Routing ===
    # Create send from Track 2 (Generator) to Track 1 (Synth)
    send_idx = RPR.RPR_CreateTrackSend(track_midi, track_synth)
    
    # Disable audio routing (-1.0 = None) so only MIDI passes through
    RPR.RPR_SetTrackSendInfo_Value(track_midi, 0, send_idx, "I_SRCCHAN", -1.0) 
    RPR.RPR_SetTrackSendInfo_Value(track_midi, 0, send_idx, "I_DSTCHAN", -1.0)
    
    # Enable MIDI routing (0.0 = All channels to All channels)
    RPR.RPR_SetTrackSendInfo_Value(track_midi, 0, send_idx, "I_MIDIFLAGS", 0.0)


    # === Step 4: Simulate the Output of the Bassline Generator Algorithm ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track_midi)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Groove matrix simulating algorithmic steps: (Scale Degree, Velocity Mod, Length Mod)
    # Degree indices automatically wrap to octaves based on the scale length
    groove_matrix = [
        (0, 1.0, 1.0),      # 1
        (0, 0.7, 0.5),      # e (staccato)
        (None, 0, 0),       # & (rest)
        (7, 1.1, 1.0),      # a (accent, octave jump typically)

        (2, 0.8, 1.0),      # 2
        (None, 0, 0),       # e
        (0, 0.9, 0.5),      # &
        (4, 0.8, 1.0),      # a

        (0, 1.0, 1.0),      # 3
        (0, 0.7, 0.5),      # e
        (2, 1.0, 1.0),      # &
        (None, 0, 0),       # a

        (5, 0.9, 1.0),      # 4
        (None, 0, 0),       # e
        (0, 0.8, 0.5),      # &
        (7, 1.1, 1.0),      # a
    ]

    selected_scale = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(selected_scale)
    base_note = NOTE_MAP.get(key.capitalize(), 0) + 36 # Anchor to MIDI Octave 2 (Bass range)
    sixteenth_len = (60.0 / bpm) * 0.25

    def get_midi_note(degree_idx):
        if degree_idx is None:
            return None
        octave_shift = degree_idx // scale_len
        note_idx = degree_idx % scale_len
        return base_note + (octave_shift * 12) + selected_scale[note_idx]

    # Populate the generator track with the algorithmic pattern
    for bar in range(bars):
        for step, (degree, vel_mod, len_mod) in enumerate(groove_matrix):
            midi_pitch = get_midi_note(degree)
            if midi_pitch is None:
                continue
                
            midi_pitch = max(0, min(127, midi_pitch))
            vel = int(velocity_base * vel_mod)
            vel = max(1, min(127, vel))

            start_time = (bar * bar_length_sec) + (step * sixteenth_len)
            end_time = start_time + (sixteenth_len * len_mod)

            RPR.RPR_MIDI_InsertNote(
                take, False, False,
                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time),
                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time),
                0, midi_pitch, vel, False
            )

    RPR.RPR_MIDI_Sort(take)

    return f"Created Generator/Synth track routing with {bars} bars of algorithmic bassline at {bpm} BPM in {key} {scale}."
