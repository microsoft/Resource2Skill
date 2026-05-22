def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SlapBass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Humanized Slap Bass & Formant Layering in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., E, C#, G).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    scale_arr = SCALES.get(scale.lower(), SCALES["minor"])
    # Set base pitch to Octave 2 for Bass (e.g., C2 = 36)
    base_midi = NOTE_MAP.get(key.capitalize(), 4) + 36 

    def get_scale_pitch(base_midi, scale_arr, degree):
        octave_shift = degree // len(scale_arr)
        scale_idx = degree % len(scale_arr)
        return base_midi + (octave_shift * 12) + scale_arr[scale_idx]

    # Progression degrees: i - iv - v - i
    progression = [0, 3, 4, 0] 

    # Groove template (beat_pos, duration, pitch_type, is_slap, vel_mod)
    groove_events = [
        (0.00, 0.50, 'root',  False,   0),  # Downbeat root
        (0.75, 0.25, 'root',  False, -30),  # Quiet ghost note
        (1.25, 0.25, 'slap',  True,  +27),  # Syncopated slap (octave)
        (1.75, 0.25, 'root',  False, -10),  # Offbeat root
        (2.50, 0.25, 'slap',  True,  +20),  # Syncopated slap (octave)
        (3.50, 0.25, 'walk1', False, -15),  # Diatonic walk-up 1
        (3.75, 0.25, 'walk2', False,  -5),  # Diatonic walk-up 2
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Create Track 1: Main Bass ===
    idx1 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx1, True)
    track1 = RPR.RPR_GetTrack(0, idx1)
    RPR.RPR_GetSetMediaTrackInfo_String(track1, "P_NAME", f"{track_name}_Main", True)

    # === Create Track 2: Slap/Uh Transient Layer ===
    idx2 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx2, True)
    track2 = RPR.RPR_GetTrack(0, idx2)
    RPR.RPR_GetSetMediaTrackInfo_String(track2, "P_NAME", f"{track_name}_Slap_Uh", True)

    # === FX Chain: Main Bass ===
    rs_main = RPR.RPR_TrackFX_AddByName(track1, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track1, rs_main, 3, 0.5) # Saw Mix
    RPR.RPR_TrackFX_SetParam(track1, rs_main, 4, 0.5) # Square Mix
    
    eq_main = RPR.RPR_TrackFX_AddByName(track1, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track1, eq_main, 9, 800.0)  # Band 4 Freq (High shelf)
    RPR.RPR_TrackFX_SetParam(track1, eq_main, 10, -24.0) # Band 4 Gain (Cut highs)

    # === FX Chain: Slap/Uh Layer ===
    rs_slap = RPR.RPR_TrackFX_AddByName(track2, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track2, rs_slap, 4, 1.0)    # Square Mix (buzzy snap)
    RPR.RPR_TrackFX_SetParam(track2, rs_slap, 10, 0.0)   # Attack = 0ms
    RPR.RPR_TrackFX_SetParam(track2, rs_slap, 11, 50.0)  # Decay = 50ms
    RPR.RPR_TrackFX_SetParam(track2, rs_slap, 12, 0.0)   # Sustain = 0
    RPR.RPR_TrackFX_SetParam(track2, rs_slap, 13, 20.0)  # Release = 20ms

    eq_slap = RPR.RPR_TrackFX_AddByName(track2, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track2, eq_slap, 0, 400.0)  # Band 1 Freq
    RPR.RPR_TrackFX_SetParam(track2, eq_slap, 1, -24.0)  # Cut Lows completely
    RPR.RPR_TrackFX_SetParam(track2, eq_slap, 6, 1200.0) # Band 3 Freq (Formant range)
    RPR.RPR_TrackFX_SetParam(track2, eq_slap, 7, 15.0)   # Boost "Uh" formant +15dB
    RPR.RPR_TrackFX_SetParam(track2, eq_slap, 8, 3.0)    # High Q for vocal resonance

    # === MIDI Generation ===
    item_len_sec = bars * 4 * (60.0 / bpm)
    
    item1 = RPR.RPR_CreateNewMIDIItemInProj(track1, 0.0, item_len_sec, False)
    take1 = RPR.RPR_GetActiveTake(item1)
    
    item2 = RPR.RPR_CreateNewMIDIItemInProj(track2, 0.0, item_len_sec, False)
    take2 = RPR.RPR_GetActiveTake(item2)

    PPQ = 960
    total_notes_added = 0

    for bar in range(bars):
        bar_start_beat = bar * 4.0
        curr_deg = progression[bar % len(progression)]
        next_deg = progression[(bar + 1) % len(progression)]
        
        for event in groove_events:
            beat, dur, ptype, is_slap, vel_mod = event
            
            # Humanize timing
            h_beat = beat + random.uniform(-0.02, 0.03)
            h_beat = max(0.0, min(3.95, h_beat)) # Keep within bar bounds
            
            start_ppq = int((bar_start_beat + h_beat) * PPQ)
            end_ppq = int((bar_start_beat + h_beat + dur) * PPQ)
            
            # Calculate Contextual Pitch
            if ptype == 'root':
                pitch = get_scale_pitch(base_midi, scale_arr, curr_deg)
            elif ptype == 'slap':
                pitch = get_scale_pitch(base_midi, scale_arr, curr_deg) + 12
            elif ptype == 'walk1':
                pitch = get_scale_pitch(base_midi, scale_arr, next_deg - 2)
            elif ptype == 'walk2':
                pitch = get_scale_pitch(base_midi, scale_arr, next_deg - 1)
                
            # Humanize Velocity
            vel = velocity_base + vel_mod + random.randint(-6, 6)
            vel = max(1, min(127, vel))
            
            # Insert into Main Bass
            RPR.RPR_MIDI_InsertNote(take1, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes_added += 1
            
            # Insert into Formant Transient Layer
            if is_slap:
                # Maximize velocity for the snappy layer
                RPR.RPR_MIDI_InsertNote(take2, False, False, start_ppq, end_ppq, 0, pitch, 127, True)

    RPR.RPR_MIDI_Sort(take1)
    RPR.RPR_MIDI_Sort(take2)

    return f"Created layered Slap Bass Groove with {total_notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}."
