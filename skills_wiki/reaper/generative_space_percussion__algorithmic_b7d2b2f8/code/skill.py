def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Space Perc",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an algorithmic, generative syncopated percussion pattern washed in reverb.
    Simulates the Reason 'Beat Map' to 'RV7000' workflow natively in REAPER.
    """
    import random
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Calculate Timings ===
    beats_per_bar = 4
    qn_sec = 60.0 / bpm
    item_len = (qn_sec * beats_per_bar) * bars
    
    # Very short notes for percussive plucks
    note_duration_sec = qn_sec * 0.15 

    # === Step 4: Create MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Derive Pitches ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Tune "drums" to the requested scale for a melodic generative feel
    kick_pitch = 36 + root_val                                          # C2 octave (Root)
    snare_pitch = 36 + root_val + scale_intervals[4 % len(scale_intervals)] # 5th degree
    hihat_pitch = 48 + root_val + scale_intervals[2 % len(scale_intervals)] # Octave up + 3rd degree

    # === Step 6: Generative Rhythmic Algorithm ===
    note_count = 0
    
    for bar in range(bars):
        for beat in range(beats_per_bar):
            for div in range(4):  # 16th note subdivisions
                time_sec = (bar * beats_per_bar * qn_sec) + (beat * qn_sec) + (div * 0.25 * qn_sec)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec + note_duration_sec)
                
                # "Kick" logic: Anchor on beats 1 and 3, occasional syncopation
                if beat in [0, 2] and div == 0:
                    vel = min(127, velocity_base + 10)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, kick_pitch, vel, True)
                    note_count += 1
                elif div == 3 and random.random() > 0.75:
                    vel = min(127, int(velocity_base * 0.7))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, kick_pitch, vel, True)
                    note_count += 1
                    
                # "Snare" logic: Anchor on beats 2 and 4, occasional ghost notes
                if beat in [1, 3] and div == 0:
                    vel = min(127, velocity_base + 15)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, snare_pitch, vel, True)
                    note_count += 1
                elif div == 2 and random.random() > 0.85:
                    vel = min(127, int(velocity_base * 0.4))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, snare_pitch, vel, True)
                    note_count += 1
                    
                # "Hi-hat" logic: Emulate "OffBeat" preset. Favor offbeats.
                is_offbeat = (div % 2 != 0)
                prob = 0.85 if is_offbeat else 0.35
                if random.random() < prob:
                    vel = random.randint(int(velocity_base * 0.75), min(127, velocity_base + 5)) if is_offbeat else random.randint(30, 60)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, hihat_pitch, vel, True)
                    note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 7: Sound Design FX Chain ===
    # 1. Add Synth to produce sound from our MIDI
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Add Reverb to create the large atmospheric space (emulating RV7000)
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    
    # Configure Reverb parameters to mimic the "ALL Hall" setting
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.6)  # Wet signal
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.8)  # Dry signal
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.9)  # Room size (Very Large)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 3, 0.4)  # Dampening

    return f"Created '{track_name}' with {note_count} algorithmically generated notes in {key} {scale} over {bars} bars at {bpm} BPM."
