def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "AltRock",
    bpm: int = 140,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Alt-Rock Arrangement (Drums, Bass, Rhythm, Lead) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the operation.
    """
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

    import reaper_python as RPR

    # === Step 1: Initialization & Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    cursor_pos = RPR.RPR_GetCursorPosition()
    
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4
    total_len = bar_len * bars
    
    # === Step 2: Create Tracks and Media Items ===
    track_labels = ["Drums", "Bass", "Rhythm Gtr", "Lead Gtr"]
    takes = {}
    tracks = {}
    
    idx = RPR.RPR_CountTracks(0)
    for label in track_labels:
        full_name = f"{track_name} {label}"
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        tracks[label] = track
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_name, True)
        
        # Add basic synths to tonal tracks for immediate audibility
        if label != "Drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Lower volume of ReaSynth slightly to prevent clipping
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes[label] = take
        idx += 1

    # === Helper Function: Add Note ===
    def add_note(take, pitch, start_beat, end_beat, velocity):
        start_time = cursor_pos + start_beat * beat_len
        end_time = cursor_pos + end_beat * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    # === Step 3: Music Theory Calculation ===
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Base C3
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Progression: vi - IV - I - V (Major) or i - VI - III - VII (Minor)
    chord_degrees = [5, 3, 0, 4] if scale == "major" else [0, 5, 2, 6]

    # === Step 4: Populate MIDI Sequences ===
    for b in range(bars):
        bar_start_beat = b * 4.0
        degree = chord_degrees[b % 4]
        
        # Diatonic calculations
        octave_offset = (degree // len(scale_intervals)) * 12
        local_degree = degree % len(scale_intervals)
        
        chord_root = root_pitch + scale_intervals[local_degree] + octave_offset
        
        # Power chords use a perfect 5th (+7) universally in rock
        chord_fifth = chord_root + 7 
        chord_octave = chord_root + 12
        
        # Third is required for the arpeggio
        third_degree = (local_degree + 2) % len(scale_intervals)
        third_octave_offset = 12 if (local_degree + 2) >= len(scale_intervals) else 0
        chord_third = root_pitch + scale_intervals[third_degree] + octave_offset + third_octave_offset

        # 1. DRUMS
        if b == 0:
            add_note(takes["Drums"], 49, 0.0, 0.5, velocity_base + 20) # Crash on Bar 1
        
        add_note(takes["Drums"], 36, bar_start_beat + 0.0, bar_start_beat + 0.25, velocity_base + 10) # Kick
        add_note(takes["Drums"], 36, bar_start_beat + 2.0, bar_start_beat + 0.25, velocity_base + 10) # Kick
        add_note(takes["Drums"], 36, bar_start_beat + 2.5, bar_start_beat + 0.25, velocity_base)      # Kick Syncopation
        
        add_note(takes["Drums"], 38, bar_start_beat + 1.0, bar_start_beat + 0.25, velocity_base + 15) # Snare
        add_note(takes["Drums"], 38, bar_start_beat + 3.0, bar_start_beat + 0.25, velocity_base + 15) # Snare
        
        for i in range(8): # 8th note Hi-Hats
            add_note(takes["Drums"], 42, bar_start_beat + i * 0.5, bar_start_beat + i * 0.5 + 0.25, velocity_base - 10)

        # 2. BASS
        bass_note = chord_root - 12 # Drop an octave
        for i in range(8):
            start = bar_start_beat + i * 0.5
            add_note(takes["Bass"], bass_note, start, start + 0.45, velocity_base)

        # 3. RHYTHM GUITAR
        for i in range(8):
            start = bar_start_beat + i * 0.5
            add_note(takes["Rhythm Gtr"], chord_root, start, start + 0.45, velocity_base - 5)
            add_note(takes["Rhythm Gtr"], chord_fifth, start, start + 0.45, velocity_base - 5)
            add_note(takes["Rhythm Gtr"], chord_octave, start, start + 0.45, velocity_base - 5)

        # 4. LEAD GUITAR
        arp_pattern = [chord_root + 12, chord_fifth + 12, chord_third + 12, chord_fifth + 12]
        for i in range(8):
            start = bar_start_beat + i * 0.5
            note = arp_pattern[i % 4]
            add_note(takes["Lead Gtr"], note, start, start + 0.45, velocity_base - 15)

    # Sort MIDI items to finalize
    for label, take in takes.items():
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track Alt-Rock arrangement '{track_name}' spanning {bars} bars at {bpm} BPM in {key} {scale}."
