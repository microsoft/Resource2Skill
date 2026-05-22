def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Jungle Break",
    bpm: int = 170,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Photek-Style Jungle Drum Break in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (160-175 recommended for Jungle).
        key: Root note (unused for drum maps, included for signature).
        scale: Scale type (unused for drum maps, included for signature).
        bars: Number of bars to generate (will loop the 2-bar core pattern).
        velocity_base: Base MIDI velocity for accented hits (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    # Jungle beats thrive at high tempos. Set to requested BPM.
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    
    # Force to a multiple of 2 bars to keep the pattern intact
    if bars < 2:
        bars = 2
        
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert MIDI Notes (The Jungle Rhythm) ===
    # General MIDI Drum Map
    KICK = 36
    SNARE = 38
    HIHAT = 42

    def add_drum_hit(pitch, start_beat, duration_beats, velocity):
        """Helper to convert beat positions to PPQ and insert a MIDI note."""
        start_pos = start_beat * beat_sec
        end_pos = start_pos + (duration_beats * beat_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        
        # Clamp velocity
        vel = max(1, min(127, int(velocity)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Note Duration (short 16th notes for drums)
    note_dur = 0.125  

    # Loop over the requested number of bars, applying the 2-bar pattern
    for bar_pair in range(0, bars, 2):
        base_beat = bar_pair * beats_per_bar
        
        # --- BAR 1: The "Minimum Effective Beat" with slight ghosting ---
        # Kick (beats 0, 2, 2.5)
        add_drum_hit(KICK, base_beat + 0.0, note_dur, velocity_base)
        add_drum_hit(KICK, base_beat + 2.0, note_dur, velocity_base - 10)
        add_drum_hit(KICK, base_beat + 2.5, note_dur, velocity_base)
        
        # Snare Main Backbeats (beats 1, 3)
        add_drum_hit(SNARE, base_beat + 1.0, note_dur, velocity_base)
        add_drum_hit(SNARE, base_beat + 3.0, note_dur, velocity_base)
        
        # Snare Ghost Notes (creating the breakbeat syncopation)
        add_drum_hit(SNARE, base_beat + 1.75, note_dur, velocity_base * 0.45) # 16th before beat 2
        add_drum_hit(SNARE, base_beat + 2.75, note_dur, velocity_base * 0.35) # 16th before beat 3
        add_drum_hit(SNARE, base_beat + 3.75, note_dur, velocity_base * 0.45) # 16th before beat 4
        
        # Hi-Hats (driving 8th notes)
        for i in range(8):
            hat_vel = velocity_base * 0.8 if i % 2 == 0 else velocity_base * 0.6
            add_drum_hit(HIHAT, base_beat + (i * 0.5), note_dur, hat_vel)

        # Ensure we don't write the second bar if requested an odd number of bars
        if bar_pair + 1 >= bars:
            break

        # --- BAR 2: The "Photek" 32nd-Note Embellishments ---
        base_beat_2 = base_beat + 4.0
        
        # Kick (syncopated: beats 0, 1.5, 2.5)
        add_drum_hit(KICK, base_beat_2 + 0.0, note_dur, velocity_base)
        add_drum_hit(KICK, base_beat_2 + 1.5, note_dur, velocity_base - 15)
        add_drum_hit(KICK, base_beat_2 + 2.5, note_dur, velocity_base)
        
        # Snare Main Backbeats (beats 1, 3)
        add_drum_hit(SNARE, base_beat_2 + 1.0, note_dur, velocity_base)
        add_drum_hit(SNARE, base_beat_2 + 3.0, note_dur, velocity_base)
        
        # Snare Ghost Notes & 32nd note Flurry
        add_drum_hit(SNARE, base_beat_2 + 2.75, note_dur, velocity_base * 0.45)
        add_drum_hit(SNARE, base_beat_2 + 3.75, note_dur, velocity_base * 0.35)   # 16th
        add_drum_hit(SNARE, base_beat_2 + 3.875, note_dur, velocity_base * 0.40)  # 32nd (Photek drag)
        
        # Hi-Hats (driving 8th notes)
        for i in range(8):
            hat_vel = velocity_base * 0.8 if i % 2 == 0 else velocity_base * 0.6
            add_drum_hit(HIHAT, base_beat_2 + (i * 0.5), note_dur, hat_vel)

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    # Add a stock EQ to prepare for standard breakbeat processing (crunchy/lo-fi)
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    return f"Created '{track_name}' with Photek-style Jungle pattern over {bars} bars at {bpm} BPM"
