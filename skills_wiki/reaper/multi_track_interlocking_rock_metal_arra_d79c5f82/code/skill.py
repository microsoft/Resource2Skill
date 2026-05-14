def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Arrangement",
    bpm: int = 130,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Track Rock/Metal Arrangement in the current REAPER project.
    Generates isolated tracks for Drums, Bass, Rhythm Chords, and Lead Arpeggios.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created track group.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
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
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 60 + NOTE_MAP.get(key.capitalize(), 0) # Middle C octave

    def get_scale_note(degree: int) -> int:
        """Convert a scale degree (0-indexed) to a MIDI pitch."""
        octave_offset = degree // len(scale_intervals)
        scale_index = degree % len(scale_intervals)
        return root_midi + (octave_offset * 12) + scale_intervals[scale_index]

    # Chord progression degrees based on scale type
    if scale.lower() == "major":
        progression = [0, 4, 5, 3]  # I - V - vi - IV
    else:
        progression = [0, 5, 2, 6]  # i - VI - III - VII

    # Sequence timings
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    sec_per_beat = 60.0 / bpm
    beats_per_bar = 4
    item_length_sec = sec_per_beat * beats_per_bar * bars

    def create_track(name: str):
        """Helper to create a track with a MIDI item and return the take."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def add_note(take, start_beat, end_beat, pitch, vel):
        """Helper to insert a MIDI note using beat timings."""
        start_sec = start_beat * sec_per_beat
        end_sec = end_beat * sec_per_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    total_notes_added = 0

    # ==========================================
    # TRACK 1: DRUMS (Standard Rock Beat)
    # ==========================================
    track_drums, take_drums = create_track(f"{track_name} - Drums")
    
    kick = 36
    snare = 38
    hihat = 42
    crash = 49

    for bar in range(bars):
        bar_beat = bar * beats_per_bar
        
        # Crash on the very first downbeat, otherwise Hi-hats every 8th note
        for eighth in range(8):
            beat_pos = bar_beat + (eighth * 0.5)
            if bar == 0 and eighth == 0:
                add_note(take_drums, beat_pos, beat_pos + 0.25, crash, velocity_base + 10)
            else:
                vel_hh = velocity_base if eighth % 2 == 0 else velocity_base - 20
                add_note(take_drums, beat_pos, beat_pos + 0.25, hihat, vel_hh)
            total_notes_added += 1
            
        # Kick and Snare pattern (Kick on 1 & 3, Snare on 2 & 4, extra Kick syncopations)
        add_note(take_drums, bar_beat + 0.0, bar_beat + 0.25, kick, velocity_base + 10) # Beat 1
        add_note(take_drums, bar_beat + 1.0, bar_beat + 0.25, snare, velocity_base + 15) # Beat 2
        add_note(take_drums, bar_beat + 1.5, bar_beat + 0.25, kick, velocity_base - 10) # Beat 2.5 (syncopation)
        add_note(take_drums, bar_beat + 2.0, bar_beat + 0.25, kick, velocity_base + 10) # Beat 3
        add_note(take_drums, bar_beat + 3.0, bar_beat + 0.25, snare, velocity_base + 15) # Beat 4
        total_notes_added += 5
        
    RPR.RPR_MIDI_Sort(take_drums)

    # ==========================================
    # TRACK 2: BASS (Driving 8th notes)
    # ==========================================
    track_bass, take_bass = create_track(f"{track_name} - Bass")
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1) # Audibility
    
    for bar in range(bars):
        bar_beat = bar * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        bass_pitch = get_scale_note(chord_degree) - 24 # 2 octaves down
        
        # 8th note pulse
        for eighth in range(8):
            beat_pos = bar_beat + (eighth * 0.5)
            vel = velocity_base + 5 if eighth % 2 == 0 else velocity_base - 10
            add_note(take_bass, beat_pos, beat_pos + 0.45, bass_pitch, vel)
            total_notes_added += 1
            
    RPR.RPR_MIDI_Sort(take_bass)

    # ==========================================
    # TRACK 3: RHYTHM GUITAR (Sustained Chords)
    # ==========================================
    track_rhy, take_rhy = create_track(f"{track_name} - Rhythm Chords")
    RPR.RPR_TrackFX_AddByName(track_rhy, "ReaSynth", False, -1)

    for bar in range(bars):
        bar_beat = bar * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Triad voicings (Root, 3rd, 5th) 1 octave down
        root = get_scale_note(chord_degree) - 12
        third = get_scale_note(chord_degree + 2) - 12
        fifth = get_scale_note(chord_degree + 4) - 12
        
        # One whole note per bar
        add_note(take_rhy, bar_beat, bar_beat + 4.0, root, velocity_base - 10)
        add_note(take_rhy, bar_beat, bar_beat + 4.0, third, velocity_base - 15)
        add_note(take_rhy, bar_beat, bar_beat + 4.0, fifth, velocity_base - 15)
        total_notes_added += 3

    RPR.RPR_MIDI_Sort(take_rhy)

    # ==========================================
    # TRACK 4: LEAD ARPEGGIOS
    # ==========================================
    track_lead, take_lead = create_track(f"{track_name} - Lead Arp")
    RPR.RPR_TrackFX_AddByName(track_lead, "ReaSynth", False, -1)

    for bar in range(bars):
        bar_beat = bar * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Arp sequence: Root, 5th, Octave, 3rd (repeated twice per bar)
        arp_notes = [
            get_scale_note(chord_degree),           # Root
            get_scale_note(chord_degree + 4),       # 5th
            get_scale_note(chord_degree + 7),       # Octave above root
            get_scale_note(chord_degree + 2) + 12   # 3rd (an octave up)
        ]
        
        for eighth in range(8):
            beat_pos = bar_beat + (eighth * 0.5)
            arp_pitch = arp_notes[eighth % len(arp_notes)]
            add_note(take_lead, beat_pos, beat_pos + 0.45, arp_pitch, velocity_base)
            total_notes_added += 1

    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created multi-track '{track_name}' arrangement ({total_notes_added} notes over 4 tracks, {bars} bars) in {key} {scale} at {bpm} BPM."
