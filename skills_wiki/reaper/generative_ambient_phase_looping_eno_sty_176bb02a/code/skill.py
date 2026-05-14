def create_pattern(
    project_name: str = "Generative Ambient",
    track_name: str = "Eno Phase Loops",
    bpm: int = 90,
    key: str = "C",
    scale: str = "pentatonic_major",
    bars: int = 32, # Generate a long section so the phasing can be heard
    velocity_base: int = 60,
    **kwargs,
) -> str:
    """
    Creates an Eno-style generative ambient track using prime-number phase looping.
    """
    import reaper_python as RPR
    import random

    # 1. Music Theory Setup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Fallback to pentatonic major if an incompatible scale is passed
    # (Pentatonic is highly recommended for generative music to avoid dissonant seconds/tritones)
    if scale not in SCALES:
        scale = "pentatonic_major"

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES[scale]

    # Generate a pool of safe notes spanning 3 octaves (MIDI 48 to 84)
    safe_notes = []
    for octave in [4, 5, 6]:
        for interval in scale_intervals:
            note = (octave * 12) + root_pitch + interval
            safe_notes.append(note)

    # 2. Track & Tempo Setup
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 3. Create MIDI Item
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    total_time = (60.0 / bpm) * total_beats
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_time)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 4. Generative Phase Looping Algorithm
    # Instead of creating separate looping items, we calculate the note positions mathematically.
    # We use prime numbers (or non-multiples) of beats for the loop intervals.
    # This ensures they drift in and out of phase organically over time.
    tape_loops = [
        {"interval_beats": 11.0, "note": random.choice(safe_notes)},
        {"interval_beats": 17.0, "note": random.choice(safe_notes)},
        {"interval_beats": 23.0, "note": random.choice(safe_notes)},
        {"interval_beats": 29.0, "note": random.choice(safe_notes)},
        {"interval_beats": 37.0, "note": random.choice(safe_notes)}
    ]

    ticks_per_quarter = 960 # Standard PPQ in REAPER
    note_length_beats = 4.0 # Long, held notes
    
    note_count = 0
    
    for loop in tape_loops:
        current_beat = 0.0
        # Add an initial random offset so they don't all strike hard on beat 1
        current_beat += random.uniform(0.0, 8.0) 
        
        while current_beat < total_beats:
            start_pos = current_beat
            end_pos = current_beat + note_length_beats
            
            # Slight velocity humanization for realism
            vel = max(30, min(100, velocity_base + random.randint(-15, 15)))
            
            # Convert beats to precise time/PPQ for API insertion
            start_time = (60.0 / bpm) * start_pos
            end_time = (60.0 / bpm) * end_pos
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, loop["note"], vel, False)
            note_count += 1
            
            # Move to the next interval for this specific "tape loop"
            current_beat += loop["interval_beats"]

    # Finalize MIDI insertion
    RPR.RPR_MIDI_Sort(take)

    # 5. Sound Design: Soft Sine/Triangle Synth + Huge Ambient Space
    # Add Synth
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.0)    # Vol
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.0)    # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.0)    # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 1.0)    # Triangle mix (soft tone)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 6, 0.05)   # Attack (slow, ~50ms)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 7, 0.5)    # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 8, 0.8)    # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 9, 0.8)    # Release (very long)

    # Add Delay (Ping Pong)
    fx_delay = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 0, 0.0)    # Tap 1 Wet
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 4, 3.0)    # Tap 1 Length (eighth note)
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 6, 0.4)    # Tap 1 Feedback
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 7, -1.0)   # Tap 1 Pan Left
    
    # Add Reverb (Huge Wash)
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.8)     # Wet
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.2)     # Dry
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.95)    # Room Size (Huge)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 3, 0.7)     # Dampening (Dark)

    return f"Created generative ambient track '{track_name}' in {key} {scale}. Placed {note_count} phasing notes over {bars} bars."
