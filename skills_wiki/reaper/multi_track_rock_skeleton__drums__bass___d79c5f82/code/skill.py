def create_pattern(
    project_name: str = "MultiTrackWorkflow",
    track_name: str = "Band Setup",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 4-track Rock/Metal MIDI arrangement (Drums, Bass, Rhythm GTR, Lead GTR)
    to facilitate multi-track MIDI editing workflows.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored here as we create 4 specific tracks).
        bpm: Tempo in BPM.
        key: Root note (e.g., "B").
        scale: Scale type (e.g., "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the multi-track layout.
    """
    import reaper_python as RPR

    # --- 1. Music Theory Lookup Tables ---
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

    def get_pitch(root_note_str, scale_name, degree, octave):
        """Calculates exact MIDI pitch based on scale degree and octave."""
        base_pitch = NOTE_MAP.get(root_note_str, 0)
        curr_scale = SCALES.get(scale_name, SCALES["minor"])
        
        scale_len = len(curr_scale)
        octave_offset = degree // scale_len
        scale_idx = degree % scale_len
        
        # REAPER's C4 is MIDI note 60 (Base C=0 + 5 octaves = 60)
        return base_pitch + (octave + octave_offset + 1) * 12 + curr_scale[scale_idx]

    # --- 2. Set Tempo & Timeline ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_len_sec = (60.0 / bpm) * beats_per_bar
    item_len_sec = bar_len_sec * bars

    # --- 3. Track Definitions & Colors ---
    # Colors mirror the visual organization in the tutorial
    track_defs = [
        ("MIDI Drums", 100, 100, 255), # Indigo
        ("BASS", 180, 50, 200),        # Purple
        ("GTR RHY", 255, 120, 50),     # Orange
        ("GTR LEAD", 50, 200, 255)     # Teal
    ]

    takes = []
    for i, (name, r, g, b) in enumerate(track_defs):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        trk = RPR.RPR_GetTrack(0, track_idx)
        
        # Name and color the track
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        color_int = int(r + (g * 256) + (b * 65536) | 0x1000000)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "I_CUSTOMCOLOR", color_int)
        
        # Create a blank MIDI item bound to the exact timeline
        item = RPR.RPR_CreateNewMIDIItemInProj(trk, 0.0, item_len_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        takes.append(take)

    take_drums, take_bass, take_gtr, take_lead = takes

    def insert_note(take, start_qn, end_qn, pitch, vel, chan=0):
        """Helper to insert MIDI events based on Quarter Note beats."""
        start_ppq = int(start_qn * 960)
        end_ppq = int(end_qn * 960)
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, pitch, vel, False)

    # --- 4. Generate Musical Content ---
    
    # Classic i - VI - III - VII rock progression
    roots = [0, 5, 2, 6] 
    
    for b in range(bars):
        root_idx = roots[b % 4]
        
        # A. Bass: Driving 8th notes
        bass_pitch = get_pitch(key, scale, root_idx, 2)
        for i in range(8):
            start_qn = b * 4 + (i * 0.5)
            insert_note(take_bass, start_qn, start_qn + 0.45, bass_pitch, velocity_base)
            
        # B. Rhythm Guitar: Syncopated Power Chords
        gtr_root = get_pitch(key, scale, root_idx, 3)
        gtr_fifth = gtr_root + 7 # Perfect 5th interval
        gtr_oct = gtr_root + 12
        # Rhythmic pattern offsets in Quarter Notes: [0, 1.5, 3.0]
        rhythm_pattern = [(0, 1.5), (1.5, 3), (3, 4)]
        for p_start, p_end in rhythm_pattern:
            start_qn = b * 4 + p_start
            end_qn = b * 4 + p_end - 0.05
            insert_note(take_gtr, start_qn, end_qn, gtr_root, velocity_base - 10)
            insert_note(take_gtr, start_qn, end_qn, gtr_fifth, velocity_base - 10)
            insert_note(take_gtr, start_qn, end_qn, gtr_oct, velocity_base - 10)
            
        # C. Lead Guitar: Flowing 16th-note broken chords
        for i in range(4): # 4 beats per bar
            base_qn = b * 4 + i
            # Scale degrees: root, 3rd, 5th, Octave
            p1 = get_pitch(key, scale, root_idx, 4)
            p2 = get_pitch(key, scale, root_idx + 2, 4)
            p3 = get_pitch(key, scale, root_idx + 4, 4)
            p4 = p1 + 12
            
            insert_note(take_lead, base_qn + 0.00, base_qn + 0.25, p1, velocity_base - 15)
            insert_note(take_lead, base_qn + 0.25, base_qn + 0.50, p2, velocity_base - 15)
            insert_note(take_lead, base_qn + 0.50, base_qn + 0.75, p3, velocity_base - 15)
            insert_note(take_lead, base_qn + 0.75, base_qn + 1.00, p4, velocity_base - 15)
            
        # D. Drums: Backbeat Groove (GM Mapping: Channel 10 -> index 9)
        for beat in range(4):
            base_qn = b * 4 + beat
            # Hi-hats (42) on 8th notes
            insert_note(take_drums, base_qn, base_qn + 0.25, 42, velocity_base - 20, 9)
            insert_note(take_drums, base_qn + 0.5, base_qn + 0.75, 42, velocity_base - 30, 9)
            
            # Snare (38) on 2 and 4
            if beat == 1 or beat == 3:
                insert_note(take_drums, base_qn, base_qn + 0.5, 38, velocity_base, 9)
                
            # Kick (36) on 1, 2.5, and 3
            if beat == 0:
                insert_note(take_drums, base_qn, base_qn + 0.25, 36, velocity_base, 9)
            if beat == 1:
                insert_note(take_drums, base_qn + 0.5, base_qn + 0.75, 36, velocity_base - 10, 9)
            if beat == 2:
                insert_note(take_drums, base_qn, base_qn + 0.25, 36, velocity_base, 9)
                
        # Crash Cymbal (49) on the first downbeat of the entire loop
        if b == 0:
            insert_note(take_drums, 0, 1.0, 49, velocity_base + 10, 9)

    # Sort MIDI events to ensure safe playback
    for take in takes:
        RPR.RPR_MIDI_Sort(take)

    return f"Created Multi-Instrument Rock Template (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
