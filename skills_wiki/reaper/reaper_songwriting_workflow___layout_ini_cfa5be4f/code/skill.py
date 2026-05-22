def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Songwriting Layout",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an additive Songwriting Track Layout in the current REAPER project,
    inspired by the "Customizable Layouts" chapter of the Reapertips tutorial.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (ignored for layout template).
        scale: Scale type (ignored for layout template).
        bars: Number of bars (ignored for layout template).
        velocity_base: Base MIDI velocity (ignored for layout template).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created layout.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Parent Folder Track ===
    start_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    folder_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(folder_track, "P_NAME", track_name, True)
    
    # Set to be a folder parent (1)
    RPR.RPR_SetMediaTrackInfo_Value(folder_track, "I_FOLDERDEPTH", 1)

    # === Step 3: Create Child Tracks for Songwriting ===
    # Using REAPER's custom color format: OS dependent, but generally Red + (Green * 256) + (Blue * 65536) | 0x1000000
    instruments = [
        {"name": "Drums", "color": 0x1000000 | 255 | (50 << 8) | (50 << 16)},     # Red-ish
        {"name": "Bass", "color": 0x1000000 | 50 | (150 << 8) | (255 << 16)},     # Blue-ish
        {"name": "Harmony", "color": 0x1000000 | 50 | (255 << 8) | (50 << 16)},   # Green-ish
        {"name": "Melody", "color": 0x1000000 | 255 | (200 << 8) | (50 << 16)}    # Yellow-ish
    ]

    for i, inst in enumerate(instruments):
        current_idx = start_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(current_idx, True)
        child_track = RPR.RPR_GetTrack(0, current_idx)
        
        # Name and color the track
        RPR.RPR_GetSetMediaTrackInfo_String(child_track, "P_NAME", inst["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_CUSTOMCOLOR", inst["color"])
        
        # If it's the last track, close the folder hierarchy (-1)
        if i == len(instruments) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_FOLDERDEPTH", -1)

    return f"Created '{track_name}' layout with {len(instruments)} child tracks (Drums, Bass, Harmony, Melody) at {bpm} BPM."
