def create_pattern(
    project_name: str = "FrankOceanVibe",
    track_name: str = "Nostalgic R&B",
    bpm: int = 95,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a Frank Ocean-style Wurlitzer chord progression and slapback drum loop.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale context (ignored for explicit out-of-key chord voicing).
        bars: Number of bars to generate (loops the 4-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string of the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    root_val = NOTE_MAP.get(key, 0)
    root_midi = 48 + root_val # C3 base

    # Define the chord progression (intervals from the root)
    # 1. I maj7
    # 2. IV maj7 
    # 3. iv min7 (borrowed)
    # 4. v min7 (shifted up 2 semitones, borrowed)
    chords = [
        {"intervals": [0, 4, 7, 11], "beat_offset": 0, "len_beats": 4},
        {"intervals": [5, 9, 12, 16], "beat_offset": 4, "len_beats": 4},
        {"intervals": [0, 4, 7, 11], "beat_offset": 8, "len_beats": 4},
        {"intervals": [5, 8, 12, 15], "beat_offset": 12, "len_beats": 2},
        {"intervals": [7, 10, 14, 17], "beat_offset": 14, "len_beats": 2},
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper function to create tracks and MIDI items
    def create_midi_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        item_len = (60.0 / bpm) * 4 * bars
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === TRACK 1: WURLITZER CHORDS ===
    track_ep, take_ep = create_midi_track(f"{track_name} - E-Piano")
    
    # Generate Chords
    for bar in range(0, bars, 4): # Pattern is 4 bars long
        bar_beat_offset = bar * 4
        for chord in chords:
            start_beat = bar_beat_offset + chord["beat_offset"]
            end_beat = start_beat + chord["len_beats"]
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_ep, start_beat)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_ep, end_beat)
            
            for interval in chord["intervals"]:
                pitch = root_midi + interval
                if 0 <= pitch <= 127:
                    # Roll off velocity slightly for a softer EPiano feel
                    vel = int(velocity_base * 0.85)
                    RPR.RPR_MIDI_InsertNote(take_ep, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
                    
    RPR.RPR_MIDI_Sort(take_ep)
    
    # EPiano FX Chain (ReaSynth)
    fx_synth = RPR.RPR_TrackFX_AddByName(track_ep, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_ep, fx_synth, 1, 0.3) # Sawtooth (bite)
    RPR.RPR_TrackFX_SetParam(track_ep, fx_synth, 2, 0.7) # Square (hollow/warm body)

    # === TRACK 2: SLAPBACK DRUMS ===
    track_drums, take_drums = create_midi_track(f"{track_name} - Tape Drums")
    
    # GM Drum Mapping
    KICK = 36
    SNARE = 38
    
    for bar in range(bars):
        bar_beat_offset = bar * 4
        
        # Primary Hits
        # Kick on 1 and 2.5 (the "and" of 2)
        # Snare on 2 and 4
        drum_hits = [
            {"beat": 0.0, "pitch": KICK},
            {"beat": 1.0, "pitch": SNARE},
            {"beat": 2.5, "pitch": KICK},
            {"beat": 3.0, "pitch": SNARE}
        ]
        
        for hit in drum_hits:
            # Main Hit
            start_beat = bar_beat_offset + hit["beat"]
            end_beat = start_beat + 0.25 # 16th note duration
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_beat)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, end_beat)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 0, hit["pitch"], velocity_base, False)
            
            # Slapback Hit (1/16th note later, 50% velocity)
            slap_start_beat = start_beat + 0.25
            slap_end_beat = slap_start_beat + 0.25
            
            slap_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, slap_start_beat)
            slap_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, slap_end_beat)
            slap_vel = int(velocity_base * 0.5)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, slap_start_ppq, slap_end_ppq, 0, hit["pitch"], slap_vel, False)

    RPR.RPR_MIDI_Sort(take_drums)
    
    # Drums FX Chain (Saturation for Tape Grit)
    fx_sat = RPR.RPR_TrackFX_AddByName(track_drums, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(track_drums, fx_sat, 0, 45.0) # Dial up the saturation amount (0-100)

    return f"Created Neo-Soul Wurlitzer Chords and Tape Slapback Drums over {bars} bars at {bpm} BPM in {key}."
