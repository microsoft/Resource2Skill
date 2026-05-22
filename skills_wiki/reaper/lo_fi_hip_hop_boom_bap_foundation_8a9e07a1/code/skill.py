def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "LoFi_Beat",
    bpm: int = 90,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Lo-Fi Hip Hop Boom Bap Foundation (Chords, Bass, Drums) in the current REAPER project.
    """
    import reaper_python as RPR
    import random

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Normalize inputs
    key_val = NOTE_MAP.get(key.upper(), 0) # Default to C if not found
    current_scale = SCALES.get(scale.lower(), SCALES["minor"])
    
    # LoFi progressions based on scale type
    if scale.lower() in ["minor", "dorian", "blues", "pentatonic_minor"]:
        progression = [0, 5, 3, 4] # i, VI, iv, v
    else:
        progression = [1, 4, 5, 3] # ii, V, vi, IV

    # Helper: Calculate pitch based on scale degree
    def get_pitch(root_note_val, scale_arr, degree, octave):
        octaves_up = degree // len(scale_arr)
        idx = degree % len(scale_arr)
        # Base octave 0 is MIDI 12. Octave 4 is MIDI 60 (Middle C).
        return root_note_val + (octave * 12) + (octaves_up * 12) + scale_arr[idx]

    # Helper: Insert MIDI note
    def insert_note(take, start_qn, end_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        # clamp velocity
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Helper: Create Track and MIDI Item
    def create_track_and_take(name, vol_linear):
        RPR.RPR_SetCurrentBPM(0, bpm, False)
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol_linear)
        
        item_length_sec = (60.0 / bpm) * 4 * bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === TRACK 1: LOFI CHORDS ===
    chord_track, chord_take = create_track_and_take(f"{track_name}_Chords", 0.5) # Quieter volume (-6dB approx)
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaEQ", False, -1) # Prep for filtering
    
    for bar in range(bars):
        b_qn = bar * 4.0
        root_degree = progression[bar % len(progression)]
        chord_degrees = [0, 2, 4, 6, 8] # Stack Root, 3rd, 5th, 7th, 9th
        
        for j, deg_offset in enumerate(chord_degrees):
            pitch = get_pitch(key_val, current_scale, root_degree + deg_offset, 4) # Octave 4
            delay_qn = j * 0.03 # 30ms strum effect translated roughly to QN fraction
            vel = int(velocity_base * (0.85 - j * 0.1)) # Higher notes get progressively softer
            insert_note(chord_take, b_qn + delay_qn, b_qn + 3.9, pitch, vel)
    RPR.RPR_MIDI_Sort(chord_take)

    # === TRACK 2: LOFI BASS ===
    bass_track, bass_take = create_track_and_take(f"{track_name}_Bass", 0.8) # -2dB
    
    for bar in range(bars):
        b_qn = bar * 4.0
        root_degree = progression[bar % len(progression)]
        pitch = get_pitch(key_val, current_scale, root_degree, 2) # Octave 2 (Sub range)
        
        # Bass follows the Kick pattern closely
        insert_note(bass_take, b_qn + 0.0, b_qn + 1.0, pitch, velocity_base)
        insert_note(bass_take, b_qn + 2.5, b_qn + 3.5, pitch, velocity_base)
        if bar % 2 == 1:
            insert_note(bass_take, b_qn + 1.5, b_qn + 2.0, pitch, velocity_base - 15)
    RPR.RPR_MIDI_Sort(bass_take)

    # === TRACK 3: BOOM BAP DRUMS ===
    drum_track, drum_take = create_track_and_take(f"{track_name}_Drums", 1.0) # 0dB
    
    kick_pitch = 36
    snare_pitch = 38
    hat_pitch = 42
    
    lazy_snare_qn = 0.04  # Delays snare to create a relaxed pocket
    swing_qn = 0.08       # MPC-style 16th note swing amount

    for bar in range(bars):
        b_qn = bar * 4.0
        
        # Kick Pattern
        insert_note(drum_take, b_qn + 0.0, b_qn + 0.5, kick_pitch, random.randint(velocity_base-10, velocity_base+10))
        insert_note(drum_take, b_qn + 2.5, b_qn + 3.0, kick_pitch, random.randint(velocity_base-20, velocity_base))
        if bar % 2 == 1: # Turnaround extra kick
            insert_note(drum_take, b_qn + 1.5, b_qn + 2.0, kick_pitch, random.randint(velocity_base-30, velocity_base-10)) 
        
        # Snare Pattern (Lazy)
        insert_note(drum_take, b_qn + 1.0 + lazy_snare_qn, b_qn + 1.5 + lazy_snare_qn, snare_pitch, random.randint(velocity_base-5, velocity_base+15))
        insert_note(drum_take, b_qn + 3.0 + lazy_snare_qn, b_qn + 3.5 + lazy_snare_qn, snare_pitch, random.randint(velocity_base-5, velocity_base+15))
        
        # Hi-Hat Pattern (Swung 8ths)
        for hat_i in range(8):
            pos_qn = b_qn + (hat_i * 0.5)
            # Apply swing to the offbeats (the "and"s)
            if hat_i % 2 != 0:
                pos_qn += swing_qn
            
            # Accent downbeats
            vel = random.randint(velocity_base-20, velocity_base) if hat_i % 2 == 0 else random.randint(velocity_base-50, velocity_base-30)
            insert_note(drum_take, pos_qn, pos_qn + 0.25, hat_pitch, vel)
            
    RPR.RPR_MIDI_Sort(drum_take)

    return f"Created Lo-Fi Boom Bap Foundation: 3 tracks (Chords, Bass, Drums) over {bars} bars at {bpm} BPM in {key} {scale}."
