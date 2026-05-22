def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "West Coast Layer",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates an Old School West Coast Groove featuring a 2-octave split piano, 
    tension strings, and a humanized swing drum pattern.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (90 recommended for this style).
        key: Root note (e.g., C, D#).
        scale: Scale type (e.g., minor, harmonic_minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), defaults to high (110) for harsh hits.
    """
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

    # Extract base pitches
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    root_pitch = root_val + 36 # Base Octave 2
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # Pitch calculators based on scale degrees
    p_root = root_pitch + scale_intervals[0]
    p_m3 = root_pitch + scale_intervals[2 % len(scale_intervals)]
    p_2 = root_pitch + scale_intervals[1 % len(scale_intervals)]
    p_b7 = root_pitch - 12 + scale_intervals[6 % len(scale_intervals)]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper: Create Track
    def create_midi_track(name):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        trk = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        return trk

    # Helper: Add MIDI Item and Take
    def add_midi_item(trk, start_qn, end_qn):
        start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
        item = RPR.RPR_CreateNewMIDIItemInProj(trk, start_time, end_time, False)
        return RPR.RPR_GetActiveTake(item)

    # Helper: Add Note
    def add_note(take, start_qn, dur_qn, pitch, vel, chan=0):
        start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + dur_qn)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        # Ensure valid velocity
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), vel, True)

    total_qn = bars * 4.0

    # === Step 2: Track 1 - Split Piano Layer ===
    trk_piano = create_midi_track(f"{track_name}_Pluck")
    RPR.RPR_TrackFX_AddByName(trk_piano, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(trk_piano, 0, 2, 0.4)  # Saw mix
    RPR.RPR_TrackFX_SetParam(trk_piano, 0, 5, 0.0)  # Attack (Fast for harsh hit)
    RPR.RPR_TrackFX_SetParam(trk_piano, 0, 6, 0.25) # Decay
    RPR.RPR_TrackFX_SetParam(trk_piano, 0, 7, 0.05) # Sustain (Low)
    RPR.RPR_TrackFX_SetParam(trk_piano, 0, 8, 0.3)  # Release
    
    take_piano = add_midi_item(trk_piano, 0.0, total_qn)

    # === Step 3: Track 2 - High Tension Strings ===
    trk_strings = create_midi_track(f"{track_name}_Strings")
    RPR.RPR_TrackFX_AddByName(trk_strings, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(trk_strings, 0, 2, 1.0)  # Saw mix (100% for classic Juno vibe)
    RPR.RPR_TrackFX_SetParam(trk_strings, 0, 5, 0.5)  # Attack (Slow/swelling)
    RPR.RPR_TrackFX_SetParam(trk_strings, 0, 6, 0.5)  # Decay
    RPR.RPR_TrackFX_SetParam(trk_strings, 0, 7, 0.9)  # Sustain (High)
    RPR.RPR_TrackFX_SetParam(trk_strings, 0, 8, 0.7)  # Release (Long)
    
    take_strings = add_midi_item(trk_strings, 0.0, total_qn)

    # === Step 4: Track 3 - Swinging Drums ===
    trk_drums = create_midi_track(f"{track_name}_Drums")
    take_drums = add_midi_item(trk_drums, 0.0, total_qn)

    # === Generate Patterns ===
    for b in range(bars):
        bar_start = b * 4.0

        # --- Piano Motif ---
        # Timing (QN): Beat 1, Beat 2.5, Beat 3.5, Beat 4.5 (syncopated)
        notes = [
            (0.0, 1.0, p_root),
            (1.5, 0.5, p_m3),
            (2.0, 1.0, p_2),
            (3.5, 0.5, p_b7)
        ]

        for st, dur, p in notes:
            # Low Register (Harsh velocity)
            add_note(take_piano, bar_start + st, dur, p, velocity_base)
            # High Register (+24 semitones, slightly softer to prevent harshness)
            add_note(take_piano, bar_start + st, dur, p + 24, velocity_base - 15)

        # --- High Strings Motif ---
        # 3 Octaves up (+36 semitones), sustained for the entire bar
        add_note(take_strings, bar_start, 4.0, p_root + 36, velocity_base - 30)

        # --- Drum Groove (GM Map, Chan 9) ---
        # Kicks (36): Hard hits on 1, 2.5, 3.5
        add_note(take_drums, bar_start + 0.0, 0.25, 36, velocity_base, chan=9)
        add_note(take_drums, bar_start + 1.5, 0.25, 36, velocity_base - 10, chan=9)
        add_note(take_drums, bar_start + 2.5, 0.25, 36, velocity_base, chan=9)
        
        # Claps/Snares (39): Steady on 2 and 4
        add_note(take_drums, bar_start + 1.0, 0.25, 39, velocity_base, chan=9)
        add_note(take_drums, bar_start + 3.0, 0.25, 39, velocity_base, chan=9)
        
        # Hi-Hats (42): 8th notes with delayed off-beats for "sluggish" swing
        swing_delay_qn = 0.08 
        for i in range(8):
            hat_qn = i * 0.5
            vel = velocity_base if (i % 2 == 0) else velocity_base - 25
            
            # If off-beat, shift it late
            if i % 2 != 0:
                hat_qn += swing_delay_qn
                
            add_note(take_drums, bar_start + hat_qn, 0.1, 42, vel, chan=9)

    # Sort MIDI items
    RPR.RPR_MIDI_Sort(take_piano)
    RPR.RPR_MIDI_Sort(take_strings)
    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created '{track_name}' (Piano, Strings, Drums) with West Coast swing over {bars} bars at {bpm} BPM in {key} {scale}."
