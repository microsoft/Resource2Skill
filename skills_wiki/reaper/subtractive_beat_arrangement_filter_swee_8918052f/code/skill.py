def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "BeatDrop",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8, 
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an 8-bar arrangement showcasing a subtractive verse-to-chorus transition
    using a drum dropout and a low-pass filter sweep.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Helper: Get MIDI pitch from scale degree
    def get_scale_note(degree_idx, root_midi, scale_intervals):
        octave = degree_idx // len(scale_intervals)
        note = scale_intervals[degree_idx % len(scale_intervals)]
        return root_midi + note + (octave * 12)

    # Helper: Create Track
    def add_new_track(name, vol=0.7):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "D_VOL", vol)
        return trk

    # Helper: Create MIDI Item
    def add_midi_item(trk, start_sec, length_sec):
        item = RPR.RPR_AddMediaItemToTrack(trk)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_sec)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take

    # Helper: Insert Note
    def insert_midi_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- Initialization ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    root_midi = NOTE_MAP.get(key, 0) + 48 # Base C3
    scale_ints = SCALES.get(scale, SCALES["minor"])
    
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4
    total_len = bar_len * 8

    # --- 1. Chords Track (Pad sound) ---
    chords_trk = add_new_track(f"{track_name}_Chords", 0.6)
    chords_item, chords_take = add_midi_item(chords_trk, 0, total_len)
    chords_fx = RPR.RPR_TrackFX_AddByName(chords_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_trk, chords_fx, 2, 0.5) # Saw
    RPR.RPR_TrackFX_SetParam(chords_trk, chords_fx, 7, 0.3) # Attack (slow)
    RPR.RPR_TrackFX_SetParam(chords_trk, chords_fx, 10, 0.5) # Release
    
    # Add Filter Sweep (ReaEQ)
    eq_fx = RPR.RPR_TrackFX_AddByName(chords_trk, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_trk, eq_fx, 10, 0.0) # Band 4 Gain to -inf (creates a low-pass)
    env_eq = RPR.RPR_GetFXEnvelope(chords_trk, eq_fx, 9, True) # Band 4 Freq (Param 9)
    
    # Automate the "Suck-in" filter transition during Bar 4
    RPR.RPR_InsertEnvelopePoint(env_eq, 0.0, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_eq, bar_len * 3, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_eq, bar_len * 4 - 0.05, 0.1, 0, 0, False, True) # Filter closes
    RPR.RPR_InsertEnvelopePoint(env_eq, bar_len * 4, 1.0, 0, 0, False, True) # Filter pops open on Drop
    RPR.RPR_Envelope_SortPoints(env_eq)

    # --- 2. Bass Track ---
    bass_trk = add_new_track(f"{track_name}_Bass", 0.8)
    bass_item, bass_take = add_midi_item(bass_trk, bar_len * 4, bar_len * 4) # Only exists in Chorus
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_trk, bass_fx, 2, 1.0) # Sawtooth
    RPR.RPR_TrackFX_SetParam(bass_trk, bass_fx, 7, 0.0) # Fast Attack

    # --- 3. Drums Track ---
    drums_trk = add_new_track(f"{track_name}_Drums", 0.9)
    drums_item, drums_take = add_midi_item(drums_trk, 0, total_len)
    drums_fx = RPR.RPR_TrackFX_AddByName(drums_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(drums_trk, drums_fx, 3, 0.5) # Square (percussive tone)
    RPR.RPR_TrackFX_SetParam(drums_trk, drums_fx, 8, 0.1) # Fast Decay
    RPR.RPR_TrackFX_SetParam(drums_trk, drums_fx, 9, 0.0) # No Sustain

    # --- 4. Riser Track (Tension builder) ---
    riser_trk = add_new_track(f"{track_name}_Riser", 0.4)
    riser_item, riser_take = add_midi_item(riser_trk, bar_len * 3, bar_len) # Only in transition bar
    riser_fx = RPR.RPR_TrackFX_AddByName(riser_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(riser_trk, riser_fx, 7, 1.0) # Very slow attack
    # Automate Pitch Tuning (Param 1) upwards over Bar 4
    env_riser = RPR.RPR_GetFXEnvelope(riser_trk, riser_fx, 1, True) 
    RPR.RPR_InsertEnvelopePoint(env_riser, bar_len * 3, 0.5, 0, 0, False, True) # Center pitch
    RPR.RPR_InsertEnvelopePoint(env_riser, bar_len * 4, 1.0, 0, 0, False, True) # Pitch shifted up
    RPR.RPR_Envelope_SortPoints(env_riser)

    # --- Sequence MIDI Data ---
    progression = [0, 5, 2, 6] # i, VI, III, VII progression

    for bar in range(8):
        b_start = bar * bar_len
        deg = progression[bar % 4]
        
        # Write Chords (All 8 bars)
        for offset in [0, 2, 4]:
            pitch = get_scale_note(deg + offset, root_midi + 12, scale_ints)
            insert_midi_note(chords_take, b_start, b_start + bar_len - 0.05, pitch, velocity_base - 20)
            
        # Write Bass (Chorus only, bars 5-8)
        if bar >= 4:
            b_pitch = get_scale_note(deg, root_midi - 12, scale_ints)
            for i in range(8): # Driving 8th notes
                n_start = b_start + i * (beat_len / 2)
                insert_midi_note(bass_take, n_start, n_start + (beat_len/2) - 0.05, b_pitch, velocity_base)
                
        # Write Drums
        if bar < 4:
            # Verse (Sparse, no Kick)
            if bar == 3: 
                # THE DROPOUT: Drums abruptly stop halfway through Bar 4
                for i in range(4): # Hats only on beats 1 and 2
                    n_start = b_start + i * (beat_len / 2)
                    insert_midi_note(drums_take, n_start, n_start + 0.1, 42, velocity_base - 10)
                insert_midi_note(drums_take, b_start + beat_len, b_start + beat_len + 0.1, 38, velocity_base) # Snare on 2
            else:
                # Normal Verse: 8th note hats, Snares on 2 & 4
                for i in range(8):
                    n_start = b_start + i * (beat_len / 2)
                    insert_midi_note(drums_take, n_start, n_start + 0.1, 42, velocity_base - 10)
                insert_midi_note(drums_take, b_start + beat_len, b_start + beat_len + 0.1, 38, velocity_base)
                insert_midi_note(drums_take, b_start + beat_len * 3, b_start + beat_len * 3 + 0.1, 38, velocity_base)
        else:
            # Chorus (Full Energy)
            for i in range(16): # 16th note hats
                n_start = b_start + i * (beat_len / 4)
                vel = velocity_base if i % 4 == 0 else velocity_base - 30
                insert_midi_note(drums_take, n_start, n_start + 0.05, 42, vel)
            
            insert_midi_note(drums_take, b_start + beat_len, b_start + beat_len + 0.1, 38, velocity_base + 10)
            insert_midi_note(drums_take, b_start + beat_len * 3, b_start + beat_len * 3 + 0.1, 38, velocity_base + 10)
            
            # Sub-shaking Trap Kick Bounce (1, 2-and, 3)
            insert_midi_note(drums_take, b_start, b_start + 0.1, 36, velocity_base + 20)
            insert_midi_note(drums_take, b_start + beat_len * 1.5, b_start + beat_len * 1.5 + 0.1, 36, velocity_base + 20)
            insert_midi_note(drums_take, b_start + beat_len * 2, b_start + beat_len * 2 + 0.1, 36, velocity_base + 20)

    # Write single Riser note for Bar 4
    insert_midi_note(riser_take, bar_len * 3, bar_len * 4, 60, velocity_base)

    # Apply sorting to commit MIDI events
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drums_take)
    RPR.RPR_MIDI_Sort(riser_take)

    return f"Created sub-arranged transition on '{track_name}' group over 8 bars at {bpm} BPM."
