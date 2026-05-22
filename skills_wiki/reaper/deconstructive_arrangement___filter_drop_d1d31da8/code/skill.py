def create_pattern(
    project_name: str = "Arrangement_Project",
    track_name: str = "Drop_Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Generates 4 bars verse + 4 bars drop
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Deconstructive Arrangement Template: Verse -> Drum Dropout/Sweep -> Chorus Drop.
    Uses MIDI Channel 10 for standard GM drums and Channel 1 for Chords/Riser.
    """
    import reaper_python as RPR

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    root_note = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Standard pop/trap chord progression: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6] 

    def get_chord_notes(root, intervals, degree, octave=4):
        notes = []
        for i in [0, 2, 4]: # Triad (Root, 3rd, 5th)
            current_deg = degree + i
            octave_shift = current_deg // 7
            note_idx = current_deg % 7
            pitch = root + (octave + octave_shift) * 12 + intervals[note_idx]
            notes.append(pitch)
        return notes

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar

    # Helper function to create tracks
    def create_track_and_item(name, color=0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        if color:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", color)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === TRACK 1: CHORDS (The Harmonic Bed) ===
    chords_track, chords_take = create_track_and_item("Synth Chords", 0x010000FF)
    
    for bar in range(bars):
        degree = progression_degrees[bar % 4]
        chord_notes = get_chord_notes(root_note, scale_intervals, degree, octave=4)
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        # Insert chord notes
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, ppq_start, ppq_end, 0, note, velocity_base - 10, False)

        # Arrangement Trick: Volume/Filter Sweep on Bar 4 (Build-up)
        if bar == 3: # 4th bar (0-indexed)
            # Sweep Expression (CC11) from 64 to 127 to build tension
            steps = 16
            for step in range(steps):
                t = start_time + (bar_length_sec / steps) * step
                ppq_cc = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t)
                val = int(64 + (63 * (step / (steps - 1))))
                RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_cc, 0xB0, 0, 11, val)
        elif bar < 3: # Verse (muted/filtered)
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_start, 0xB0, 0, 11, 64)
        elif bar >= 4: # Chorus / Drop (Wide open)
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_start, 0xB0, 0, 11, 127)

    RPR.RPR_MIDI_Sort(chords_take)


    # === TRACK 2: DRUMS (The Rhythmic Contrast) ===
    drums_track, drums_take = create_track_and_item("Drums (GM Ch 10)", 0x0100FF00)
    
    KICK, SNARE, HAT = 36, 38, 42

    for bar in range(bars):
        # Arrangement Trick: Complete Drum Dropout before the drop
        if bar == 3:
            continue # Silence for the build-up!
            
        start_time = bar * bar_length_sec
        is_chorus = bar >= 4

        for beat in range(4):
            # Kick Pattern (Sparse in verse, dense in chorus)
            if beat == 0 or (beat == 2 and is_chorus):
                t = start_time + beat * beat_length_sec
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, t)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq, ppq + 240, 9, KICK, velocity_base, False)
            
            # Snare Pattern (Backbeat)
            if beat == 1 or beat == 3:
                t = start_time + beat * beat_length_sec
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, t)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq, ppq + 240, 9, SNARE, velocity_base, False)

            # Hi-hats (Half-time in verse, regular in chorus)
            hat_subdivisions = 4 if is_chorus else 2
            for sub in range(hat_subdivisions):
                t = start_time + beat * beat_length_sec + (beat_length_sec / hat_subdivisions) * sub
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, t)
                vel = velocity_base if sub == 0 else velocity_base - 20
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq, ppq + 120, 9, HAT, vel, False)

    RPR.RPR_MIDI_Sort(drums_take)


    # === TRACK 3: THE RISER (Tension Builder) ===
    riser_track, riser_take = create_track_and_item("Riser FX", 0x01FF0000)
    
    # Riser plays only in bar 4 (the gap)
    riser_start = 3 * bar_length_sec
    riser_end = 4 * bar_length_sec
    ppq_r_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, riser_start)
    ppq_r_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, riser_end)
    
    riser_pitch = root_note + 72 # High octave
    RPR.RPR_MIDI_InsertNote(riser_take, False, False, ppq_r_start, ppq_r_end, 0, riser_pitch, velocity_base, False)
    
    # Automate Riser Swell
    steps = 32
    for step in range(steps):
        t = riser_start + (bar_length_sec / steps) * step
        ppq_cc = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, t)
        val = int((step / (steps - 1)) * 127) # Sweep 0 to 127
        RPR.RPR_MIDI_InsertCC(riser_take, False, False, ppq_cc, 0xB0, 0, 11, val) # CC11 Expression
    
    RPR.RPR_MIDI_Sort(riser_take)

    RPR.RPR_UpdateArrange()

    return f"Created Deconstructive Arrangement ({bars} bars) at {bpm} BPM in {key} {scale}. Includes Verse, Dropout/Sweep transition, and Chorus drop."
