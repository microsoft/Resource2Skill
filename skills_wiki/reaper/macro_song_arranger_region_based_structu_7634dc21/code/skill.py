def create_pattern(
    project_name: str = "Arrangement_Project",
    track_name: str = "Structure_Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 0, # Ignored, overridden by structure array
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a full Macro Song Arrangement using color-coded Regions and placeholder MIDI items.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the guide track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Unused in this specific skill (dictated by structure list).
        velocity_base: Base MIDI velocity for placeholder notes.
        **kwargs: Can accept a custom 'structure' list of tuples: (Section_Name, Length_In_Bars)
    """
    import reaper_python as RPR
    
    # Define default pop/rock structure if none is provided via kwargs
    # Format: (Section Name, Bar Count)
    structure = kwargs.get("structure", [
        ("Intro", 4),
        ("Verse 1", 8),
        ("Chorus 1", 8),
        ("Post-Chorus", 4),
        ("Verse 2", 8),
        ("Chorus 2", 8),
        ("Post-Chorus", 4),
        ("Bridge / Solo", 8),
        ("Chorus 3", 8),
        ("Outro", 4)
    ])

    # Music theory lookup for root note
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root MIDI note (Octave 3 for a solid bass/mid register pad)
    root_pitch = NOTE_MAP.get(key, 0) + 48 

    # Color definitions mapping REAPER's native color format (R + G*256 + B*65536 | 0x1000000)
    # RPR color flag requires the 0x1000000 bitwise OR to be recognized
    def rgb_to_reaper(r, g, b):
        return int(r + (g * 256) + (b * 65536)) | 0x1000000

    COLORS = {
        "Intro": rgb_to_reaper(100, 100, 100),       # Gray
        "Verse": rgb_to_reaper(100, 150, 200),       # Blue-ish
        "Chorus": rgb_to_reaper(100, 200, 100),      # Green
        "Post-Chorus": rgb_to_reaper(150, 100, 200), # Purple
        "Bridge": rgb_to_reaper(200, 200, 100),      # Yellow
        "Solo": rgb_to_reaper(200, 150, 100),        # Orange
        "Outro": rgb_to_reaper(100, 100, 100)        # Gray
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Timing calculations
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar

    # === Step 2: Create Arrangement Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a basic synth so the placeholders make sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Reduce track volume to act as a background scratch pad (-12dB approx = 0.25)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.25)

    # === Step 3: Iterate Structure and Build Regions/Items ===
    current_time = 0.0
    marker_id = 1
    total_bars = 0
    
    for section_name, section_bars in structure:
        section_length_sec = section_bars * bar_length_sec
        end_time = current_time + section_length_sec
        total_bars += section_bars
        
        # Determine color based on keyword in section name
        region_color = rgb_to_reaper(150, 150, 150) # Default
        for key_word, color_val in COLORS.items():
            if key_word in section_name:
                region_color = color_val
                break
                
        # 1. Create Region
        # Signature: AddProjectMarker2(proj, isrgn, pos, rgnend, name, markrgnindexnumber, color)
        RPR.RPR_AddProjectMarker2(0, True, current_time, end_time, section_name, marker_id, region_color)
        
        # 2. Create Placeholder MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", section_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Enable MIDI for the take
        RPR.RPR_MIDI_CountEvts(take, 0, 0, 0)
        
        # 3. Inject Placeholder 8th notes to act as a structural pulse
        notes_per_bar = 8 # 8th notes
        note_length_qn = 0.5 # half a quarter note = 8th note
        
        for bar in range(section_bars):
            for beat in range(notes_per_bar):
                # Calculate MIDI pulse timing in pulses per quarter note (PPQ = 960 standard)
                start_ppq = (bar * beats_per_bar * 960) + (beat * 480)
                end_ppq = start_ppq + 430 # Slightly staccato
                
                # Add minor velocity humanization (accents on downbeats)
                vel = velocity_base if beat % 2 == 0 else velocity_base - 15
                
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, root_pitch, vel, False
                )
        
        RPR.RPR_MIDI_Sort(take)
        
        # Advance time to next section
        current_time = end_time
        marker_id += 1

    return f"Created Song Arrangement with {len(structure)} regions ({total_bars} total bars) at {bpm} BPM in Key of {key}."
