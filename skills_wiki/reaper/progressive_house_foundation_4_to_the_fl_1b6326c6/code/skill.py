def create_pattern(
    project_name: str = "ProgressiveHouse",
    track_name: str = "ProgHouse_Group",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Progressive House Foundation with 4-to-the-floor drums,
    8th note chords/bass, and active sidechain pumping via ReaComp.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generate a pool of diatonic notes across a few octaves
    diatonic_pool = []
    for oct in range(2, 7):
        for interval in scale_intervals:
            diatonic_pool.append((oct * 12) + root_val + interval)

    # Progression: i - VI - III - VII
    progression_degrees = [0, 5, 2, 4]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4
    total_length = bar_len * bars

    # Helper function to create tracks
    def create_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        return trk, idx

    # Helper function to add MIDI notes
    def add_note(take, start_time, end_time, pitch, vel, chan=0):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)

    # === Step 2: Create Drum Track (Trigger) ===
    drum_track, drum_idx = create_track(f"{track_name}_Drums")
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Populate Drums (4-to-the-floor kick + offbeat hats)
    kick_pitch = 36 # General MIDI Kick
    hat_pitch = 42  # General MIDI Closed Hat
    
    for b in range(bars):
        for beat in range(4):
            # Kick on downbeats
            t_kick_start = (b * bar_len) + (beat * beat_len)
            t_kick_end = t_kick_start + (beat_len * 0.5)
            add_note(drum_take, t_kick_start, t_kick_end, kick_pitch, 110, 9) # Chan 10 (0-indexed 9)
            
            # Hat on offbeats ("ands")
            t_hat_start = t_kick_start + (beat_len * 0.5)
            t_hat_end = t_hat_start + (beat_len * 0.25)
            add_note(drum_take, t_hat_start, t_hat_end, hat_pitch, 80, 9)

    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: Create Synth Chords & Bass Tracks ===
    chords_track, chords_idx = create_track(f"{track_name}_Chords")
    bass_track, bass_idx = create_track(f"{track_name}_Bass")

    # Add Synths
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Tune bass down
    RPR.RPR_TrackFX_SetParamNormalized(bass_track, 0, 0, 0.2) # lower tuning

    # === Step 4: Configure Track Channels and Sidechain Routing ===
    # Expand channels to 4 on receiving tracks
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "I_NCHAN", 4)

    # Create Sends: Drums -> Chords/Bass (Audio only, dest channel 3/4)
    send_chords = RPR.RPR_CreateTrackSend(drum_track, chords_track)
    RPR.RPR_SetTrackSendInfo_Value(drum_track, 0, send_chords, "I_SRCCHAN", 0) # Source 1/2
    RPR.RPR_SetTrackSendInfo_Value(drum_track, 0, send_chords, "I_DSTCHAN", 2) # Dest 3/4 (value 2 = channel 3)
    RPR.RPR_SetTrackSendInfo_Value(drum_track, 0, send_chords, "I_MIDIFLAGS", 31) # Disable MIDI send

    send_bass = RPR.RPR_CreateTrackSend(drum_track, bass_track)
    RPR.RPR_SetTrackSendInfo_Value(drum_track, 0, send_bass, "I_SRCCHAN", 0)
    RPR.RPR_SetTrackSendInfo_Value(drum_track, 0, send_bass, "I_DSTCHAN", 2)
    RPR.RPR_SetTrackSendInfo_Value(drum_track, 0, send_bass, "I_MIDIFLAGS", 31)

    # Add ReaComp to receive sidechain
    for trk in [chords_track, bass_track]:
        comp_idx = RPR.RPR_TrackFX_AddByName(trk, "ReaComp", False, -1)
        # Normalized Parameters for ReaComp to create pumping:
        RPR.RPR_TrackFX_SetParamNormalized(trk, comp_idx, 0, 0.3)  # Threshold (lowered to catch kick)
        RPR.RPR_TrackFX_SetParamNormalized(trk, comp_idx, 1, 0.6)  # Ratio (~5:1)
        RPR.RPR_TrackFX_SetParamNormalized(trk, comp_idx, 2, 0.0)  # Attack (instant)
        RPR.RPR_TrackFX_SetParamNormalized(trk, comp_idx, 3, 0.05) # Release (~50-100ms for quick pump)
        # Set Detector Input to Auxiliary (channels 3/4). Param 11 value 0.5+ maps to Aux.
        RPR.RPR_TrackFX_SetParamNormalized(trk, comp_idx, 11, 1.0) 

    # === Step 5: Generate Harmonic MIDI ===
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    
    for itm in [chords_item, bass_item]:
        RPR.RPR_SetMediaItemInfo_Value(itm, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(itm, "D_LENGTH", total_length)
        
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    note_length = (beat_len / 2.0) * 0.85 # 8th notes with slight staccato gap

    for b in range(bars):
        degree = progression_degrees[b % len(progression_degrees)]
        
        # Build Triad based on degree (octave 4 for chords, octave 2 for bass)
        root_idx = degree + 14 # roughly C4 range in our generated pool
        chord_notes = [diatonic_pool[root_idx], diatonic_pool[root_idx + 2], diatonic_pool[root_idx + 4]]
        bass_note = diatonic_pool[root_idx - 14] # Down 2 octaves

        # Pulse 8th notes for the whole bar
        for eighth in range(8):
            start_t = (b * bar_len) + (eighth * (beat_len / 2.0))
            end_t = start_t + note_length
            
            # Insert Bass
            add_note(bass_take, start_t, end_t, bass_note, velocity_base)
            # Insert Chords
            for note in chord_notes:
                add_note(chords_take, start_t, end_t, note, velocity_base - 10)

    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(bass_take)
    
    # Lower base track volumes slightly to prevent clipping from synths
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "D_VOL", 0.4)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "D_VOL", 0.5)

    return f"Created Progressive House Foundation: Drums, sidechain-ducked Chords & Bass ({bars} bars, {bpm} BPM, {key} {scale})"
