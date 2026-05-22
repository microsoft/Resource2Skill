def create_pattern(
    project_name: str = "SubtractiveArrangement",
    track_name: str = "Arranger",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16, # Fixed to 16 for this specific structural pattern
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 16-bar Subtractive Arrangement (Intro -> Sparse Verse -> Full Verse -> Chorus)
    complete with 1-bar Riser transitions.
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
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Setup
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    root_midi = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generic progression (1-5-6-4 logic adapted for generic scale)
    degrees = [0, 4, 5, 3] 

    def get_chord_notes(root, intervals, degree):
        chord = []
        for d in [degree, degree + 2, degree + 4]:
            octave = d // 7
            idx = d % 7
            chord.append(root + (octave * 12) + intervals[idx])
        return chord

    def create_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        return track

    def add_midi_item(track, start_bar, num_bars):
        bar_sec = (60.0 / bpm) * 4
        start_sec = start_bar * bar_sec
        length_sec = num_bars * bar_sec
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_sec)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take, start_sec

    # Timings
    bar_sec = (60.0 / bpm) * 4
    beat_sec = 60.0 / bpm

    # ---------------------------------------------------------
    # 1. CHORDS TRACK (Plays throughout the whole arrangement)
    # ---------------------------------------------------------
    tr_chords = create_track(f"{track_name}_Chords")
    _, take_chords, _ = add_midi_item(tr_chords, 0, 16)
    
    for bar in range(16):
        degree = degrees[bar % 4]
        chord = get_chord_notes(root_midi, scale_intervals, degree)
        start_time = bar * bar_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, start_time + bar_sec - 0.1)
        
        for note in chord:
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
    RPR.RPR_MIDI_Sort(take_chords)

    # ---------------------------------------------------------
    # 2. DRUMS TRACK (Subtractive Arrangement)
    # ---------------------------------------------------------
    tr_drums = create_track(f"{track_name}_Drums")
    _, take_drums, _ = add_midi_item(tr_drums, 4, 12) # Starts at bar 4 (Verse)

    for bar in range(4, 16):
        section = "Chorus" if bar >= 12 else ("VerseB" if bar >= 8 else "VerseA")
        bar_start_time = bar * bar_sec

        # Kicks and Snares
        for beat in range(4):
            beat_time = bar_start_time + (beat * beat_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, beat_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, beat_time + 0.1)

            # Subtractive Rule: Drop downbeat kick in Verse A to reduce energy
            if beat == 0 and section == "VerseA":
                continue 

            if beat % 2 == 0: # Kick
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 0, 36, 110, False)
            else: # Snare
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 0, 38, 100, False)

        # Hihats
        # Subtractive Rule: No hi-hats in Verse A
        if section in ["VerseB", "Chorus"]:
            for eighth in range(8):
                hh_time = bar_start_time + (eighth * (beat_sec / 2))
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hh_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hh_time + 0.05)
                # Subtle velocity groove on hats
                vel = 90 if eighth % 2 == 0 else 70
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 0, 42, vel, False)
    RPR.RPR_MIDI_Sort(take_drums)

    # ---------------------------------------------------------
    # 3. LEAD TRACK (Only active in the Chorus)
    # ---------------------------------------------------------
    tr_lead = create_track(f"{track_name}_Lead")
    _, take_lead, _ = add_midi_item(tr_lead, 12, 4)
    
    for bar in range(12, 16):
        degree = degrees[bar % 4]
        bar_start_time = bar * bar_sec
        melody_note = get_chord_notes(root_midi + 12, scale_intervals, degree)[2] # Play the 5th of the chord up an octave
        
        # Simple rhythmic motif (2 quarter notes, 1 half note)
        for i, mult in enumerate([0, 1, 2]):
            m_start = bar_start_time + (mult * beat_sec)
            m_length = beat_sec * 0.8 if i < 2 else beat_sec * 1.8
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_lead, m_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_lead, m_start + m_length)
            RPR.RPR_MIDI_InsertNote(take_lead, False, False, start_ppq, end_ppq, 0, melody_note, velocity_base, False)
    RPR.RPR_MIDI_Sort(take_lead)

    # ---------------------------------------------------------
    # 4. RISER FX TRACK (Tension transitions)
    # ---------------------------------------------------------
    tr_fx = create_track(f"{track_name}_RiserFX")
    _, take_fx, _ = add_midi_item(tr_fx, 0, 16)
    
    # Place 1-bar risers immediately before section changes
    riser_bars = [3, 7, 11] 
    for r_bar in riser_bars:
        r_start_time = r_bar * bar_sec
        r_end_time = r_start_time + bar_sec

        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_fx, r_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_fx, r_end_time)

        # Sustained high note for the sweep
        fx_note = root_midi + 24
        RPR.RPR_MIDI_InsertNote(take_fx, False, False, start_ppq, end_ppq, 0, fx_note, 100, False)

        # MIDI CC 7 (Volume) Swell over 1 bar
        steps = 32
        for i in range(steps):
            pos_time = r_start_time + (i * bar_sec / steps)
            pos_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_fx, pos_time)
            # Exponential curve for more dramatic sweep
            vol = int(127 * ((i / (steps - 1)) ** 2))
            RPR.RPR_MIDI_InsertCC(take_fx, False, False, pos_ppq, 176, 0, 7, vol)
            
        # Snap volume back to 0 at the start of the next section
        end_snap_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_fx, r_end_time + 0.01)
        RPR.RPR_MIDI_InsertCC(take_fx, False, False, end_snap_ppq, 176, 0, 7, 0)
        
    RPR.RPR_MIDI_Sort(take_fx)

    return f"Created 16-bar Subtractive Arrangement '{track_name}' in {key} {scale} at {bpm} BPM with riser transitions."
