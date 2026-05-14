def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a rhythmically comped, velocity-humanized chord progression in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created element.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.upper(), 0)

    # Helper function to generate in-scale notes
    def get_scale_note(degree, octave):
        scale_len = len(scale_intervals)
        oct_offset = (degree // scale_len) * 12
        note_idx = degree % scale_len
        return (octave * 12) + scale_intervals[note_idx] + oct_offset

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Sound Design (ReaSynth Piano-ish patch) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape the envelope for a percussive/plucky piano feel
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)   # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)   # Decay (Medium)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.15)  # Sustain (Low)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)   # Release (Natural fade)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.8)   # Triangle mix (Warm body)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.2)   # Saw mix (Slight harmonic bite)

    # Add EQ to roll off harsh highs
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 0) # Band 4 Type: Low Pass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 13, 2000) # Band 4 Freq

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_qn = bars * beats_per_bar
    item_length_sec = RPR.RPR_TimeMap2_QNToTime(0, total_qn)
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Humanized Notes ===
    # I - V - vi - IV progression (Scale degrees: 0, 4, 5, 3)
    progression_degrees = [0, 4, 5, 3]
    
    # 1/8th note comping rhythm with varied dynamic accents
    rhythm_qn_offsets = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    macro_velocities = [20, -10, -15, 15, -15, 10, -20, -5] # Groove accents
    note_duration_qn = 0.4  # Slightly staccato to let the envelope work

    notes_created = 0

    for bar in range(bars):
        chord_degree = progression_degrees[bar % len(progression_degrees)]
        
        # Construct diatonic triad
        chord_pitches = [
            get_scale_note(chord_degree, 4) + root_val,     # Root
            get_scale_note(chord_degree + 2, 4) + root_val, # Third
            get_scale_note(chord_degree + 4, 4) + root_val  # Fifth
        ]

        bar_start_qn = bar * beats_per_bar

        for qn_offset, macro_vel in zip(rhythm_qn_offsets, macro_velocities):
            start_qn = bar_start_qn + qn_offset
            end_qn = start_qn + note_duration_qn
            
            # Convert Quarter Notes to Project Time to PPQ
            start_proj = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_proj = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_proj)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_proj)

            for pitch in chord_pitches:
                # Apply humanization: Macro groove + Micro finger variation
                human_vel = velocity_base + macro_vel + random.randint(-6, 6)
                # Clamp safely within MIDI standard
                human_vel = max(1, min(127, int(human_vel)))

                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), human_vel, True)
                notes_created += 1

    # Sort MIDI events to finalize
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} humanized MIDI notes across {bars} bars at {bpm} BPM."
