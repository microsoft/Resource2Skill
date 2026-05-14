def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "GrooveBass",
    bpm: int = 115,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Dual-Articulation Groove Bass in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks (Folder + 2 Articulations) ===
    folder_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(folder_idx, True)
    folder = RPR.RPR_GetTrack(0, folder_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(folder, "P_NAME", track_name, True)

    mellow_idx = folder_idx + 1
    RPR.RPR_InsertTrackAtIndex(mellow_idx, True)
    track_mellow = RPR.RPR_GetTrack(0, mellow_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_mellow, "P_NAME", f"{track_name}_Mellow", True)

    slap_idx = folder_idx + 2
    RPR.RPR_InsertTrackAtIndex(slap_idx, True)
    track_slap = RPR.RPR_GetTrack(0, slap_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_slap, "P_NAME", f"{track_name}_Slap", True)

    # Set up folder routing structure (1 = start folder, 0 = normal, -1 = end folder)
    RPR.RPR_SetMediaTrackInfo_Value(folder, "I_FOLDERDEPTH", 1)
    RPR.RPR_SetMediaTrackInfo_Value(track_mellow, "I_FOLDERDEPTH", 0)
    RPR.RPR_SetMediaTrackInfo_Value(track_slap, "I_FOLDERDEPTH", -1)

    # === Step 3: Add Instruments & Sound Design ===
    # Mellow Bass (Subby, fundamental heavy, no high frequencies)
    RPR.RPR_TrackFX_AddByName(track_mellow, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 0, 0.7)   # Volume
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 2, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 3, 0.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 4, 1.0)   # Triangle mix (dominant)
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 5, 0.02)  # Attack
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 6, 0.5)   # Decay
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 7, 0.8)   # Sustain
    RPR.RPR_TrackFX_SetParam(track_mellow, 0, 8, 0.1)   # Release

    # Slap Bass (Bright, punchy, immediate decay)
    RPR.RPR_TrackFX_AddByName(track_slap, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 0, 0.6)    # Volume
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 2, 0.4)    # Square mix
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 3, 0.6)    # Saw mix (dominant)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 4, 0.0)    # Triangle mix
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 5, 0.0)    # Attack (instant)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 6, 0.1)    # Decay (snappy)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 7, 0.1)    # Sustain (low)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 8, 0.05)   # Release

    # === Step 4: Create MIDI Items ===
    item_length_sec = RPR.RPR_TimeMap2_QNToTime(0, bars * 4.0)
    
    item_mellow = RPR.RPR_AddMediaItemToTrack(track_mellow)
    RPR.RPR_SetMediaItemInfo_Value(item_mellow, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_mellow, "D_LENGTH", item_length_sec)
    take_mellow = RPR.RPR_AddTakeToMediaItem(item_mellow)
    
    item_slap = RPR.RPR_AddMediaItemToTrack(track_slap)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_LENGTH", item_length_sec)
    take_slap = RPR.RPR_AddTakeToMediaItem(item_slap)

    # === Step 5: Pitch Calculation & Note Generation ===
    def get_pitch(degree, b_note, s_intervals):
        octave_offset = degree // len(s_intervals)
        scale_idx = degree % len(s_intervals)
        return b_note + (octave_offset * 12) + s_intervals[scale_idx]

    # Base note around E1 (MIDI 28) for solid sub bass
    base_note = NOTE_MAP.get(key, 4) + 24 
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)
    vel_mult = velocity_base / 100.0

    notes_created = 0

    for bar in range(bars):
        bar_qn = bar * 4.0
        
        # --- Mellow rhythm (beat_pos, degree, length, vel) ---
        mellow_seq = [
            (0.0, 0, 0.75, 95),   # Downbeat 1
            (1.5, 0, 0.5, 90),    # "And" of beat 2
            (2.5, 0, 0.5, 95),    # "And" of beat 3
            (3.5, -2, 0.25, 85),  # Diatonic step down
            (3.75, -1, 0.25, 90)  # Diatonic step leading back to root
        ]
        
        for b_pos, deg, length, vel in mellow_seq:
            # Subtle humanization for sustained notes (+/- 1% of a beat)
            h_offset = random.uniform(-0.01, 0.01)
            start_qn = bar_qn + b_pos + h_offset
            end_qn = start_qn + length
            
            pitch = get_pitch(deg, base_note, scale_intervals)
            final_vel = max(1, min(127, int(vel * vel_mult)))
            
            start_sec = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_sec = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mellow, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mellow, end_sec)
            
            RPR.RPR_MIDI_InsertNote(take_mellow, False, False, start_ppq, end_ppq, 0, pitch, final_vel, True)
            notes_created += 1

        # --- Slap rhythm (beat_pos, octaves_up, length, vel) ---
        slap_seq = [
            (0.75, 1, 0.15, 120),  # 16th before beat 2
            (2.25, 1, 0.15, 120),  # "e" of beat 3
            (3.25, 1, 0.15, 120)   # "e" of beat 4
        ]
        
        for b_pos, octs_up, length, vel in slap_seq:
            # Push slaps slightly late in the pocket for groove (+0.5% to +2.5% of a beat)
            h_offset = random.uniform(0.005, 0.025)
            start_qn = bar_qn + b_pos + h_offset
            end_qn = start_qn + length
            
            pitch = get_pitch(octs_up * scale_len, base_note, scale_intervals)
            final_vel = max(1, min(127, int(vel * vel_mult)))
            
            start_sec = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_sec = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_slap, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_slap, end_sec)
            
            RPR.RPR_MIDI_InsertNote(take_slap, False, False, start_ppq, end_ppq, 0, pitch, final_vel, True)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take_mellow)
    RPR.RPR_MIDI_Sort(take_slap)

    return f"Created dual-articulation bass folder '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM."
