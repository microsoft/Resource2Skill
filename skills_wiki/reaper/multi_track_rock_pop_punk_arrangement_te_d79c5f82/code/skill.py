def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Arrangement",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock/Pop-Punk Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored, track names are hardcoded to band roles).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Build Diatonic Multi-Octave Scale ===
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_val = NOTE_MAP.get(key, 0)
    
    full_scale = []
    # Build array from C-2 to C8
    for oct in range(-2, 8):
        for interval in scale_intervals:
            full_scale.append(root_val + oct * 12 + interval)

    # Find the index of the root note in octave 3 (base MIDI 48)
    base_idx = 0
    while full_scale[base_idx] < 48:
        base_idx += 1

    # === Step 3: Create Tracks & Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    band_tracks = ["Drums", "Bass", "Rhythm Guitar", "Lead Guitar"]
    takes = {}

    for name in band_tracks:
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        takes[name] = take

    # Helper function to insert notes accurately
    def insert_note(take, beat_pos, beat_len, pitch, vel):
        pos_sec = beat_pos * (60.0 / bpm)
        end_sec = (beat_pos + beat_len) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Standard progression: 1 - 5 - 6 - 4 (scale degrees relative to root)
    progression = [0, 4, 5, 3] 

    # === Step 4: Populate MIDI Notes ===
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        bar_beat = bar * 4.0

        # --- 1. RHYTHM GUITAR ---
        # Sustained triad block chords (Root, 3rd, 5th of current scale degree)
        for note_offset in [0, 2, 4]:
            pitch = full_scale[base_idx + degree + note_offset]
            insert_note(takes["Rhythm Guitar"], bar_beat, 4.0, pitch, velocity_base - 10)

        # --- 2. BASS ---
        # Driving 8th notes, 1 octave down (-7 scale degrees)
        bass_base = base_idx - 7 + degree
        bass_pitch = full_scale[bass_base]
        for eighth in range(8):
            insert_note(takes["Bass"], bar_beat + eighth * 0.5, 0.45, bass_pitch, velocity_base)

        # --- 3. LEAD GUITAR ---
        # Arpeggio pattern (Root, 3rd, 5th, 3rd), 1 octave up (+7 scale degrees)
        lead_base = base_idx + 7 + degree
        arp_offsets = [0, 2, 4, 2, 0, 2, 4, 2]
        for eighth in range(8):
            pitch = full_scale[lead_base + arp_offsets[eighth]]
            insert_note(takes["Lead Guitar"], bar_beat + eighth * 0.5, 0.45, pitch, velocity_base - 15)

        # --- 4. DRUMS ---
        # Kick (36) on 1, 2-and, 3-and (Syncopated Rock Groove)
        insert_note(takes["Drums"], bar_beat + 0.0, 0.25, 36, velocity_base + 10)
        insert_note(takes["Drums"], bar_beat + 1.5, 0.25, 36, velocity_base)
        insert_note(takes["Drums"], bar_beat + 2.5, 0.25, 36, velocity_base)

        # Snare (38) strictly on 2 and 4
        insert_note(takes["Drums"], bar_beat + 1.0, 0.25, 38, velocity_base + 15)
        insert_note(takes["Drums"], bar_beat + 3.0, 0.25, 38, velocity_base + 15)

        # Hi-hat (42) riding straight 8th notes with alternating velocities
        for eighth in range(8):
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 20
            insert_note(takes["Drums"], bar_beat + eighth * 0.5, 0.2, 42, vel)

        # Crash (49) on the downbeat of the 1st bar of every 4-bar phrase
        if bar % 4 == 0:
            insert_note(takes["Drums"], bar_beat + 0.0, 0.5, 49, velocity_base + 20)

    # Sort all MIDI items to ensure proper playback
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track rock arrangement ({bars} bars, {key} {scale}, {bpm} BPM) with dynamic routing roles."
