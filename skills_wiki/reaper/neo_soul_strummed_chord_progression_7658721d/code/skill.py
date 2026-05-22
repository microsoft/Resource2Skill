def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul E.Piano",
    bpm: int = 85,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a Neo-Soul strummed chord progression with lush voicings and a vintage EP tone.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create Media Item and Take ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Music Theory & Harmony Definitions ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave 2 for deep, warm bass notes
    base_pitch = 36 + NOTE_MAP.get(key.capitalize(), 0)

    # Specific Neo-Soul voicings (Intervals from the root)
    # Spaced out to avoid muddiness: Root, 7th, 3rd(octave up), extension(octave up)
    voicings = {
        "min9": [0, 10, 15, 22],   # R, b7, b3, 9
        "maj9": [0, 11, 16, 23],   # R, M7, M3, 9
        "dom13": [0, 10, 16, 21],  # R, b7, M3, 13
        "dom7#9": [0, 10, 16, 27]  # R, b7, M3, #9 (Classic altered tension)
    }

    # Define scales and their corresponding Neo-Soul progressions
    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
    MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]

    # Dynamically select progression based on scale
    if scale.lower() == "major":
        # ii9 - V13 - Imaj9 - VI7#9
        progression = [
            {"degree": MAJOR_SCALE[1], "type": "min9"},
            {"degree": MAJOR_SCALE[4], "type": "dom13"},
            {"degree": MAJOR_SCALE[0], "type": "maj9"},
            {"degree": MAJOR_SCALE[5], "type": "dom7#9"}
        ]
    else:
        # i9 - iv9 - bVIImaj9 - V7#9
        progression = [
            {"degree": MINOR_SCALE[0], "type": "min9"},
            {"degree": MINOR_SCALE[3], "type": "min9"},
            {"degree": MINOR_SCALE[6], "type": "maj9"},
            {"degree": MINOR_SCALE[4], "type": "dom7#9"}
        ]

    # === Step 5: Insert Strummed MIDI Notes ===
    total_notes_created = 0
    strum_delay_sec = 0.035 # 35ms delay between notes for a lazy, natural strum
    
    for b in range(bars):
        chord = progression[b % len(progression)]
        
        # Calculate root pitch and keep it in octave 2
        root = base_pitch + chord["degree"]
        while root >= 48:
            root -= 12
            
        voicing_intervals = voicings[chord["type"]]
        
        chord_start_sec = b * bar_length_sec
        # Sustain almost the whole bar, brief gap for breathing
        chord_end_sec = chord_start_sec + bar_length_sec - 0.05 
        
        for i, interval in enumerate(voicing_intervals):
            note_pitch = root + interval
            
            # Strum timing offset
            note_start_sec = chord_start_sec + (i * strum_delay_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_end_sec)
            
            # Humanize velocity: Root is solid, inner notes soft, top melody note accented
            if i == 0:
                vel = velocity_base
            elif i == len(voicing_intervals) - 1:
                vel = velocity_base + 12
            else:
                vel = velocity_base - 15 + (i * 2)
                
            vel = max(1, min(127, int(vel))) # Clamp velocity 1-127
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_pitch, vel, True)
            total_notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Sound Design (FX Chain) ===
    # 1. Electric Piano Tone using ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Mute harsh saw/square, mix sine and triangle for smooth EP tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0) # Square mix 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.0) # Saw mix 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.8) # Triangle mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.5) # Sine mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.02) # Soft Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.3) # Natural Release

    # 2. Warm Vintage EQ (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 (High Shelf) - Roll off digital highs for lo-fi warmth
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 3000.0) # Freq ~3kHz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, -12.0) # Gain -12dB
    # Band 2 (Band) - Boost warm low-mids
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 3, 400.0) # Freq 400Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 4, 3.5) # Gain +3.5dB

    # 3. Tremolo for Classic Rhodes modulation
    trem_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Tremolo", False, -1)
    if trem_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, trem_idx, 0, 2.5) # Tremolo rate 2.5 Hz
        RPR.RPR_TrackFX_SetParam(track, trem_idx, 1, -4.0) # Tremolo amount

    return f"Created '{track_name}' with {total_notes_created} strummed notes (Jazz voicings) over {bars} bars at {bpm} BPM."
