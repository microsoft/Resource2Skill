def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Melody_And_Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Creates a full Diatonic Triad progression and an interlocking step-melody
    in the current REAPER project, following the "Part 3" tutorial approach.
    """
    import reaper_python as RPR

    # --- Music Theory Lookup Tables ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }
    
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Octave offsets
    chord_octave_base = 48 # C3
    melody_octave_base = 72 # C5

    # Helper function to get the MIDI pitch for any scale degree (0-indexed)
    def get_pitch(base_midi, degree):
        octave_shift = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return base_midi + (octave_shift * 12) + scale_intervals[idx] + root_val

    # Standard progression in scale degrees (e.g., i, VI, III, VII)
    progression = [0, 5, 2, 6] 
    # Repeat or trim progression to fit the requested bars
    progression = [progression[i % len(progression)] for i in range(bars)]

    # === Setup Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    
    # === Track 1: Triad Chords (Mellow Pad) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name}_Chords", True)
    
    # Add Soft Synth (ReaSynth)
    fx_synth1 = RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a softer pad tone: sine/triangle wave, lower attack
    RPR.RPR_TrackFX_SetParam(chord_track, fx_synth1, 0, 0.5) # Waveform mix
    RPR.RPR_TrackFX_SetParam(chord_track, fx_synth1, 3, 0.2) # Attack
    
    # Create MIDI Item for Chords
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", bar_length_sec * bars)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    # === Track 2: Melody (Plucky Lead) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    mel_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(mel_track, "P_NAME", f"{track_name}_Melody", True)
    
    # Turn melody track down so it doesn't clash (-5dB approx)
    RPR.RPR_SetMediaTrackInfo_Value(mel_track, "D_VOL", 0.56) 
    
    # Add Synth and FX (Reverb)
    fx_synth2 = RPR.RPR_TrackFX_AddByName(mel_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(mel_track, fx_synth2, 0, 1.0) # Square wave mix
    RPR.RPR_TrackFX_SetParam(mel_track, fx_synth2, 4, 0.1) # Short decay/release for pluck
    
    # Cut mud via basic EQ placeholder, add Reverb for space
    fx_verb = RPR.RPR_TrackFX_AddByName(mel_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(mel_track, fx_verb, 0, 0.2) # Wet mix
    RPR.RPR_TrackFX_SetParam(mel_track, fx_verb, 1, 0.8) # Dry mix
    RPR.RPR_TrackFX_SetParam(mel_track, fx_verb, 2, 0.6) # Room size
    
    # Create MIDI Item for Melody
    mel_item = RPR.RPR_AddMediaItemToTrack(mel_track)
    RPR.RPR_SetMediaItemInfo_Value(mel_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(mel_item, "D_LENGTH", bar_length_sec * bars)
    mel_take = RPR.RPR_AddTakeToMediaItem(mel_item)

    # === Note Generation Loop ===
    for bar, root_degree in enumerate(progression):
        bar_start_time = bar * bar_length_sec
        
        # --- 1. Construct the Triad Chord (1-3-5) ---
        c_root = get_pitch(chord_octave_base, root_degree)
        c_third = get_pitch(chord_octave_base, root_degree + 2)
        c_fifth = get_pitch(chord_octave_base, root_degree + 4)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, bar_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, bar_start_time + bar_length_sec)
        
        for pitch in [c_root, c_third, c_fifth]:
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            
        # --- 2. Construct the Melody ---
        # The tutorial advises: Start on a chord note (e.g., the 3rd), place on strong beats, 
        # step up/down by 1-2 notes, keep rhythm clean and leave space.
        
        # Note 1: Downbeat of Beat 1. Pitch = 3rd of the current chord.
        mel_pitch_1 = get_pitch(melody_octave_base, root_degree + 2)
        m1_start = bar_start_time
        m1_end = bar_start_time + (sec_per_beat * 1.0) # 1/4 note length
        
        # Note 2: Upbeat of Beat 2. Pitch = Step up one scale degree from Note 1.
        mel_pitch_2 = get_pitch(melody_octave_base, root_degree + 3)
        m2_start = bar_start_time + (sec_per_beat * 1.5)
        m2_end = m2_start + (sec_per_beat * 0.5) # 1/8 note length
        
        # Note 3: Downbeat of Beat 3. Pitch = The 5th of the chord (step up again).
        mel_pitch_3 = get_pitch(melody_octave_base, root_degree + 4)
        m3_start = bar_start_time + (sec_per_beat * 2.0)
        m3_end = m3_start + (sec_per_beat * 1.0) # 1/4 note length
        
        # Beat 4 is left empty to "leave space" as instructed.
        
        for p, s, e in [(mel_pitch_1, m1_start, m1_end),
                        (mel_pitch_2, m2_start, m2_end),
                        (mel_pitch_3, m3_start, m3_end)]:
            m_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(mel_take, s)
            m_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(mel_take, e)
            RPR.RPR_MIDI_InsertNote(mel_take, False, False, m_start_ppq, m_end_ppq, 0, p, velocity_base + 5, False)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(mel_take)
    RPR.RPR_UpdateArrange()

    return f"Created Chords and Melody over {bars} bars at {bpm} BPM in {key} {scale} with applied Reverb and leveling."
