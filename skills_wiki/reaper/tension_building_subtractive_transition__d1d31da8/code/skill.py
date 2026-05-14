def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Transition Build",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Tension-Building Subtractive Transition' in the current REAPER project.
    Generates an 8-bar arrangement consisting of a filtered build-up with sparse 
    drums, a sudden drop gap, and a full-frequency heavy chorus hit.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars (forces at least 8 to demonstrate the transition).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # Enforce minimum 8 bars for the Verse -> Chorus transition to function
    bars = max(bars, 8)

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    # === Step 2: Create Tracks ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Track A: Chords / Pad
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name} - Pad Riser", True)
    
    # Track B: Drums
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    drums_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_track, "P_NAME", f"{track_name} - Subtractive Drums", True)

    # === Step 3: Sound Design via FX ===
    # Pad Synth
    pad_synth = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, pad_synth, 1, 0.4) # Attack (slow swell)
    RPR.RPR_TrackFX_SetParam(chords_track, pad_synth, 2, 1.0) # Decay
    RPR.RPR_TrackFX_SetParam(chords_track, pad_synth, 3, 0.8) # Sustain
    
    # Pad Filter (For the drop sweep)
    fx_lp = RPR.RPR_TrackFX_AddByName(chords_track, "JS: Filters/resonantlowpass", False, -1)
    
    # Drum Percussion Synth (Short, plucky settings to simulate drums)
    drum_synth = RPR.RPR_TrackFX_AddByName(drums_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(drums_track, drum_synth, 1, 0.0) # Attack (instant)
    RPR.RPR_TrackFX_SetParam(drums_track, drum_synth, 2, 0.1) # Decay (very fast)
    RPR.RPR_TrackFX_SetParam(drums_track, drum_synth, 3, 0.0) # Sustain (none)

    # === Step 4: Chords & Filter Automation ===
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", bar_len * bars)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)
    
    root_val = NOTE_MAP.get(key, 0) + 48 # Base Octave
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_note(degree):
        oct_shift = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_val + scale_intervals[idx] + (oct_shift * 12)
        
    # Standard 4-bar progression loop (i, VI, III, VII)
    chord_degrees = [[0, 2, 4], [5, 7, 9], [2, 4, 6], [6, 8, 10]]
    
    for bar in range(bars):
        c_idx = bar % 4
        start_time = bar * bar_len
        end_time = start_time + bar_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        for deg in chord_degrees[c_idx]:
            pitch = get_note(deg)
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, 70, True)
            
    RPR.RPR_MIDI_Sort(chords_take)
    
    # Automate the Filter Cutoff (Param 0 of JS: resonantlowpass)
    env = RPR.RPR_GetFXEnvelope(chords_track, fx_lp, 0, True)
    if env:
        # Shapes: 0=Linear, 2=Slow start/end (parabolic swell)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.15, 2, 0.0, False, True)               # Muffled at start of verse
        RPR.RPR_InsertEnvelopePoint(env, bar_len * 3.0, 0.35, 2, 0.0, False, True)     # Start sweeping during 2nd half of verse
        RPR.RPR_InsertEnvelopePoint(env, bar_len * 4.0 - 0.05, 1.0, 0, 0.0, False, True) # Snap fully open immediately before drop
        RPR.RPR_InsertEnvelopePoint(env, bar_len * 4.0, 1.0, 0, 0.0, False, True)      # Keep open for chorus
        RPR.RPR_Envelope_SortPoints(env)

    # === Step 5: Subtractive Drum Arrangement ===
    drums_item = RPR.RPR_AddMediaItemToTrack(drums_track)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_LENGTH", bar_len * bars)
    drums_take = RPR.RPR_AddTakeToMediaItem(drums_item)
    
    for bar in range(bars):
        for beat in range(4):
            # THE CORE SKILL: The Drop Gap. Silence drums completely right before the Chorus.
            # Bar index 3 is the last bar of the verse.
            if bar == 3 and beat >= 2:
                continue 
                
            beat_time = (bar * 4 + beat) * beat_len
            
            # Kicks (Beat 1, and 'and' of Beat 3 represented via 2.5 index)
            if beat == 0:
                k_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, k_ppq, k_ppq + 120, 0, 36, velocity_base, True)
            if beat == 2:
                k_time2 = beat_time + (beat_len * 0.5)
                k_ppq2 = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, k_time2)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, k_ppq2, k_ppq2 + 120, 0, 36, velocity_base, True)
                
            # Snares (Beats 2 and 4)
            if beat == 1 or beat == 3:
                s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, s_ppq, s_ppq + 120, 0, 38, velocity_base, True)
                
            # Hi-Hats Arrangement Automation
            if bar >= 4:
                # Chorus: Dense, standard 8th note hats
                h_ppq1 = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time)
                h_ppq2 = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time + (beat_len * 0.5))
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, h_ppq1, h_ppq1 + 60, 0, 42, 85, True)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, h_ppq2, h_ppq2 + 60, 0, 42, 60, True)
            elif bar >= 2:
                # Verse 2nd Half: Stretched/Half-time hats (Quarter notes only)
                h_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, beat_time)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, h_ppq, h_ppq + 60, 0, 42, 85, True)
            # Bars 0-1 (Verse 1st Half) have no hats at all (subtractive layering)

    RPR.RPR_MIDI_Sort(drums_take)
    
    return f"Created subtractive build-and-drop arrangement over {bars} bars at {bpm} BPM in {key} {scale}."
