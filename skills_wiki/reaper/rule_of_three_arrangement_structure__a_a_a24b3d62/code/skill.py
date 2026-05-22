def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Arps",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 12, # 12 bars perfectly demonstrates the 3-part rule
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 12-bar 'Rule of 3' arrangement structure in the current REAPER project.
    Generates Phrase 1, repeats it for Phrase 2, and varies it for Phrase 3.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
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
    
    root_midi = NOTE_MAP.get(key.capitalize(), 9) + 48 # Octave 4
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(scale_intervals)

    def get_diatonic_triad(degree):
        """Returns MIDI notes for a diatonic triad based on scale degree (0-indexed)"""
        notes = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            curr_deg = degree + i
            octave_shift = curr_deg // scale_len
            note_idx = curr_deg % scale_len
            notes.append(root_midi + scale_intervals[note_idx] + (12 * octave_shift))
        return notes

    # === Structural Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Add FX Chain (ReaSynth + Space) ===
    # Add ReaSynth for a plucky arp sound
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set to sawtooth with short decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Volume mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 1.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.3)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.0)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.1)   # Release
    
    # Add Delay
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, 0.15) # Wet mix

    # === Create MIDI Item ===
    beats_per_bar = 4
    bar_len_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_len_sec * 12 # 12 bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # === Apply The Rule of 3 Compositional Logic ===
    # We define a 4-bar progression.
    # Repetition 1 (Intro) & Repetition 2 (Reinforce): [0, 5, 3, 4] -> i, VI, iv, v
    # Repetition 3 (Variation): [0, 5, 6, 2] -> i, VI, VII, III (Starts same, ends lifting up)
    
    macro_progression = [
        0, 5, 3, 4,  # Phrase A (Bars 1-4)
        0, 5, 3, 4,  # Phrase A Repeated (Bars 5-8)
        0, 5, 6, 2   # Phrase A' Varied (Bars 9-12)
    ]
    
    note_count = 0
    # Generate 8th note arpeggios
    for bar in range(12):
        chord_degree = macro_progression[bar]
        triad = get_diatonic_triad(chord_degree)
        
        # Arp pattern: Root, 3rd, 5th, Octave(Root+12), 5th, 3rd, Root, 3rd
        arp_sequence = [triad[0], triad[1], triad[2], triad[0]+12, triad[2], triad[1], triad[0], triad[1]]
        
        bar_start_sec = bar * bar_len_sec
        step_len_sec = bar_len_sec / 8.0 # 8th notes
        
        for i, pitch in enumerate(arp_sequence):
            start_pos = bar_start_sec + (i * step_len_sec)
            end_pos = start_pos + (step_len_sec * 0.8) # Slight staccato/gap
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            
            # Add dynamic accent to the downbeat
            vel = velocity_base + 20 if i == 0 else velocity_base
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' applying the 'Rule of 3' ({note_count} notes over 12 bars). Listen to the pattern change at bar 9."
