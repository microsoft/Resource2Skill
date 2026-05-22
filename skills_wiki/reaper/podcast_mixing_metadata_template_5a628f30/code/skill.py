def create_pattern(
    project_name: str = "Podcast_Template",
    track_name: str = "Host Vocal",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Podcast Mixing & Metadata Template in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the primary vocal track.
        bpm: Tempo in BPM (included for signature compatibility, less relevant here).
        key: Root note (ignored for podcast workflow).
        scale: Scale type (ignored for podcast workflow).
        bars: Number of bars (ignored for podcast workflow).
        velocity_base: Base MIDI velocity (ignored for podcast workflow).
        **kwargs: Additional overrides for metadata (artist, album, genre).

    Returns:
        Status string describing the created tracks and metadata.
    """
    import reaper_python as RPR

    # === Step 1: Create Host Vocal Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    vocal_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(vocal_track, "P_NAME", track_name, True)

    # === Step 2: Add Multi-Stage Vocal FX Chain ===
    # Stage 1: Auto-Leveler (Replaces Vocal Rider)
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaComp (Cockos)", False, -1)
    
    # Stage 2: Main Color Compressor (Replaces API 2500)
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaComp (Cockos)", False, -1)
    
    # Stage 3: Peak Limiter (Replaces 3rd Party Limiter)
    RPR.RPR_TrackFX_AddByName(vocal_track, "JS: Event Horizon Limiter/Clipper", False, -1)

    # === Step 3: Create Music Bed / Intro Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    music_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(music_track, "P_NAME", "Music Bed / Outro", True)
    
    # Attenuate the music bed volume to sit behind the vocal (approx -12dB is 0.25 in linear scale)
    RPR.RPR_SetMediaTrackInfo_Value(music_track, "D_VOL", 0.25)

    # === Step 4: Set Render Metadata (ID3 Tags) ===
    # Uses REAPER's wildcard system as demonstrated in the tutorial
    artist = kwargs.get("artist", "Podcast Host")
    album = kwargs.get("album", "My Killer Podcast")
    genre = kwargs.get("genre", "Podcast / Health")
    
    # The string format requires "Format:Tag|Value"
    # RENDER_METADATA is natively supported in REAPER to configure the render dialog automatically
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", f"ID3:TPE1|{artist}", True)
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", f"ID3:TALB|{album}", True)
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", f"ID3:TCON|{genre}", True)
    
    # REAPER wildcard for the current 4-digit year ($year)
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", "ID3:TYER|$year", True)

    return f"Created Podcast Template with '{track_name}', a 'Music Bed' track, and injected ID3 render metadata."
