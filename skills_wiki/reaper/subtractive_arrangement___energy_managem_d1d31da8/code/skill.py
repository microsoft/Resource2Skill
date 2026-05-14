def create_pattern(
    project_name: str = "Wodzu Subtractive Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 32,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete 32-bar Hip-Hop/Rap arrangement using the 'Subtractive' method.
    Sections: 8-bar Intro, 8-bar Chorus, 8-bar Verse (A/B), 8-bar Chorus.
    
    Args:
        project_name: Project identifier.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type (e.g., minor).
        bars: Total bars (forces 32 for the full song structure).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # --- Music Theory & Tuning Setup ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root = NOTE_MAP.get(key, 0)
    
    # Define a generic 2-bar progression: i - VI (e.g. Cmin -> AbMaj)
    chord_1_root = root + 48 # Octave 4
    chord_1 = [chord_1_root, chord_1_root + scale_intervals[2], chord_1_root + scale_intervals[4]]
    
    # VI chord is 5 scale degrees up from the root
    chord_2_root = root + 48 + scale_intervals[5]
    # Rough approximation of the diatonic triad for the VI chord
    chord_2 = [chord_2_root, chord_2_root + 4, chord_2_root + 7] if scale == "minor" else [chord_2_root, chord_2_root + 3, chord_2_root + 7]

    # --- Initialization ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    total_bars = 32

    # Track creation helper
    def create_track_with_instrument(name, instrument="ReaSynth"):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        RPR.RPR_TrackFX_AddByName(trk, instrument, False, -1)
        return trk

    tracks = {
        "Chords": create_track_with_instrument("Chords Pad"),
        "Lead": create_track_with_instrument("Lead Melody"),
        "Bass": create_track_with_instrument("808 Bass"),
        "Drums": create_track_with_instrument("Drums (ReaSamplOmatic)")
    }
    
    # Detune the lead slightly for character
    RPR.RPR_TrackFX_SetParam(tracks["Lead"], 0, 0, 0.5)  # Waveform adjust
    RPR.RPR_TrackFX_SetParam(tracks["Bass"], 0, 0, 1.0)  # Make Bass a Sawtooth
    
    # --- Arrangement Logic ---
    # We create one large MIDI item per track to represent the full song timeline.
    items = {}
    takes = {}
    for t_name, trk in tracks.items():
        item = RPR.RPR_AddMediaItemToTrack(trk)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_bars * beats_per_bar * beat_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        items[t_name] = item
        takes[t_name] = take

    def insert_note(take, start_beat, duration_beats, pitch, vel):
        s_sec = start_beat * beat_sec
        e_sec = (start_beat + duration_beats) * beat_sec
        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, s_sec)
        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, e_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, int(pitch), int(vel), False)

    # --- Programmatic Subtractive Construction ---
    for bar in range(total_bars):
        bar_start_beat = bar * beats_per_bar
        
        # Determine current song section based on Wodzu's 8-bar blocking
        is_intro      = bar < 8
        is_chorus1    = 8 <= bar < 16
        is_verse_ptA  = 16 <= bar < 20
        is_verse_ptB  = 20 <= bar < 24
        is_chorus2    = 24 <= bar < 32
        
        # Tension transition logic: Delete drums 2 beats before the next section drops
        is_transition_bar = (bar == 7) or (bar == 15) or (bar == 23)
        
        # 1. CHORDS (Plays continuously as the backbone)
        current_chord = chord_1 if (bar % 2 == 0) else chord_2
        for pitch in current_chord:
            insert_note(takes["Chords"], bar_start_beat, beats_per_bar, pitch, velocity_base - 20)
            
        # 2. LEAD (Plays only during peak energy - the Chorus)
        if is_chorus1 or is_chorus2:
            # Simple rhythmic melody pattern
            lead_root = current_chord[0] + 12 # Up an octave
            insert_note(takes["Lead"], bar_start_beat + 0.0, 0.5, lead_root, velocity_base)
            insert_note(takes["Lead"], bar_start_beat + 1.5, 0.5, lead_root + scale_intervals[2], velocity_base)
            insert_note(takes["Lead"], bar_start_beat + 2.5, 1.0, lead_root + scale_intervals[4], velocity_base)

        # 3. BASS (Muted in Intro and Verse Part A to leave room for vocals/create dynamic dip)
        if is_chorus1 or is_verse_ptB or is_chorus2:
            bass_pitch = current_chord[0] - 24 # Down two octaves
            # Follows the kick rhythm
            insert_note(takes["Bass"], bar_start_beat + 0.0, 1.0, bass_pitch, velocity_base)
            insert_note(takes["Bass"], bar_start_beat + 2.5, 1.0, bass_pitch, velocity_base)

        # 4. DRUMS (Sparse in Verse Part A, full everywhere else except Intro)
        if not is_intro:
            for b in range(4): # Loop through the 4 beats of the bar
                beat_pos = bar_start_beat + b
                
                # TRANSITION LOGIC: Wodzu's trick of muting drums right before the drop
                if is_transition_bar and b >= 2:
                    continue # Skip inserting drums for beats 3 and 4 of transition bars
                
                # HI-HATS (8th notes) - Plays everywhere drums are active
                insert_note(takes["Drums"], beat_pos, 0.25, 42, velocity_base - 10)
                insert_note(takes["Drums"], beat_pos + 0.5, 0.25, 42, velocity_base - 30)

                # SNARE (Beats 2 and 4)
                if b == 1 or b == 3:
                    insert_note(takes["Drums"], beat_pos, 0.5, 38, velocity_base)
                
                # KICK (Beats 1 and 2.5) - Muted in Verse Part A!
                if not is_verse_ptA:
                    if b == 0:
                        insert_note(takes["Drums"], beat_pos, 0.5, 36, velocity_base + 10)
                    if b == 2:
                        insert_note(takes["Drums"], beat_pos + 0.5, 0.5, 36, velocity_base + 10)

    # Sort MIDI events for all takes
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created Subtractive Arrangement (Intro, Chorus, Verse A, Verse B, Chorus) over {total_bars} bars at {bpm} BPM in Key {key} {scale}."
