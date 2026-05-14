def create_pattern(
    project_name: str = "LoFiProject",
    track_name: str = "LoFi_Drum_Groove",
    bpm: int = 80,
    key: str = "C",  # Included for API consistency, but mapped to GM Drums
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Lo-Fi 'Drunken' Drum Groove with micro-timing offsets and Lo-Fi FX.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created drum track.
        bpm: Tempo in BPM (typically 70-85 for standard time Lo-Fi).
        key: Root note (unused natively here, respects GM Drum Map).
        scale: Scale type (unused natively here, respects GM Drum Map).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for strong hits (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # General MIDI Drum Map (Acts as our "theory" for this rhythm instrument)
    DRUM_MAP = {
        "kick": 36,   # C1
        "snare": 38,  # D1
        "hat": 42     # F#1
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Enable MIDI for the take
    RPR.RPR_MIDI_InsertNote(take, False, False, 0, 0, 1, 0, 1) # Dummy note to init
    RPR.RPR_MIDI_DeleteNote(take, 0) # Remove dummy

    # Timing constants
    ppq = 960 # Reaper default ticks per quarter note
    
    # Lo-Fi Humanization / "Drunken" offset
    # Shift hats late by about 10% of a 16th note
    hat_delay_ticks = int(ppq * 0.05) 
    
    note_count = 0

    # === Step 4: Program the Groove ===
    for bar in range(bars):
        bar_start_tick = bar * beats_per_bar * ppq
        
        # -- KICK -- (Beat 1, and Beat 2.5 for syncopation)
        kick_positions = [0, 1.5]
        for beat_pos in kick_positions:
            start_tick = int(bar_start_tick + (beat_pos * ppq))
            end_tick = start_tick + int(ppq * 0.25)
            # Slight velocity humanization
            vel = max(10, min(127, velocity_base + (bar % 2 * 5))) 
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, DRUM_MAP["kick"], vel)
            note_count += 1

        # -- SNARE -- (Beat 2 and Beat 4)
        snare_positions = [1.0, 3.0]
        for beat_pos in snare_positions:
            start_tick = int(bar_start_tick + (beat_pos * ppq))
            end_tick = start_tick + int(ppq * 0.25)
            vel = max(10, min(127, velocity_base - 5))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, DRUM_MAP["snare"], vel)
            note_count += 1

        # -- HI-HATS -- (8th notes, drunken timing, alternating velocity)
        for eighth in range(8):
            beat_pos = eighth * 0.5
            
            # Apply drunken delay offset
            start_tick = int(bar_start_tick + (beat_pos * ppq) + hat_delay_ticks)
            end_tick = start_tick + int(ppq * 0.125)
            
            # Alternating velocity: strong on downbeats, weak on upbeats
            if eighth % 2 == 0:
                vel = max(10, min(127, int(velocity_base * 0.85)))
            else:
                vel = max(10, min(127, int(velocity_base * 0.55)))
                
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, DRUM_MAP["hat"], vel)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Lo-Fi FX Chain ===
    
    # 1. Add ReaEQ to simulate bandwidth limiting / sampler degradation
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # ReaEQ Parameter logic:
    # Band 4 High Shelf Gain is roughly parameter 10. 
    # We drop the high shelf gain to -24dB to simulate a low-pass filter.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 0.0) # 0.0 internal usually maps to lowest gain (-24dB)
    # Band 4 Frequency is parameter 9. Set to around 3kHz.
    # Note: internal 0.0-1.0 mapping for freq is logarithmic, 0.6 is roughly in the mid-highs.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 0.55) 

    # 2. Add Tremolo for tape wow/flutter amplitude modulation
    trem_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Tremolo", False, -1)
    if trem_idx >= 0:
        # Tremolo Amount (Parameter 0)
        RPR.RPR_TrackFX_SetParam(track, trem_idx, 0, 15.0) # ~15% depth
        # Tremolo Frequency (Parameter 1)
        RPR.RPR_TrackFX_SetParam(track, trem_idx, 1, 2.0)  # ~2 Hz for slow tape wobble

    return f"Created '{track_name}' with {note_count} drunken groove notes over {bars} bars at {bpm} BPM with Lo-Fi FX."
