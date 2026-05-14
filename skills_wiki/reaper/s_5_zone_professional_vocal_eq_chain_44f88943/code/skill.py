def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lead Vocal (Pro EQ)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a vocal-style MIDI melody and process it with the 5-Zone Pro Vocal EQ Chain.

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
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # We will use the pentatonic minor to simulate a soulful vocal ad-lib
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Initialize Tempo & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create "Vocal Proxy" Sound Source (ReaSynth) ===
    # This generates a soft, continuous tone with harmonics so the EQ has frequencies to manipulate
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 0, 0.0)     # Volume (prevent clipping)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.4)     # Square mix (gives it some 'throat' harmonics)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 5, 0.2)     # Attack (soft vocal-like start)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 6, 0.3)     # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 7, 0.8)     # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 8, 0.4)     # Release

    # === Step 3: Add Zone 1 - Rumble (High Pass Filter) ===
    fx_hpf = RPR.RPR_TrackFX_AddByName(track, "JS: filters/rbj_hpf_lpf", False, -1)
    # Param 0: Lowpass (leave at max), Param 1: Highpass
    RPR.RPR_TrackFX_SetParam(track, fx_hpf, 1, 160.0) 

    # === Step 4: Add Zones 2-5 - Body, Boxy, Presence, Air (4-Band EQ) ===
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "JS: loser/4BandEQ", False, -1)
    
    # Zone 2: Body (Controls warmth, left at neutral 0dB here but parameterized)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 0, 200.0) # Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 1, 0.0)   # dB

    # Zone 3: Boxy / Muddy (Cutting the cheap room sound)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 2, 600.0) # Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 3, -3.0)  # dB

    # Zone 4: Presence (Intelligibility and bite)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 4, 3000.0)# Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 5, 2.5)   # dB

    # Zone 5: Air (Expensive high-end sheen)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 6, 10000.0)# Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 7, 3.0)    # dB

    # Gain Compensation (pulling down slightly to match perceived volume)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 8, -1.0)   # Output dB

    # === Step 5: Generate Vocal-Style MIDI Data ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Ensure MIDI item has a valid source
    RPR.RPR_MIDI_CountEvts(take, 0, 0, 0)
    
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    # Using octave 4 (approx 261Hz for middle C) to fall perfectly into the "Body" and "Boxy" zones
    base_note = root_val + 60 
    
    chosen_scale = SCALES.get(scale.lower(), SCALES["pentatonic_minor"])

    # Simulate a slow, soulful vocal phrase (mostly long notes)
    # Rhythms are fractions of a beat
    vocal_phrase = [
        # (Scale degree index, start_beat, duration_beats)
        (0, 0.0, 2.0),
        (2, 2.0, 1.0),
        (1, 3.0, 1.0),
        (0, 4.0, 3.0),
        (3, 7.0, 1.0),
        (4, 8.0, 4.0),
        (2, 12.0, 1.5),
        (1, 13.5, 0.5),
        (0, 14.0, 2.0)
    ]

    ticks_per_quarter = 960

    for i, (degree_idx, start_b, dur_b) in enumerate(vocal_phrase):
        # Stop generating if we exceed requested bars
        if start_b >= (bars * 4): 
            break
            
        note_pitch = base_note + chosen_scale[degree_idx % len(chosen_scale)]
        # Add an octave if the degree wraps around
        note_pitch += 12 * (degree_idx // len(chosen_scale))
        
        start_pos = RPR.RPR_MIDI_GetProjTimeFromPPQPos(take, start_b * ticks_per_quarter)
        end_pos = RPR.RPR_MIDI_GetProjTimeFromPPQPos(take, (start_b + dur_b) * ticks_per_quarter)

        # Emulate human vocal dynamics (slight variations)
        velocity = max(40, min(127, velocity_base + (i % 3) * 5 - 10))

        RPR.RPR_MIDI_InsertNote(
            take,
            False,               # selected
            False,               # muted
            start_b * ticks_per_quarter,  # startppqpos
            (start_b + dur_b) * ticks_per_quarter, # endppqpos
            0,                   # chan
            note_pitch,          # pitch
            velocity,            # vel
            False                # noSort
        )

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' featuring the 5-Zone Pro Vocal EQ Chain over {bars} bars at {bpm} BPM."
