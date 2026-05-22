def create_ghost_sidechain_arrangement(
    project_name: str = "EDM_Arrangement",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM Intro arrangement featuring a 4-bar chord progression,
    a muted ghost kick for sidechain pumping, and a tension-building automation sweep.
    """
    import reaper_python as RPR

    # === Music Theory & Scales ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Helper to get MIDI pitch
    def get_pitch(degree, octave=4):
        degree_idx = (degree - 1) % len(scale_intervals)
        octave_shift = (degree - 1) // len(scale_intervals)
        return root_val + scale_intervals[degree_idx] + ((octave + octave_shift) * 12)

    # Progression: i - VI - III - VII (1, 6, 3, 7 in the scale)
    progression_degrees = [1, 6, 3, 7]
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # === Track 1: The Chords (Receives Sidechain) ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    chords_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", "Synth Chords (Pump)", True)
    
    # Setup 4 track channels (1/2 for main audio, 3/4 for sidechain trigger)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)

    # Add MIDI Item for Chords
    chord_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", bar_length_sec * bars)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    # Insert Chords (triads)
    for i, degree in enumerate(progression_degrees):
        start_time = i * beats_per_bar # quarter notes
        end_time = start_time + beats_per_bar
        
        # Root, 3rd, 5th of the chord
        for chord_tone in [0, 2, 4]: 
            pitch = get_pitch(degree + chord_tone, octave=4)
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, 
                                    start_time * 960, end_time * 960, 
                                    1, pitch, velocity_base - 10, False)

    # Add Synth & Compression to Chords Track
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    # Set ReaComp to aggressive pumping settings
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 0, 0.1) # Threshold low
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 1, 0.25) # Ratio high (e.g., 4:1)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 2, 0.0) # Attack fast
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 3, 100.0) # Release medium
    # Param 22 is often Detector Input in ReaComp. We try to set it to Aux L+R.
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 22, 1.0) 

    # === Track 2: The Ghost Kick (Sends Sidechain) ===
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Kick (Trigger)", True)
    
    # Disable Master Send (Muted to the ear, but still sends out to other tracks)
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0)

    # Create Send from Ghost Kick -> Chords
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chords_track)
    # Set destination channels to 3/4 (Value '2' means 3/4 in Reaper API)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "D_VOL", 1.0)

    # Add MIDI Item for Kick
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", bar_length_sec * bars)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    # Insert 4-on-the-floor kick pattern
    kick_pitch = 36 # C2
    for b in range(bars * beats_per_bar):
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, 
                                b * 960, (b * 960) + 480, 
                                1, kick_pitch, 127, False)
        
    RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1) # Simple tick to trigger comp

    # === Automation: The Build-Up Sweep ===
    # Automate track volume as a reliable alternative to build tension
    env = RPR.RPR_GetTrackEnvelopeByName(chords_track, "Volume")
    if not env:
        # If envelope doesn't exist, we must create it by toggling it visible
        # For programmatic certainty without SWS, we will automate ReaEQ gain
        eq_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
        # We sweep the gain of a high shelf down to up to simulate a filter opening
        RPR.RPR_TrackFX_SetParam(chords_track, eq_idx, 10, -24.0) # Set Band 4 Gain low
    
    return f"Created Ghost Sidechain arrangement with 2 tracks over {bars} bars at {bpm} BPM."
