def create_pattern(
    project_name: str = "BoomBapProject",
    track_name: str = "Boom Bap",
    bpm: int = 85,
    key: str = "C#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a classic Boom Bap drum groove and locked sub-bass line.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (80-90 recommended for Boom Bap).
        key: Root note (e.g., C#, D, E).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Theory: Root note calculation for Sub Bass (Octave 2)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch_class = NOTE_MAP.get(key, 0)
    sub_bass_midi_note = 36 + root_pitch_class # C2 = 36

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # ==========================================
    # Step 2: Create Drum Track
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # GM Drum Map
    KICK = 36
    SNARE = 38
    HIHAT = 42

    # Groove grid (relative to a single bar in beats)
    # Boom Bap Syncopation: Kick on 1, 2.5, 3.5. Snare on 2, 4.
    kick_positions = [0.0, 1.5, 2.5]
    snare_positions = [1.0, 3.0]
    hihat_positions = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        
        # Insert Kicks
        for pos in kick_positions:
            start_time = (bar_offset_beats + pos) * beat_length_sec
            end_time = start_time + (0.25 * beat_length_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_time)
            vel = min(127, velocity_base + 10)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, KICK, vel, False)

        # Insert Snares
        for pos in snare_positions:
            start_time = (bar_offset_beats + pos) * beat_length_sec
            end_time = start_time + (0.25 * beat_length_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_time)
            vel = min(127, velocity_base + 15)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, SNARE, vel, False)
            
        # Insert Hats (with velocity humanization)
        for i, pos in enumerate(hihat_positions):
            start_time = (bar_offset_beats + pos) * beat_length_sec
            end_time = start_time + (0.125 * beat_length_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_time)
            # Accent the downbeats
            vel = velocity_base if i % 2 == 0 else max(20, velocity_base - 30)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, HIHAT, vel, False)

    RPR.RPR_MIDI_Sort(drum_take)


    # ==========================================
    # Step 3: Create Sub Bass Track
    # ==========================================
    bass_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(bass_track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, bass_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Sub Bass", True)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Bass rhythm completely locked to Kick drums for bottom-end cohesion
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        
        for pos in kick_positions:
            start_time = (bar_offset_beats + pos) * beat_length_sec
            # Short, staccato sub notes (1/8th note duration) to leave space for snares
            end_time = start_time + (0.45 * beat_length_sec) 
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
            vel = velocity_base
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, sub_bass_midi_note, vel, False)

    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # Step 4: Sound Design (ReaSynth + ReaEQ)
    # ==========================================
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # By default, ReaSynth plays a Sine wave. 
    # Tame the volume slightly so it doesn't clip
    RPR.RPR_TrackFX_SetParam(bass_track, synth_idx, 0, 0.5) # Vol
    
    # Add ReaEQ to lowpass the bass to ensure it acts purely as a sub
    eq_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    # Enable Band 4 as Lowpass
    RPR.RPR_TrackFX_SetParam(bass_track, eq_idx, 9, 2)   # Band 4 Type: Lowpass
    RPR.RPR_TrackFX_SetParam(bass_track, eq_idx, 10, 150) # Band 4 Freq: 150 Hz
    RPR.RPR_TrackFX_SetParam(bass_track, eq_idx, 11, -12) # Band 4 Gain: -12dB (steep curve)

    return f"Created Boom Bap groove: Drums & Sub Bass ({bars} bars at {bpm} BPM in {key})."

