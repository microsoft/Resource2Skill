def create_pattern(
    project_name: str = "Arrangement_Template",
    track_name: str = "Subtractive_Beat",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar Subtractive Beat Arrangement in the current REAPER project.
    Bars 1-4: Chorus (Full Energy)
    Bars 5-8: Verse A (Sparse - No kick/hats)
    Bars 9-12: Verse B (Build up - Half-time hats, ending in a dropout gap)
    """
    
    import reaper_python as RPR

    # --- Music Theory & Mappings ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 48 # Base octave 3

    # Define a simple i - VI - iv - v chord progression based on scale degrees
    # Array of [Root degree, Third degree, Fifth degree]
    progression_degrees = [
        [0, 2, 4], # i
        [5, 0, 2], # VI
        [3, 5, 0], # iv
        [4, 6, 1]  # v
    ]

    # --- Step 1: Set Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    total_length_sec = bar_sec * bars

    # --- Helper Function for MIDI Insertion ---
    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # ==========================================
    # --- Step 2: Create Drum Track & Item ---
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Standard MIDI Drum Map
    KICK = 36
    SNARE = 38
    HAT = 42

    # Loop through each bar to create the subtractive arrangement
    for bar in range(bars):
        bar_start = bar * bar_sec
        
        # Determine current section structure
        is_chorus = bar < 4
        is_verse_a = 4 <= bar < 8
        is_verse_b = 8 <= bar < 12
        is_last_bar = (bar == 11)
        
        # 1. KICK (Beat 1 and Beat 2.5)
        # Subtractive logic: Omit kick entirely in Verse A
        if not is_verse_a:
            kick_beats = [0, 2.5]
            for b in kick_beats:
                # GAP TRANSITION: Skip last 2 beats of the final bar
                if is_last_bar and b >= 2.0:
                    continue
                start_t = bar_start + (b * beat_sec)
                insert_note(drum_take, start_t, start_t + (beat_sec*0.5), KICK, velocity_base)

        # 2. SNARE (Beat 2 and Beat 4)
        # Snare drives the rhythm, so it stays in all sections (until the gap)
        snare_beats = [1.0, 3.0] # 0-indexed beats (1.0 = beat 2)
        for b in snare_beats:
            if is_last_bar and b >= 2.0:
                continue
            start_t = bar_start + (b * beat_sec)
            insert_note(drum_take, start_t, start_t + (beat_sec*0.5), SNARE, velocity_base)

        # 3. HI-HAT
        # Subtractive logic: Omit in Verse A. Half-speed in Verse B. Full speed in Chorus.
        if is_chorus:
            hat_beats = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5] # 8th notes
        elif is_verse_b:
            hat_beats = [0.0, 1.0, 2.0, 3.0] # Quarter notes (Half-time stretched)
        else:
            hat_beats = [] # Omitted in Verse A
            
        for b in hat_beats:
            if is_last_bar and b >= 2.0:
                continue
            start_t = bar_start + (b * beat_sec)
            vel = velocity_base if b % 1.0 == 0 else velocity_base - 20 # Slight groove
            insert_note(drum_take, start_t, start_t + (beat_sec*0.25), HAT, vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # ==========================================
    # --- Step 3: Create Chords Track & Item ---
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name}_Chords", True)

    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_length_sec)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    # Generate sustained chords mapping to the sections
    for bar in range(bars):
        bar_start = bar * bar_sec
        prog_idx = bar % 4
        degrees = progression_degrees[prog_idx]
        
        # Calculate literal MIDI notes for this chord
        chord_notes = []
        for d in degrees:
            octave_shift = 12 if d < degrees[0] else 0 # Simple inversion to keep voicing tight
            pitch = root_pitch + scale_intervals[d % len(scale_intervals)] + octave_shift
            chord_notes.append(pitch)
            
        is_last_bar = (bar == 11)
        
        # GAP TRANSITION: Cut chord off early on the last bar
        end_time = bar_start + bar_sec
        if is_last_bar:
            end_time = bar_start + (2.0 * beat_sec) # Cut off on Beat 3

        for pitch in chord_notes:
            insert_note(chord_take, bar_start, end_time, pitch, velocity_base - 15)

    RPR.RPR_MIDI_Sort(chord_take)

    return f"Created Subtractive Arrangement: 12 bars at {bpm}BPM in {key} {scale}. Features Chorus -> Subtractive Verse -> Build -> Gap Transition."
