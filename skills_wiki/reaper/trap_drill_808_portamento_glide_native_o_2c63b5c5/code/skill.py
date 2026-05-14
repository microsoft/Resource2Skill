def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "808 Glide Bass",
    bpm: int = 150,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Trap/Drill 808 bass pattern with overlapping notes triggering Portamento glides.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # We drop the root note down to the sub-bass octave (MIDI octave 2 -> base 24)
    base_midi_note = NOTE_MAP.get(key, 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (ReaSynth tuned as an 808 Sub) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth to sound like a deep 808 and enable Portamento
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.8)   # Param 0: Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Param 3: Square Mix (0 = clean)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0)   # Param 5: Triangle Mix (fat sub)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.8)   # Param 6: Extra Sine Mix (deep sub)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.35)  # Param 8: Portamento (approx 150ms glide)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 5: Program MIDI Notes (with deliberate overlapping) ===
    # Pattern: 
    # Beat 0.0 -> 1.0: Sustained root note
    # Beat 1.5 -> 2.5: Sustained root note
    # Beat 2.5 -> 3.5: Sustained root note 
    # Beat 3.25 -> 4.0: High glide note (Overlaps the 2.5 note to trigger the portamento slide!)
    
    pattern_beats = [
        {"start": 0.0,  "end": 1.0, "pitch_offset": 0},
        {"start": 1.5,  "end": 2.5, "pitch_offset": 0},
        {"start": 2.5,  "end": 3.5, "pitch_offset": 0},
        {"start": 3.25, "end": 4.0, "pitch_offset": 12}, # Overlaps previous note by 0.25 beats, slides +1 Octave
    ]
    
    notes_created = 0
    
    for bar in range(bars):
        bar_beat_offset = bar * beats_per_bar
        
        for note in pattern_beats:
            # Convert beats to time in seconds
            start_time = (bar_beat_offset + note["start"]) * (60.0 / bpm)
            end_time = (bar_beat_offset + note["end"]) * (60.0 / bpm)
            
            # Convert time to PPQ (Pulses Per Quarter Note) for accurate MIDI placement
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = base_midi_note + note["pitch_offset"]
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity_base, False
            )
            notes_created += 1

    # Force sort to finalize MIDI
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} overlapping notes over {bars} bars at {bpm} BPM to trigger portamento glides."
