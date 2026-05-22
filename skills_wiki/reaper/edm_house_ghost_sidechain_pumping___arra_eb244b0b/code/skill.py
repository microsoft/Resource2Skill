def create_pattern(
    project_name: str = "EDM_House_Arrangement",
    track_name: str = "Pumping_Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM House setup featuring a Ghost Sidechain pumping effect.
    Generates a muted 4/4 trigger track, a receiving chord track, and 
    advanced routing to a ReaComp sidechain.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10], # Natural minor
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_note = NOTE_MAP.get(key.upper(), 0)
    octave_base = 48 # Octave 3/4 range

    # Chord progression: i, VI, III, VII (1st, 6th, 3rd, 7th scale degrees)
    progression_degrees = [0, 5, 2, 6] 

    def get_chord_pitches(degree_index):
        """Returns a basic triad for a given scale degree"""
        root_idx = progression_degrees[degree_index % len(progression_degrees)]
        third_idx = (root_idx + 2) % 7
        fifth_idx = (root_idx + 4) % 7
        
        # Calculate semitone offsets, handling octave wrap-around
        p1 = root_note + scale_intervals[root_idx] + (12 if root_idx < progression_degrees[0] else 0)
        p2 = root_note + scale_intervals[third_idx] + (12 if third_idx < root_idx else 0)
        p3 = root_note + scale_intervals[fifth_idx] + (12 if fifth_idx < third_idx else 0)
        return [octave_base + p1, octave_base + p2, octave_base + p3]

    def insert_midi_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(vel), False)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Calculate timing
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar

    # === Step 2: Create Tracks ===
    start_track_idx = RPR.RPR_CountTracks(0)
    
    # 2a. Create Ghost Kick (Sidechain Trigger)
    RPR.RPR_InsertTrackAtIndex(start_track_idx, True)
    ghost_track = RPR.RPR_GetTrack(0, start_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_track, "P_NAME", "Ghost Kick (Sidechain)", True)
    # Disable Master/Parent Send (muting it from the mix)
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0.0)

    # 2b. Create Chords Track
    RPR.RPR_InsertTrackAtIndex(start_track_idx + 1, True)
    chords_track = RPR.RPR_GetTrack(0, start_track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    # Upgrade to 4 channels to receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4.0)

    # === Step 3: Setup Sidechain Routing ===
    # Send from Ghost Kick to Chords Track
    send_idx = RPR.RPR_CreateTrackSend(ghost_track, chords_track)
    # Set destination channels to 3/4 (value 2 corresponds to 3/4 in REAPER API)
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_DSTCHAN", 2.0)
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "D_VOL", 1.0) # Unity gain send

    # === Step 4: Create MIDI Items & Notes ===
    # 4a. Ghost Kick Triggers
    ghost_item = RPR.RPR_AddMediaItemToTrack(ghost_track)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_LENGTH", bar_length * bars)
    ghost_take = RPR.RPR_AddTakeToMediaItem(ghost_item)

    for bar in range(bars):
        bar_start = bar * bar_length
        for beat in range(beats_per_bar):
            trigger_start = bar_start + (beat * beat_length)
            trigger_end = trigger_start + 0.15 # Short punchy trigger
            insert_midi_note(ghost_take, trigger_start, trigger_end, 36, 120) # C2 kick

    RPR.RPR_MIDI_Sort(ghost_take)

    # 4b. Sustained Chords
    chord_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", bar_length * bars)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    for bar in range(bars):
        bar_start = bar * bar_length
        chord_end = bar_start + bar_length
        pitches = get_chord_pitches(bar)
        for p in pitches:
            insert_midi_note(chord_take, bar_start, chord_end, p, velocity_base)

    RPR.RPR_MIDI_Sort(chord_take)

    # === Step 5: Add Instruments & FX ===
    # Synthesizer for chords
    synth_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, synth_fx, 1, 1.0) # Square wave volume up
    RPR.RPR_TrackFX_SetParam(chords_track, synth_fx, 2, 0.5) # Saw wave volume up
    
    # Sidechain Compressor
    comp_fx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    # Common parameter indices for ReaComp:
    # 0 = Thresh, 1 = Ratio, 2 = Attack, 3 = Release, 8 = Detector Input
    RPR.RPR_TrackFX_SetParam(chords_track, comp_fx, 0, -30.0) # Threshold: -30dB (heavy ducking)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_fx, 1, 5.0)   # Ratio: 5:1
    RPR.RPR_TrackFX_SetParam(chords_track, comp_fx, 2, 0.0)   # Attack: 0 ms
    RPR.RPR_TrackFX_SetParam(chords_track, comp_fx, 3, 150.0) # Release: 150 ms
    # Set Detector Input to Auxiliary L+R (Usually 1.0 sets to Aux if the param accepts floats or enums)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_fx, 8, 1.0) 
    
    return f"Created Ghost Sidechain setup: {bars} bars of pumping chords in {key} {scale} at {bpm} BPM."
