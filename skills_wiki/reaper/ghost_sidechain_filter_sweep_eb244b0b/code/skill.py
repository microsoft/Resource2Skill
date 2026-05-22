def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pump Chords",
    bpm: int = 125,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Ghost Sidechain Filter Sweep (EDM Build-up Chords) in REAPER.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    if scale not in SCALES:
        scale = "minor"
    
    root_pitch = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 9) + 48 # Octave 4
    scale_intervals = SCALES[scale]

    # Helper to build diatonic triads
    def get_diatonic_chord(degree):
        chord_notes = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            idx = degree + i
            octave_shift = idx // len(scale_intervals)
            note_idx = idx % len(scale_intervals)
            pitch = root_pitch + scale_intervals[note_idx] + (octave_shift * 12)
            chord_notes.append(pitch)
        return chord_notes

    # Progression: i - VI - III - VII (0, 5, 2, 6 in 0-indexed scale degrees)
    progression = [0, 5, 2, 6]

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    # === TRACK 1: GHOST KICK TRIGGER ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    ghost_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_track, "P_NAME", "Ghost SC Trigger", True)
    
    # Disable Master/Parent send so the kick is silent but still available for routing
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0.0)

    # Ghost Kick MIDI Item
    k_item = RPR.RPR_AddMediaItemToTrack(ghost_track)
    RPR.RPR_SetMediaItemInfo_Value(k_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(k_item, "D_LENGTH", total_length)
    k_take = RPR.RPR_AddTakeToMediaItem(k_item)
    
    # Add 4-on-the-floor quarter notes
    quarter_note_len = 60.0 / bpm
    q_ticks = RPR.RPR_MIDI_GetPPQPosFromProjTime(k_take, quarter_note_len)
    for b in range(bars):
        for q in range(4):
            start_tick = (b * 4 + q) * q_ticks
            end_tick = start_tick + (q_ticks * 0.5) # 8th note duration
            RPR.RPR_MIDI_InsertNote(k_take, False, False, start_tick, end_tick, 0, 36, 127, False)

    # Add quick decay synth for the kick transient
    fx_kick = RPR.RPR_TrackFX_AddByName(ghost_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(ghost_track, fx_kick, 3, 0.05) # Fast Release
    RPR.RPR_TrackFX_SetParam(ghost_track, fx_kick, 4, 0.0)  # Sustain 0

    # === TRACK 2: SYNTH CHORDS ===
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    synth_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", track_name, True)
    
    # Synth Chords MIDI Item
    s_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(s_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(s_item, "D_LENGTH", total_length)
    s_take = RPR.RPR_AddTakeToMediaItem(s_item)

    bar_ticks = RPR.RPR_MIDI_GetPPQPosFromProjTime(s_take, bar_length_sec)
    for i, degree in enumerate(progression):
        chord_notes = get_diatonic_chord(degree)
        start_tick = i * bar_ticks
        end_tick = start_tick + bar_ticks - 10 # Slight gap
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(s_take, False, False, start_tick, end_tick, 0, note, velocity_base, False)

    # Make it a sawtooth pad
    fx_synth = RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(synth_track, fx_synth, 1, 1.0) # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(synth_track, fx_synth, 2, 0.5) # Attack
    RPR.RPR_TrackFX_SetParam(synth_track, fx_synth, 3, 0.5) # Release

    # JS Filter for Automation
    fx_filter = RPR.RPR_TrackFX_AddByName(synth_track, "JS: filter/resonantlowpass", False, -1)
    
    # ReaComp for Sidechain Pumping
    fx_comp = RPR.RPR_TrackFX_AddByName(synth_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(synth_track, fx_comp, 0, -30.0) # Threshold low
    RPR.RPR_TrackFX_SetParam(synth_track, fx_comp, 1, 8.0)   # Ratio high
    RPR.RPR_TrackFX_SetParam(synth_track, fx_comp, 2, 2.0)   # Fast Attack (ms)
    RPR.RPR_TrackFX_SetParam(synth_track, fx_comp, 3, 150.0) # Medium Release (ms)
    RPR.RPR_TrackFX_SetParam(synth_track, fx_comp, 8, 1.0)   # Detector Input = Aux L+R (Value 1)

    # === ROUTING: GHOST -> SYNTH (SIDECHAIN) ===
    # Set synth track to have 4 channels so it can receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_NCHAN", 4)
    send_idx = RPR.RPR_CreateTrackSend(ghost_track, synth_track)
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_SRCCHAN", 0) # Source 1/2
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_DSTCHAN", 2) # Dest 3/4
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_SENDMODE", 3) # Pre-Fader (so track mute doesn't kill send)

    # === AUTOMATION: FILTER SWEEP ===
    # Automate JS Filter frequency (Param 0) from low to high
    env = RPR.RPR_GetFXEnvelope(synth_track, fx_filter, 0, True)
    # JS: resonantlowpass freq is normalized 0 to 1
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 0, 0.0, False, True) # Start muffled
    RPR.RPR_InsertEnvelopePoint(env, total_length, 0.9, 0, 0.0, False, True) # End open
    RPR.RPR_Envelope_Sort(env)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' pumping progression and ghost trigger over {bars} bars at {bpm} BPM."
