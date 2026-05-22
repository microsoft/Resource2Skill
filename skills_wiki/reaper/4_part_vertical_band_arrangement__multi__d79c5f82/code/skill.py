def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Band Arrangement",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-part Band Arrangement Scaffold in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated setup.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the multi-track loop.
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

    # Ensure valid inputs
    key = key if key in NOTE_MAP else "C"
    scale = scale if scale in SCALES else "minor"
    root_pitch = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # Helper function to get correct MIDI pitch for a scale degree
    def get_pitch(degree, octave):
        scale_len = len(scale_intervals)
        octaves_shifted = degree // scale_len
        scale_index = degree % scale_len
        return root_pitch + ((octave + octaves_shifted) * 12) + scale_intervals[scale_index]

    # Define the 4-bar chord progression based on scale flavor
    if scale in ["major", "mixolydian", "pentatonic_major"]:
        progression = [0, 4, 5, 3]  # I - V - vi - IV
    else:
        progression = [0, 5, 2, 6]  # i - VI - III - VII

    # === Global Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_length = bar_len * bars
    
    # Helper to calculate PPQ
    def insert_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        # Ensure velocities are within 1-127
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, False)

    # Track Configurations (Name, RGB Color, Octave)
    # Custom colors in REAPER: 0x1000000 | R | (G << 8) | (B << 16)
    tracks_config = [
        {"name": "1. DRUMS (MIDI)", "r": 90, "g": 50, "b": 150, "octave": 0},    # Indigo
        {"name": "2. BASS", "r": 200, "g": 80, "b": 200, "octave": 2},           # Violet
        {"name": "3. GTR RHY", "r": 255, "g": 140, "b": 0, "octave": 4},         # Orange
        {"name": "4. GTR LEAD", "r": 0, "g": 200, "b": 220, "octave": 5}         # Teal
    ]

    total_notes_added = 0
    start_track_idx = RPR.RPR_CountTracks(0)

    for i, cfg in enumerate(tracks_config):
        # Create Track
        idx = start_track_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Apply Name & Color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", cfg["name"], True)
        color_val = 0x1000000 | cfg["r"] | (cfg["g"] << 8) | (cfg["b"] << 16)
        RPR.RPR_SetTrackColor(track, color_val)

        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length, False)
        take = RPR.RPR_GetActiveTake(item)

        # Generate MIDI Notes per Bar
        for b in range(bars):
            bar_start = b * bar_len
            chord_degree = progression[b % len(progression)]
            
            if "DRUMS" in cfg["name"]:
                # Standard GM Drum Pattern (Kick: 36, Snare: 38, Hat: 42)
                # Kick on 1, 2-AND, 3, 4-AND (syncopated)
                kick_beats = [0.0, 1.5, 2.0, 3.5]
                for kb in kick_beats:
                    insert_note(take, bar_start + (kb * beat_len), bar_start + ((kb + 0.25) * beat_len), 36, velocity_base)
                    total_notes_added += 1
                
                # Snare on 2 and 4
                snare_beats = [1.0, 3.0]
                for sb in snare_beats:
                    insert_note(take, bar_start + (sb * beat_len), bar_start + ((sb + 0.25) * beat_len), 38, velocity_base + 10)
                    total_notes_added += 1
                
                # Hi-Hats every 8th note
                for hb in range(8):
                    beat_pos = hb * 0.5
                    insert_note(take, bar_start + (beat_pos * beat_len), bar_start + ((beat_pos + 0.25) * beat_len), 42, velocity_base - 20)
                    total_notes_added += 1

            elif "BASS" in cfg["name"]:
                # Syncopated Root Notes locking in with the Kick Drum
                bass_pitch = get_pitch(chord_degree, cfg["octave"])
                bass_beats = [0.0, 1.5, 2.0, 3.5]
                for bb in bass_beats:
                    insert_note(take, bar_start + (bb * beat_len), bar_start + ((bb + 0.4) * beat_len), bass_pitch, velocity_base)
                    total_notes_added += 1
                
                # Add basic ReaSynth tuned to bass frequencies
                RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

            elif "RHY" in cfg["name"]:
                # Block Chords (Root, 3rd, 5th) sustained for the whole bar
                root = get_pitch(chord_degree, cfg["octave"])
                third = get_pitch(chord_degree + 2, cfg["octave"])
                fifth = get_pitch(chord_degree + 4, cfg["octave"])
                
                for pitch in [root, third, fifth]:
                    insert_note(take, bar_start, bar_start + bar_len - 0.05, pitch, velocity_base - 15)
                    total_notes_added += 1
                    
                RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

            elif "LEAD" in cfg["name"]:
                # Arpeggiated melody over the chord (Root, 5th, Octave, 3rd)
                arp_degrees = [chord_degree, chord_degree + 4, chord_degree + 7, chord_degree + 2]
                for i, arp_deg in enumerate(arp_degrees):
                    p = get_pitch(arp_deg, cfg["octave"])
                    start = bar_start + (i * beat_len)
                    insert_note(take, start, start + (beat_len * 0.8), p, velocity_base)
                    total_notes_added += 1
                    
                RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Sort MIDI events to ensure proper playback
        RPR.RPR_MIDI_Sort(take)

    return f"Created multi-track loop '{track_name}' (4 tracks, {total_notes_added} MIDI events) over {bars} bars at {bpm} BPM in {key} {scale}."
