def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated_Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an Automated Swell & Rhythmic Pump Pad in the current REAPER project.
    Generates a chord progression and applies macro volume swells followed by 
    micro rhythmic ducking (sidechain simulation) using the Track Volume Envelope.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (first half will swell, second half will pump).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created automated track.
    """
    import reaper_python as RPR

    # === Step 1: Music Theory & Input Normalization ===
    # Format key input (e.g., "c#" -> "C#")
    key_clean = key.strip().capitalize()
    if len(key_clean) > 1 and key_clean[1] == '#':
        key_clean = key_clean[0].upper() + '#'
        
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_offset = NOTE_MAP.get(key_clean, 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    def get_note(octave, degree):
        deg_idx = (degree - 1) % 7
        oct_shift = (degree - 1) // 7
        return (octave + oct_shift) * 12 + root_offset + scale_intervals[deg_idx]

    # Progression: i - VI - III - VII
    voicings = [
        [get_note(4, 1), get_note(4, 3), get_note(4, 5)], # i
        [get_note(3, 6), get_note(4, 1), get_note(4, 3)], # VI
        [get_note(4, 3), get_note(4, 5), get_note(4, 7)], # III
        [get_note(3, 7), get_note(4, 2), get_note(4, 4)], # VII
    ]

    # === Step 2: Global Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar

    # === Step 3: Track & FX Setup ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth and soften it into a pad texture
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 1, 0.0)  # Square mix to 0 (pure saw/sine)
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 4, 0.6)  # Increase Release time

    # === Step 4: MIDI Generation ===
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, bar_length_sec * bars, False)
    take = RPR.RPR_GetActiveTake(item)

    for i in range(bars):
        start_sec = i * bar_length_sec
        end_sec = start_sec + bar_length_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

        chord = voicings[i % len(voicings)]
        for pitch in chord:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, True)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Programmatic Envelope Automation ===
    # Select track and trigger Action 41866: "Track: Toggle track volume envelope visible"
    # This guarantees the Volume envelope track is initialized and visible.
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(41866, 0) 
    
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env:
        total_beats = bars * beats_per_bar
        half_beats = total_beats // 2
        
        for b in range(total_beats):
            t_beat = b * beat_sec
            
            # First half of the region: Macro Swells (Fade in over 1 whole bar)
            if b < half_beats:
                if b % beats_per_bar == 0:
                    t_start = t_beat
                    t_mid = t_start + (bar_length_sec * 0.7)
                    t_end = t_start + bar_length_sec - 0.02
                    # Shape 2 is "Slow start/end" for smooth curves
                    RPR.RPR_InsertEnvelopePoint(env, t_start, 0.01, 2, 0.0, False, True)
                    RPR.RPR_InsertEnvelopePoint(env, t_mid, 0.5, 2, 0.0, False, True)
                    RPR.RPR_InsertEnvelopePoint(env, t_end, 1.0, 0, 0.0, False, True)
            
            # Second half of the region: Micro Rhythmic Pumping (Sidechain effect)
            else:
                t_pump = t_beat
                t_drop = t_pump - 0.01 if t_pump > 0 else 0
                t_recover = t_pump + (beat_sec * 0.4)
                t_full = t_pump + (beat_sec * 0.85)

                # Sharp drop to 5% volume right on the downbeat
                RPR.RPR_InsertEnvelopePoint(env, t_drop, 1.0, 0, 0.0, False, True)
                RPR.RPR_InsertEnvelopePoint(env, t_pump, 0.05, 2, 0.0, False, True) 
                # Smooth curve recovering to full volume by the offbeat
                RPR.RPR_InsertEnvelopePoint(env, t_recover, 0.6, 2, 0.0, False, True)
                RPR.RPR_InsertEnvelopePoint(env, t_full, 1.0, 0, 0.0, False, True)

        RPR.RPR_Envelope_SortRects(env)

    return f"Created '{track_name}' with automated swells and rhythmic ducking over {bars} bars in {key} {scale} at {bpm} BPM."
