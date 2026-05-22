def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Funky Slap Bass",
    bpm: int = 115,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a groovy, syncopated slap bassline in the current REAPER project.
    Features split lengths, octave slaps, passing tones, and humanized timing/velocity.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_pitch = NOTE_MAP.get(key.upper(), 4) + 24 # +24 puts it in the E1/C2 bass range

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & FX Chain ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for basic tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set synth params for a punchy, plucked bass
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7)  # Mix: Sawtooth/Square blend
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)  # Attack: 0ms (Instant punch)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.15) # Decay: Short
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.2)  # Sustain: Low
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.1)  # Release: Short

    # Add ReaComp to tame the harsh octave slaps and glue the groove
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -15.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio 4:1
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 3.0)   # Attack 3ms
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 50.0)  # Release 50ms

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = (bars * beats_per_bar) * sec_per_beat
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Define the Groove Pattern ===
    # Tuple format: (Beat_Position, Length_in_beats, Scale_Degree, Octave_Shift, Velocity_Multiplier)
    # 1 Beat = 1 Quarter note.
    groove_pattern = [
        (0.0,  0.5,   0,  0, 1.0),   # Downbeat root
        (0.75, 0.25,  0,  0, 0.8),   # Syncopated split 1
        (1.5,  0.25,  0,  0, 0.8),   # Syncopated split 2
        (1.75, 0.125, 0,  1, 1.25),  # SLAP! (Octave up, very short, max vel)
        (2.0,  0.5,   0,  0, 0.9),   # Beat 3 anchor
        (2.75, 0.125, 0,  1, 1.25),  # SLAP!
        (3.0,  0.25,  4,  0, 0.85),  # Passing tone (5th) step towards next bar
        (3.5,  0.25,  0,  0, 0.7),   # Ghost note root
        (3.75, 0.125, 0,  1, 1.25),  # SLAP! leading into the downbeat
    ]

    # === Step 5: Generate and Humanize MIDI Notes ===
    for bar in range(bars):
        # Alternate root note between I (0) and IV (3) scale degrees for a standard funk progression
        chord_root_deg = 0 if bar % 2 == 0 else 3 

        for beat_pos, length, scale_offset, octave_shift, vel_mult in groove_pattern:
            
            # Calculate pitch
            # If chord root changes, we transpose the whole pattern, but ensure passing tones remain in scale
            deg_idx = (chord_root_deg + scale_offset) % len(scale_intervals)
            octave_base = (chord_root_deg + scale_offset) // len(scale_intervals)
            
            pitch = base_pitch + scale_intervals[deg_idx] + (octave_base * 12) + (octave_shift * 12)
            
            # Calculate velocity
            vel = int(velocity_base * vel_mult)
            vel = max(1, min(127, vel + random.randint(-4, 4))) # Slight velocity randomization

            # Calculate timing (with "imitate reality" offset)
            base_beat = (bar * beats_per_bar) + beat_pos
            start_sec = base_beat * sec_per_beat
            end_sec = start_sec + (length * sec_per_beat)

            # Humanize timing: +/- up to 10ms
            timing_offset = random.uniform(-0.010, 0.010)
            start_sec = max(0, start_sec + timing_offset)
            end_sec = max(0.01, end_sec + timing_offset)

            # Convert to PPQ for exact MIDI placement
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, None)

    # Finalize MIDI data
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {len(groove_pattern) * bars} humanized groove notes over {bars} bars at {bpm} BPM in {key} {scale}."
