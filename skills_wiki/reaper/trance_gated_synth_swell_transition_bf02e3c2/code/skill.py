def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Synth Swell Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Trance-Gated Synth Swell Transition in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars for the transition swell.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # === Step 1: Music Theory & Setup ===
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

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Calculate timing
    start_time = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    item_length_sec = beat_length_sec * beats_per_bar * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Harmony ===
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, start_time + item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + item_length_sec)

    # Build a massive multi-octave chord
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Octave 3 and 4 blend
    base_midi = 48 + root_val
    chord_degrees = [0, 2, 4] # Root, 3rd, 5th
    
    notes_to_insert = []
    # Core triad
    for degree in chord_degrees:
        if degree < len(scale_intervals):
            notes_to_insert.append(base_midi + scale_intervals[degree])
    # Octave down
    notes_to_insert.append(base_midi - 12)
    # Octave up
    notes_to_insert.append(base_midi + 12)

    for pitch in notes_to_insert:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Construct FX Chain ===
    # 1. Synthesizer
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Reverb to wash out the sound
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.5)  # Wet
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.5)  # Dry
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.9)  # Room Size (Huge)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 4, 1.0)  # Stereo width out of the verb

    # 3. Macro Volume Swell (JS: Volume Adjustment)
    fx_swell = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    env_swell = RPR.RPR_GetFXEnvelope(track, fx_swell, 0, True) # Param 0: Adjustment (dB)
    
    # 4. Micro Volume Chop / Trance Gate (JS: Volume Adjustment)
    fx_chop = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    env_chop = RPR.RPR_GetFXEnvelope(track, fx_chop, 0, True)

    # 5. Stereo Width Expansion (JS: Stereo Width)
    fx_width = RPR.RPR_TrackFX_AddByName(track, "JS: Stereo Width", False, -1)
    env_width = RPR.RPR_GetFXEnvelope(track, fx_width, 0, True) # Param 0: Width (0-200%)

    # === Step 5: Draw Automation Envelopes ===
    
    # Envelope 1: Macro Swell (-40dB to 0dB)
    # Shape 2 is slow start/end curve for a natural build
    RPR.RPR_InsertEnvelopePoint(env_swell, start_time, -40.0, 2, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_swell, start_time + item_length_sec, 0.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env_swell)

    # Envelope 2: Width Swell (0% to 100%)
    # Shape 0 is Linear
    RPR.RPR_InsertEnvelopePoint(env_width, start_time, 0.0, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_width, start_time + item_length_sec, 100.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env_width)

    # Envelope 3: The 32nd Note Chop (Trance Gate)
    # 32nd note = 1/8th of a beat. Shape 1 is Square (holds value until next point).
    chop_length_sec = beat_length_sec / 8.0 
    total_chops = int(item_length_sec / chop_length_sec)
    
    for i in range(total_chops + 1):
        t = start_time + (i * chop_length_sec)
        # Alternate between 0dB (on) and -12dB (gated)
        val = 0.0 if i % 2 == 0 else -12.0
        RPR.RPR_InsertEnvelopePoint(env_chop, t, val, 1, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(env_chop)

    return f"Created '{track_name}' with a {bars}-bar trance-gated swell at {bpm} BPM in {key} {scale}."
