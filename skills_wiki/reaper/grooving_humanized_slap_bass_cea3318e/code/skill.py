def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Grooving Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a grooving, humanized slap bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR
    import random

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

    # Validate inputs
    key = key.capitalize() if key.capitalize() in NOTE_MAP else "C"
    scale = scale if scale in SCALES else "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    sec_per_beat = 60.0 / bpm

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure Plucky Bass Synth ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth Parameters to emulate a tight, plucked bass:
    # Param 0: Volume, Param 1: Tuning, Param 2: Attack, Param 3: Decay, Param 4: Sustain, Param 5: Release
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)  # Fast attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.2)  # Short decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.1)  # Low sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.3)  # Medium release

    # === Step 4: Create MIDI Item ===
    item_length_sec = sec_per_beat * 4 * bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Groove & Insert Notes ===
    notes_added = 0
    base_octave = 24  # C1 for deep bass
    root_midi = base_octave + NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # The tutorial emphasizes splitting lengths, octaves, ghost notes, and offsets
    # Here we define a 1-bar rhythmic groove template (beat_pos, scale_deg, octave_shift, duration, velocity_mod)
    groove_template = [
        {"beat": 0.0,  "deg": 0, "octave": 0, "dur": 0.75, "vel": 0},    # Root anchor
        {"beat": 1.5,  "deg": 0, "octave": 1, "dur": 0.25, "vel": 25},   # Syncopated slap (Octave up)
        {"beat": 2.5,  "deg": 0, "octave": 0, "dur": 0.50, "vel": -10},  # Root step mid-bar
        {"beat": 3.25, "deg": 0, "octave": 0, "dur": 0.25, "vel": -20},  # Ghost note
        {"beat": 3.75, "deg": 4, "octave": 0, "dur": 0.25, "vel": +10}   # Passing tone (usually the 5th) to lead into next bar
    ]

    for b in range(bars):
        # Create a simple chord progression: stays on Root (i) for 2 bars, goes up to the Subdominant (iv) for 2 bars
        chord_deg = 0 if (b % 4) < 2 else 3 
        chord_root = root_midi + scale_intervals[chord_deg]

        for note in groove_template:
            # Imitate reality: Add slight humanization offsets to timing
            timing_offset = random.uniform(-0.03, 0.03)  # Push/pull by up to ~30ms
            dur_variance = random.uniform(0.9, 1.1)      # Slight variance in length
            
            start_beat = (b * 4) + note["beat"] + timing_offset
            end_beat = start_beat + (note["dur"] * dur_variance)

            # Convert beats to time, then to PPQ for REAPER API
            start_time = start_beat * sec_per_beat
            end_time = end_beat * sec_per_beat
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Calculate pitch
            target_deg = note["deg"]
            oct_shift = target_deg // len(scale_intervals)
            rem_deg = target_deg % len(scale_intervals)
            pitch = chord_root + scale_intervals[rem_deg] + (oct_shift * 12) + (note["octave"] * 12)
            
            # Keep pitch in bounds
            pitch = max(0, min(127, pitch))

            # Humanize velocity
            vel = velocity_base + note["vel"] + random.randint(-8, 8)
            vel = max(1, min(127, int(vel)))

            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_added += 1

    # Sort MIDI data after insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM (Humanized Slap groove)."
