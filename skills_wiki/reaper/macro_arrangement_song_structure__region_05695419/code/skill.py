def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 56, 
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Macro-Arrangement Song Structure using Regions in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Unused for this project-level skill.
        bpm: Tempo in BPM used to calculate region lengths.
        key: Unused.
        scale: Unused.
        bars: Unused (driven by the internal arrangement structure).
        velocity_base: Unused.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Calculate timing conversions (assuming 4/4 time signature)
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar
    
    # === Step 2: Define Standard Song Structure ===
    # Format: (Section Name, Length in Bars, (R, G, B))
    sections = [
        ("Intro", 4, (255, 255, 0)),      # Yellow
        ("Verse 1", 8, (0, 128, 255)),    # Blue
        ("Chorus 1", 8, (0, 255, 0)),     # Green
        ("Verse 2", 8, (0, 128, 255)),    # Blue
        ("Chorus 2", 8, (0, 255, 0)),     # Green
        ("Bridge", 8, (128, 0, 128)),     # Purple
        ("Chorus 3", 8, (0, 255, 0)),     # Green
        ("Outro", 4, (255, 0, 0))         # Red
    ]
    
    # === Step 3: Generate Regions on Timeline ===
    current_time = 0.0
    rgn_idx = 1
    
    for name, length_bars, color_rgb in sections:
        # Calculate start and end times in seconds
        end_time = current_time + (length_bars * sec_per_bar)
        
        # Convert RGB to REAPER's native color format
        # Note: 0x1000000 must be bitwise OR'd for REAPER to recognize it as a custom color
        r, g, b = color_rgb
        color_val = RPR.RPR_ColorToNative(r, g, b) | 0x1000000
        
        # Add the region to the project
        # RPR_AddProjectMarker2(proj, isrgn, pos, rgnend, name, ID, color)
        RPR.RPR_AddProjectMarker2(0, True, current_time, end_time, name, rgn_idx, color_val)
        
        # Advance the timeline for the next section
        current_time = end_time
        rgn_idx += 1
        
    # Refresh the UI to show the new regions
    RPR.RPR_UpdateTimeline()
    
    total_bars = sum(s[1] for s in sections)
    return f"Created Song Arrangement with {len(sections)} regions over {total_bars} bars at {bpm} BPM"
