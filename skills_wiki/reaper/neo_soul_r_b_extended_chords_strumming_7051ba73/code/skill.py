def create_pattern(
    project_name: str = "Neo Soul R&B",
    track_name: str = "R&B Chords",
    bpm: int = 95,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create an R&B / Neo-Soul chord progression with extended 9ths/11ths and strum timing.
    """
    import reaper_python as RPR

    # Music theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base MIDI note (C3 = 48)
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length = (60.0 / bpm) * beats_per_bar * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to insert MIDI notes
    def insert_note(start_qn, end_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # R&B Chord Voicings (semitones from root)
    # 1. Minor 9
    # 2. Minor 11 (Root down oct, 11th down oct)
    # 3. Minor 9 flat 7 (flattened 7th for altered tension)
    # 4. Diminished passing chord (built on minor 3rd)
    chord_progression = [
        {"intervals": [0, 3, 7, 10, 14], "start_qn": 0.0, "len_qn": 3.5},
        {"intervals": [-12, 3, 7, 10, 14, 5], "start_qn": 4.0, "len_qn": 3.5},
        {"intervals": [0, 3, 7, 9, 14], "start_qn": 8.0, "len_qn": 3.5},
        {"intervals": [3, 6, 9], "start_qn": 14.0, "len_qn": 1.5}
    ]

    # Strum parameters
    strum_delay_qn = 0.035 # Milliseconds of delay per note in the chord
    note_count = 0

    # === Step 4: Generate Chords across requested bars ===
    # Loop the 4-bar progression to fill the requested number of bars
    for bar_offset in range(0, bars, 4):
        offset_qn = bar_offset * 4.0
        
        for chord in chord_progression:
            # Skip if chord falls outside requested bar count
            if offset_qn + chord["start_qn"] >= bars * 4.0:
                continue
                
            base_start = offset_qn + chord["start_qn"]
            
            # Sort intervals so we strum from bottom to top
            sorted_intervals = sorted(chord["intervals"])
            
            for i, interval in enumerate(sorted_intervals):
                pitch = root_midi + interval
                # Apply strum delay: each successive note starts slightly later
                note_start = base_start + (i * strum_delay_qn)
                note_end = base_start + chord["len_qn"]
                
                # Slight velocity humanization (higher notes slightly softer)
                vel = max(40, velocity_base - (i * 4))
                
                # Keep MIDI pitch in bounds
                if 0 <= pitch <= 127:
                    insert_note(note_start, note_end, pitch, vel)
                    note_count += 1

    # Sort the MIDI stream after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain for Pad Tone ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a pad feel (Soft attack, soft release)
    # Param 1 = Attack (0.1 = ~100ms)
    # Param 2 = Decay
    # Param 3 = Sustain
    # Param 4 = Release (0.5 = long release)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.1) 
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4) 

    return f"Created '{track_name}' with {note_count} strummed R&B chord notes over {bars} bars in {key} minor at {bpm} BPM."
