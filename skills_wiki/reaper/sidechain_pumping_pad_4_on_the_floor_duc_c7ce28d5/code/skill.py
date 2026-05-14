def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Sidechain Pumping Pad in the current REAPER project.
    Generates a 4-on-the-floor trigger track and a sustained chord track, 
    linked via ReaComp for rhythmic ducking.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 2: Create Target Track (Sustained Synth Pad) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    target_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(target_track, "P_NAME", f"{track_name}_Pad", True)
    
    # Enable 4 track channels to receive sidechain audio
    RPR.RPR_SetMediaTrackInfo_Value(target_track, "I_NCHAN", 4)

    target_item = RPR.RPR_AddMediaItemToTrack(target_track)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_LENGTH", item_length)
    target_take = RPR.RPR_AddTakeToMediaItem(target_item)
    RPR.RPR_SetMediaItemTakeInfo_Value(target_take, "B_ISMIDI", 1)

    # Calculate 7th chord from key/scale parameters
    root_note = NOTE_MAP.get(key.capitalize(), 0) + 60 # C4
    scale_notes = SCALES.get(scale.lower(), SCALES["minor"])
    chord_degrees = [0, 2, 4, 6] # 1st, 3rd, 5th, 7th scale degrees
    chord_intervals = [scale_notes[i % len(scale_notes)] + 12 * (i // len(scale_notes)) for i in chord_degrees]

    # Insert sustained chord spanning the entire item
    for interval in chord_intervals:
        insert_note(target_take, 0.0, item_length, root_note + interval, velocity_base - 10)
    RPR.RPR_MIDI_Sort(target_take)

    # Add Target FX (ReaSynth + ReaComp)
    RPR.RPR_TrackFX_AddByName(target_track, "ReaSynth", False, -1)
    comp_fx = RPR.RPR_TrackFX_AddByName(target_track, "ReaComp", False, -1)
    
    # Configure ReaComp for Sidechain Ducking
    num_params = RPR.RPR_TrackFX_GetNumParams(target_track, comp_fx)
    for i in range(num_params):
        _, _, _, name, _ = RPR.RPR_TrackFX_GetParamName(target_track, comp_fx, i, "", 256)
        name = name.lower()
        if "thresh" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, -20.0) # -20 dB Threshold
        elif "ratio" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 5.0)   # 5:1 Ratio
        elif "detector" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 1.0)   # 1.0 = Aux L+R Input
        elif "attack" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 5.0)   # 5 ms Attack
        elif "release" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 150.0) # 150 ms Release

    # === Step 3: Create Trigger Track (4-on-the-Floor Kick) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    trigger_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(trigger_track, "P_NAME", f"{track_name}_Trigger", True)

    trigger_item = RPR.RPR_AddMediaItemToTrack(trigger_track)
    RPR.RPR_SetMediaItemInfo_Value(trigger_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trigger_item, "D_LENGTH", item_length)
    trigger_take = RPR.RPR_AddTakeToMediaItem(trigger_item)
    RPR.RPR_SetMediaItemTakeInfo_Value(trigger_take, "B_ISMIDI", 1)

    # Insert 1/4 note rhythmic triggers
    kick_pitch = 36 # C2
    quarter_note_sec = 60.0 / bpm
    total_beats = bars * beats_per_bar
    for beat in range(int(total_beats)):
        start_sec = beat * quarter_note_sec
        end_sec = start_sec + (quarter_note_sec * 0.5) # 8th note duration
        insert_note(trigger_take, start_sec, end_sec, kick_pitch, velocity_base)
    RPR.RPR_MIDI_Sort(trigger_take)

    RPR.RPR_TrackFX_AddByName(trigger_track, "ReaSynth", False, -1)

    # === Step 4: Routing (The Sidechain Link) ===
    send_idx = RPR.RPR_CreateTrackSend(trigger_track, target_track)
    # Send Audio to Channels 3/4 on the target track (Value 2)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_DSTCHAN", 2) 
    # Send from Channels 1/2 on the trigger track (Value 0)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_SRCCHAN", 0) 
    # Disable MIDI send (Magic number 417792 / 0x66000 prevents the pad from playing the kick notes)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_MIDIFLAGS", 417792)

    return f"Created Sidechain Pumping setup (Tracks: Pad & Trigger) over {bars} bars in {key} {scale} at {bpm} BPM"
