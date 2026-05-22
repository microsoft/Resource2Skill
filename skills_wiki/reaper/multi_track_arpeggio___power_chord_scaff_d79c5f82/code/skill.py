def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RockArrangement",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a interlocking Multi-Track Arrangement (Drums, Bass, Rhythm, Lead)
    demonstrating multi-track MIDI synchronization.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the created tracks.
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

    if scale not in SCALES:
        scale = "minor"
    if key not in NOTE_MAP:
        key = "C"

    # Set up global timing
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len = 60.0 / bpm
    
    # Octave 1 baseline (e.g., C1 = 24)
    base_pitch = 24 + NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    def get_scale_note(degree: int, octave_offset: int = 0) -> int:
        """Calculates exact MIDI pitch for a given diatonic scale degree."""
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return base_pitch + ((octave + octave_offset) * 12) + scale_intervals[idx]

    def create_midi_track(suffix: str, length_beats: float):
        """Helper to create a track with a properly sized MIDI item."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", f"{track_name} {suffix}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(tr)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_beats * beat_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return tr, item, take

    def add_note(take, start_beat: float, end_beat: float, pitch: int, vel: int):
        """Helper to insert MIDI notes accurately using PPQ."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_beat * beat_len)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_beat * beat_len)
        # Constrain pitch/velocity
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Progression degrees: I, VI, IV, V (0, 5, 3, 4 zero-indexed)
    progression = [0, 5, 3, 4]
    
    total_beats = bars * 4

    # --- 1. DRUMS TRACK ---
    _, _, take_drums = create_midi_track("Drums", total_beats)
    for b in range(bars):
        # Kick (MIDI 36) - Syncopated
        for kb in [0, 1.5, 2.5]:
            add_note(take_drums, (b*4) + kb, (b*4) + kb + 0.25, 36, velocity_base)
        # Snare (MIDI 38) - Backbeat
        for sb in [1, 3]:
            add_note(take_drums, (b*4) + sb, (b*4) + sb + 0.25, 38, velocity_base)
        # Hi-Hats (MIDI 42) - 8th notes
        for hb in range(8):
            hat_vel = velocity_base if hb % 2 == 0 else velocity_base - 20
            add_note(take_drums, (b*4) + (hb * 0.5), (b*4) + (hb * 0.5) + 0.15, 42, hat_vel)
    RPR.RPR_MIDI_Sort(take_drums)

    # --- 2. BASS TRACK ---
    _, _, take_bass = create_midi_track("Bass", total_beats)
    for b in range(bars):
        deg = progression[b % len(progression)]
        r_note = get_scale_note(deg, 0) # Octave 1
        for i in range(8): # Driving 8th notes
            add_note(take_bass, (b*4) + (i*0.5), (b*4) + (i*0.5) + 0.45, r_note, velocity_base)
    RPR.RPR_MIDI_Sort(take_bass)

    # --- 3. RHYTHM GUITAR/CHORDS TRACK ---
    _, _, take_rhy = create_midi_track("Rhythm", total_beats)
    for b in range(bars):
        deg = progression[b % len(progression)]
        # Power chord: Root, 5th, Octave (in Octave 2/3)
        r_note = get_scale_note(deg, 1)
        fifth = get_scale_note(deg + 4, 1)
        octave = get_scale_note(deg + 7, 1)
        
        add_note(take_rhy, b*4, (b*4) + 4.0, r_note, velocity_base - 10)
        add_note(take_rhy, b*4, (b*4) + 4.0, fifth, velocity_base - 10)
        add_note(take_rhy, b*4, (b*4) + 4.0, octave, velocity_base - 10)
    RPR.RPR_MIDI_Sort(take_rhy)

    # --- 4. LEAD ARPEGGIO TRACK ---
    _, _, take_lead = create_midi_track("Lead", total_beats)
    for b in range(bars):
        deg = progression[b % len(progression)]
        # 8-note rolling arpeggio: 1, 3, 5, 7, 8(octave), 7, 5, 3
        n1 = get_scale_note(deg, 2)
        n2 = get_scale_note(deg + 2, 2)
        n3 = get_scale_note(deg + 4, 2)
        n4 = get_scale_note(deg + 6, 2)
        n5 = get_scale_note(deg + 7, 2)
        arp_pattern = [n1, n2, n3, n4, n5, n4, n3, n2]
        
        for i in range(16): # 16th notes
            pitch = arp_pattern[i % len(arp_pattern)]
            add_note(take_lead, (b*4) + (i*0.25), (b*4) + (i*0.25) + 0.2, pitch, velocity_base)
    RPR.RPR_MIDI_Sort(take_lead)

    RPR.RPR_UpdateArrange()

    return f"Created multi-track arrangement '{track_name}' (Drums, Bass, Rhythm, Lead) over {bars} bars in {key} {scale} at {bpm} BPM."
