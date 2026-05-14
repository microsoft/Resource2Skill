def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Rock/Metal Multi-Track Arrangement in the current REAPER project.
    Generates 4 synchronized tracks (Drums, Bass, Rhythm Gtr, Lead Gtr) with an epic chord progression.
    
    Args:
        project_name: Project identifier (for logging).
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

    # --- Music Theory Lookup Tables ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10]
    }
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 11)  # Default B
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Epic i - VI - III - VII progression (indices in diatonic scale)
    progression = [0, 5, 2, 4] 

    # --- Environment Setup ---
    # Set project tempo
    RPR.RPR_SetCurrentBPM(0, True, bpm)
    cursor_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # --- Helper Functions ---
    def add_track_with_midi(name, use_synth=True):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, cursor_pos, cursor_pos + item_length, False)
        take = RPR.RPR_GetActiveTake(item)
        
        if use_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        return take

    def get_diatonic_triad(degree, root, intervals, base_oct):
        pitches = []
        for interval in [0, 2, 4]:  # Root, 3rd, 5th
            scale_idx = (degree + interval) % len(intervals)
            octave_offset = (degree + interval) // len(intervals)
            pitch = root + intervals[scale_idx] + (base_oct + octave_offset) * 12
            pitches.append(pitch)
        return pitches

    def insert_note(take, start_beat, duration_beats, pitch, vel):
        start_time = cursor_pos + (start_beat * (60.0 / bpm))
        end_time = cursor_pos + ((start_beat + duration_beats) * (60.0 / bpm))
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # --- Track 1: Drums (General MIDI) ---
    take_drums = add_track_with_midi("Drums", use_synth=False)
    for bar in range(bars):
        bar_start = bar * beats_per_bar
        
        # Kick (36) - Syncopated driving rhythm
        for b in [0.0, 1.5, 2.5]:
            insert_note(take_drums, bar_start + b, 0.25, 36, velocity_base)
            
        # Snare (38) - Backbeat
        for b in [1.0, 3.0]:
            insert_note(take_drums, bar_start + b, 0.25, 38, velocity_base + 10)
            
        # Hi-hat (42) - Steady 8ths
        for i in range(8):
            b = i * 0.5
            insert_note(take_drums, bar_start + b, 0.25, 42, velocity_base - 15)
            
        # Crash (49) - On chord changes (every bar start)
        insert_note(take_drums, bar_start, 0.5, 49, velocity_base + 5)
        
    RPR.RPR_MIDI_Sort(take_drums)

    # --- Track 2: Bass ---
    take_bass = add_track_with_midi("Bass", use_synth=True)
    for bar in range(bars):
        bar_start = bar * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Base note 1 octave down
        scale_idx = chord_degree % len(scale_intervals)
        oct_offset = chord_degree // len(scale_intervals)
        bass_pitch = root_pitch + scale_intervals[scale_idx] + (2 + oct_offset) * 12
        
        # 8th note driving pulse
        for i in range(8):
            insert_note(take_bass, bar_start + (i * 0.5), 0.35, bass_pitch, velocity_base)
            
    RPR.RPR_MIDI_Sort(take_bass)

    # --- Track 3: Rhythm Guitar ---
    take_rhythm = add_track_with_midi("GTR Rhythm", use_synth=True)
    for bar in range(bars):
        bar_start = bar * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Power chord construction (Root + P5 + Octave)
        scale_idx = chord_degree % len(scale_intervals)
        oct_offset = chord_degree // len(scale_intervals)
        chord_root = root_pitch + scale_intervals[scale_idx] + (3 + oct_offset) * 12
        power_chord = [chord_root, chord_root + 7, chord_root + 12]
        
        # 8th note driving pulse (matches bass)
        for i in range(8):
            for pitch in power_chord:
                insert_note(take_rhythm, bar_start + (i * 0.5), 0.35, pitch, velocity_base - 5)
                
    RPR.RPR_MIDI_Sort(take_rhythm)

    # --- Track 4: Lead Guitar ---
    take_lead = add_track_with_midi("GTR Lead", use_synth=True)
    for bar in range(bars):
        bar_start = bar * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Diatonic triad arpeggio (Octave 5)
        triad = get_diatonic_triad(chord_degree, root_pitch, scale_intervals, 5)
        
        # 16th note cascading arpeggio pattern: Root, 3rd, 5th, 3rd
        arp_pattern = [0, 1, 2, 1]
        
        for i in range(16): # 16 sixteenth notes per bar
            beat_offset = i * 0.25
            pitch = triad[arp_pattern[i % 4]]
            insert_note(take_lead, bar_start + beat_offset, 0.20, pitch, velocity_base)
            
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created Multi-Track Arrangement (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
