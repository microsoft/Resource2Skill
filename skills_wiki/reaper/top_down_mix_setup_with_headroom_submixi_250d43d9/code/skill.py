def create_pattern(
    project_name: str = "MixSetup",
    track_name: str = "Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Top-Down Mix Architecture with a generated musical loop in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the submix bus.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created mix layout.
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

    if scale not in SCALES:
        scale = "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Helper Functions ===
    def insert_track(name, folder_depth=0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", folder_depth)
        return track

    def add_midi_item(track, bars_count):
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars_count)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take

    def insert_note(take, start_qn, end_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 2: Build Track Architecture & Routing ===
    
    # 2a. Parent Submix Track (Headroom control)
    submix_track = insert_track(f"{track_name}_SUBMIX", 1)  # 1 = Start of folder
    # Attenuate by approx -3dB to ensure master bus headroom
    RPR.RPR_SetMediaTrackInfo_Value(submix_track, "D_VOL", 0.707) 
    
    # 2b. Child Tracks
    drums_track = insert_track(f"{track_name}_DRUMS", 0)
    RPR.RPR_TrackFX_AddByName(drums_track, "ReaSamplOmatic5000", False, -1)
    
    bass_track = insert_track(f"{track_name}_BASS", 0)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    keys_track = insert_track(f"{track_name}_KEYS", -1) # -1 = End of folder
    RPR.RPR_TrackFX_AddByName(keys_track, "ReaSynth", False, -1)

    # === Step 3: Apply Corrective Mixing FX ===
    
    # High-pass the keys to clear mud for the bass (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(keys_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(keys_track, eq_idx, 0, 150.0)  # Band 1 Freq: 150Hz
    RPR.RPR_TrackFX_SetParam(keys_track, eq_idx, 1, -24.0)  # Band 1 Gain: -24dB cut
    
    # Compress the keys to tame dynamics (ReaComp)
    comp_idx = RPR.RPR_TrackFX_AddByName(keys_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(keys_track, comp_idx, 0, -12.0) # Threshold: -12dB
    RPR.RPR_TrackFX_SetParam(keys_track, comp_idx, 1, 4.0)   # Ratio: 4:1

    # === Step 4: Populate MIDI to demonstrate the mix ===
    
    _, take_drums = add_midi_item(drums_track, bars)
    _, take_bass = add_midi_item(bass_track, bars)
    _, take_keys = add_midi_item(keys_track, bars)

    root_pitch_bass = 36 + NOTE_MAP.get(key, 0)
    root_pitch_keys = 60 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES[scale]
    scale_len = len(scale_intervals)

    for b in range(bars):
        bar_qn = b * 4
        
        # Drums: Kick on 1, 3. Snare on 2, 4.
        insert_note(take_drums, bar_qn + 0, bar_qn + 0.5, 36, velocity_base)
        insert_note(take_drums, bar_qn + 2, bar_qn + 2.5, 36, velocity_base)
        insert_note(take_drums, bar_qn + 1, bar_qn + 1.5, 38, velocity_base)
        insert_note(take_drums, bar_qn + 3, bar_qn + 3.5, 38, velocity_base)

        # Harmony Degree (alternate between root and an upper degree)
        degree = 0 if b % 2 == 0 else min(3, scale_len - 1)
        
        # Bass: Driving 8th notes
        bass_p = root_pitch_bass + scale_intervals[degree]
        for i in range(8):
            insert_note(take_bass, bar_qn + (i * 0.5), bar_qn + (i * 0.5) + 0.4, bass_p, velocity_base - 10)
            
        # Keys: Sustained Triad
        p1 = root_pitch_keys + scale_intervals[degree]
        p2 = root_pitch_keys + scale_intervals[(degree + 2) % scale_len]
        if (degree + 2) >= scale_len: p2 += 12
        p3 = root_pitch_keys + scale_intervals[(degree + 4) % scale_len]
        if (degree + 4) >= scale_len: p3 += 12
        
        insert_note(take_keys, bar_qn, bar_qn + 4.0, p1, velocity_base - 20)
        insert_note(take_keys, bar_qn, bar_qn + 4.0, p2, velocity_base - 20)
        insert_note(take_keys, bar_qn, bar_qn + 4.0, p3, velocity_base - 20)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_keys)

    return f"Created Top-Down Mix folder '{track_name}_SUBMIX' with High-Pass/Comp EQ on '{track_name}_KEYS' at {bpm} BPM."
