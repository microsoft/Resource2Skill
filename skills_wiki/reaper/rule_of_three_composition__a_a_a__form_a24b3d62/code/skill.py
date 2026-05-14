def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a composition demonstrating the Rule of 3 (A-A-A' Form) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Total number of bars (will be quantized to chunks of 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
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
    }

    # Enforce a 7-note diatonic scale for standard chord building. Fallback to major.
    if scale not in SCALES or len(SCALES.get(scale, [])) < 7:
        scale = "major"
        
    scale_arr = SCALES[scale]
    root_midi = 48 + NOTE_MAP.get(key, 0) # Base octave is C3
    
    # Velocity clamping
    vel_chord = max(1, min(127, int(velocity_base * 0.85)))
    vel_melody = max(1, min(127, int(velocity_base)))

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure 4-Bar Macro Structure ===
    # The Rule of 3 pattern takes 12 bars (3 iterations of 4 bars). 
    # We round up the requested bars to ensure complete 4-bar phrases.
    if bars < 12:
        bars = 12
    num_sections = max(3, bars // 4)
    actual_bars = num_sections * 4

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * actual_bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Music Theory Generation ===
    # A = I, V, vi, IV | A' = I, V, ii, V
    progression_A = [0, 4, 5, 3] 
    progression_A_prime = [0, 4, 1, 4] 

    def get_diatonic_chord(degree: int, s_arr: list, root: int) -> list:
        """Returns the MIDI notes for a root position triad built on the given scale degree."""
        chord = []
        for i in range(3):
            s_idx = (degree + i * 2) % len(s_arr)
            octave_shift = (degree + i * 2) // len(s_arr)
            note = root + s_arr[s_idx] + (octave_shift * 12)
            chord.append(note)
        return chord

    item_start = float(RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION"))
    note_count = 0

    # Write the MIDI data
    for section in range(num_sections):
        # The core rule: Every 3rd iteration diverges
        is_divergent = (section % 3) == 2
        prog = progression_A_prime if is_divergent else progression_A
        
        for bar_in_iter, degree in enumerate(prog):
            bar_idx = section * 4 + bar_in_iter
            bar_start_sec = bar_idx * bar_length_sec
            
            start_time = item_start + bar_start_sec
            start_ppq = float(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time))
            end_ppq = float(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + bar_length_sec))
            
            # 1. Left Hand: Background Chord (Whole Note)
            chord = get_diatonic_chord(degree, scale_arr, root_midi)
            for pitch in chord:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel_chord, True)
                note_count += 1
                
            # 2. Right Hand: Foreground Melody
            if is_divergent and bar_in_iter >= 2:
                # DIVERGENT BEHAVIOR: "Start the same, but go somewhere different"
                # Melody becomes 4 descending quarter notes to signal the change
                for beat in range(4):
                    note_start = start_time + beat * (60.0 / bpm)
                    note_end = note_start + (60.0 / bpm)
                    n_s_ppq = float(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start))
                    n_e_ppq = float(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end))
                    
                    m_pitch = chord[2 - (beat % 3)] + 12 # Arpeggiate down from the 5th
                    RPR.RPR_MIDI_InsertNote(take, False, False, n_s_ppq, n_e_ppq, 0, m_pitch, vel_melody, True)
                    note_count += 1
            else:
                # STANDARD BEHAVIOR: 1/4 note, 1/4 note, 1/2 note rhythm
                beats_len = [1, 1, 2]
                current_beat = 0
                for i, bl in enumerate(beats_len):
                    note_start = start_time + current_beat * (60.0 / bpm)
                    note_end = note_start + bl * (60.0 / bpm)
                    n_s_ppq = float(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start))
                    n_e_ppq = float(RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end))
                    
                    m_pitch = chord[i] + 12 # Arpeggiate up
                    RPR.RPR_MIDI_InsertNote(take, False, False, n_s_ppq, n_e_ppq, 0, m_pitch, vel_melody, True)
                    note_count += 1
                    current_beat += bl

    # Sort MIDI event buffer
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Native Instruments & FX ===
    # Add native synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add reverb to soften the digital harshness
    reverb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    if reverb_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, reverb_idx, 0, 0.4) # Wet mix
        RPR.RPR_TrackFX_SetParam(track, reverb_idx, 1, 0.8) # Dry mix
        RPR.RPR_TrackFX_SetParam(track, reverb_idx, 2, 0.7) # Room size

    return f"Created '{track_name}' demonstrating Rule of 3 (A-A-A') with {note_count} notes over {actual_bars} bars at {bpm} BPM in {key} {scale}."
