def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SynthRock",
    bpm: int = 125,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track driving Rock/Synthwave arrangement (Drums, Bass, Rhythm, Lead).

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "B", "C#").
        scale: Scale type ("minor" is highly recommended for this vibe).
        bars: Number of bars to loop the progression.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10]
    }

    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_pitch = NOTE_MAP.get(key, 0)

    # Convert scale degree to MIDI note
    def get_pitch(degree, base_octave=4):
        octave_shift = degree // 7
        idx = degree % 7
        return root_pitch + (base_octave + octave_shift) * 12 + scale_intervals[idx]

    # Initialize Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Setup time math
    qn_per_bar = 4.0
    item_length_sec = (60.0 / bpm) * qn_per_bar * bars
    
    # Helper: Create Track, MIDI Item, and add FX
    def setup_instrument_track(name, idx_offset, fx_name=None):
        idx = RPR.RPR_CountTracks(0) + idx_offset
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Add basic synth placeholder (except for drums)
        if fx_name:
            RPR.RPR_TrackFX_AddByName(track, fx_name, False, -1)
            
        # Create single looping MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        return track, item, take

    # Safely add notes using Project Time to PPQ conversion
    def add_note(take, qn_start, qn_length, pitch, vel, chan=0):
        proj_time_start = qn_start * (60.0 / bpm)
        proj_time_end = (qn_start + qn_length) * (60.0 / bpm)
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time_start)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time_end)
        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, chan, int(pitch), int(vel), True)

    # Create the 4 Tracks
    _, _, take_drum = setup_instrument_track(f"{track_name}_Drums", 0)
    _, _, take_bass = setup_instrument_track(f"{track_name}_Bass", 1, "ReaSynth")
    _, _, take_rhy  = setup_instrument_track(f"{track_name}_Rhythm", 2, "ReaSynth")
    _, _, take_lead = setup_instrument_track(f"{track_name}_Lead", 3, "ReaSynth")

    # Epic Rock/Synthwave Progression: i - VI - III - VII
    progression = [0, 5, 2, 6] 

    # Generate Notes bar by bar
    for b in range(bars):
        bar_start_qn = b * qn_per_bar
        chord_root = progression[b % len(progression)]

        # --- 1. DRUMS ---
        # Syncopated Kick, 2&4 Snare, driving 8th hats
        for i in range(8): 
            qn_offset = i * 0.5
            start_qn = bar_start_qn + qn_offset
            
            # Hi-hat (Channel 9, Note 42)
            hat_vel = velocity_base if i % 2 == 0 else velocity_base - 20
            add_note(take_drum, start_qn, 0.25, 42, hat_vel, 9)
            
            # Kick (Channel 9, Note 36)
            if i in [0, 3, 5]: # Beats 1, 2.5, 3.5
                add_note(take_drum, start_qn, 0.25, 36, velocity_base + 10, 9)
                
            # Snare (Channel 9, Note 38)
            if i in [2, 6]: # Beats 2, 4
                add_note(take_drum, start_qn, 0.25, 38, velocity_base + 15, 9)

        # --- 2. BASS & RHYTHM ---
        # 8th-note chopped pulses with slight staccato gap (length = 0.4 QN instead of 0.5)
        bass_pitch = get_pitch(chord_root, 2)
        chord_pitches = [
            get_pitch(chord_root, 3), 
            get_pitch(chord_root + 2, 3), 
            get_pitch(chord_root + 4, 3)
        ]
        
        for i in range(8):
            qn_offset = i * 0.5
            start_qn = bar_start_qn + qn_offset
            
            # Bass pulse
            add_note(take_bass, start_qn, 0.4, bass_pitch, velocity_base)
            # Rhythm chord pulse
            for p in chord_pitches:
                add_note(take_rhy, start_qn, 0.4, p, velocity_base - 10)

        # --- 3. LEAD ARPEGGIO ---
        # 16th note sweeps: Root, 3rd, 5th, Octave
        arp_pitches = [
            get_pitch(chord_root, 4), 
            get_pitch(chord_root + 2, 4), 
            get_pitch(chord_root + 4, 4), 
            get_pitch(chord_root + 7, 4) # Degree 7 in this context is octave jump
        ]
        
        for i in range(16):
            qn_offset = i * 0.25
            start_qn = bar_start_qn + qn_offset
            pitch = arp_pitches[i % 4]
            add_note(take_lead, start_qn, 0.2, pitch, velocity_base - 5)

    # Sort MIDI events to finalize items
    RPR.RPR_MIDI_Sort(take_drum)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_rhy)
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created 4-track driving '{track_name}' loop over {bars} bars at {bpm} BPM in {key} {scale}."
