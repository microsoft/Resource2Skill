def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Dynamic Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a humanized, moving slap bassline with octaves, approach notes, 
    and timing offsets inside REAPER.
    """
    import reaper_python as RPR
    import random

    # 1. Music theory lookup tables
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

    # Setup core pitch (Octave 1 or 2 for bass)
    root_val = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 4)) # Default to E
    base_octave = 24 if root_val > 5 else 36 # Keep it in the bass register
    root_midi = base_octave + root_val
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    # 5th degree of the scale (approx 7 semitones, but we use the scale array if possible)
    fifth_interval = scale_intervals[4] if len(scale_intervals) > 4 else 7

    # 2. Set Tempo & Create Track
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 3. Create MIDI Item
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # 4. Generate the Bassline Groove
    # Pattern: 
    # Beat 1: Root (legato, medium vel)
    # Beat 2.5: Octave Slap (staccato, high vel)
    # Beat 3.5: Root Split (staccato, med vel)
    # Beat 4: 5th degree approach (legato, lower vel)
    # Beat 4.75: Ghost/Pickup Octave (staccato, high vel)
    
    notes = [
        {"beat": 0.0,  "pitch": root_midi,                   "dur": 1.0,  "vel": velocity_base},
        {"beat": 1.5,  "pitch": root_midi + 12,              "dur": 0.25, "vel": min(127, velocity_base + 30)}, # Slap
        {"beat": 2.5,  "pitch": root_midi,                   "dur": 0.25, "vel": velocity_base + 5},
        {"beat": 3.0,  "pitch": root_midi + fifth_interval,  "dur": 0.5,  "vel": velocity_base - 10},
        {"beat": 3.75, "pitch": root_midi + 12,              "dur": 0.15, "vel": min(127, velocity_base + 25)}  # Ghost Slap
    ]

    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        for n in notes:
            # Humanize timing: +/- 15ms offset
            timing_offset = random.uniform(-0.015, 0.015) 
            # Ensure we don't push the very first note before 0.0
            if bar == 0 and n["beat"] == 0.0:
                timing_offset = abs(timing_offset)
                
            start_time = (bar_start_beat + n["beat"]) * beat_length_sec + timing_offset
            end_time = start_time + (n["dur"] * beat_length_sec)
            
            # Humanize velocity: +/- 5
            vel_offset = random.randint(-5, 5)
            final_vel = max(1, min(127, n["vel"] + vel_offset))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, n["pitch"], final_vel, True)

    RPR.RPR_MIDI_Sort(take)

    # 5. Add Sound Design & Mix FX
    # Add a synthesizer
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Dial in ReaSynth for a plucky bass sound (short decay/release)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)  # Attack: 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.3)  # Decay: fairly short
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.2)  # Sustain: low
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.2)  # Release: short
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.8)  # Sawtooth mix: high for harmonics
    
    # Add EQ to shape the slap tone
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: Low Shelf boost (weight)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0.0)  # Type: Low Shelf
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 80.0) # Freq: 80Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, 3.0)  # Gain: +3dB
    # Band 4: High Shelf boost (string attack / slap transient)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 2.0)  # Type: High Shelf (approx)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 3000.0) # Freq: 3kHz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, 4.0)  # Gain: +4dB

    return f"Created '{track_name}' (Dynamic Slap Bass) with humanized timing/velocity over {bars} bars in {key} {scale} at {bpm} BPM."
