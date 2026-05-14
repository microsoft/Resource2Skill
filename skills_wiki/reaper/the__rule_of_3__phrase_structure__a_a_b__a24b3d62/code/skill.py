def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    variation_type: str = "new_section",  # Options: "new_section" or "diverge_halfway"
    **kwargs,
) -> str:
    """
    Creates a 12-bar piano progression that strictly obeys the 'Rule of 3'.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Fallback tempo (script will sync to REAPER's actual project tempo).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Internally clamped to 12 to demonstrate the 3-part micro-structure.
        velocity_base: Base MIDI velocity (0-127).
        variation_type: How the 3rd iteration diverges ("new_section" or "diverge_halfway").
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Initialize Music Theory Data ===
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

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Define progressions based on scale type
    if scale in ["major", "mixolydian", "pentatonic_major"]:
        prog_A = [1, 5, 6, 4]       # I - V - vi - IV
        prog_B = [6, 4, 1, 5]       # vi - IV - I - V (New Section)
        prog_A_prime = [1, 5, 2, 6] # I - V - ii - vi (Diverges halfway)
    else:
        prog_A = [1, 6, 3, 7]       # i - VI - III - VII
        prog_B = [4, 6, 1, 7]       # iv - VI - i - VII (New Section)
        prog_A_prime = [1, 6, 4, 5] # i - VI - iv - v (Diverges halfway)

    # Apply the "Rule of 3" Structure
    if variation_type == "diverge_halfway":
        full_progression = prog_A + prog_A + prog_A_prime
    else: 
        full_progression = prog_A + prog_A + prog_B

    # === Step 2: Setup Track & Timing ===
    # Sync to actual project tempo to guarantee MIDI aligns to grid
    proj_bpm = RPR.RPR_Master_GetTempo()
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    beats_per_bar = 4
    bars = 12 # Hardcoded to 12 to enforce the 3-part phrase concept
    bar_length_sec = (60.0 / proj_bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    start_time = 0.0
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, start_time + item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 3: MIDI Generation Logic ===
    def get_chord(degree, intervals, root, base_octave):
        """Extracts a diatonic triad based on the provided scale."""
        safe_degree = ((degree - 1) % len(intervals))
        notes = []
        for offset in [0, 2, 4]:
            scale_idx = (safe_degree + offset) % len(intervals)
            octave_shift = (safe_degree + offset) // len(intervals)
            pitch = root + intervals[scale_idx] + (base_octave + 1 + octave_shift) * 12
            notes.append(pitch)
        return notes

    # Classic pop rhythmic piano pattern: [Start Beat, Length in Beats]
    rhythm_pattern = [
        (0.0, 0.8), # Beat 1 (1/4)
        (1.0, 0.8), # Beat 2 (1/4)
        (2.0, 0.4), # Beat 3 (1/8)
        (2.5, 0.4), # Beat 3.5 (1/8)
        (3.0, 0.8)  # Beat 4 (1/4)
    ]

    note_count = 0
    
    for bar in range(bars):
        raw_degree = full_progression[bar]
        chord_notes = get_chord(raw_degree, scale_intervals, root_pitch, 4) # Base octave 4
        bass_note = chord_notes[0] - 12 # Drop root down an octave for bass
        
        bar_start_sec = bar * bar_length_sec
        
        for beat_start, beat_len in rhythm_pattern:
            note_start_sec = bar_start_sec + beat_start * (60.0 / proj_bpm)
            note_end_sec = note_start_sec + beat_len * (60.0 / proj_bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + note_end_sec)
            
            # Insert Bass Note
            bass_vel = max(1, min(127, velocity_base + random.randint(-5, 5)))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_note, bass_vel, False)
            note_count += 1
            
            # Insert Triad Notes
            for pitch in chord_notes:
                chord_vel = max(1, min(127, velocity_base - 10 + random.randint(-5, 5)))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, chord_vel, False)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (FX Chain) ===
    # Setup ReaSynth to mimic an Electric Piano
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7)   # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.05)  # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.5)   # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.3)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.5)   # Release
    RPR.RPR_TrackFX_SetParam(track, 0, 8, 0.6)   # Triangle mix (warmer tone)

    # Add Reverb
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 1, 0, 0.2)   # Wet
    RPR.RPR_TrackFX_SetParam(track, 1, 1, 0.9)   # Dry
    RPR.RPR_TrackFX_SetParam(track, 1, 2, 0.6)   # Room size

    return f"Created '{track_name}' featuring a 12-bar 'Rule of 3' structure ({variation_type}) with {note_count} notes synced to {proj_bpm} BPM."
