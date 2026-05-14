def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "MPC_Chops",
    bpm: int = 85,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an MPC-Style Micro-Chop sequence with a 4th-bar turnaround.

    Args:
        project_name: Project identifier.
        track_name: Name for the created chop track.
        bpm: Tempo in BPM (85 is ideal for boom-bap).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (should be a multiple of 4).
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the operation.
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

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # Helper: Build Diatonic Triads
    def get_chord(degree, octave=3):
        notes = []
        for i in [0, 2, 4]:  # Root, 3rd, 5th of the chord
            note_deg = degree + i
            scale_len = len(scale_intervals)
            oct_offset = note_deg // scale_len
            scale_deg = note_deg % scale_len
            pitch = root_pitch + (octave + oct_offset + 1) * 12 + scale_intervals[scale_deg]
            notes.append(pitch)
        return notes

    # Helper: Insert Track
    def add_track(name, vol=1.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol)
        return track

    # Helper: Add MIDI Item
    def add_midi_item(track, num_bars, tempo):
        beats_per_bar = 4
        item_length = (60.0 / tempo) * beats_per_bar * num_bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take

    # Helper: Insert Note
    def insert_note(take, pos_qn, length_qn, pitch, vel):
        vel = max(1, min(127, int(vel)))
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, pos_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, pos_qn + length_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    track_chops = add_track(track_name, 0.7)
    item_chops, take_chops = add_midi_item(track_chops, bars, bpm)

    track_drums = add_track(track_name + "_Drums", 0.8)
    item_drums, take_drums = add_midi_item(track_drums, bars, bpm)

    # === Step 3: Sequence Pattern ===
    notes_added = 0
    for b in range(bars):
        bar_start_qn = b * 4.0
        is_turnaround = (b % 4 == 3) # The 4th bar turnaround (A-A-A-B structure)

        # -- CHOPS GENERATION --
        if not is_turnaround:
            # Main repeating motif (simulate 1/4 and 1/8 note chops)
            # Tuple: (Beat Offset QN, Length QN, Scale Degree)
            chop_events = [
                (0.0, 1.0, 0),  # Downbeat Pad hit
                (1.0, 0.5, 3),  # 1/8 chop
                (1.5, 0.5, 0),  # 1/8 chop back to root
                (2.0, 1.0, 4),  # Snare hit Pad
                (3.0, 0.5, 5),  # 1/8 chop
                (3.5, 0.5, 6)   # 1/8 chop turnaround lead-in
            ]
        else:
            # Turnaround Motif (Bar 4)
            chop_events = [
                (0.0, 1.0, 6),
                (1.0, 0.5, 5),
                (1.5, 0.5, 4),
                (2.0, 0.5, 3),
                (2.5, 0.5, 0),
                (3.0, 1.0, 4)
            ]
            
        for beat_ofs, length_qn, degree in chop_events:
            # Octave 3 to mimic the "pitched down 6 semitones" technique
            chord_notes = get_chord(degree, octave=3) 
            pos_qn = bar_start_qn + beat_ofs
            vel = velocity_base - int((beat_ofs % 1.0) * 20) # Accent downbeats
            for pitch in chord_notes:
                # Multiply length by 0.95 to leave a tiny gap between pads
                insert_note(take_chops, pos_qn, length_qn * 0.95, pitch, vel)
                notes_added += 1

        # -- DRUMS GENERATION --
        # Kick (General MIDI: 36)
        kicks = [(0.0, velocity_base), (1.5, velocity_base), (2.5, velocity_base - 20)]
        for beat_ofs, vel in kicks:
            insert_note(take_drums, bar_start_qn + beat_ofs, 0.25, 36, vel)
            
        # Snare (General MIDI: 38)
        snares = [(1.0, velocity_base + 10), (3.0, velocity_base + 10)]
        for beat_ofs, vel in snares:
            insert_note(take_drums, bar_start_qn + beat_ofs, 0.25, 38, vel)
            
        # Technique 5: 1/16th Note Hi-Hats (General MIDI: 42)
        for i in range(16):
            beat_ofs = i * 0.25
            # Accent pattern to create groove: 100, 70, 85, 70
            if i % 4 == 0:
                hat_vel = velocity_base
            elif i % 2 == 0:
                hat_vel = velocity_base - 15
            else:
                hat_vel = velocity_base - 30
            insert_note(take_drums, bar_start_qn + beat_ofs, 0.125, 42, hat_vel)

    RPR.RPR_MIDI_Sort(take_chops)
    RPR.RPR_MIDI_Sort(take_drums)

    # === Step 4: Sound Design (MPC Gating Effect) ===
    # Add a stock synth and set the ADSR envelope to act like an MPC choke group
    RPR.RPR_TrackFX_AddByName(track_chops, "ReaSynth", False, -1)
    # Param 1=Attack, 2=Decay, 3=Sustain, 4=Release
    RPR.RPR_TrackFX_SetParamNormalized(track_chops, 0, 1, 0.0) # Instant Attack
    RPR.RPR_TrackFX_SetParamNormalized(track_chops, 0, 2, 0.3) # Short Decay
    RPR.RPR_TrackFX_SetParamNormalized(track_chops, 0, 3, 0.8) # High Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track_chops, 0, 4, 0.0) # Zero Release (CRUCIAL for chop effect)

    return f"Created MPC-style chopped sequence '{track_name}' and drums with {notes_added} chord notes over {bars} bars at {bpm} BPM."
