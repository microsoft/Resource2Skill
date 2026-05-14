def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # Hardcoded internally to 12 to enforce the 3-block structure
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' (A-A-A') chord progression in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type ('major' or 'minor').
        bars: Overridden to 12 internally to demonstrate the 3x4 block rule.
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Music Theory Mapping ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pc = NOTE_MAP.get(key.capitalize(), 0)
    base_octave = 48 # Octave 3 (C3)
    
    # Determine progressions based on scale type
    is_major = ("major" in scale.lower())
    
    if is_major:
        # Base: IV - I - V - vi
        chords_base = [
            (5, [0, 4, 7]),  # IV Maj
            (0, [0, 4, 7]),  # I Maj
            (7, [0, 4, 7]),  # V Maj
            (9, [0, 3, 7])   # vi Min
        ]
        # Variation: IV - I - III(maj) - vi
        chords_var = [
            (5, [0, 4, 7]),  # IV Maj
            (0, [0, 4, 7]),  # I Maj
            (4, [0, 4, 7]),  # III Maj (Chromatic variation)
            (9, [0, 3, 7])   # vi Min
        ]
    else:
        # Base: VI - III - VII - i
        chords_base = [
            (8, [0, 4, 7]),  # VI Maj
            (3, [0, 4, 7]),  # III Maj
            (10, [0, 4, 7]), # VII Maj
            (0, [0, 3, 7])   # i Min
        ]
        # Variation: VI - III - V(maj) - i
        chords_var = [
            (8, [0, 4, 7]),  # VI Maj
            (3, [0, 4, 7]),  # III Maj
            (7, [0, 4, 7]),  # V Maj (Chromatic variation / Harmonic minor)
            (0, [0, 3, 7])   # i Min
        ]

    # Structure: Establish -> Reinforce -> Deviate
    blocks = [chords_base, chords_base, chords_var]

    # === Step 2: Project & Track Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: MIDI Item Creation ===
    qn_per_bar = 4
    total_bars = 12 # 3 blocks * 4 bars
    total_qn = total_bars * qn_per_bar 
    bar_len_sec = (60.0 / bpm) * qn_per_bar
    item_len_sec = total_bars * bar_len_sec

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: MIDI Generation ===
    # Rhythmic syncopation within each 4-beat bar:
    # Hit 1: 1.5 beats long
    # Hit 2: 1.5 beats long
    # Hit 3: 1.0 beats long
    rhythm_hits_qn = [
        (0.0, 1.45), # slight gap for articulation
        (1.5, 2.95),
        (3.0, 3.95)
    ]
    
    note_count = 0
    for block_idx, chord_prog in enumerate(blocks):
        block_start_qn = block_idx * 16 # 4 bars * 4 QN
        
        for chord_idx, (root_offset, intervals) in enumerate(chord_prog):
            bar_start_qn = block_start_qn + (chord_idx * 4)
            
            # Keep chords inside the same octave range (C3-B3 base)
            root_pitch = base_octave + root_pc + root_offset
            if root_pitch > base_octave + 11:
                root_pitch -= 12
                
            # Apply rhythm to the chord
            for hit_start_offset, hit_end_offset in rhythm_hits_qn:
                start_qn = bar_start_qn + hit_start_offset
                end_qn = bar_start_qn + hit_end_offset
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
                
                # Insert notes for the chord
                for interval in intervals:
                    pitch = root_pitch + interval
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
                    note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (FX Chain) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a plucky keyboard sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Square mix = 0 (Pure Saw/Triangle)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.5) # Saw mix = 50%
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4) # Release = 40% (Creates space between rhythmic hits)

    return f"Created '{track_name}' applying the Rule of 3 ({note_count} notes over 12 bars, changing the progression on bar 9) in {key} {scale} at {bpm} BPM."
