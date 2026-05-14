def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "Arrangement",
    bpm: int = 128,
    key: str = "A",
    scale: str = "minor",
    bars: int = 16,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a full 16-bar EDM House arrangement structure including Intro, Build, Drop, and Verse.
    Features automated sidechain pumping via CC11 and pre-drop drum cutouts.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM (128 is standard for House).
        key: Root note (e.g., A, C, G).
        scale: major or minor.
        bars: Fixed to 16 bars macro-structure for this arrangement pattern.
        velocity_base: Base velocity for MIDI notes.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    root_offset = NOTE_MAP.get(key.upper(), 0)
    
    # Standard EDM progression: vi-IV-I-V (Major) or i-VI-III-VII (Minor)
    if "minor" in scale.lower():
        prog_degrees = [0, 5, 2, 6] 
    else:
        prog_degrees = [5, 3, 0, 4] 

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    def get_diatonic_pitch(degree_index, octave):
        octave_shift = (degree_index // 7)
        scale_idx = degree_index % 7
        return root_offset + scale_intervals[scale_idx] + (octave + octave_shift) * 12

    # === Step 1: Initialize Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    q_sec = 60.0 / bpm
    bar_sec = q_sec * 4
    total_len = 16 * bar_sec

    def add_track_with_item(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(tr)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return tr, item, take

    tr_chords, item_chords, take_chords = add_track_with_item("EDM_Chords")
    tr_bass, item_bass, take_bass = add_track_with_item("EDM_Bass")
    tr_drums, item_drums, take_drums = add_track_with_item("EDM_Drums")

    # Add basic synthesized tone generators
    RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(tr_bass, "ReaSynth", False, -1)

    # === Step 2: Generate 16-Bar Structure ===
    for bar in range(16):
        chord_idx = bar % 4
        d = prog_degrees[chord_idx]
        start_time = bar * bar_sec
        end_time = start_time + bar_sec
        
        # Pre-drop pause: Cut the 8th and 16th bars short by 2 beats
        is_pause_bar = (bar == 7 or bar == 15)
        chord_end_time = start_time + q_sec * 2 if is_pause_bar else end_time

        # --- CHORDS (Sustained pads) ---
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, chord_end_time)
        
        pitches = [
            get_diatonic_pitch(d, 3),      # Doubled Low Root
            get_diatonic_pitch(d, 4),      # Root
            get_diatonic_pitch(d + 2, 4),  # Third
            get_diatonic_pitch(d + 4, 4)   # Fifth
        ]
        for p in pitches:
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, p, 80, False)

        # --- BASS (Drop and Verse only: Bars 9-16) ---
        if bar >= 8:
            bass_p = get_diatonic_pitch(d, 2)
            for q in range(4):
                if is_pause_bar and q >= 2:
                    continue # Silence for pause
                
                # Off-beat rhythm (plays on the 'and' of the beat)
                b_start = start_time + q * q_sec + q_sec * 0.5
                b_end = b_start + q_sec * 0.5
                b_s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_bass, b_start)
                b_e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_bass, b_end)
                RPR.RPR_MIDI_InsertNote(take_bass, False, False, b_s_ppq, b_e_ppq, 0, bass_p, 110, False)

        # --- DRUMS (Build, Drop, Verse) ---
        for q in range(4):
            if is_pause_bar and q >= 2:
                continue # Cut drums before the next section
                
            beat_time = start_time + q * q_sec
            beat_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_drums, beat_time)
            k_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_drums, beat_time + q_sec * 0.25)

            # KICK (4-on-the-floor, starts at bar 5)
            if bar >= 4:
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, beat_ppq, k_end, 0, 36, 110, False)

            # SNARE RISER (Build only: Bars 5-8)
            if 4 <= bar < 8:
                if bar < 6 and (q == 1 or q == 3): # 2 & 4
                    RPR.RPR_MIDI_InsertNote(take_drums, False, False, beat_ppq, k_end, 0, 38, 100, False)
                elif bar == 6: # Quarter notes
                    RPR.RPR_MIDI_InsertNote(take_drums, False, False, beat_ppq, k_end, 0, 38, 100 + q*5, False)
                elif bar == 7: # Eighth notes
                    RPR.RPR_MIDI_InsertNote(take_drums, False, False, beat_ppq, k_end, 0, 38, 120, False)
                    mid_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_drums, beat_time + q_sec * 0.5)
                    mid_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_drums, beat_time + q_sec * 0.75)
                    RPR.RPR_MIDI_InsertNote(take_drums, False, False, mid_ppq, mid_end, 0, 38, 120, False)

            # CLAP (Drop and Verse: Bars 9-16)
            if bar >= 8:
                if q == 1 or q == 3:
                    RPR.RPR_MIDI_InsertNote(take_drums, False, False, beat_ppq, k_end, 0, 39, 100, False)

            # HI-HAT (Drop only: Bars 9-12)
            if 8 <= bar < 12:
                h_start = beat_time + q_sec * 0.5
                h_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_drums, h_start)
                h_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_drums, h_start + q_sec * 0.25)
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, h_ppq, h_end, 0, 42, 90, False)

    # === Step 3: CC11 Sidechain Pumping Automation ===
    # Set volume flat for Intro
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, 0)
    RPR.RPR_MIDI_InsertCC(take_chords, False, False, start_ppq, 176, 0, 11, 127)
    
    # Apply pumping during Build and Drop (Bars 5-12)
    for bar in range(4, 12):
        for q in range(4):
            if bar == 7 and q >= 2:
                continue # Keep volume flat during the pause
                
            beat_time = bar * bar_sec + q * q_sec
            ppq0 = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, beat_time)
            ppq1 = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, beat_time + q_sec * 0.25) # 16th
            ppq2 = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, beat_time + q_sec * 0.5)  # 8th
            
            # Duck volume to 40 on the kick, ramp back up to 127 on the offbeat
            RPR.RPR_MIDI_InsertCC(take_chords, False, False, ppq0, 176, 0, 11, 40)
            RPR.RPR_MIDI_InsertCC(take_chords, False, False, ppq1, 176, 0, 11, 90)
            RPR.RPR_MIDI_InsertCC(take_chords, False, False, ppq2, 176, 0, 11, 127)

    # Return to flat volume for the Verse breakdown (Bars 13-16)
    v_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(item_chords, 12 * bar_sec)
    RPR.RPR_MIDI_InsertCC(take_chords, False, False, v_ppq, 176, 0, 11, 127)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_UpdateArrange()

    return f"Created full 16-bar EDM Arrangement in {key} {scale} at {bpm} BPM with sidechain pumping."
