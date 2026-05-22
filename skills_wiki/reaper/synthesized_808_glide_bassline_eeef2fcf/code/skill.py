def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "808 Glide Bass",
    bpm: int = 130,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a synthesized 808 bassline with distortion, compression, and pitch-glide automation.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    import reaper_python as RPR
    
    # 1. Setup Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # 2. Base Pitch Calculation (Octave 2 for 808s)
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_octave = 24  # C1 is 24, C2 is 36. We want it very low.
    
    # Generate a simple trap-style bass pattern relative to scale degrees
    # Tuples of (scale_degree_index, start_beat, duration_beats, pitch_drop_flag)
    rhythm_pattern = [
        (0, 0.0, 1.5, False),  # Downbeat root
        (0, 2.5, 1.0, False),  # Syncopated hit
        (4, 4.0, 0.5, False),  # Quick 5th hit
        (0, 5.0, 2.5, True)    # Long note that glides down
    ]
    pattern_beats = 8 # 2 bars per pattern loop
    
    # 3. Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # 4. Create FX Chain
    # ReaSynth
    synth_fx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_fx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_fx, 1, 0.5) # Tuning (0.5 = 0 cents)
    RPR.RPR_TrackFX_SetParam(track, synth_fx, 2, 0.0) # Attack (fast)
    RPR.RPR_TrackFX_SetParam(track, synth_fx, 5, 0.6) # Release (medium-long)
    
    # JS Distortion (Fuzz)
    dist_fx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    if dist_fx >= 0:
        RPR.RPR_TrackFX_SetParam(track, dist_fx, 0, 4.0) # Drive/Shape
        RPR.RPR_TrackFX_SetParam(track, dist_fx, 1, 0.5) # Output Mix
    
    # ReaComp (Smash it)
    comp_fx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_fx, 0, -15.0) # Thresh
    RPR.RPR_TrackFX_SetParam(track, comp_fx, 1, 50.0)  # Ratio
    RPR.RPR_TrackFX_SetParam(track, comp_fx, 2, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, comp_fx, 3, 50.0)  # Release
    
    # 5. Get Pitch Envelope (ReaSynth Parameter 1: Tuning)
    env = RPR.RPR_GetFXEnvelope(track, synth_fx, 1, True)
    
    # 6. Create MIDI Item
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    item_length_sec = (60.0 / bpm) * total_beats
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # 7. Populate MIDI & Automation
    note_count = 0
    
    for bar_pair in range(0, bars, int(pattern_beats/beats_per_bar)):
        offset_beats = bar_pair * beats_per_bar
        
        for scale_idx, start_b, dur_b, is_glide in rhythm_pattern:
            current_beat = offset_beats + start_b
            if current_beat >= total_beats:
                break
                
            # Calculate Pitch
            degree = scale_intervals[scale_idx % len(scale_intervals)]
            octave_shift = (scale_idx // len(scale_intervals)) * 12
            midi_pitch = base_octave + root_val + degree + octave_shift
            
            # Timing
            start_sec = (60.0 / bpm) * current_beat
            end_sec = start_sec + ((60.0 / bpm) * dur_b)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, False)
            note_count += 1
            
            # Write Pitch Envelope Automation
            # 0.5 is center tuning. 0.0 is -1200 cents (1 octave down).
            
            if env:
                if is_glide:
                    # Hold pitch for a short moment, then slide down
                    glide_start_sec = start_sec + ((60.0 / bpm) * 0.5) # start slide half a beat in
                    RPR.RPR_InsertEnvelopePoint(env, start_sec, 0.5, 0, 0, False, True)
                    RPR.RPR_InsertEnvelopePoint(env, glide_start_sec, 0.5, 0, 0, False, True)
                    RPR.RPR_InsertEnvelopePoint(env, end_sec, 0.0, 0, 0, False, True) # Drop to 0.0
                    RPR.RPR_InsertEnvelopePoint(env, end_sec + 0.01, 0.5, 0, 0, False, True) # Reset
                else:
                    # Keep pitch flat for standard notes
                    RPR.RPR_InsertEnvelopePoint(env, start_sec, 0.5, 0, 0, False, True)
                    RPR.RPR_InsertEnvelopePoint(env, end_sec, 0.5, 0, 0, False, True)

    if env:
        RPR.RPR_Envelope_SortPoints(env)
    
    RPR.RPR_UpdateArrange()
    
    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM, including custom FX chain and pitch automation."
