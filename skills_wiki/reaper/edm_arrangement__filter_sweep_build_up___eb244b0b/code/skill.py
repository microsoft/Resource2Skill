def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 128,
    key: str = "E",
    scale: str = "minor",
    bars: int = 8,  # First 4 bars = Buildup, Last 4 bars = Drop
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM arrangement featuring a filter-sweep buildup, a sidechain-pumped 
    chord progression, and a defined Drop section with a lead melody.
    """
    import reaper_python as RPR

    # === Music Theory & Scales ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    root_val = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 4)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Pre-compute scale pitches spanning multiple octaves
    scale_pitches = []
    for oct in range(2, 6):
        for interval in scale_intervals:
            scale_pitches.append(root_val + interval + (oct * 12))

    # === Step 1: Initialize Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    bar_sec = (60.0 / bpm) * 4
    buildup_duration = bar_sec * (bars // 2) # First half
    total_duration = bar_sec * bars

    track_count = RPR.RPR_CountTracks(0)

    # === Step 2: Create SC Kick Trigger (Muted) ===
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    sc_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(sc_track, "P_NAME", "SC Trigger (Muted)", True)
    RPR.RPR_SetMediaTrackInfo_Value(sc_track, "B_MAINSEND", 0) # Mute from master
    
    # Add Kick MIDI Item
    sc_item = RPR.RPR_AddMediaItemToTrack(sc_track)
    RPR.RPR_SetMediaItemInfo_Value(sc_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(sc_item, "D_LENGTH", total_duration)
    sc_take = RPR.RPR_AddTakeToMediaItem(sc_item)
    
    # 4-on-the-floor kick pattern
    kick_pitch = 36 # C2
    for beat in range(bars * 4):
        pos = beat * (60.0 / bpm)
        RPR.RPR_MIDI_InsertNote(sc_take, False, False, 
                                pos, pos + 0.1, 
                                0, kick_pitch, 110, False)

    # === Step 3: Create Synth Chords (Target) ===
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    chord_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", "Synth Chords (Pump & Sweep)", True)
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "I_NCHAN", 4) # Enable 4 channels for sidechain
    
    # Route SC Trigger (1/2) to Chord Track (3/4)
    send_idx = RPR.RPR_CreateTrackSend(sc_track, chord_track)
    RPR.RPR_SetTrackSendInfo_Value(sc_track, 0, send_idx, "I_DSTCHAN", 2) # 2 = Channels 3/4
    
    # Add ReaComp for Sidechain Pumping
    comp_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, comp_idx, 0, -25.0) # Threshold
    RPR.RPR_TrackFX_SetParam(chord_track, comp_idx, 1, 6.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(chord_track, comp_idx, 2, 2.0)   # Attack ms
    RPR.RPR_TrackFX_SetParam(chord_track, comp_idx, 3, 100.0) # Release ms
    RPR.RPR_TrackFX_SetParam(chord_track, comp_idx, 12, 1.0)  # Detector Input: Aux L+R (Ch 3/4)

    # Add ReaEQ for Buildup Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, eq_idx, 11, 0.0) # Band 4 Type: Low Pass (usually type index 0-9 depending on layout, safe default parametering below)
    # Band 4 Frequency is parameter 9 (0-indexed: (Band_num - 1) * 3)
    
    # Automate EQ Band 4 Frequency
    env = RPR.RPR_GetFXEnvelope(chord_track, eq_idx, 9, True)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 300.0, 0, 0.0, False, True) # Start muffled
    RPR.RPR_InsertEnvelopePoint(env, buildup_duration, 15000.0, 0, 0.0, False, True) # Open up at the drop
    RPR.RPR_Envelope_SortPoints(env)

    # Add Chord MIDI Item (i - VI - III - VII progression)
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_duration)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    # Progression indices in scale: i=0, VI=5, III=2, VII=6
    progression = [0, 5, 2, 6] 
    
    for i in range(bars):
        chord_root_idx = progression[i % len(progression)]
        # Offset to octave 3 (middle of our precomputed array)
        start_idx = 7 + chord_root_idx
        notes = [scale_pitches[start_idx], scale_pitches[start_idx+2], scale_pitches[start_idx+4]]
        
        start_time = i * bar_sec
        end_time = start_time + bar_sec
        for note in notes:
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, 
                                    start_time, end_time, 
                                    0, note, velocity_base - 10, False)

    # === Step 4: Create Lead Melody (Drop Only) ===
    # Demonstrates arrangement contrast
    RPR.RPR_InsertTrackAtIndex(track_count + 2, True)
    lead_track = RPR.RPR_GetTrack(0, track_count + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", "Drop Lead Melody", True)
    
    # Melody item only exists during the Drop
    lead_item = RPR.RPR_AddMediaItemToTrack(lead_track)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_POSITION", buildup_duration)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_LENGTH", total_duration - buildup_duration)
    lead_take = RPR.RPR_AddTakeToMediaItem(lead_item)
    
    # Simple rhythmic motif on the root and 5th
    root_note = scale_pitches[14] # Root, Octave 4
    fifth_note = scale_pitches[18] # 5th, Octave 4
    
    for i in range(bars // 2):
        base_time = buildup_duration + (i * bar_sec)
        eighth = (60.0 / bpm) / 2
        
        # Syncopated rhythm: 1, 2-and, 4
        notes_def = [
            (0.0, eighth * 1.5, root_note),
            (eighth * 2.5, eighth * 3.5, fifth_note),
            (eighth * 6.0, eighth * 7.5, root_note + 12) # Octave up
        ]
        
        for start_offset, end_offset, pitch in notes_def:
            RPR.RPR_MIDI_InsertNote(lead_take, False, False, 
                                    base_time + start_offset, base_time + end_offset, 
                                    0, pitch, velocity_base, False)
                                    
    RPR.RPR_UpdateArrange()

    return f"Created EDM Arrangement with Sidechain pumping, EQ Filter buildup (4 bars), and Drop Melody (4 bars) in {key} {scale} at {bpm} BPM."
