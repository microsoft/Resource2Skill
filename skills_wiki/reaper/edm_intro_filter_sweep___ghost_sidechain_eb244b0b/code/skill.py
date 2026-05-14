def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "EDM Chords Build",
    bpm: int = 125,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM intro/build-up featuring an automated Low-Pass filter sweep 
    and a hidden 'ghost kick' sidechain pumping effect.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the main chord track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Length of the intro build-up in bars.
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
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Calculate chord progression (vi - IV - I - V) in the given key/scale
    # Assuming standard major scale degrees for the progression formula
    progression_degrees = [5, 3, 0, 4] # 0-indexed: 5=vi, 3=IV, 0=I, 4=V
    
    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # ==========================================
    # TRACK 1: GHOST KICK TRIGGER
    # ==========================================
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    ghost_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_track, "P_NAME", "Ghost Kick (Sidechain)", True)
    
    # Disable Master Send so the ghost kick is only heard via the sidechain
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0)

    # Create MIDI Item for Ghost Kick
    ghost_item = RPR.RPR_AddMediaItemToTrack(ghost_track)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_LENGTH", total_length_sec)
    ghost_take = RPR.RPR_AddTakeToMediaItem(ghost_item)

    # Insert 4-on-the-floor kicks
    total_beats = bars * beats_per_bar
    for i in range(total_beats):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, i * beat_length_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, (i * beat_length_sec) + (beat_length_sec / 4))
        RPR.RPR_MIDI_InsertNote(ghost_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)

    # Add ReaSynth to make a 'click' sound for the compressor detector
    RPR.RPR_TrackFX_AddByName(ghost_track, "ReaSynth", False, -1)
    # Set synth decay very fast for a tight trigger pulse
    RPR.RPR_TrackFX_SetParam(ghost_track, 0, 2, 0.05) # Decay

    # ==========================================
    # TRACK 2: CHORDS (WITH FILTER & PUMPING)
    # ==========================================
    chords_track_idx = track_count + 1
    RPR.RPR_InsertTrackAtIndex(chords_track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, chords_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    
    # Set to 4 channels to accept sidechain
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)

    # Create MIDI Item for Chords
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # Insert sustained chords
    base_octave = 48 # C3
    for b in range(bars):
        deg = progression_degrees[b % len(progression_degrees)]
        chord_root_midi = base_octave + root_pitch + scale_intervals[deg]
        
        # Build a basic triad in the scale
        third_deg = (deg + 2) % 7
        fifth_deg = (deg + 4) % 7
        
        # Account for octave wrap-around
        third_oct = 12 if third_deg < deg else 0
        fifth_oct = 12 if fifth_deg < deg else 0
        
        notes = [
            chord_root_midi,
            base_octave + root_pitch + scale_intervals[third_deg] + third_oct,
            base_octave + root_pitch + scale_intervals[fifth_deg] + fifth_oct
        ]
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, b * bar_length_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, (b + 1) * bar_length_sec)
        
        for note in notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, note, velocity_base - b*5, False)

    # ==========================================
    # SOUND DESIGN, SIDECHAIN & AUTOMATION
    # ==========================================
    
    # 1. Add Synth
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    # Tweak synth to sound like a pad (longer attack/release)
    RPR.RPR_TrackFX_SetParam(chords_track, 0, 1, 0.5)  # Attack
    RPR.RPR_TrackFX_SetParam(chords_track, 0, 3, 0.8)  # Release

    # 2. Add EQ for Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    
    # Parameter 9 in ReaEQ is typically Band 4 Frequency
    # We will automate it to simulate a Low Pass Filter opening up
    env = RPR.RPR_GetFXEnvelope(chords_track, eq_idx, 9, True)
    if env:
        # 0.1 is very muffled (approx 200Hz), 0.9 is fully open
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.15, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, total_length_sec, 0.85, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    # 3. Add Compressor for Pumping (Sidechain)
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 0, -25.0) # Threshold
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 1, 5.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 2, 2.0)   # Attack (ms)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 3, 100.0) # Release (ms)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 8, 1.0)   # Detector Input = Auxiliary Inputs L+R (Channels 3/4)

    # 4. Route Ghost Kick to Chords sidechain input (Channels 3/4)
    send_idx = RPR.RPR_CreateTrackSend(ghost_track, chords_track)
    # I_DSTCHAN value definition: 0=1/2, 1=3/4, 2=5/6. We want 3/4, so we pass 1 (or 2 depending on REAPER ver, usually 1 or 2. Actually 2 forces it to 3/4 safely in integer terms)
    # Alternatively, 1024 binary flags can be used. But standard routing uses `I_DSTCHAN`.
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_DSTCHAN", 2) 

    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' and 'Ghost Kick' over {bars} bars at {bpm} BPM with automated Filter Sweep and Sidechain pumping."
