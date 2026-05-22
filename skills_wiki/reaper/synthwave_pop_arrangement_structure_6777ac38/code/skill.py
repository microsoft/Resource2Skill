def create_pattern(
    project_name: str = "Synthwave_Pop",
    track_name: str = "Arrangement Guide",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 96,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete Synthwave Pop Arrangement template in the current REAPER project.
    Generates colored empty media items and Project Regions to map out the "Rollercoaster" 
    energy structure detailed in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created arrangement guide track.
        bpm: Tempo in BPM.
        key: Root note (ignored for structure, kept for signature).
        scale: Scale type (ignored for structure, kept for signature).
        bars: Total bars (overridden by the fixed 96-bar pop structure).
        velocity_base: Base MIDI velocity (ignored for structure).
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the structure created.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Define the Synthwave Pop Structure ===
    # Format: (Section Name, Length in Bars, R, G, B)
    # Colors represent energy: Blues/Cool = Low Energy, Purples = Medium, Reds/Oranges = High Peak Energy
    structure = [
        ("Intro",                   8,  50,  50, 150),  # Low energy
        ("Verse 1 (No Drums)",      8,  50, 100, 150),  # Low energy
        ("Pre-Chorus 1",            8, 100,  50, 150),  # Tension building
        ("Chorus 1",                8, 200,  50,  50),  # First Peak
        ("Verse 2 (Drums In)",      8,  50, 150, 150),  # Energy dips, but higher than V1
        ("Pre-Chorus 2",            8, 150,  50, 150),  # Tension building
        ("Chorus 2 (Double/Solo)", 16, 220,  50,  50),  # Second Peak (Longer, features solo)
        ("Bridge",                  8, 100, 100, 200),  # Harmonic shift / Energy dip
        ("Chorus 3 (Max Energy)",  16, 255,   0,   0),  # Final Climax
        ("Outro",                   8,  50,  50,  50)   # Energy decay
    ]

    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar

    # === Step 3: Create Arrangement Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    current_bar = 0

    # === Step 4: Populate Timeline with Regions and Blocks ===
    for name, length_bars, r, g, b in structure:
        start_time = current_bar * sec_per_bar
        end_time = (current_bar + length_bars) * sec_per_bar

        # 4a. Add Empty Media Item as a placeholder block
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_bars * sec_per_bar)

        # Convert RGB to REAPER's native custom color format (r + g*256 + b*65536 | 0x1000000 flag)
        native_color = int(r + (g * 256) + (b * 65536)) | 0x1000000
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", native_color)

        # 4b. Add Take and Name it so it displays on the item
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", name, True)

        # 4c. Add Project Region for global DAW navigation
        # AddProjectMarker2(proj, isrgn, pos, rgnend, name, wantidx, color)
        RPR.RPR_AddProjectMarker2(0, True, start_time, end_time, name, -1, native_color)

        current_bar += length_bars

    # Update REAPER UI to show the new items and regions
    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' and Project Regions mapping a {current_bar}-bar Synthwave Pop structure at {bpm} BPM."
