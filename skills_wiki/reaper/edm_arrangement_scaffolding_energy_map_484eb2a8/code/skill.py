def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Energy Map & Structure",
    bpm: int = 126,
    key: str = "C",
    scale: str = "minor",
    bars: int = 104,  # Overridden by structural math
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an industry-standard EDM arrangement scaffold with an automated Energy Map.
    Inserts labeled, color-coded block items, project markers, and an automation curve 
    representing the track's tension/release journey.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created structure track.
        bpm: Tempo in BPM.
        key: Root note (unused directly, but fits signature).
        scale: Scale type (unused directly, but fits signature).
        bars: Total duration (managed internally by sections).
        velocity_base: Unused for arrangement.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Step 1: Initialize Tempo & Math ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # Helper function to generate safe OS-native colors
    def make_color(r, g, b):
        return int(r + (g << 8) + (b << 16) | 0x1000000)

    # Standard EDM Arrangement Journey (Length in bars, Energy 0.0 - 1.0)
    sections = [
        {"name": "Intro",   "bars": 16, "e_start": 0.20, "e_end": 0.30, "color": make_color(50, 150, 200)},  # Blue
        {"name": "Verse 1", "bars": 16, "e_start": 0.30, "e_end": 0.40, "color": make_color(50, 200, 50)},   # Green
        {"name": "Build 1", "bars": 8,  "e_start": 0.40, "e_end": 0.90, "color": make_color(220, 200, 50)},  # Yellow
        {"name": "Drop 1",  "bars": 16, "e_start": 1.00, "e_end": 0.85, "color": make_color(250, 50, 50)},   # Red
        {"name": "Verse 2", "bars": 16, "e_start": 0.35, "e_end": 0.50, "color": make_color(50, 200, 50)},   # Green
        {"name": "Build 2", "bars": 8,  "e_start": 0.50, "e_end": 0.95, "color": make_color(220, 200, 50)},  # Yellow
        {"name": "Drop 2",  "bars": 16, "e_start": 1.00, "e_end": 0.90, "color": make_color(250, 50, 50)},   # Red
        {"name": "Outro",   "bars": 16, "e_start": 0.50, "e_end": 0.00, "color": make_color(100, 100, 100)}  # Grey
    ]

    # === Step 2: Create Structure Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup Energy Map (Volume Envelope) ===
    # Select only the new track and make the volume envelope visible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Command: "Track: Toggle track volume envelope visible"
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    current_time = 0.0
    marker_idx = 1
    
    # === Step 4: Scaffold the Track ===
    for sec in sections:
        sec_len_sec = sec["bars"] * bar_length_sec

        # A. Insert Navigation Marker
        RPR.RPR_AddProjectMarker(0, False, current_time, 0, sec["name"], marker_idx)
        marker_idx += 1

        # B. Insert Structural Block (Empty MIDI Item)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, current_time, current_time + sec_len_sec, False)
        
        # Colorize the item based on energy/function
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", sec["color"])
        
        # Name the item take to display the section name
        take = RPR.RPR_GetActiveTake(item)
        if take:
            RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", sec["name"], True)

        # C. Draw the Energy Curve (Volume Automation)
        if env:
            # RPR_InsertEnvelopePoint params: env, time, value, shape, tension, selected, noSort
            # shape 0 = Linear (perfect for mapping builds and fades)
            RPR.RPR_InsertEnvelopePoint(env, current_time, sec["e_start"], 0, 0, False, True)
            RPR.RPR_InsertEnvelopePoint(env, current_time + sec_len_sec - 0.001, sec["e_end"], 0, 0, False, True)

        current_time += sec_len_sec

    # Sort envelope points to ensure proper display
    if env:
        RPR.RPR_Envelope_SortPoints(env)

    total_bars_created = sum(s["bars"] for s in sections)
    return f"Created EDM Arrangement Scaffold: {len(sections)} sections ({total_bars_created} bars) at {bpm} BPM with Energy Map curve."
