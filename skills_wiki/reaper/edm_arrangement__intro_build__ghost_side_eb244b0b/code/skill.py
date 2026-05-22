def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an 8-bar EDM arrangement demonstrating a sidechain ghost pump
    and a 1-bar pre-drop drum pause.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Total length of the arrangement (default 8).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    def get_note(degree, octave):
        """Returns MIDI note number for a given scale degree and octave."""
        deg_mod = degree % len(scale_intervals)
        oct_shift = degree // len(scale_intervals)
        return root_val + scale_intervals[deg_mod] + (octave + oct_shift) * 12

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    # === Step 2: Create Tracks ===
    num_existing_tracks = RPR.RPR_CountTracks(0)
    
    # Track 1: Chords
    RPR.RPR_InsertTrackAtIndex(num_existing_tracks, True)
    chords_tr = RPR.RPR_GetTrack(0, num_existing_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_tr, "P_NAME", "Synth Chords", True)
    
    # Track 2: Main Drums
    RPR.RPR_InsertTrackAtIndex(num_existing_tracks + 1, True)
    drums_tr = RPR.RPR_GetTrack(0, num_existing_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_tr, "P_NAME", "Main Drums", True)

    # Track 3: Ghost Kick (Sidechain Trigger)
    RPR.RPR_InsertTrackAtIndex(num_existing_tracks + 2, True)
    ghost_tr = RPR.RPR_GetTrack(0, num_existing_tracks + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_tr, "P_NAME", "Ghost Kick (SC Trigger)", True)
    # MUTE master send so we don't hear the ghost kick
    RPR.RPR_SetMediaTrackInfo_Value(ghost_tr, "B_MAINSEND", 0.0)

    # === Step 3: Configure Advanced Sidechain Routing ===
    # Send Ghost Kick to Chords
    send_idx = RPR.RPR_CreateTrackSend(ghost_tr, chords_tr)
    # Set send destination channels to 3/4 (Category 0=Audio, 5=Dest Chan)
    RPR.RPR_SetTrackSendInfo_Value(ghost_tr, 0, send_idx, "I_DSTCHAN", 2) 
    
    # Add ReaComp to Chords
    fx_idx = RPR.RPR_TrackFX_AddByName(chords_tr, "ReaComp", False, -1)
    # Dial in aggressive sidechain settings
    RPR.RPR_TrackFX_SetParam(chords_tr, fx_idx, 0, 0.05) # Threshold (low)
    RPR.RPR_TrackFX_SetParam(chords_tr, fx_idx, 1, 0.8)  # Ratio (high)
    RPR.RPR_TrackFX_SetParam(chords_tr, fx_idx, 2, 0.0)  # Attack (fast)
    RPR.RPR_TrackFX_SetParam(chords_tr, fx_idx, 3, 0.1)  # Release (quick pump)
    # Add a stock synth to generate sound
    RPR.RPR_TrackFX_AddByName(chords_tr, "ReaSynth", False, -1)

    # === Step 4: Generate MIDI (Arrangement Structure) ===

    # A. CHORDS (Plays entire 8 bars)
    chord_item = RPR.RPR_AddMediaItemToTrack(chords_tr)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", bar_len * bars)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    # Standard i - VI - III - VII progression (degrees: 0, 5, 2, 6)
    progression = [0, 5, 2, 6]
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        start_pos = bar * bar_len
        end_pos = start_pos + bar_len
        
        # Build triad
        for offset in [0, 2, 4]:
            note = get_note(degree + offset, 4) # Octave 4
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, 
                                    start_pos * RPR.RPR_ProjectTimeToQN(0, 1) * 960, 
                                    end_pos * RPR.RPR_ProjectTimeToQN(0, 1) * 960, 
                                    0, note, velocity_base, False)

    # B. MAIN DRUMS (Bars 5 to 7. Bar 8 is the DROP OUT)
    drums_item = RPR.RPR_AddMediaItemToTrack(drums_tr)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_POSITION", bar_len * 4) # Start at bar 5
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_LENGTH", bar_len * 3)   # Length 3 bars
    drums_take = RPR.RPR_AddTakeToMediaItem(drums_item)
    
    kick_note = 36 # C2
    # 4 on the floor for 3 bars
    for beat in range(4 * 3):
        pos = (bar_len * 4) + (beat * beat_len)
        ppq_start = pos * RPR.RPR_ProjectTimeToQN(0, 1) * 960
        ppq_end = ppq_start + (beat_len * 0.25 * RPR.RPR_ProjectTimeToQN(0, 1) * 960)
        RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq_start, ppq_end, 0, kick_note, velocity_base, False)

    # C. GHOST KICK (Bars 5 to 8. Continues through the Drop Out!)
    ghost_item = RPR.RPR_AddMediaItemToTrack(ghost_tr)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_POSITION", bar_len * 4) # Start at bar 5
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_LENGTH", bar_len * 4)   # Length 4 bars
    ghost_take = RPR.RPR_AddTakeToMediaItem(ghost_item)

    # 4 on the floor for all 4 bars
    for beat in range(4 * 4):
        pos = (bar_len * 4) + (beat * beat_len)
        ppq_start = pos * RPR.RPR_ProjectTimeToQN(0, 1) * 960
        ppq_end = ppq_start + (beat_len * 0.25 * RPR.RPR_ProjectTimeToQN(0, 1) * 960)
        RPR.RPR_MIDI_InsertNote(ghost_take, False, False, ppq_start, ppq_end, 0, kick_note, velocity_base, False)

    # Force MIDI evaluation
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(drums_take)
    RPR.RPR_MIDI_Sort(ghost_take)
    RPR.RPR_UpdateArrange()

    return f"Created {bars}-bar arrangement: 4-bar intro, 3-bar verse, 1-bar dropout pause. Ghost sidechain routing established."
