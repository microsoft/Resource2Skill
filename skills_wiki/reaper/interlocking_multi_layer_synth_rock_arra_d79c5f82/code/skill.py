def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SynthRock",
    bpm: int = 130,
    key: str = "F#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an interlocking 4-track Synth-Rock Arrangement (Drums, Bass, Chords, Lead).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "F#", "C", "A").
        scale: Scale type (major, minor, harmonic_minor, dorian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
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

    # Validate scale and key
    root_pitch = NOTE_MAP.get(key, 6) # Default to F#
    intervals = SCALES.get(scale, SCALES["minor"])

    # Set tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    beat_len = 60.0 / bpm
    
    # Progression degrees: i - VI - VII - iv
    progression = [0, 5, 6, 3]

    # Helper: Create a track with an empty MIDI item
    def create_track_with_midi(name, index_offset):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} {name}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", beat_len * beats_per_bar * bars)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, item, take

    # Helper: Insert MIDI note via PPQ calculation
    def insert_note(take, start_beat, length_beats, pitch, vel):
        start_time = start_beat * beat_len
        end_time = (start_beat + length_beats) * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Clamp velocity
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Initialize the 4 layers
    _, _, take_drums = create_track_with_midi("Drums", 0)
    _, _, take_bass = create_track_with_midi("Bass", 1)
    _, _, take_rhythm = create_track_with_midi("Rhythm Chords", 2)
    _, _, take_lead = create_track_with_midi("Lead Arp", 3)

    # Generate patterns bar by bar
    for b in range(bars):
        # Determine current chord degree and notes
        deg = progression[b % len(progression)]
        
        # Calculate chord triad (root, 3rd, 5th of the current degree)
        c0 = intervals[deg]
        c1 = intervals[(deg + 2) % 7] + (12 if (deg + 2) >= 7 else 0)
        c2 = intervals[(deg + 4) % 7] + (12 if (deg + 4) >= 7 else 0)
        chord_pitches = [c0, c1, c2]

        # --- 1. DRUMS ---
        for beat in range(4):
            curr_beat = b * 4 + beat
            
            # Kick (MIDI 36) on 1 and 3
            if beat in [0, 2]:
                insert_note(take_drums, curr_beat, 0.25, 36, velocity_base + 10)
            
            # Snare (MIDI 38) on 2 and 4
            if beat in [1, 3]:
                insert_note(take_drums, curr_beat, 0.25, 38, velocity_base + 15)

            # Hi-hats (MIDI 42) on 8th notes (downbeat heavier than upbeat)
            insert_note(take_drums, curr_beat, 0.25, 42, velocity_base - 10)
            insert_note(take_drums, curr_beat + 0.5, 0.25, 42, velocity_base - 20)

        # Crash cymbal (MIDI 49) on the very first beat of the loop
        if b == 0:
            insert_note(take_drums, 0, 1.0, 49, velocity_base + 20)

        # --- 2. BASS ---
        # Driving 8th notes following the chord root (Octave 2)
        bass_pitch = root_pitch + 24 + c0
        for i in range(8):
            insert_note(take_bass, b * 4 + i * 0.5, 0.45, bass_pitch, velocity_base)

        # --- 3. RHYTHM CHORDS ---
        # Whole note block chords (Octave 4) + top octave
        rhythm_octave = root_pitch + 48
        for p in chord_pitches:
            insert_note(take_rhythm, b * 4, 4.0, rhythm_octave + p, velocity_base - 10)
        # Add root an octave up for thickness
        insert_note(take_rhythm, b * 4, 4.0, rhythm_octave + c0 + 12, velocity_base - 10)

        # --- 4. LEAD ARP ---
        # 16th notes executing a 6-note shifting pattern over the chord tones (Octave 5)
        lead_octave = root_pitch + 60
        arp_pattern = [c0, c1, c2, c0 + 12, c2, c1]
        
        for i in range(16): # 16 sixteenth notes per bar
            arp_pitch = lead_octave + arp_pattern[i % len(arp_pattern)]
            insert_note(take_lead, b * 4 + i * 0.25, 0.2, arp_pitch, velocity_base - 5)

    # Sort MIDI events sequentially for all takes
    for take in [take_drums, take_bass, take_rhythm, take_lead]:
        RPR.RPR_MIDI_Sort(take)

    return f"Created interlocking 4-track arrangement ('{track_name}...') over {bars} bars at {bpm} BPM in {key} {scale}."
