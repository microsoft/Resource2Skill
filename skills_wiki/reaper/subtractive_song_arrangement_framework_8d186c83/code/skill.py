def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement", # Base name, will be expanded
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16, # Total bars (4 blocks of 4)
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Subtractive Song Arrangement (Intro -> Verse -> Build -> Chorus)
    by generating a full loop and selectively muting items across a 16-bar timeline.
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

    # Normalize key and scale
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Define pitches
    midi_kick = 36
    midi_snare = 38
    midi_hat = 42
    midi_bass = 36 + root_val # C2 octave
    midi_pad = [
        48 + root_val + scale_intervals[0], # Root (C3 octave)
        48 + root_val + scale_intervals[2 % len(scale_intervals)], # Third
        48 + root_val + scale_intervals[4 % len(scale_intervals)]  # Fifth
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    qn_len = 60.0 / bpm

    # === Step 2: Track Creation Setup ===
    def create_instrument_track(name, index):
        RPR.RPR_InsertTrackAtIndex(index, True)
        track = RPR.RPR_GetTrack(0, index)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        return track

    start_idx = RPR.RPR_CountTracks(0)
    track_pad = create_instrument_track(f"{track_name}_Pad", start_idx)
    track_bass = create_instrument_track(f"{track_name}_Bass", start_idx + 1)
    track_kick = create_instrument_track(f"{track_name}_Kick", start_idx + 2)
    track_snare = create_instrument_track(f"{track_name}_Snare", start_idx + 3)
    track_hat = create_instrument_track(f"{track_name}_Hat", start_idx + 4)

    # Helper function to add MIDI notes robustly
    def add_midi_note(take, item, start_qn_rel, end_qn_rel, pitch, vel):
        item_start = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")
        proj_start_time = item_start + (start_qn_rel * qn_len)
        proj_end_time = item_start + (end_qn_rel * qn_len)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 3: Subtractive Arrangement Matrix ===
    # We build 4 blocks of 4 bars. True = Unmuted, False = Muted.
    # Block 0: Intro, Block 1: Verse, Block 2: Build, Block 3: Chorus
    arrangement_matrix = {
        "Pad":   [True,  False, True,  True], 
        "Bass":  [False, True,  False, True],
        "Kick":  [True,  True,  True,  True],
        "Snare": [False, True,  True,  True],
        "Hat":   [False, False, True,  True]
    }

    block_bars = 4
    block_qn = block_bars * 4
    block_sec = block_qn * qn_len

    # === Step 4: Generate Climax & Apply Mutes ===
    for block_idx in range(4):
        start_time = block_idx * block_sec
        end_time = start_time + block_sec
        
        # --- Pad Item ---
        item_pad = RPR.RPR_CreateNewMIDIItemInProj(track_pad, start_time, end_time, False)
        take_pad = RPR.RPR_GetActiveTake(item_pad)
        for note in midi_pad:
            add_midi_note(take_pad, item_pad, 0, block_qn, note, velocity_base - 30)
        RPR.RPR_MIDI_Sort(take_pad)
        if not arrangement_matrix["Pad"][block_idx]:
            RPR.RPR_SetMediaItemInfo_Value(item_pad, "B_MUTE", 1.0)

        # --- Bass Item ---
        item_bass = RPR.RPR_CreateNewMIDIItemInProj(track_bass, start_time, end_time, False)
        take_bass = RPR.RPR_GetActiveTake(item_bass)
        for q in range(int(block_qn * 2)): # 8th notes
            add_midi_note(take_bass, item_bass, q * 0.5, (q * 0.5) + 0.3, midi_bass, velocity_base - 10)
        RPR.RPR_MIDI_Sort(take_bass)
        if not arrangement_matrix["Bass"][block_idx]:
            RPR.RPR_SetMediaItemInfo_Value(item_bass, "B_MUTE", 1.0)

        # --- Kick Item ---
        item_kick = RPR.RPR_CreateNewMIDIItemInProj(track_kick, start_time, end_time, False)
        take_kick = RPR.RPR_GetActiveTake(item_kick)
        for q in range(int(block_qn)): # 4-on-the-floor
            add_midi_note(take_kick, item_kick, q, q + 0.25, midi_kick, velocity_base)
        RPR.RPR_MIDI_Sort(take_kick)
        if not arrangement_matrix["Kick"][block_idx]:
            RPR.RPR_SetMediaItemInfo_Value(item_kick, "B_MUTE", 1.0)

        # --- Snare Item ---
        item_snare = RPR.RPR_CreateNewMIDIItemInProj(track_snare, start_time, end_time, False)
        take_snare = RPR.RPR_GetActiveTake(item_snare)
        for q in range(int(block_qn)): 
            if q % 2 != 0: # Beats 2 and 4
                add_midi_note(take_snare, item_snare, q, q + 0.25, midi_snare, velocity_base)
        RPR.RPR_MIDI_Sort(take_snare)
        if not arrangement_matrix["Snare"][block_idx]:
            RPR.RPR_SetMediaItemInfo_Value(item_snare, "B_MUTE", 1.0)

        # --- Hat Item ---
        item_hat = RPR.RPR_CreateNewMIDIItemInProj(track_hat, start_time, end_time, False)
        take_hat = RPR.RPR_GetActiveTake(item_hat)
        for q in range(int(block_qn * 2)): # 8th notes
            vel = velocity_base if q % 2 == 0 else velocity_base - 20 # Accent downbeats
            add_midi_note(take_hat, item_hat, q * 0.5, (q * 0.5) + 0.125, midi_hat, vel)
        RPR.RPR_MIDI_Sort(take_hat)
        if not arrangement_matrix["Hat"][block_idx]:
            RPR.RPR_SetMediaItemInfo_Value(item_hat, "B_MUTE", 1.0)

    RPR.RPR_UpdateArrange()

    return f"Created 16-bar subtractive arrangement matrix (Intro, Verse, Build, Chorus) at {bpm} BPM in {key} {scale} using 5 tracks."
