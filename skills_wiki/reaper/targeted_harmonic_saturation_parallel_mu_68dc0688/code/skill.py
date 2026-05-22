def create_pattern(
    project_name: str = "Saturation_Demo",
    track_name: str = "Sat_Demo",
    bpm: int = 90,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates parallel saturation buses for Drums (Broadband Crunch) and Leads (500-5k Hz Warmth).
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_pitch = NOTE_MAP.get(key, 4) + 48 # Octave 4

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    start_idx = RPR.RPR_CountTracks(0)
    
    # Track 1: Dry Drums
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    drum_trk = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_trk, "P_NAME", "Dry Drums", True)
    RPR.RPR_TrackFX_AddByName(drum_trk, "ReaSynth", False, -1)
    
    # Track 2: Drum Saturation Bus (Broadband Crunch)
    RPR.RPR_InsertTrackAtIndex(start_idx + 1, True)
    drum_bus = RPR.RPR_GetTrack(0, start_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_bus, "P_NAME", "Drum Saturation Bus", True)
    # Add JS Saturation for overall grit
    dsat_idx = RPR.RPR_TrackFX_AddByName(drum_bus, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_bus, dsat_idx, 0, 75.0) # Drive amount %
    
    # Track 3: Dry Lead / Vocals
    RPR.RPR_InsertTrackAtIndex(start_idx + 2, True)
    lead_trk = RPR.RPR_GetTrack(0, start_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_trk, "P_NAME", "Dry Lead", True)
    RPR.RPR_TrackFX_AddByName(lead_trk, "ReaSynth", False, -1)
    
    # Track 4: Lead Saturation Bus (Multiband 500-5000Hz Warmth)
    RPR.RPR_InsertTrackAtIndex(start_idx + 3, True)
    lead_bus = RPR.RPR_GetTrack(0, start_idx + 3)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_bus, "P_NAME", "Lead Multiband Sat Bus", True)
    
    # Isolate 500 - 5000 Hz using JS 3-Band EQ
    eq_idx = RPR.RPR_TrackFX_AddByName(lead_bus, "JS: 3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_bus, eq_idx, 0, -60.0) # Kill Lows (dB)
    RPR.RPR_TrackFX_SetParam(lead_bus, eq_idx, 1, 0.0)   # Keep Mids (dB)
    RPR.RPR_TrackFX_SetParam(lead_bus, eq_idx, 2, -60.0) # Kill Highs (dB)
    RPR.RPR_TrackFX_SetParam(lead_bus, eq_idx, 3, 500.0) # Low Crossover (Hz)
    RPR.RPR_TrackFX_SetParam(lead_bus, eq_idx, 4, 5000.0)# High Crossover (Hz)
    
    # Add Saturation to the isolated band
    lsat_idx = RPR.RPR_TrackFX_AddByName(lead_bus, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_bus, lsat_idx, 0, 80.0) # Drive amount %
    
    # Setup Parallel Routing (Sends)
    RPR.RPR_CreateTrackSend(drum_trk, drum_bus)
    RPR.RPR_CreateTrackSend(lead_trk, lead_bus)

    # --- Generate Dummy MIDI to demonstrate the effect ---
    
    # 1. Drum MIDI
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_trk)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    # Basic boom-bap pattern (Kick on 1 & 3, Snare on 2 & 4)
    q_len = 960 # 1 quarter note in MIDI ticks
    for b in range(bars):
        bar_offset = b * 4 * q_len
        # Kick (MIDI 36)
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, bar_offset, bar_offset + q_len//2, 0, 36, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, bar_offset + 2*q_len, bar_offset + 2*q_len + q_len//2, 0, 36, velocity_base, False)
        # Snare (MIDI 38)
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, bar_offset + q_len, bar_offset + q_len + q_len//2, 0, 38, velocity_base+10, False)
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, bar_offset + 3*q_len, bar_offset + 3*q_len + q_len//2, 0, 38, velocity_base+10, False)

    # 2. Lead MIDI (Sustained chords to show harmonic richness)
    lead_item = RPR.RPR_AddMediaItemToTrack(lead_trk)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_LENGTH", item_length)
    lead_take = RPR.RPR_AddTakeToMediaItem(lead_item)
    
    # Chord progression: i - VI - III - VII
    progression = [0, 5, 2, 6] # Scale degrees
    for b in range(bars):
        deg = progression[b % len(progression)]
        start_tick = b * 4 * q_len
        end_tick = start_tick + (4 * q_len) - 120 # Sustained for the whole bar
        
        # Build triad
        for offset in [0, 2, 4]:
            idx = (deg + offset) % len(scale_intervals)
            octave_shift = 12 * ((deg + offset) // len(scale_intervals))
            note = root_pitch + scale_intervals[idx] + octave_shift
            RPR.RPR_MIDI_InsertNote(lead_take, False, False, start_tick, end_tick, 0, note, int(velocity_base * 0.8), False)

    RPR.RPR_UpdateArrange()
    
    return f"Created Multiband & Bus Saturation routing over {bars} bars at {bpm} BPM in {key} {scale}."
