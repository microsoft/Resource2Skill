def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groove Bass",
    bpm: int = 115,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a groovy, syncopated slap bassline split across two tracks (Body and Slap)
    with staccato note lengths and humanized timing, as shown in the tutorial.
    """
    import reaper_python as RPR
    import random

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

    # === Step 1: Initialize Setup & Calculations ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Calculate pitches (Bass typically sits in octave 1 or 2)
    # E1 = MIDI 28. C1 = MIDI 24.
    base_note = NOTE_MAP.get(key, 0) + 24 
    octave_note = base_note + 12
    
    # Get the 7th degree for the walk-up (default to flat 7 if scale not found/short)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    passing_interval = scale_intervals[6] if len(scale_intervals) > 6 else 10
    passing_note = base_note + passing_interval

    beat_length_sec = 60.0 / bpm
    sixteenth_sec = beat_length_sec / 4.0
    item_length_sec = beat_length_sec * 4 * bars

    # === Step 2: Create Track 1 (Bass Body) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_body = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_body, "P_NAME", f"{track_name} - Body", True)
    
    # Setup ReaSynth for the deep, plucky body
    RPR.RPR_TrackFX_AddByName(track_body, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_body, 0, 0, 0.6)  # Volume
    RPR.RPR_TrackFX_SetParam(track_body, 0, 1, 0.0)  # Tuning
    RPR.RPR_TrackFX_SetParam(track_body, 0, 2, 0.0)  # Square mix (0 = pure sine/saw)
    RPR.RPR_TrackFX_SetParam(track_body, 0, 3, 0.3)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track_body, 0, 4, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(track_body, 0, 5, 0.2)  # Decay (Moderate)
    RPR.RPR_TrackFX_SetParam(track_body, 0, 6, 0.1)  # Sustain
    
    # Create MIDI Item for Body
    item_body = RPR.RPR_AddMediaItemToTrack(track_body)
    RPR.RPR_SetMediaItemInfo_Value(item_body, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_body, "D_LENGTH", item_length_sec)
    take_body = RPR.RPR_AddTakeToMediaItem(item_body)

    # === Step 3: Create Track 2 (Bass Slap) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_slap = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_slap, "P_NAME", f"{track_name} - Slaps", True)
    
    # Setup ReaSynth for the bright, percussive slaps
    RPR.RPR_TrackFX_AddByName(track_slap, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 0, 0.5)   # Volume
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 2, 0.8)   # Square mix (Bright, aggressive)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 4, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 5, 0.05)  # Decay (Extremely fast pluck)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 6, 0.0)   # Sustain
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 7, 0.05)  # Release
    
    # Create MIDI Item for Slap
    item_slap = RPR.RPR_AddMediaItemToTrack(track_slap)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_LENGTH", item_length_sec)
    take_slap = RPR.RPR_AddTakeToMediaItem(item_slap)

    # === Step 4: Generate the Musical Pattern ===
    notes_created = 0
    
    for b in range(bars):
        bar_start_sec = b * 4 * beat_length_sec
        
        # Step map: (16th_step_index, pitch, length_in_16ths, velocity)
        body_pattern = [
            (0, base_note, 2.0, velocity_base),                 # Beat 1.0 (Downbeat)
            (3, base_note, 1.5, int(velocity_base * 0.85)),     # Beat 1.75 (Syncopated)
            (8, base_note, 2.0, velocity_base),                 # Beat 3.0 (Downbeat)
            (11, base_note, 1.5, int(velocity_base * 0.85)),    # Beat 3.75 (Syncopated)
            (15, passing_note, 1.0, int(velocity_base * 0.90)), # Beat 4.75 (Walk-up)
        ]
        
        slap_pattern = [
            (6, octave_note, 1.0, 127),                         # Beat 2.5 (Slap)
            (14, octave_note, 1.0, 127),                        # Beat 4.5 (Slap)
        ]
        
        # Insert Body Notes
        for step, pitch, length, vel in body_pattern:
            # Add humanization (-10ms to +15ms)
            human_offset = random.uniform(-0.010, 0.015)
            pos_sec = max(0, bar_start_sec + (step * sixteenth_sec) + human_offset)
            
            # Create extreme staccato effect by shortening actual duration
            end_sec = pos_sec + (length * sixteenth_sec) - 0.02 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_body, pos_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_body, end_sec)
            
            # Minor velocity humanization
            human_vel = max(1, min(127, vel + random.randint(-5, 5)))
            
            RPR.RPR_MIDI_InsertNote(take_body, False, False, start_ppq, end_ppq, 0, pitch, human_vel, True)
            notes_created += 1

        # Insert Slap Notes
        for step, pitch, length, vel in slap_pattern:
            # Slaps are slightly laid back (behind the beat)
            human_offset = random.uniform(0.005, 0.020)
            pos_sec = bar_start_sec + (step * sixteenth_sec) + human_offset
            end_sec = pos_sec + (length * sixteenth_sec) - 0.01
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_slap, pos_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_slap, end_sec)
            
            RPR.RPR_MIDI_InsertNote(take_slap, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            notes_created += 1

    # Sort MIDI events after batch insertion
    RPR.RPR_MIDI_Sort(take_body)
    RPR.RPR_MIDI_Sort(take_slap)

    return f"Created split-track Groove Bass (Body + Slaps) with {notes_created} humanized notes over {bars} bars in {key} {scale} at {bpm} BPM."
