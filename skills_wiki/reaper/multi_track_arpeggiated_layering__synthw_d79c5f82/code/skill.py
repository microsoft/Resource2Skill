def create_pattern(
    project_name: str = "Arrangement_Scaffold",
    track_name: str = "Layered",
    bpm: int = 120,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Arpeggiated Layering Scaffold (Drums, Bass, Rhythm, Lead).

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (unused directly as we spawn 4 specific tracks).
        bpm: Tempo in BPM.
        key: Root note (e.g., "D").
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # --- Music Theory & Pitch Calculation ---
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

    root_note_num = NOTE_MAP.get(key, 2) # Default to D
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Classic vi - IV - I - V progression (0-indexed scale degrees)
    # E.g., in D Major: Bm (5), G (3), D (0), A (4)
    progression = [5, 3, 0, 4] 

    def get_scale_pitch(degree, octave=4):
        """Returns the exact MIDI note for a given scale degree (handles octaves automatically)."""
        scale_length = len(scale_intervals)
        octave_offset = degree // scale_length
        scale_degree = degree % scale_length
        pitch = root_note_num + scale_intervals[scale_degree] + (octave + octave_offset) * 12
        return max(0, min(127, pitch))

    # --- Setup Timing ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    qn_sec = 60.0 / bpm
    bar_length_sec = qn_sec * 4.0
    total_length_sec = bar_length_sec * bars

    # --- Setup Tracks ---
    track_names = ["Drums", "Bass", "Rhythm GTR", "Lead Arp"]
    takes = {}
    
    for name in track_names:
        # Add tracks at the end of the project
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        
        # Name track & lower volume to prevent master bus clipping (-10dB approx = 0.3)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(tr, "D_VOL", 0.3)
        
        # Create MIDI Item and get Take
        item = RPR.RPR_CreateNewMIDIItemInProj(tr, 0.0, total_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        takes[name] = take
        
        # Add stock synths to melodic tracks
        if name != "Drums":
            RPR.RPR_TrackFX_AddByName(tr, "ReaSynth", False, -1)

    # --- MIDI Insertion Helper ---
    def add_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- Generate Arrangement ---
    for b in range(bars):
        degree = progression[b % len(progression)]
        
        # Compute triad
        root_pitch = get_scale_pitch(degree, octave=4)
        third_pitch = get_scale_pitch(degree + 2, octave=4)
        fifth_pitch = get_scale_pitch(degree + 4, octave=4)

        bar_start = b * bar_length_sec

        # 1. DRUMS (Standard rock/synthwave 4/4)
        # Kicks on 1 & 3
        for beat in [0, 2]:
            add_note(takes["Drums"], bar_start + beat * qn_sec, bar_start + beat * qn_sec + 0.1, 36, velocity_base)
        # Snares on 2 & 4
        for beat in [1, 3]:
            add_note(takes["Drums"], bar_start + beat * qn_sec, bar_start + beat * qn_sec + 0.1, 38, velocity_base)
        # Hi-hats every 8th note
        for i in range(8):
            add_note(takes["Drums"], bar_start + i * (qn_sec/2), bar_start + i * (qn_sec/2) + 0.05, 42, velocity_base - 20)

        # 2. BASS (Driving 8th notes, 2 octaves down)
        bass_pitch = root_pitch - 24
        for i in range(8):
            n_start = bar_start + i * (qn_sec/2)
            n_end = n_start + (qn_sec/2) * 0.85 # Slight gap for staccato rhythm
            add_note(takes["Bass"], n_start, n_end, bass_pitch, velocity_base)

        # 3. RHYTHM GTR (Sustained whole note chords, 1 octave down)
        add_note(takes["Rhythm GTR"], bar_start, bar_start + bar_length_sec, root_pitch - 12, velocity_base - 15)
        add_note(takes["Rhythm GTR"], bar_start, bar_start + bar_length_sec, third_pitch - 12, velocity_base - 15)
        add_note(takes["Rhythm GTR"], bar_start, bar_start + bar_length_sec, fifth_pitch - 12, velocity_base - 15)

        # 4. LEAD ARP (16th note cascading arpeggio: Root -> 5th -> Octave -> 3rd)
        sixteenth_sec = qn_sec / 4.0
        lead_pattern = [root_pitch, fifth_pitch, root_pitch + 12, third_pitch + 12]
        
        for i in range(16):
            n_start = bar_start + i * sixteenth_sec
            n_end = n_start + sixteenth_sec * 0.9
            p = lead_pattern[i % 4]
            add_note(takes["Lead Arp"], n_start, n_end, p, velocity_base + 5)

    # Sort MIDI events to ensure clean playback and rendering
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track Arpeggiated Layering over {bars} bars in {key} {scale} at {bpm} BPM."
