def create_pattern(
    project_name: str = "Arrangement_Project",
    track_name: str = "Beat",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 20,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Subtractive Arrangement' Beat Structure in REAPER.
    Generates a 20-bar arrangement demonstrating Intro, Chorus, Verse A, Verse B, and a Filter Gap.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Prog: i - VI - III - VII
    chord_prog_degrees = [
        [0, 2, 4], # i
        [5, 7, 9], # VI
        [2, 4, 6], # III
        [6, 8, 10] # VII
    ]

    def get_pitch(degree, octave):
        deg_idx = degree % 7
        oct_offset = degree // 7
        return root_val + scale_intervals[deg_idx] + ((octave + oct_offset) * 12)

    # Calculate timing
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_sec = (60.0 / bpm) * beats_per_bar
    step_sec = bar_sec / 16.0  # 16th notes
    total_length = bars * bar_sec

    # Setup 4 Tracks
    track_names = [f"{track_name}_Chords", f"{track_name}_Lead", f"{track_name}_Bass", f"{track_name}_Drums"]
    takes = {}

    for i, t_name in enumerate(track_names):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_name, True)
        
        # Add a simple synth to make it audible
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        if "Bass" in t_name: # Lower pitch/sine for bass
            RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Square mix down
            RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) # Saw mix down
            RPR.RPR_TrackFX_SetParam(track, 0, 2, 1.0) # Triangle up
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes[t_name] = take

    def insert_note(take, start_t, end_t, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_t)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_t)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Generate Arrangement Block by Block
    # 0-3: Intro | 4-11: Chorus | 12-15: Verse A | 16-18: Verse B | 19: Transition Gap
    for bar in range(bars):
        chord_degs = chord_prog_degrees[bar % 4]
        
        # Determine current arrangement section
        is_intro = bar < 4
        is_chorus = 4 <= bar < 12
        is_verseA = 12 <= bar < 16
        is_verseB = 16 <= bar < 19
        is_gap = bar == 19

        # 1. Chords (Play continuously through all sections)
        for d in chord_degs:
            p = get_pitch(d, 4)
            insert_note(takes[track_names[0]], bar * bar_sec, (bar + 1) * bar_sec, p, velocity_base - 10)
            
        # Transition Gap CC Sweep (Filter closing down on chords)
        if is_gap:
            for step in range(16):
                t_val = (bar * bar_sec) + (step * step_sec)
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(takes[track_names[0]], t_val)
                val = int(127 - (step * (100 / 15))) # Sweep 127 down to 27
                RPR.RPR_MIDI_InsertCC(takes[track_names[0]], False, False, ppq, 176, 0, 74, val)

        # 2. Lead (Only plays during high-energy Chorus)
        if is_chorus:
            for step in [0, 6, 8, 14]: # Syncopated melody
                t_start = (bar * bar_sec) + (step * step_sec)
                t_end = t_start + step_sec
                p = get_pitch(chord_degs[1], 5) # Play the middle note an octave up
                insert_note(takes[track_names[1]], t_start, t_end, p, velocity_base)

        # 3. Bass (Plays in Chorus and Verse B, matches kick rhythm)
        if is_chorus or is_verseB:
            bass_p = get_pitch(chord_degs[0], 2) # Root note, octave 2
            for step in [0, 10]:
                t_start = (bar * bar_sec) + (step * step_sec)
                t_end = t_start + (step_sec * 2)
                insert_note(takes[track_names[2]], t_start, t_end, bass_p, velocity_base + 10)

        # 4. Drums (Subtractive Rules applied)
        if not is_gap and not is_intro:
            for step in range(16):
                t_start = (bar * bar_sec) + (step * step_sec)
                t_end = t_start + step_sec
                
                # Snare (Beats 2 and 4 equivalent in trap halftime: Step 4 and 12)
                if step in [4, 12]:
                    # Snare is the anchor, never subtracted unless it's a transition gap
                    insert_note(takes[track_names[3]], t_start, t_end, 38, velocity_base + 10)
                
                # Kick (Step 0, 10) - Subtracted in Verse A!
                if step in [0, 10] and (is_chorus or is_verseB):
                    insert_note(takes[track_names[3]], t_start, t_end, 36, velocity_base + 20)
                
                # Hi-Hats - Subtracted in Verse A, Halftimed in Verse B!
                if is_chorus:
                    # 16th notes
                    insert_note(takes[track_names[3]], t_start, t_end, 42, velocity_base - 15)
                elif is_verseB:
                    # 8th notes (half-time, opens up space for vocals)
                    if step % 2 == 0:
                        insert_note(takes[track_names[3]], t_start, t_end, 42, velocity_base - 15)

    # Sort MIDI events
    for t_name, take in takes.items():
        RPR.RPR_MIDI_Sort(take)

    return f"Created Subtractive Arrangement '{track_name}' ({bars} bars) at {bpm} BPM with dynamic dropping sections."
