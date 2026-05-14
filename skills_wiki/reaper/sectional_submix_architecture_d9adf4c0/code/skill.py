def create_pattern(
    project_name: str = "SectionalMastering",
    track_name: str = "Master Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 16,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Sectional Submix Architecture in the current REAPER project.
    
    Creates a master folder track with glue compression, and child tracks
    for Verse, Pre-Chorus, and Chorus with their own specific levels/FX.
    Generates placeholder regions with overlapping crossfades.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (unused, structural skill).
        scale: Scale type (unused, structural skill).
        bars: Total number of bars to generate the arrangement for.
        velocity_base: Base MIDI velocity (unused, structural skill).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created routing architecture.
    """
    import reaper_python as RPR
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # === Step 1: Create Parent Track ===
    parent_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(parent_idx, True)
    parent_track = RPR.RPR_GetTrack(0, parent_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    # Set as Folder Parent
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1) 
    
    # Add Glue Compressor and Limiter to Parent
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaLimit", False, -1)
    
    # === Step 2: Create Child Tracks (Sections) ===
    unique_sections = ["Verse", "Pre-Chorus", "Chorus"]
    track_refs = {}
    
    for i, sec_name in enumerate(unique_sections):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        child_track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(child_track, "P_NAME", sec_name, True)
        
        # Folder depth: -1 on the last track closes the folder grouping
        depth = -1 if i == len(unique_sections) - 1 else 0
        RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_FOLDERDEPTH", depth)
        
        # Add baseline EQ to all sections
        RPR.RPR_TrackFX_AddByName(child_track, "ReaEQ", False, -1)
        
        # Distinguish sections by volume and specific FX processing
        if sec_name == "Verse":
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "D_VOL", 0.7)  # Tame, quiet
        elif sec_name == "Pre-Chorus":
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "D_VOL", 0.85) # Building energy
        elif sec_name == "Chorus":
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "D_VOL", 1.0)  # Full power
            # Add saturation to make the chorus pop
            RPR.RPR_TrackFX_AddByName(child_track, "JS: Saturation", False, -1)
            
        track_refs[sec_name] = child_track

    # === Step 3: Layout Arrangement with Crossfades ===
    # Dynamically generate 4-bar sections up to the requested 'bars' limit
    sections_layout = []
    current_bar = 1
    cycle_idx = 0
    
    while current_bar <= bars:
        sec_name = unique_sections[cycle_idx % len(unique_sections)]
        len_bars = min(4, bars - current_bar + 1)
        if len_bars <= 0:
            break
            
        sections_layout.append({"name": sec_name, "start_bar": current_bar, "len_bars": len_bars})
        current_bar += len_bars
        cycle_idx += 1
    
    beats_per_bar = 4
    crossfade_len = 0.05 # 50ms overlap to ensure seamless transitions
    
    for i, sec in enumerate(sections_layout):
        track = track_refs[sec["name"]]
        start_sec = (60.0 / bpm) * beats_per_bar * (sec["start_bar"] - 1)
        length_sec = (60.0 / bpm) * beats_per_bar * sec["len_bars"]
        
        is_first = (i == 0)
        is_last = (i == len(sections_layout) - 1)
        
        item_len = length_sec
        # Extend item length slightly to overlap with the next section
        if not is_last:
            item_len += crossfade_len 
            
        # Create a placeholder MIDI item to represent the section's audio
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_sec, start_sec + item_len, False)
        
        # Apply fades: Because they sum to the same parent bus, concurrent 
        # fade-outs and fade-ins mathematically create a perfect crossfade.
        if not is_first:
            RPR.RPR_SetMediaItemInfo_Value(item, "D_FADEINLEN", crossfade_len)
        if not is_last:
            RPR.RPR_SetMediaItemInfo_Value(item, "D_FADEOUTLEN", crossfade_len)
            
        # Give the region a visible name
        take = RPR.RPR_GetActiveTake(item)
        if take:
            RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", f"{sec['name']} Region", True)
        
    return f"Created Sectional Submix Architecture ('{track_name}') mapping {len(sections_layout)} sections over {bars} bars at {bpm} BPM."
