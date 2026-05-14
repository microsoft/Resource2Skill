def create_pattern(
    project_name: str = "Dubstep Drop",
    track_name: str = "Drop",
    bpm: int = 150,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 120,
    **kwargs,
) -> str:
    """
    Create a Dubstep/Riddim Call-and-Response Drop with LFO volume wobbles.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Root MIDI in Octave 1 for deep sub bass
    root_midi = 24 + NOTE_MAP.get(key.upper(), NOTE_MAP["C"])

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Helper to create track, item, and MIDI notes ---
    def create_track_with_midi(name, notes_list, root_pitch):
        # Create Track
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create Item
        beats_per_bar = 4
        item_len_sec = (60.0 / bpm) * beats_per_bar * bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Insert Notes
        for n in notes_list:
            start_time = (60.0 / bpm) * n["start_beat"]
            end_time = start_time + (60.0 / bpm) * n["duration_beats"]
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = n.get("pitch", root_pitch + n.get("pitch_offset", 0))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, n["velocity"], False)
            
        RPR.RPR_MIDI_Sort(take)
        return track

    # ==========================================
    # 1. DRUMS (Half-Time Groove)
    # ==========================================
    drums = []
    for b in range(bars):
        # Kick (1.0 and 2.5)
        drums.append({"pitch": 36, "start_beat": b * 4 + 0.0, "duration_beats": 0.25, "velocity": 127})
        if b % 2 == 0: # Extra syncopated kick on even bars
            drums.append({"pitch": 36, "start_beat": b * 4 + 1.5, "duration_beats": 0.25, "velocity": 127})
            
        # Main Snare/Clap on beat 3 (2.0 in 0-indexed beats)
        drums.append({"pitch": 38, "start_beat": b * 4 + 2.0, "duration_beats": 0.25, "velocity": 127})
        # Flam element (slightly early snap to give width, as discussed in video)
        drums.append({"pitch": 39, "start_beat": b * 4 + 1.95, "duration_beats": 0.1, "velocity": 90})
        
        # Open hat on upbeat
        drums.append({"pitch": 46, "start_beat": b * 4 + 2.5, "duration_beats": 0.25, "velocity": 100})
        
        # 8th note hi-hats
        for i in range(8):
            pos = i * 0.5
            if pos not in [0.0, 2.0]: # Skip where kick and snare hit
                drums.append({"pitch": 42, "start_beat": b * 4 + pos, "duration_beats": 0.1, "velocity": 85})

    create_track_with_midi(f"{track_name} Drums (MIDI)", drums, 0)

    # ==========================================
    # 2. MAIN BASS (Sustained + LFO Automation)
    # ==========================================
    main_bass = []
    for b in range(bars):
        if b % 2 == 0:
            main_bass.append({"start_beat": b * 4.0, "duration_beats": 4.0, "velocity": velocity_base})
        else:
            # Leave the 4th beat empty for the response growl
            main_bass.append({"start_beat": b * 4.0, "duration_beats": 3.0, "velocity": velocity_base})

    main_track = create_track_with_midi(f"{track_name} Main Wobble", main_bass, root_midi)
    
    # Sound Design: Saw/Square blend -> Distortion -> LPF
    fx_synth = RPR.RPR_TrackFX_AddByName(main_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(main_track, fx_synth, 6, 0.6) # Square mix
    RPR.RPR_TrackFX_SetParam(main_track, fx_synth, 7, 0.6) # Saw mix
    
    RPR.RPR_TrackFX_AddByName(main_track, "JS: Distortion", False, -1)
    
    fx_eq = RPR.RPR_TrackFX_AddByName(main_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(main_track, fx_eq, 10, -18.0) # Lower high-shelf to reduce digital fizz

    # LFOTool emulation via Volume Envelope
    RPR.RPR_Main_OnCommand(40297, 0) # Unselect all tracks
    RPR.RPR_SetMediaTrackInfo_Value(main_track, "I_SELECTED", 1)
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    
    env = RPR.RPR_GetTrackEnvelopeByName(main_track, "Volume")
    if env:
        eighth_len = (60.0 / bpm) * 0.5
        for i in range(bars * 8):
            b = i // 8
            eighth_in_bar = i % 8
            
            # If we are in the gap designated for the response bass, flatline volume to 0
            if b % 2 != 0 and eighth_in_bar >= 6:
                RPR.RPR_InsertEnvelopePoint(env, i * eighth_len, 0.0, 0, 0, False, True)
                continue
                
            t0 = i * eighth_len
            t1 = t0 + 0.15 * eighth_len # Fast attack
            t2 = t0 + 0.85 * eighth_len # Slower decay
            
            # Recreate 1/8 note "sawtooth down" rhythmic wobble pumping
            RPR.RPR_InsertEnvelopePoint(env, t0, 0.0, 0, 0, False, True)  # Min volume (ducked)
            RPR.RPR_InsertEnvelopePoint(env, t1, 1.0, 0, 0, False, True)  # Peak volume
            RPR.RPR_InsertEnvelopePoint(env, t2, 0.1, 0, 0, False, True)  # Decay out
            
        RPR.RPR_Envelope_SortPoints(env)

    # ==========================================
    # 3. RESPONSE BASS (Staccato Growl)
    # ==========================================
    response_bass = []
    for b in range(bars):
        if b % 2 != 0: # Plays only in the gaps of odd bars
            # Jumps 2 Octaves up (+24) and then a minor 3rd (+27)
            response_bass.append({"start_beat": b * 4 + 3.0, "duration_beats": 0.25, "velocity": 127, "pitch_offset": 24})
            response_bass.append({"start_beat": b * 4 + 3.5, "duration_beats": 0.25, "velocity": 127, "pitch_offset": 27})

    resp_track = create_track_with_midi(f"{track_name} Response Growl", response_bass, root_midi)
    
    # Sound Design: Square-heavy -> Distortion -> Chorus -> Reverb
    fx_synth2 = RPR.RPR_TrackFX_AddByName(resp_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(resp_track, fx_synth2, 6, 0.9) # Heavy Square
    RPR.RPR_TrackFX_SetParam(resp_track, fx_synth2, 7, 0.2) # Light Saw
    
    RPR.RPR_TrackFX_AddByName(resp_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_AddByName(resp_track, "JS: Chorus", False, -1)
    
    fx_verb = RPR.RPR_TrackFX_AddByName(resp_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(resp_track, fx_verb, 0, 0.15) # Wet
    RPR.RPR_TrackFX_SetParam(resp_track, fx_verb, 1, 0.85) # Dry
    RPR.RPR_TrackFX_SetParam(resp_track, fx_verb, 2, 0.20) # Tight Room Size

    return f"Created Dubstep Drop with LFO automation over {bars} bars at {bpm} BPM in {key} {scale}."
