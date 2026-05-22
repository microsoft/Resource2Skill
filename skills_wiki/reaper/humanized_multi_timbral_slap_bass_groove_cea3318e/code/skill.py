def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "GrooveBass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a humanized, multi-track Slap Bass groove.
    Generates two tracks (Fingered and Slapped) to separate the timbres,
    using ReaSynth to synthesize the contrasting tones.
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
        "pentatonic_minor": [0, 3, 5, 7, 10]
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_idx = NOTE_MAP.get(key.capitalize(), 4) # Default to E if missing

    # 2. Set environment
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # 3. Create Main (Fingered) Bass Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    main_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(main_track, "P_NAME", f"{track_name} (Fingered)", True)

    # 4. Create Slap Bass Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    slap_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(slap_track, "P_NAME", f"{track_name} (Slap)", True)

    # 5. Build Sound Design via ReaSynth
    # Track 1: Warm, muted tone (Triangle wave dominant, low filter)
    RPR.RPR_TrackFX_AddByName(main_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(main_track, 0, 0, 0.4)   # Volume
    RPR.RPR_TrackFX_SetParamNormalized(main_track, 0, 4, 0.8)   # Triangle blend
    RPR.RPR_TrackFX_SetParamNormalized(main_track, 0, 11, 0.15) # Filter cutoff (Lowpass)

    # Track 2: Bright, snappy tone (Square/Saw blend, open filter, fast decay)
    RPR.RPR_TrackFX_AddByName(slap_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(slap_track, 0, 0, 0.5)   # Volume
    RPR.RPR_TrackFX_SetParamNormalized(slap_track, 0, 2, 0.3)   # Square blend
    RPR.RPR_TrackFX_SetParamNormalized(slap_track, 0, 3, 0.3)   # Saw blend
    RPR.RPR_TrackFX_SetParamNormalized(slap_track, 0, 7, 0.05)  # Fast decay for transient snap
    RPR.RPR_TrackFX_SetParamNormalized(slap_track, 0, 11, 0.8)  # Filter cutoff (Bright)

    # 6. Create MIDI Items
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_len_sec = beat_len_sec * beats_per_bar
    total_len = bar_len_sec * bars

    main_item = RPR.RPR_AddMediaItemToTrack(main_track)
    RPR.RPR_SetMediaItemInfo_Value(main_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(main_item, "D_LENGTH", total_len)
    main_take = RPR.RPR_AddTakeToMediaItem(main_item)

    slap_item = RPR.RPR_AddMediaItemToTrack(slap_track)
    RPR.RPR_SetMediaItemInfo_Value(slap_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(slap_item, "D_LENGTH", total_len)
    slap_take = RPR.RPR_AddTakeToMediaItem(slap_item)

    # 7. Define 2-bar groove template
    # Format: (beat_position, scale_degree, octave_relative_to_E1, duration_in_beats, default_velocity, track_assignment)
    pattern = [
        # Bar 1: Anchored root, low approach note, single slap, low b7
        (1.0, 0, 0, 0.5, 100, 'main'),
        (2.5, 0, 0, 0.25, 80, 'main'),
        (3.0, 4, -1, 0.5, 90, 'main'),    # Low perfect 5th below root
        (3.5, 0, 1, 0.25, 127, 'slap'),   # The Slap! (High root octave)
        (4.5, 6, -1, 0.25, 85, 'main'),   # Low flat 7th
        (4.75, 0, 0, 0.25, 90, 'main'),   # Syncopated anticipation of bar 2

        # Bar 2: Double slap syncopation, trailing walk-up fill
        (5.0, 0, 0, 0.5, 100, 'main'),
        (6.0, 0, 1, 0.25, 120, 'slap'),   # First Slap
        (6.5, 0, 1, 0.25, 127, 'slap'),   # Second Slap
        (7.5, 2, 0, 0.25, 85, 'main'),    # Walkup: minor 3rd
        (8.0, 3, 0, 0.25, 90, 'main'),    # Walkup: perfect 4th
        (8.5, 4, 0, 0.5, 95, 'main')      # Walkup: perfect 5th leading back to '1'
    ]

    # 8. Generate Notes with Humanization
    notes_created = 0
    for bar in range(0, bars, 2):
        for note in pattern:
            beat, deg, oct, dur, vel, trk_type = note
            
            # Absolute beat position
            abs_beat = (bar * beats_per_bar) + (beat - 1.0)
            if abs_beat >= bars * beats_per_bar:
                continue
                
            # Humanize start timing (simulate natural playing inaccuracy)
            time_offset = random.uniform(-0.03, 0.03)
            if abs_beat == 0.0 and time_offset < 0:
                time_offset = 0.0 # Don't shift the very first note outside the item

            start_pos = (abs_beat + time_offset) * beat_len_sec
            
            # Force staccato lengths ("Shorten it down")
            staccato_multiplier = random.uniform(0.75, 0.90)
            end_pos = start_pos + (dur * beat_len_sec * staccato_multiplier) 

            # Map pitch mathematically
            oct_shift = deg // len(scale_intervals)
            rem_deg = deg % len(scale_intervals)
            # Baseline offset (+2 * 12) pushes "0" to MIDI octave 1 (e.g. E1 = MIDI 28)
            pitch = root_idx + scale_intervals[rem_deg] + (oct + oct_shift + 2) * 12
            
            # Apply dynamic velocity base and randomize slightly
            scaled_vel = int((vel / 100.0) * velocity_base)
            final_vel = min(127, max(1, scaled_vel + random.randint(-6, 6)))
            
            # Select proper track destination
            take = main_take if trk_type == 'main' else slap_take
            
            # Convert seconds to REAPER's PPQ (Pulses Per Quarter Note) for API insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, False)
            notes_created += 1

    # Cleanup MIDI events
    RPR.RPR_MIDI_Sort(main_take)
    RPR.RPR_MIDI_Sort(slap_take)

    return f"Created multi-timbral slap bass groove across 2 tracks with {notes_created} notes over {bars} bars."
