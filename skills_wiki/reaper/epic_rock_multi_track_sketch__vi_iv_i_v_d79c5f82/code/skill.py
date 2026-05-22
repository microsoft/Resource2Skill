def create_pattern(
    project_name: str = "MultiTrackSketch",
    track_name: str = "Epic Rock",
    bpm: int = 130,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Epic Rock Sketch (Drums, Bass, Rhythm, Lead) in the current REAPER project.
    Features color-coded tracks optimized for REAPER's multi-track MIDI editor workflow.
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

    def get_pitch(k, s, degree, octave):
        base_note = NOTE_MAP.get(k, 0)
        scale_intervals = SCALES.get(s, SCALES["minor"])
        octave_offset = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return base_note + ((octave + octave_offset) * 12) + scale_intervals[scale_idx]

    def get_reaper_color(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    # The vi - IV - I - V progression relative degrees
    # In minor, i = 0, VI = 5, III = 2, VII = 6
    progression = [0, 5, 2, 6] 

    # Step 1: Set Tempo
    try:
        RPR.RPR_SetCurrentBPM(0, bpm, True)
    except:
        pass # Fallback if specific REAPER version complains

    start_time = 0.0
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    end_time = bar_length_sec * bars

    track_defs = [
        {"name": f"{track_name} Drums", "color": get_reaper_color(150, 0, 200), "synth": False},
        {"name": f"{track_name} Bass", "color": get_reaper_color(0, 100, 200), "synth": True},
        {"name": f"{track_name} Rhythm", "color": get_reaper_color(255, 150, 0), "synth": True},
        {"name": f"{track_name} Lead", "color": get_reaper_color(0, 200, 200), "synth": True},
    ]

    # Arrays to hold notes per track: (start_qn, end_qn, pitch, velocity)
    notes_drums = []
    notes_bass = []
    notes_rhythm = []
    notes_lead = []

    for bar in range(bars):
        base_qn = bar * 4
        chord_degree = progression[bar % len(progression)]
        
        # --- DRUMS ---
        # Kick (1 and 3)
        notes_drums.append((base_qn + 0.0, base_qn + 0.5, 36, velocity_base + 10))
        notes_drums.append((base_qn + 2.0, base_qn + 2.5, 36, velocity_base + 10))
        # Snare (2 and 4)
        notes_drums.append((base_qn + 1.0, base_qn + 1.5, 38, velocity_base + 5))
        notes_drums.append((base_qn + 3.0, base_qn + 3.5, 38, velocity_base + 5))
        # Hi-hat (8th notes)
        for eighth in range(8):
            notes_drums.append((base_qn + eighth * 0.5, base_qn + eighth * 0.5 + 0.25, 42, velocity_base - 10))

        # --- BASS ---
        bass_pitch = get_pitch(key, scale, chord_degree, octave=2)
        for eighth in range(8):
            vel = velocity_base + 10 if eighth % 2 == 0 else velocity_base - 5
            notes_bass.append((base_qn + eighth * 0.5, base_qn + eighth * 0.5 + 0.45, bass_pitch, vel))

        # --- RHYTHM GUITAR (Triads) ---
        p1 = get_pitch(key, scale, chord_degree, octave=3)
        p2 = get_pitch(key, scale, chord_degree + 2, octave=3)
        p3 = get_pitch(key, scale, chord_degree + 4, octave=3)
        for eighth in range(8):
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 10
            start = base_qn + eighth * 0.5
            end = start + 0.45
            notes_rhythm.append((start, end, p1, vel))
            notes_rhythm.append((start, end, p2, vel))
            notes_rhythm.append((start, end, p3, vel))

        # --- LEAD GUITAR (Arpeggios) ---
        arp_degrees = [chord_degree, chord_degree + 2, chord_degree + 4, chord_degree + 7]
        for eighth in range(8):
            deg = arp_degrees[eighth % 4]
            lead_pitch = get_pitch(key, scale, deg, octave=4)
            start = base_qn + eighth * 0.5
            end = start + 0.45
            notes_lead.append((start, end, lead_pitch, velocity_base + 5))

    all_notes = [notes_drums, notes_bass, notes_rhythm, notes_lead]

    # Insert tracks and MIDI items
    for idx, tdef in enumerate(track_defs):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Name and Color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", tdef["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", tdef["color"])
        
        if tdef["synth"]:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
        take = RPR.RPR_GetActiveTake(item)
        
        # Populate Notes
        track_notes = all_notes[idx]
        for start_qn, end_qn, pitch, vel in track_notes:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            # Args: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)
            
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track Epic Rock template (vi-IV-I-V in {key} {scale}) with color-coded multi-track routing over {bars} bars at {bpm} BPM."
