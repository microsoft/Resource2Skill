def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "LowEnd_Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Low-End Anchor Gain Staging template in the current REAPER project.
    Sets up a Bus containing a Kick and a Bass, applying utility gain drops
    (-5dB and -7dB respectively) at the end of the chain as demonstrated in the tutorial.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Folder Topology (Bus -> Kick, Bass) ===
    track_idx = RPR.RPR_CountTracks(0)

    # 1. Parent Bus
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bus_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1)  # 1 = Start of folder

    # 2. Kick Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Kick_GainStaged", True)
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "I_FOLDERDEPTH", 0) # 0 = Normal track inside folder

    # 3. Bass Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", "Bass_GainStaged", True)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "I_FOLDERDEPTH", -1) # -1 = Last track in folder

    # === Step 3: Add Instruments & Gain Plugins ===
    
    # Kick Synth & Gain Drop
    kick_synth = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 1, 0.0)    # Tune down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 4, 0.05)   # Fast decay
    
    kick_gain = RPR.RPR_TrackFX_AddByName(kick_track, "JS: Volume Adjustment", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_gain, 0, -5.0)    # Target: -5 VU equivalent

    # Bass Synth & Gain Drop
    bass_synth = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 4, 0.5)    # Longer decay
    
    bass_gain = RPR.RPR_TrackFX_AddByName(bass_track, "JS: Volume Adjustment", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_gain, 0, -7.0)    # Target: -7 VU equivalent

    # === Step 4: Generate Auditable MIDI Data ===
    bar_len_sec = (60.0 / bpm) * 4
    item_len_sec = bar_len_sec * bars

    # Generate Kick MIDI (4-on-the-floor)
    kick_item = RPR.RPR_CreateNewMIDIItemInProj(kick_track, 0.0, item_len_sec, False)
    kick_take = RPR.RPR_GetActiveTake(kick_item)
    
    for bar in range(bars):
        for beat in range(4):
            start_t = bar * bar_len_sec + beat * (60.0 / bpm)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_t)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_t + 0.1)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
    RPR.RPR_MIDI_Sort(kick_take)

    # Calculate Bass Note
    NOTE_MAP = {"C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
                "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
                "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35}
    bass_pitch = NOTE_MAP.get(key.capitalize(), 24)

    # Generate Bass MIDI (Sustained notes to check summing level)
    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, 0.0, item_len_sec, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)
    
    for bar in range(bars):
        start_t = bar * bar_len_sec
        end_t = start_t + bar_len_sec - 0.1
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_t)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_t)
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created Low-End Bus with Kick (anchored to -5.0 dB) and Bass (anchored to -7.0 dB) over {bars} bars at {bpm} BPM in {key} {scale}."
