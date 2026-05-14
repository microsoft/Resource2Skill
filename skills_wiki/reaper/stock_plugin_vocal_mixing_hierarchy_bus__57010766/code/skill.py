def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Vocal Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Stock Plugin Vocal Mixing Hierarchy (Bus, Lead, BGVs) in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables for generating placeholder "vocal" harmonies
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_midi = 60 + NOTE_MAP.get(key.capitalize(), 0) # Middle C octave
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Simple progression indices (I - VI - IV - V in the scale)
    progression = [0, 5, 3, 4] 

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    
    start_idx = RPR.RPR_CountTracks(0)

    # === 1. Create Vocal Bus (Parent) ===
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    bus_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1) # 1 = Folder Parent
    
    # Add Bus FX Chain
    RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: Saturation", False, -1)
    comp_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bus_track, comp_idx, 0, 0.7) # Light Threshold
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: De-esser", False, -1)
    RPR.RPR_TrackFX_AddByName(bus_track, "ReaLimit", False, -1)

    # Helper function to create a child vocal track with MIDI
    def create_vocal_layer(track_offset, name, pan, vol, folder_depth, scale_degree_offset):
        idx = start_idx + track_offset
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", folder_depth)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol)
        
        # Add Placeholder Synth (so we can hear the MIDI)
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Generate harmony notes
        for i in range(bars):
            chord_root_idx = progression[i % len(progression)]
            degree = (chord_root_idx + scale_degree_offset) % 7
            octave_shift = ((chord_root_idx + scale_degree_offset) // 7) * 12
            note_pitch = root_midi + scale_intervals[degree] + octave_shift
            
            start_pos = i * beats_per_bar
            end_pos = start_pos + (beats_per_bar * 0.9) # Slightly legato
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_pos * RPR.RPR_MIDI_GetProjTimeFromPPQPos(take, 960), 
                end_pos * RPR.RPR_MIDI_GetProjTimeFromPPQPos(take, 960), 
                1, note_pitch, int(velocity_base * vol), False
            )
        return track

    # === 2. Create Lead Vocal (Child 1) ===
    # Center panned, 0dB volume, plays the root (offset 0)
    lead_track = create_vocal_layer(1, "Lead Vocal", 0.0, 1.0, 0, 0)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaEQ", False, -1)
    lead_comp = RPR.RPR_TrackFX_AddByName(lead_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(lead_track, lead_comp, 0, 0.4) # Aggressive Threshold
    RPR.RPR_TrackFX_SetParamNormalized(lead_track, lead_comp, 1, 0.8) # High Ratio
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaVerbate", False, -1)

    # === 3. Create Background Vocal Left (Child 2) ===
    # Panned Hard Left, -10dB volume (approx 0.316 linear), plays the 3rd (offset 2)
    bgv_l_track = create_vocal_layer(2, "BGV L", -1.0, 0.316, 0, 2)
    RPR.RPR_TrackFX_AddByName(bgv_l_track, "ReaEQ", False, -1)
    bgv_comp_l = RPR.RPR_TrackFX_AddByName(bgv_l_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bgv_l_track, bgv_comp_l, 0, 0.3) # Very Aggressive
    RPR.RPR_TrackFX_AddByName(bgv_l_track, "ReaVerbate", False, -1)

    # === 4. Create Background Vocal Right (Child 3) ===
    # Panned Hard Right, -10dB volume, plays the 5th (offset 4).
    # Folder depth -1 closes the Vocal Bus folder.
    bgv_r_track = create_vocal_layer(3, "BGV R", 1.0, 0.316, -1, 4)
    RPR.RPR_TrackFX_AddByName(bgv_r_track, "ReaEQ", False, -1)
    bgv_comp_r = RPR.RPR_TrackFX_AddByName(bgv_r_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(bgv_r_track, bgv_comp_r, 0, 0.3) 
    RPR.RPR_TrackFX_AddByName(bgv_r_track, "ReaVerbate", False, -1)

    return f"Created '{track_name}' folder hierarchy with Lead and 2 BGVs over {bars} bars at {bpm} BPM in {key} {scale}."
