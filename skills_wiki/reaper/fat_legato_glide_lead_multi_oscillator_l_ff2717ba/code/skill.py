def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Fat Glide Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Fat Legato Glide Lead synth pattern using stacked ReaSynths and dynamic filtering.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    
    # Base octave for a lead synth
    octave_offset = 5 
    scale_pitches = [root_val + (12 * octave_offset) + interval for interval in scale_intervals]
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Add FX Chain (Multi-Oscillator Synth) ===
    # Instance 1: Center / Main Osc
    synth_main = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Instance 2: Detuned down
    synth_det1 = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Instance 3: Detuned up
    synth_det2 = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Instance 4: Sub Octave
    synth_sub = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth VST Normalized parameters estimate:
    # Param 0: Volume, Param 1: Tuning, Param 6: Portamento, Param 9: Sawtooth Mix
    for fx_idx in [synth_main, synth_det1, synth_det2, synth_sub]:
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 9, 0.8) # 80% Sawtooth
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.1) # Portamento ON (approx 30-40ms)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.4) # Lower volume to prevent clipping
        
    # Detuning & Octave offsets
    # Tuning normalized: 0.5 is 0 cents. Range is typically -1200 to +1200 (or -100 to +100 depending on plugin).
    # We will use direct SetParam for explicit values if known, or normalized. 
    # For VSTi:ReaSynth, Param 1 is Tuning. Let's use slight normalized offsets for detune.
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_det1, 1, 0.48) # Slightly flat
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_det2, 1, 0.52) # Slightly sharp
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_sub, 1, 0.0)   # Octave down
    
    # Filter
    filter_fx = RPR.RPR_TrackFX_AddByName(track, "JS: Moog 4-Pole Filter", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, filter_fx, 1, 0.54) # Resonance
    RPR.RPR_TrackFX_SetParamNormalized(track, filter_fx, 2, 0.32) # Drive
    
    # Spatial FX
    RPR.RPR_TrackFX_AddByName(track, "JS: Ping Pong Pan", False, -1)
    delay_fx = RPR.RPR_TrackFX_AddByName(track, "VST: ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, delay_fx, 0, 0.3) # Delay length approx
    reverb_fx = RPR.RPR_TrackFX_AddByName(track, "VST: ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, reverb_fx, 0, 0.95) # Room size large
    RPR.RPR_TrackFX_SetParamNormalized(track, reverb_fx, 1, 0.08) # Dampening low
    RPR.RPR_TrackFX_SetParamNormalized(track, reverb_fx, 4, 0.3)  # Wet mix low

    # === Step 4: Create MIDI Item & Legato Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Create a dynamic legato melody
    # Note durations are intentionally longer than the step gap to force overlapping (portamento)
    melody_pattern = [
        # (beat_start, beat_end, scale_degree)
        (0.0, 1.75, 0),  # Root, overlaps into next note heavily
        (1.5, 2.75, 2),  # Overlaps into next
        (2.5, 3.75, 4), 
        (3.5, 4.5,  3),
        (5.0, 5.75, 1),
        (5.5, 7.5,  0)   # Resolve to root
    ]
    
    # Repeat the 2-bar pattern across the specified total bars
    notes_added = 0
    quarter_note_len = 60.0 / bpm
    
    for bar in range(0, bars, 2):
        bar_offset = bar * beats_per_bar
        for start_beat, end_beat, degree in melody_pattern:
            # Time math
            start_time = (bar_offset + start_beat) * quarter_note_len
            end_time = (bar_offset + end_beat) * quarter_note_len
            
            # PPQ Math
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = scale_pitches[degree % len(scale_pitches)]
            # Add dynamic velocity for realism
            vel = min(127, velocity_base + (degree * 3))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_added += 1
            
            # === Step 5: Automate Filter Sweep (Auto-Wah Effect) ===
            # We programmatically create the envelope follower effect by adding an automation point 
            # at the start of every note, sweeping up, then decaying.
            # Param 0 is typically the Cutoff in Moog 4-Pole.
            env = RPR.RPR_GetFXEnvelope(track, filter_fx, 0, True)
            if env:
                # 0.2 = dark cutoff, 0.8 = bright cutoff
                RPR.RPR_InsertEnvelopePoint(env, start_time, 0.2, 0, 0, False, True)
                # Sweep up quickly (attack)
                RPR.RPR_InsertEnvelopePoint(env, start_time + 0.1, 0.8, 0, 0, False, True)
                # Decay down slowly
                RPR.RPR_InsertEnvelopePoint(env, end_time, 0.2, 0, 0, False, True)

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_Envelope_SortPoints(env) if env else None

    return f"Created '{track_name}' with {notes_added} legato notes (portamento) and 4-oscillator Detuned Synth FX over {bars} bars at {bpm} BPM."
