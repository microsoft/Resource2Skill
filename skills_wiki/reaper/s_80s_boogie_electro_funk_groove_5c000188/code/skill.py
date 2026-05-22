def create_pattern(
    project_name: str = "BoogieFunk",
    track_name: str = "80s Boogie Groove",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an 80s Boogie / Electro Funk rhythm section in the current REAPER project.
    Generates a swung drum machine track and a highly syncopated staccato/legato synth bass.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name prefix for the created tracks.
        bpm: Tempo in BPM (105-115 recommended).
        key: Root note (e.g., "E", "A", "F").
        scale: Scale type (defaults to minor/dorian feel).
        bars: Number of bars to generate (should be even, e.g., 4 or 8).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Music theory lookup table
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Ensure bars is a multiple of 2 for our 2-bar groove loop
    if bars % 2 != 0:
        bars += 1

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper function to calculate swing (delays off-beat 16th notes)
    # 1 Quarter Note (QN) = 1 Beat. 16th note = 0.25 QN.
    # Off-beat 16ths fall on .25 and .75 marks.
    def apply_swing(qn_pos, swing_amount=0.08):
        rem = round(qn_pos % 0.5, 3)
        if rem == 0.25:
            return qn_pos + swing_amount
        return qn_pos

    # Helper function to safely insert MIDI notes
    def insert_midi_note(take, pitch, start_qn, duration_qn, velocity):
        start_qn_swung = apply_swing(start_qn)
        end_qn_swung = apply_swing(start_qn + duration_qn) # Prevent notes from overlapping grid incorrectly
        
        # Convert Quarter Notes to PPQ (Pulses Per Quarter Note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn_swung)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn_swung)
        
        # Insert note: take, selected, muted, startppq, endppq, channel, pitch, velocity, None
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), None)

    # === Step 2: Create Drum Track & MIDI ===
    drum_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Drums (Add Sampler)", True)

    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Generate Drum Groove
    for b in range(bars):
        bar_offset = b * 4.0
        
        # --- KICK (36) ---
        # Bar 1: Strong downbeat
        if b % 2 == 0:
            insert_midi_note(drum_take, 36, bar_offset + 0.0, 0.25, 110)
        # Bar 2: Drop the 1! Kick comes in late to create space
        else:
            insert_midi_note(drum_take, 36, bar_offset + 1.5, 0.25, 90) # Ghost kick
            
        insert_midi_note(drum_take, 36, bar_offset + 2.75, 0.25, 100) # Swung syncopation
        insert_midi_note(drum_take, 36, bar_offset + 3.5, 0.25, 105)

        # --- SNARE (38) ---
        insert_midi_note(drum_take, 38, bar_offset + 1.0, 0.25, 115) # Beat 2
        insert_midi_note(drum_take, 38, bar_offset + 3.0, 0.25, 115) # Beat 4
        
        # --- HI-HAT (42 closed, 46 open) ---
        for i in range(16):
            beat_pos = bar_offset + (i * 0.25)
            
            # Open hi-hat flourish at the end of every 2-bar loop
            if b % 2 == 1 and i == 14:
                insert_midi_note(drum_take, 46, beat_pos, 0.5, 95)
                continue
            if b % 2 == 1 and i == 15:
                continue # Skip closed hat to let open ring
                
            is_offbeat_16th = (i % 2 != 0)
            # Accent downbeats and 8ths, lower velocity for 16ths
            vel = 65 if is_offbeat_16th else 105
            duration = 0.1 if is_offbeat_16th else 0.15
            insert_midi_note(drum_take, 42, beat_pos, duration, vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: Create Bass Track & MIDI ===
    bass_track_idx = drum_track_idx + 1
    RPR.RPR_InsertTrackAtIndex(bass_track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, bass_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} - Synth Bass", True)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Calculate Bass Pitches based on key
    root_pitch = NOTE_MAP.get(key, 4) + 24 # Drop to bass octave (E1/E2 range)
    m3 = root_pitch + 3
    fifth = root_pitch + 7
    m7 = root_pitch + 10
    octave = root_pitch + 12

    # Generate Bass Groove
    for b in range(0, bars, 2):
        bar_offset = b * 4.0
        
        # --- MEASURE 1 ---
        # Beat 1: Root staccato
        insert_midi_note(bass_take, root_pitch, bar_offset + 0.0, 0.15, 115)
        # Beat 2 'a': Octave pop staccato (swung)
        insert_midi_note(bass_take, octave, bar_offset + 1.75, 0.15, 95)
        # Beat 3 '&': m7 staccato passing tone
        insert_midi_note(bass_take, m7, bar_offset + 2.5, 0.15, 100)
        # Beat 4: Root LEGATO (long hold)
        insert_midi_note(bass_take, root_pitch, bar_offset + 3.0, 0.75, 105)
        # Beat 4 'a': 5th staccato lead-in
        insert_midi_note(bass_take, fifth, bar_offset + 3.75, 0.15, 90)

        # --- MEASURE 2 (The Drop) ---
        # Beat 1 is left completely blank for groove/space!
        
        # Beat 2 '&': m3 staccato
        insert_midi_note(bass_take, m3, bar_offset + 4.0 + 1.5, 0.15, 95)
        # Beat 3: Root staccato
        insert_midi_note(bass_take, root_pitch, bar_offset + 4.0 + 2.0, 0.15, 110)
        # Beat 4: 5th LEGATO resolving hold
        insert_midi_note(bass_take, fifth, bar_offset + 4.0 + 3.0, 0.5, 105)

    RPR.RPR_MIDI_Sort(bass_take)

    # === Step 4: Bass Sound Design (ReaSynth + ReaEQ) ===
    # Add ReaSynth to act as our analog 80s bass
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a punchy, warm square/saw bass
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.0)    # Volume (avoid clipping)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.01)   # Attack (snappy)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.15)   # Decay
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.4)    # Sustain
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.1)    # Release
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.7)    # Square mix (fundamental body)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.4)    # Saw mix (bite/harmonics)
    
    # Add ReaEQ to emulate a low-pass filter cutting off the harsh digital highs
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    # Band 4 (High Shelf -> Low Pass)
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 8, 2.0) # Type = Low Pass
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 9, 800.0 / 24000.0) # Freq ~800Hz for warm low end

    return f"Created '{track_name}' (Drums and Bass) over {bars} bars at {bpm} BPM in {key} {scale} with 16th-note swing."
