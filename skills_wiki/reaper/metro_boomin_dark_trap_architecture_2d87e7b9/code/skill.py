def create_pattern(
    project_name: str = "MetroTrap",
    track_name: str = "Dark_Trap",
    bpm: int = 117,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Metro Boomin style Dark Trap Beat in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created tracks prefix.
        bpm: Tempo in BPM (110-120 recommended for half-time).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (minor).
        bars: Number of bars to generate (4 or 8 recommended).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11]
    }
    
    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_note(degree: int, octave: int) -> int:
        """Convert a 1-based scale degree and octave into a MIDI pitch."""
        deg = degree - 1
        oct_shift = deg // len(scale_intervals)
        rem = deg % len(scale_intervals)
        return (octave + oct_shift + 1) * 12 + root_pitch + scale_intervals[rem]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    track_names = [f"{track_name}_Melody", f"{track_name}_808", f"{track_name}_Drums (Map VST here)"]
    tracks = []
    
    for tn in track_names:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        trk = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", tn, True)
        tracks.append(trk)

    track_melody, track_808, track_drums = tracks

    # === Step 3: Create MIDI Items ===
    total_len_sec = RPR.RPR_TimeMap2_QNToTime(0, bars * 4.0)
    
    item_melody = RPR.RPR_CreateNewMIDIItemInProj(track_melody, 0.0, total_len_sec, False)
    take_melody = RPR.RPR_GetActiveTake(item_melody)
    
    item_808 = RPR.RPR_CreateNewMIDIItemInProj(track_808, 0.0, total_len_sec, False)
    take_808 = RPR.RPR_GetActiveTake(item_808)
    
    item_drums = RPR.RPR_CreateNewMIDIItemInProj(track_drums, 0.0, total_len_sec, False)
    take_drums = RPR.RPR_GetActiveTake(item_drums)

    def insert_note(take, start_qn: float, length_qn: float, pitch: int, vel: int = velocity_base):
        """Insert a MIDI note into the given take using absolute Quarter Note timing."""
        start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + length_qn)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Step 4: Sequence the Pattern ===
    progression = [1, 6, 5, 1]  # i - VI - v - i (Dark Trap staple)
    
    for bar in range(bars):
        offset_qn = bar * 4.0
        deg = progression[bar % len(progression)]
        
        # --- Melody/Chords (Track 1) ---
        p0 = get_note(deg, 3) # Bass root
        p1 = get_note(deg, 4) # Triad Root
        p2 = get_note(deg + 2, 4) # Triad Third
        p3 = get_note(deg + 4, 4) # Triad Fifth
        
        insert_note(take_melody, offset_qn, 4.0, p0, 75)
        insert_note(take_melody, offset_qn, 4.0, p1, 80)
        insert_note(take_melody, offset_qn, 4.0, p2, 80)
        insert_note(take_melody, offset_qn, 4.0, p3, 85)

        # --- 808 Bass (Track 2) ---
        bass_pitch = get_note(deg, 2)
        
        if bar == bars - 1:
            # Last bar: standard hits then stutter roll
            insert_note(take_808, offset_qn + 0.0, 1.5, bass_pitch, 110)
            insert_note(take_808, offset_qn + 1.5, 1.0, bass_pitch, 110)
            # 1/16th stutters mimicking the "cut self" / slice action
            insert_note(take_808, offset_qn + 2.5, 0.25, bass_pitch, 115)
            insert_note(take_808, offset_qn + 2.75, 0.25, bass_pitch, 115)
            insert_note(take_808, offset_qn + 3.0, 0.25, bass_pitch, 115)
            insert_note(take_808, offset_qn + 3.25, 0.25, bass_pitch, 115)
            insert_note(take_808, offset_qn + 3.5, 0.5, bass_pitch, 120)
        else:
            # "Obey Note Offs" strict sustain matching kicks
            insert_note(take_808, offset_qn + 0.0, 1.5, bass_pitch, 110)
            insert_note(take_808, offset_qn + 1.5, 1.0, bass_pitch, 110)
            insert_note(take_808, offset_qn + 2.5, 1.5, bass_pitch, 110)

        # --- Drums (Track 3) ---
        # Kick (MIDI 36)
        insert_note(take_drums, offset_qn + 0.0, 0.5, 36, 120)
        insert_note(take_drums, offset_qn + 1.5, 0.5, 36, 115) # Syncopated kick on the 'and' of 2
        insert_note(take_drums, offset_qn + 2.5, 0.5, 36, 115) # Syncopated kick on the 'and' of 3
        
        # Snare (MIDI 38)
        insert_note(take_drums, offset_qn + 2.0, 0.5, 38, 110) # Half-time snare on beat 3
        
        # Hi-Hats 2-step (MIDI 42)
        for i in range(8):
            hat_qn = offset_qn + i * 0.5
            
            # Insert a 1/32nd note hat roll right before the 4th beat on odd bars
            if bar % 2 == 1 and i == 6:
                # Velocity ramp down for smooth roll effect
                insert_note(take_drums, hat_qn, 0.125, 42, 100)
                insert_note(take_drums, hat_qn + 0.125, 0.125, 42, 85)
                insert_note(take_drums, hat_qn + 0.25, 0.125, 42, 75)
                insert_note(take_drums, hat_qn + 0.375, 0.125, 42, 65)
            else:
                # Standard 1/8th note hat
                insert_note(take_drums, hat_qn, 0.25, 42, 95)

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take_melody)
    RPR.RPR_MIDI_Sort(take_808)
    RPR.RPR_MIDI_Sort(take_drums)

    # === Step 5: Basic FX Setup ===
    # Melody FX (Synth + Delay)
    RPR.RPR_TrackFX_AddByName(track_melody, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_melody, "ReaDelay", False, -1)
    
    # 808 FX (Synth)
    RPR.RPR_TrackFX_AddByName(track_808, "ReaSynth", False, -1)

    return f"Created '{track_name}' architecture (Melody, 808, Drums) with {bars} bars at {bpm} BPM in {key} {scale}."
