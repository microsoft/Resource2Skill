def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create the Reapertips Songwriting Track Scaffold in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Ignored in favor of the template track names.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate for the scaffold item.
        velocity_base: Base MIDI velocity (0-127) for the placeholder.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created template.
    """
    import reaper_python as RPR

    # Music theory lookup tables for root note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper function to create REAPER native colors (r | g<<8 | b<<16 | 0x1000000)
    def make_reaper_color(r, g, b):
        return int(r) | (int(g) << 8) | (int(b) << 16) | 0x1000000

    # The track template as seen at 02:18
    template_tracks = [
        {"name": "Drums",    "color": make_reaper_color(255, 50, 150)},   # Pink
        {"name": "GTRs CLN", "color": make_reaper_color(255, 120, 0)},    # Orange
        {"name": "GTRs RHY", "color": make_reaper_color(255, 220, 0)},    # Yellow
        {"name": "BASS",     "color": make_reaper_color(0, 180, 255)},    # Blue/Cyan
        {"name": "VOX",      "color": make_reaper_color(150, 50, 255)},   # Purple
        {"name": "FX",       "color": make_reaper_color(0, 220, 100)}     # Green
    ]

    # === Step 2: Create Tracks ===
    start_idx = RPR.RPR_CountTracks(0)
    created_tracks = []
    
    for i, t_info in enumerate(template_tracks):
        idx = start_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Set Name
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        # Set Color
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_info["color"])
        
        created_tracks.append(track)

    # === Step 3: Create Musical Scaffold (Bass Anchor) ===
    # Add a driving 8th note bassline matching the requested key on the BASS track
    bass_track = created_tracks[3]
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Calculate root pitch in C2 octave (MIDI 36-47)
    root_offset = NOTE_MAP.get(key.upper(), 0)
    bass_pitch = 36 + root_offset
    
    # Create MIDI Item
    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, 0.0, item_length, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)
    
    # Insert 8th notes
    step_sec = (60.0 / bpm) / 2.0  # length of an 8th note in seconds
    total_notes = int(beats_per_bar * bars * 2)
    
    for i in range(total_notes):
        start_time = i * step_sec
        end_time = start_time + (step_sec * 0.8) # 80% gate length for staccato feel
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
        
        # Determine velocity (accent on downbeats)
        vel = velocity_base if (i % 2 == 0) else int(velocity_base * 0.8)
        vel = max(1, min(127, vel))
        
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, vel, False)

    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_UpdateArrange()

    return f"Created Reapertips 6-track template and {bars}-bar {key} {scale} bass scaffold at {bpm} BPM."
