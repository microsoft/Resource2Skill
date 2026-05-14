def create_pattern(
    project_name: str = "LoFi_Downcode",
    track_name: str = "Drunken Lo-Fi Bus",
    bpm: int = 82,
    bars: int = 4,
    swing_amount: float = 0.04,  # Amount of swing on off-beat hats (in beats)
    snare_drag: float = 0.03,    # Amount to delay the snare (in beats) to make it "lazy"
    **kwargs,
) -> str:
    """
    Creates a 'Drunken' Lo-Fi drum groove featuring micro-timed (off-grid) MIDI notes
    and a heavy vintage tape processing bus using stock REAPER plugins.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Calculate timing
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    q_note = 1.0 # 1 beat
    e_note = 0.5 # 1/2 beat
    s_note = 0.25 # 1/4 beat

    # === Step 2: Create Track Architecture (Bus + 3 Children) ===
    start_idx = RPR.RPR_CountTracks(0)
    
    # Insert 4 tracks
    for i in range(4):
        RPR.RPR_InsertTrackAtIndex(start_idx + i, True)
        
    bus_track = RPR.RPR_GetTrack(0, start_idx)
    kick_track = RPR.RPR_GetTrack(0, start_idx + 1)
    snare_track = RPR.RPR_GetTrack(0, start_idx + 2)
    hat_track = RPR.RPR_GetTrack(0, start_idx + 3)
    
    # Name tracks
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Kick (Swap with RS5K)", True)
    RPR.RPR_GetSetMediaTrackInfo_String(snare_track, "P_NAME", "Snare (Swap with RS5K)", True)
    RPR.RPR_GetSetMediaTrackInfo_String(hat_track, "P_NAME", "Hats (Swap with RS5K)", True)
    
    # Setup Folder Routing (Bus is parent, Hat is last child)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1)  # Start folder
    RPR.RPR_SetMediaTrackInfo_Value(hat_track, "I_FOLDERDEPTH", -1) # End folder

    # === Step 3: Add Lo-Fi Tape Processing to Bus ===
    # 1. Saturation (Grit)
    sat_idx = RPR.RPR_TrackFX_AddByName(bus_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(bus_track, sat_idx, 0, 50.0) # Amount
    
    # 2. ReaEQ (Bandpass filter mimicking the tutorial's 'Origin' plugin)
    eq_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    # Band 1: High Pass at 62Hz (removes sub rumble)
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 0, 62.0)  # Freq
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 2, 1.0)   # Type: High Pass (approx mapping depending on version, 1 usually HP)
    # Band 4: Low Pass at 7500Hz (removes modern air)
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 9, 7500.0) # Freq for band 4
    
    # 3. ReaGate (Choppy drum tails as requested in tutorial)
    gate_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaGate", False, -1)
    RPR.RPR_TrackFX_SetParam(bus_track, gate_idx, 0, -35.0) # Threshold dB
    RPR.RPR_TrackFX_SetParam(bus_track, gate_idx, 3, 20.0)  # Attack ms
    RPR.RPR_TrackFX_SetParam(bus_track, gate_idx, 5, 80.0)  # Release ms (fast for choppy feel)

    # === Step 4: Add Synthesized Placeholders (so it makes sound immediately) ===
    for trk in [kick_track, snare_track, hat_track]:
        RPR.RPR_TrackFX_AddByName(trk, "ReaSynth", False, -1)
    # Tweak Kick
    RPR.RPR_TrackFX_SetParam(kick_track, 0, 1, 0.05) # fast decay
    # Tweak Snare/Hat (make them noisy)
    RPR.RPR_TrackFX_SetParam(snare_track, 0, 1, 0.1) # short
    RPR.RPR_TrackFX_SetParam(snare_track, 0, 3, 0.8) # Mix in noise
    RPR.RPR_TrackFX_SetParam(hat_track, 0, 1, 0.05)  # very short
    RPR.RPR_TrackFX_SetParam(hat_track, 0, 3, 1.0)   # 100% noise
    RPR.RPR_TrackFX_SetParam(hat_track, 0, 6, 8000.0)# Highpass the noise
    
    # === Step 5: Program the "Drunken" MIDI Rhythms ===
    def add_midi_item_and_notes(track, pattern_func):
        item = RPR.RPR_AddMediaItemToTrack(track)
        item_len_sec = RPR.RPR_TimeMap2_beatsToTime(0, total_beats, 0)[0]
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for bar in range(bars):
            bar_start_beat = bar * beats_per_bar
            pattern_func(take, bar_start_beat)

    def kick_pattern(take, offset):
        # Kick on 1 and 2.5 (standard boom bap)
        notes = [
            (0.0, 110), 
            (2.5, 90)
        ]
        for start, vel in notes:
            start_time = RPR.RPR_TimeMap2_beatsToTime(0, offset + start, 0)[0]
            end_time = RPR.RPR_TimeMap2_beatsToTime(0, offset + start + 0.2, 0)[0]
            RPR.RPR_MIDI_InsertNote(take, False, False, start_time, end_time, 0, 36, vel, False)

    def snare_pattern(take, offset):
        # Snare on 2 and 4, heavily delayed by 'snare_drag'
        notes = [
            (1.0 + snare_drag, 105), # Beat 2 (0-indexed -> 1.0)
            (3.0 + snare_drag, 115)  # Beat 4 (0-indexed -> 3.0)
        ]
        for start, vel in notes:
            start_time = RPR.RPR_TimeMap2_beatsToTime(0, offset + start, 0)[0]
            end_time = RPR.RPR_TimeMap2_beatsToTime(0, offset + start + 0.2, 0)[0]
            RPR.RPR_MIDI_InsertNote(take, False, False, start_time, end_time, 0, 38, vel, False)

    def hat_pattern(take, offset):
        # 8th note hats with swing on the off-beats
        for i in range(8):
            beat_pos = i * e_note
            is_offbeat = i % 2 != 0
            
            # Apply swing to offbeats
            actual_pos = beat_pos + (swing_amount if is_offbeat else 0.0)
            
            # Accent the downbeats, softer on offbeats
            vel = 65 if is_offbeat else 95
            
            start_time = RPR.RPR_TimeMap2_beatsToTime(0, offset + actual_pos, 0)[0]
            end_time = RPR.RPR_TimeMap2_beatsToTime(0, offset + actual_pos + 0.1, 0)[0]
            RPR.RPR_MIDI_InsertNote(take, False, False, start_time, end_time, 0, 42, vel, False)

    # Inject the patterns into the tracks
    add_midi_item_and_notes(kick_track, kick_pattern)
    add_midi_item_and_notes(snare_track, snare_pattern)
    add_midi_item_and_notes(hat_track, hat_pattern)
    
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' folder with Kick, Snare, and Hats over {bars} bars at {bpm} BPM. Applied drunken micro-timing (Snare drag: {snare_drag}, Hat swing: {swing_amount}) and Lo-Fi Tape Bus FX."
