def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 44, # Total bars of the template
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Song Structure Skeleton (Region & Marker Auto-Arrangement) in REAPER.
    
    This sets up a standard track arrangement (Intro, Verse, Chorus, etc.)
    using REAPER Regions and Markers, enabling rapid structural editing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Unused here (operates globally on timeline).
        bpm: Tempo in BPM.
        key: Root note (unused).
        scale: Scale type (unused).
        bars: Unused directly (uses the internal structure list).
        velocity_base: Unused.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created structure.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Define Arrangement Structure ===
    # Format: (Section Name, Length in Bars, (R, G, B) color)
    structure = [
        ("Intro", 4, (200, 200, 50)),   # Yellow
        ("Verse 1", 8, (50, 200, 50)),  # Green
        ("Chorus 1", 8, (50, 100, 255)),# Blue
        ("Verse 2", 8, (50, 200, 50)),  # Green
        ("Chorus 2", 8, (50, 100, 255)),# Blue
        ("Bridge", 4, (200, 50, 200)),  # Purple
        ("Outro", 4, (200, 100, 50))    # Orange
    ]

    current_measure = 0
    markers_added = 0
    regions_added = 0

    # === Step 3: Generate Markers and Regions ===
    for section in structure:
        name, length_bars, color_rgb = section
        r, g, b = color_rgb

        # REAPER color calculation: R + G*256 + B*65536. 
        # The bitwise OR with 0x1000000 tells REAPER to actively use this color.
        reaper_color = int(r + (g * 256) + (b * 65536)) | 0x1000000

        # Calculate start and end times in seconds using REAPER's tempo map.
        # RPR_TimeMap2_beatsToTime(proj, tpos_beats, tpos_measures)
        # We pass 0 beats and target the measure index.
        start_time = RPR.RPR_TimeMap2_beatsToTime(0, 0, current_measure)
        
        current_measure += length_bars
        
        end_time = RPR.RPR_TimeMap2_beatsToTime(0, 0, current_measure)

        # Add Marker at the start of the section (isrgn=False)
        # Signature: AddProjectMarker2(proj, isrgn, pos, rgnend, name, wantidx, color)
        RPR.RPR_AddProjectMarker2(0, False, start_time, 0, name, -1, reaper_color)
        markers_added += 1

        # Add Region covering the section (isrgn=True)
        RPR.RPR_AddProjectMarker2(0, True, start_time, end_time, name, -1, reaper_color)
        regions_added += 1

    # Force UI update to show the new timeline elements
    RPR.RPR_UpdateTimeline()

    total_bars = sum([sec[1] for sec in structure])
    return f"Created {regions_added} Regions and {markers_added} Markers forming a {total_bars}-bar song structure at {bpm} BPM."
