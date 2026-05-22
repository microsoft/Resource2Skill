def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Guide",
    bpm: int = 120,
    key: str = "C",      # Accepted for compatibility, unused in structural generation
    scale: str = "minor",  # Accepted for compatibility, unused in structural generation
    bars: int = 0,       # Override total bars if needed, though 'arrangement' list dictates this
    velocity_base: int = 100,
    arrangement: list = None,
    **kwargs,
) -> str:
    """
    Create a standard song structure using Regions and guide items in REAPER.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created arrangement guide track.
        bpm: Tempo in BPM.
        arrangement: A list of tuples defining the structure (Section Name, Length in Bars).
                     Defaults to a standard Pop/EDM structure.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # Default arrangement if none is provided: Intro, Verse 1, Chorus 1, Verse 2, Chorus 2, Outro
    if arrangement is None:
        arrangement = [
            ("Intro", 4),
            ("Verse", 8),
            ("Chorus", 8),
            ("Verse", 8),
            ("Chorus", 8),
            ("Outro", 4)
        ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Guide Track ===
    # This track will hold empty media items serving as visual blocks for the sections
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Optional: Lock the track controls so it serves purely as a visual guide
    # RPR.RPR_SetMediaTrackInfo_Value(track, "B_SHOWINMIXER", 0) # Hide from mixer

    # === Step 3: Calculate Timing & Colors ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar

    # Helper function to generate REAPER compatible color integers
    def make_color(r, g, b):
        return (r | (g << 8) | (b << 16)) | 0x1000000

    # Color mapping matching the tutorial's aesthetic
    color_map = {
        "intro": make_color(255, 255, 0),   # Yellow
        "verse": make_color(0, 255, 0),     # Green
        "chorus": make_color(0, 0, 255),    # Blue
        "bridge": make_color(255, 0, 255),  # Magenta
        "outro": make_color(255, 100, 0)    # Orange
    }

    # === Step 4: Generate Regions and Guide Items ===
    current_bar = 0
    total_bars = 0
    
    for section_name, section_bars in arrangement:
        start_pos = current_bar * sec_per_bar
        length_sec = section_bars * sec_per_bar
        end_pos = start_pos + length_sec
        
        # Determine color (fallback to grey if name isn't recognized)
        name_lower = section_name.lower().strip()
        region_color = make_color(150, 150, 150) # Default Grey
        for key in color_map:
            if key in name_lower:
                region_color = color_map[key]
                break

        # Add Region to the timeline
        # proj=0, isrgn=True, pos=start_pos, rgnend=end_pos, name=section_name, markrgnindexnumber=-1 (auto), color
        RPR.RPR_AddProjectMarker2(0, True, start_pos, end_pos, section_name, -1, region_color)

        # Add visual guide block (empty item) to the guide track
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        
        # Color the item to match the region
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", region_color)
        
        # Add an empty take to set the item name display
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", f"[{section_name}]", True)

        current_bar += section_bars
        total_bars += section_bars

    # Force UI update
    RPR.RPR_UpdateArrange()

    # Format output status
    section_names = ", ".join([f"{name} ({b}b)" for name, b in arrangement])
    return f"Created '{track_name}' and Regions for {len(arrangement)} sections ({total_bars} total bars at {bpm} BPM): {section_names}."
