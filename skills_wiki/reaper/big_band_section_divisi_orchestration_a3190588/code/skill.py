def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Big Band Saxes",
    bpm: int = 120,
    key: str = "C",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 5-part Big Band Divisi orchestration in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (informational here, as jazz voicings are hardcoded to relative root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Step 1: Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_offset = NOTE_MAP.get(key.capitalize(), 0)
    root_midi = 36 + root_offset  # Base octave C2

    # 5-part extended big band voicings (Bottom to Top: Bari, T2, T1, A2, A1)
    voicings = [
        [0, 10, 15, 19, 26],  # i min9 (Root, b7, b3, 5, 9)
        [5, 15, 21, 24, 31],  # IV dom9 (relative to Root)
        [7, 17, 23, 26, 33],  # V dom9 (relative to Root)
        [0, 10, 15, 19, 26],  # i min9
    ]

    # Syncopated horn stab rhythm (start_beat, duration_in_beats)
    rhythm = [
        (0.0, 0.5),   # Downbeat 1
        (1.5, 0.5),   # Syncopated 'and' of 2
        (3.0, 0.75),  # Downbeat 4
    ]

    # === Step 2: Create Parent Folder Track ===
    parent_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(parent_idx, True)
    parent_track = RPR.RPR_GetTrack(0, parent_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1) # Start folder

    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    
    # Stage layout for 5-part sax section
    parts = [
        {"name": "Bari Sax",   "pan": 0.0},   # Center
        {"name": "Tenor Sax 2", "pan": 0.3},  # Mid Right
        {"name": "Tenor Sax 1", "pan": -0.3}, # Mid Left
        {"name": "Alto Sax 2",  "pan": 0.6},  # Right
        {"name": "Alto Sax 1",  "pan": -0.6}, # Left
    ]

    # === Step 3: Generate Divisi Tracks ===
    for i, part in enumerate(parts):
        track_idx = parent_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} - {part['name']}", True)
        
        # Apply panning
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", part["pan"])
        
        # Manage folder hierarchy
        if i == len(parts) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", -1) # End folder
        else:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", 0)

        # Add generic synth (Placeholder for SWAM / Kontakt instruments)
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.7)  # Saw mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.03) # Fast Attack for stabs
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 0.1) # Short Release

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_len * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Insert Divisi Notes & Expression
        for bar in range(bars):
            chord = voicings[bar % len(voicings)]
            note_val = root_midi + chord[i]
            
            for start_beat, len_beats in rhythm:
                start_time = (bar * bar_len) + (start_beat * (60.0 / bpm))
                end_time = start_time + (len_beats * (60.0 / bpm))
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Note
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note_val), velocity_base, False)
                
                # --- Emulate Physical Controller Dynamics ---
                # CC2 (Breath/Expression) Swell
                RPR.RPR_MIDI_InsertCC(take, False, False, start_ppq, 176, 0, 2, 60)
                mid_ppq = start_ppq + (end_ppq - start_ppq) / 2
                RPR.RPR_MIDI_InsertCC(take, False, False, mid_ppq, 176, 0, 2, 115)
                RPR.RPR_MIDI_InsertCC(take, False, False, end_ppq - 10, 176, 0, 2, 40)

                # CC1 (Bite Sensor/Vibrato) Delayed application
                RPR.RPR_MIDI_InsertCC(take, False, False, start_ppq, 176, 0, 1, 0)
                if len_beats >= 0.5:
                    RPR.RPR_MIDI_InsertCC(take, False, False, mid_ppq, 176, 0, 1, 75)

    return f"Created 5-part Divisi Horn Section '{track_name}' in {key} over {bars} bars at {bpm} BPM"
