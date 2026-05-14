def create_pattern(
    project_name: str = "Arrangement",
    track_name: str = "Beat Structure",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Subtractive Arrangement Framework demonstrating Verse/Chorus transitions,
    kick drops, halftime hi-hats, and a synthesized Reverb Riser.
    
    Args:
        project_name: Project identifier.
        track_name: Prefix for created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, D#, F).
        scale: Scale type (e.g., minor, major).
        bars: Total arrangement length (defaults to 16: 8 bar Chorus + 8 bar Verse).
        velocity_base: Base velocity.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_idx = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_octave = 48 # Octave 3 for chords
    
    # Set Project BPM
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Start appending tracks at the end
    start_track_idx = RPR.RPR_CountTracks(0)
    
    def create_track_with_midi(name, num_bars):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create MIDI Item
        item_length = (60.0 / bpm) * 4.0 * num_bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def insert_note(take, start_beat, len_beats, pitch, vel):
        start_sec = start_beat * (60.0 / bpm)
        end_sec = (start_beat + len_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # ==========================================
    # TRACK 1: CHORDS (Constant Foundation)
    # ==========================================
    _, take_chords = create_track_with_midi(f"{track_name} - Chords", bars)
    # i - VI - III - VII progression
    progression = [0, 5, 2, 6] 
    
    for bar in range(bars):
        chord_degree = progression[bar % 4]
        root_pitch = base_octave + root_idx + scale_intervals[chord_degree]
        
        # Calculate minor/major thirds within scale
        third_idx = (chord_degree + 2) % 7
        fifth_idx = (chord_degree + 4) % 7
        oct_up_3 = 12 if (chord_degree + 2) >= 7 else 0
        oct_up_5 = 12 if (chord_degree + 4) >= 7 else 0
        
        third_pitch = base_octave + root_idx + scale_intervals[third_idx] + oct_up_3
        fifth_pitch = base_octave + root_idx + scale_intervals[fifth_idx] + oct_up_5
        
        insert_note(take_chords, bar * 4, 4.0, root_pitch, 70)
        insert_note(take_chords, bar * 4, 4.0, third_pitch, 70)
        insert_note(take_chords, bar * 4, 4.0, fifth_pitch, 70)
        
    RPR.RPR_MIDI_Sort(take_chords)

    # ==========================================
    # TRACK 2: LEAD (Subtractive Melody)
    # ==========================================
    _, take_lead = create_track_with_midi(f"{track_name} - Lead", bars)
    for bar in range(bars):
        # CORE LESSON: Subtract lead in the Verse (Bars 9-16) to create space for vocal
        if 8 <= bar < 16:
            continue
            
        pos = bar * 4
        insert_note(take_lead, pos, 1.0, base_octave + 24 + root_idx, 95)
        insert_note(take_lead, pos + 1.5, 0.5, base_octave + 24 + root_idx + 7, 90)
        insert_note(take_lead, pos + 2.5, 1.5, base_octave + 24 + root_idx + 3, 90)
        
    RPR.RPR_MIDI_Sort(take_lead)

    # ==========================================
    # TRACK 3: DRUMS (Subtractive & Halftime)
    # ==========================================
    _, take_drums = create_track_with_midi(f"{track_name} - Drums", bars)
    for beat in range(bars * 4):
        # Snare always hits on 2 and 4 (beat 1 and 3 of a 0-indexed 4-beat bar)
        if beat % 4 == 1 or beat % 4 == 3:
            insert_note(take_drums, beat, 0.5, 38, 110) # Snare
            
        # Kick Pattern
        # CORE LESSON: Drop the kick for the first half of the verse (Bars 9-12 / Beats 32-47)
        is_kick_drop_zone = (32 <= beat < 48)
        if not is_kick_drop_zone:
            if beat % 4 == 0:
                insert_note(take_drums, beat, 0.5, 36, 120) # Downbeat Kick
            if beat % 4 == 1:
                insert_note(take_drums, beat + 0.5, 0.5, 36, 110) # Syncopated Kick
                
        # Hi-Hat Pattern
        # CORE LESSON: Halftime groove in second half of verse (Bars 13-16 / Beats 48-63)
        is_halftime_zone = (48 <= beat < 64)
        if is_halftime_zone:
            # Quarter notes only
            insert_note(take_drums, beat, 0.25, 42, 95)
        else:
            # 8th notes
            insert_note(take_drums, beat, 0.25, 42, 95)
            insert_note(take_drums, beat + 0.5, 0.25, 42, 75)
            
    RPR.RPR_MIDI_Sort(take_drums)

    # ==========================================
    # TRACK 4: TRANSITION RISER (Synth + Verb)
    # ==========================================
    track_riser, take_riser = create_track_with_midi(f"{track_name} - Riser", bars)
    
    # Setup FX for synthetic sweep
    RPR.RPR_TrackFX_AddByName(track_riser, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_riser, "ReaVerbate", False, -1)
    
    # Configure ReaVerbate for massive "Tail" to spill into the next section
    # Param 0: Wet, Param 1: Dry, Param 2: RoomSize, Param 3: Damp
    RPR.RPR_TrackFX_SetParam(track_riser, 1, 0, 1.0)  # 100% Wet
    RPR.RPR_TrackFX_SetParam(track_riser, 1, 1, 0.4)  # 40% Dry
    RPR.RPR_TrackFX_SetParam(track_riser, 1, 2, 0.95) # Huge Room Size
    
    # Generate riser note swells right before structural changes
    # Bar 8 (Transition to Verse) and Bar 16 (Transition loop)
    transition_bars = [7, 15] 
    for bar in transition_bars:
        start_beat = bar * 4
        for step in range(16): # 16th notes swelling up over 1 bar
            pitch = 48 + step # Pitch rises
            vel = 30 + int((step / 15.0) * 80) # Velocity (volume) rises from 30 to 110
            insert_note(take_riser, start_beat + (step * 0.25), 0.25, pitch, vel)
            
    RPR.RPR_MIDI_Sort(take_riser)

    return f"Created Subtractive Arrangement (4 tracks, {bars} bars) at {bpm} BPM: Features Kick Drop, Halftime Hats, and Reverb Riser."
