def create_pattern(
    project_name: str = "Rock_Template",
    track_name: str = "Band",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock/Metal arrangement (Drums, Bass, Rhythm Gtr, Lead Gtr)
    demonstrated in the REAPER workflow tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
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
        "major":          [0, 2, 4, 5, 7, 9, 11],
        "minor":          [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian":         [0, 2, 3, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = NOTE_MAP.get(key.capitalize(), 11) # Default to B

    # Diatonic progression relative to scale: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6] 

    # --- Setup Project Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def get_pitch(degree_idx, octave):
        """Convert a scale degree index and octave into an absolute MIDI pitch."""
        octave_offset = degree_idx // len(scale_intervals)
        scale_idx = degree_idx % len(scale_intervals)
        pitch = root_midi + scale_intervals[scale_idx] + 12 * (octave + octave_offset)
        return max(0, min(127, pitch))

    def create_midi_track(name, with_synth=True):
        """Helper to create a track, a MIDI item, and add basic FX."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        beats_per_bar = 4
        item_length_sec = (60.0 / bpm) * beats_per_bar * bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        if with_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Lower volume for safety
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.2)

        return take

    def insert_note(take, pitch, beat_pos, beat_len, vel):
        """Insert a MIDI note using beat-based positioning."""
        start_time = (beat_pos / bpm) * 60.0
        end_time = ((beat_pos + beat_len) / bpm) * 60.0
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(vel), True)

    # === Track 1: DRUMS ===
    take_drums = create_midi_track("1 MIDI Drums", with_synth=False)
    for b in range(bars):
        bar_offset = b * 4
        # Kick (36)
        insert_note(take_drums, 36, bar_offset + 0.0, 0.25, velocity_base)
        insert_note(take_drums, 36, bar_offset + 1.5, 0.25, velocity_base - 10)
        insert_note(take_drums, 36, bar_offset + 2.5, 0.25, velocity_base)
        
        # Snare (38)
        insert_note(take_drums, 38, bar_offset + 1.0, 0.25, velocity_base + 10)
        insert_note(take_drums, 38, bar_offset + 3.0, 0.25, velocity_base + 10)
        
        # Hi-hat (42) - 8th notes
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 20
            insert_note(take_drums, 42, bar_offset + (i * 0.5), 0.2, vel)
            
        # Crash (49) on downbeat of first bar
        if b == 0:
            insert_note(take_drums, 49, bar_offset + 0.0, 0.5, velocity_base + 15)

    RPR.RPR_MIDI_Sort(take_drums)

    # === Track 2: BASS ===
    take_bass = create_midi_track("2 BASS")
    for b in range(bars):
        bar_offset = b * 4
        degree = progression_degrees[b % len(progression_degrees)]
        pitch = get_pitch(degree, 2) # Octave 2
        
        # Driving 8th notes
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 10
            insert_note(take_bass, pitch, bar_offset + (i * 0.5), 0.45, vel)
    RPR.RPR_MIDI_Sort(take_bass)

    # === Track 3: RHYTHM GUITAR ===
    take_rhy = create_midi_track("3 GTR RHY")
    for b in range(bars):
        bar_offset = b * 4
        degree = progression_degrees[b % len(progression_degrees)]
        
        # Power Chord block (Root, 5th, Octave) sustained for the whole bar
        p1 = get_pitch(degree, 3)     # Root
        p2 = get_pitch(degree + 4, 3) # 5th
        p3 = get_pitch(degree + 7, 3) # Octave
        
        for p in [p1, p2, p3]:
            insert_note(take_rhy, p, bar_offset, 3.9, velocity_base - 5)
    RPR.RPR_MIDI_Sort(take_rhy)

    # === Track 4: LEAD GUITAR ===
    take_lead = create_midi_track("4 GTR LEAD")
    for b in range(bars):
        bar_offset = b * 4
        degree = progression_degrees[b % len(progression_degrees)]
        
        # Up-and-down 8th note arpeggio: Root, 3rd, 5th, Octave, 5th, 3rd, Root, 3rd
        arp_pattern = [0, 2, 4, 7, 4, 2, 0, 2] 
        
        for i, arp_deg in enumerate(arp_pattern):
            pitch = get_pitch(degree + arp_deg, 4) # Octave 4
            vel = velocity_base + (5 if i == 0 else -10)
            insert_note(take_lead, pitch, bar_offset + (i * 0.5), 0.4, vel)
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created 4-track Rock/Metal Band Template ({bars} bars in {key} {scale} at {bpm} BPM)."
