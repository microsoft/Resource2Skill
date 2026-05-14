def create_pattern(
    project_name: str = "First_MIDI_Song",
    track_name: str = "Funk_Groove",
    bpm: int = 88,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 4-part Indie-Funk arrangement (Drums, Keys, Pad, Lead) with FX chains.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_note = NOTE_MAP.get(key.upper(), 0) + 48 # Octave 4 base

    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def add_track_with_midi(name: str, length_sec: float) -> tuple:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def sec_to_ppq(take, time_sec):
        return RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)

    # ==========================================
    # TRACK 1: DRUMS
    # ==========================================
    drum_track, drum_take = add_track_with_midi(f"{track_name}_Drums", total_length_sec)
    
    # Basic General MIDI mapping
    kick_pitch = 36 # C1
    snare_pitch = 38 # D1
    hat_pitch = 42 # F#1

    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        beat_sec = 60.0 / bpm
        
        # Kick (Beats 1, 2.5, 3)
        for b in [0, 1.5, 2]:
            st = sec_to_ppq(drum_take, bar_start_sec + (b * beat_sec))
            end = sec_to_ppq(drum_take, bar_start_sec + (b * beat_sec) + 0.1)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, st, end, 9, kick_pitch, velocity_base, False)
            
        # Snare (Beats 2, 4)
        for b in [1, 3]:
            st = sec_to_ppq(drum_take, bar_start_sec + (b * beat_sec))
            end = sec_to_ppq(drum_take, bar_start_sec + (b * beat_sec) + 0.1)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, st, end, 9, snare_pitch, velocity_base, False)
            
        # Hats (Straight 8ths)
        for b in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
            st = sec_to_ppq(drum_take, bar_start_sec + (b * beat_sec))
            end = sec_to_ppq(drum_take, bar_start_sec + (b * beat_sec) + 0.05)
            vel = velocity_base if b % 1 == 0 else int(velocity_base * 0.7) # Accent on downbeats
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, st, end, 9, hat_pitch, vel, False)

    # ==========================================
    # TRACK 2: ELECTRIC PIANO CHORDS
    # ==========================================
    keys_track, keys_take = add_track_with_midi(f"{track_name}_EPiano", total_length_sec)
    
    # Progression: i - v - iv - i (using scale degrees 0, 4, 3, 0)
    progression_degrees = [0, 4, 3, 0] 
    
    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        degree_idx = progression_degrees[bar % len(progression_degrees)]
        
        # Build a basic triad from the scale
        root = root_note + scale_intervals[degree_idx]
        third = root_note + scale_intervals[(degree_idx + 2) % len(scale_intervals)]
        if (degree_idx + 2) >= len(scale_intervals): third += 12
        fifth = root_note + scale_intervals[(degree_idx + 4) % len(scale_intervals)]
        if (degree_idx + 4) >= len(scale_intervals): fifth += 12
        
        chord_notes = [root - 12, third, fifth] # Drop root an octave for weight
        
        # Play chord for 1 full bar minus a tiny gap
        st = sec_to_ppq(keys_take, bar_start_sec)
        end = sec_to_ppq(keys_take, bar_start_sec + bar_length_sec - 0.1)
        
        for p in chord_notes:
            RPR.RPR_MIDI_InsertNote(keys_take, False, False, st, end, 0, p, int(velocity_base*0.8), False)

    # Keys FX: ReaSynth + JS Ping Pong Delay
    RPR.RPR_TrackFX_AddByName(keys_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(keys_track, 0, 1, 0.5) # Attack
    RPR.RPR_TrackFX_SetParam(keys_track, 0, 2, 0.5) # Decay
    
    delay_idx = RPR.RPR_TrackFX_AddByName(keys_track, "JS: Delay w/Tempo Ping-Pong", False, -1)
    # JS Ping Pong Delay Param 4 is Width (usually 0 to 100)
    RPR.RPR_TrackFX_SetParam(keys_track, delay_idx, 4, 100.0) 

    # ==========================================
    # TRACK 3: STRING PAD
    # ==========================================
    pad_track, pad_take = add_track_with_midi(f"{track_name}_Strings", total_length_sec)
    
    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        degree_idx = progression_degrees[bar % len(progression_degrees)]
        root = root_note + scale_intervals[degree_idx]
        
        st = sec_to_ppq(pad_take, bar_start_sec)
        end = sec_to_ppq(pad_take, bar_start_sec + bar_length_sec)
        
        # Sustained root note and 5th
        RPR.RPR_MIDI_InsertNote(pad_take, False, False, st, end, 0, root, int(velocity_base*0.6), False)

    # Pad FX: ReaSynth (long release) + ReaVerbate
    synth_idx = RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, synth_idx, 1, 2.0) # Long Attack
    RPR.RPR_TrackFX_SetParam(pad_track, synth_idx, 3, 2.0) # Long Release
    
    verb_idx = RPR.RPR_TrackFX_AddByName(pad_track, "VST: ReaVerbate (Cockos)", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, verb_idx, 0, 0.5) # Wet
    RPR.RPR_TrackFX_SetParam(pad_track, verb_idx, 1, 0.2) # Dry
    RPR.RPR_TrackFX_SetParam(pad_track, verb_idx, 2, 0.95) # Room size 95%

    # ==========================================
    # TRACK 4: FUNK SOLO LEAD
    # ==========================================
    lead_track, lead_take = add_track_with_midi(f"{track_name}_FunkLead", total_length_sec)
    
    blues_intervals = SCALES["blues"]
    
    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        beat_sec = 60.0 / bpm
        
        # Simple syncopated funk riff
        rhythm_hits = [0, 0.75, 1.5, 2.5, 3.25]
        mel_indices = [0, 3, 4, 2, 0] # Using blues scale indices
        
        for i, b in enumerate(rhythm_hits):
            st = sec_to_ppq(lead_take, bar_start_sec + (b * beat_sec))
            end = sec_to_ppq(lead_take, bar_start_sec + (b * beat_sec) + 0.15) # Short staccato
            pitch = root_note + 12 + blues_intervals[mel_indices[i]] # 1 octave up
            RPR.RPR_MIDI_InsertNote(lead_take, False, False, st, end, 0, pitch, velocity_base + 10, False)

    # Lead FX: ReaSynth + EQ + Saturation + Delay
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)
    
    eq_idx = RPR.RPR_TrackFX_AddByName(lead_track, "VST: ReaEQ (Cockos)", False, -1)
    # Band 1: High Pass
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 0, 0) # Band 1 Type: High Pass
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 1, 200.0) # Freq
    # Band 2: Mid Boost
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 3, 1) # Band 2 Type: Band
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 4, 1500.0) # Freq 1.5kHz
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 5, 9.0) # Gain +9dB

    sat_idx = RPR.RPR_TrackFX_AddByName(lead_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, sat_idx, 0, 75.0) # Amount 75%
    
    RPR.RPR_TrackFX_AddByName(lead_track, "JS: Delay w/Tempo Ping-Pong", False, -1)

    # Sort all MIDI takes
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(keys_take)
    RPR.RPR_MIDI_Sort(pad_take)
    RPR.RPR_MIDI_Sort(lead_take)

    RPR.RPR_UpdateArrange()

    return f"Created 4-part arrangement '{track_name}' (Drums, Keys, Strings, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
