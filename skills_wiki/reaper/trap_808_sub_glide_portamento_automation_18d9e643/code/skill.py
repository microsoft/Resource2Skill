def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "808 Sub Glide",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Trap/Drill 808 sub bass with a characteristic octave glide.
    """
    import reaper_python as RPR

    # Music theory lookup for sub bass (C1 - B1 range)
    NOTE_MAP = {
        "C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
        "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
        "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35
    }
    base_pitch = NOTE_MAP.get(key.upper(), 24)

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Build 808 Sound Design (ReaSynth + Saturation) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth as a Sub Bass
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.8)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5)  # Tuning (Center 0.5 = 0 shift)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.05) # Attack (slight fade to avoid clicks)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.6)  # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.8)  # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.3)  # Release
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.0)  # Saw mix

    # Add Saturation to generate 808 harmonics
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    if sat_idx >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, sat_idx, 0, 0.75) # Drive amount

    # === Step 3: Create MIDI Item & Rhythm ===
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    item_len = bar_len * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 808 Pattern: Hit on Beat 1, Hit on Beat 3, Slide on Beat 4
    sec_per_beat = 60.0 / bpm
    
    for b in range(bars):
        bar_start = b * bar_len
        
        # Note 1: Downbeat
        start1 = bar_start + 0.0
        end1 = bar_start + (sec_per_beat * 1.5)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start1), 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end1), 
                                0, base_pitch, velocity_base, False)
                                
        # Note 2: Offbeat hitting into the slide
        start2 = bar_start + (sec_per_beat * 2.5)
        end2 = bar_start + (sec_per_beat * 4.0)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start2), 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end2), 
                                0, base_pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Automate the 808 Pitch Glide ===
    # Get the envelope for ReaSynth "Tuning" (Param Index 1)
    # Range is 0.0 (-24st) to 1.0 (+24st). Center is 0.5. An octave up (+12st) is 0.75.
    env = RPR.RPR_GetFXEnvelope(track, synth_idx, 1, True)
    
    for b in range(bars):
        bar_start = b * bar_len
        
        # Slide timing: starts half a beat before the end of the bar, peaks at the end
        slide_start = bar_start + (sec_per_beat * 3.0)
        slide_peak = bar_start + (sec_per_beat * 3.5)
        slide_end = bar_start + (sec_per_beat * 4.0)
        
        # Insert Envelope Points (Time, Value, Shape, Tension, Selected, NoSort)
        # Shape 2 = Slow Start/End (perfect for smooth glides)
        RPR.RPR_InsertEnvelopePoint(env, slide_start - 0.01, 0.5, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, slide_start, 0.5, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, slide_peak, 0.75, 0, 0.0, False, True) # Glides up +1 octave
        RPR.RPR_InsertEnvelopePoint(env, slide_end, 0.75, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, slide_end + 0.01, 0.5, 0, 0.0, False, True) # Snap back to normal

    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with 808 Pitch Automation Glide (+1 Octave) over {bars} bars at {bpm} BPM."
