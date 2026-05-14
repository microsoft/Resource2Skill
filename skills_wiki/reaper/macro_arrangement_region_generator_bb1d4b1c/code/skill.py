def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Scratchpad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 60, # Total bars fallback
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Macro-Arrangement Region Template in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created underlying track.
        bpm: Tempo in BPM.
        key: Root note (unused natively in markers, but kept for signature).
        scale: Scale type (unused natively in markers, but kept for signature).
        bars: Total fallback length.
        velocity_base: Base MIDI velocity (unused here).
        **kwargs: Can accept a 'structure' list of tuples (Name, Bars, (R,G,B)).

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Define the Macro Arrangement Structure ===
    # Format: [("Section Name", Length_In_Bars, (R, G, B))]
    structure = kwargs.get("structure", [
        ("Intro",      4, (100, 150, 200)),  # Soft Blue
        ("Verse 1",    8, (150, 200, 100)),  # Green
        ("Pre-Chorus", 4, (200, 175,  50)),  # Orange/Yellow
        ("Chorus 1",   8, (220,  80,  80)),  # Red (High Energy)
        ("Verse 2",    8, (150, 200, 100)),  # Green
        ("Chorus 2",   8, (220,  80,  80)),  # Red
        ("Bridge",     8, (150, 100, 200)),  # Purple (Alternative harmonic center)
        ("Chorus 3",   8, (220,  80,  80)),  # Red
        ("Outro",      4, (100, 100, 100))   # Gray
    ])

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    current_time = 0.0

    # === Step 3: Generate the Timeline Regions ===
    for idx, section in enumerate(structure):
        name = section[0]
        section_bars = section[1]
        r, g, b = section[2]

        # REAPER Custom color bitwise logic: 0x1000000 | (B << 16) | (G << 8) | R
        color_int = 0x1000000 | (b << 16) | (g << 8) | r

        end_time = current_time + (section_bars * bar_length_sec)

        # Add Project Marker as Region (isrgn=True is the 2nd parameter)
        # RPR_AddProjectMarker2(proj, isrgn, pos, rgnend, name, wantidx, color)
        RPR.RPR_AddProjectMarker2(0, True, current_time, end_time, name, -1, color_int)

        current_time = end_time

    # === Step 4: Add an empty Scratchpad Track for pre-pro demoing ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    total_bars_created = sum(sec[1] for sec in structure)
    
    return f"Created {len(structure)} arrangement Regions ({total_bars_created} total bars) and track '{track_name}' at {bpm} BPM"
