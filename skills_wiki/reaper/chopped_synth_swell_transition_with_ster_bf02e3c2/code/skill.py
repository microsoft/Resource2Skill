def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Chopped Swell Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Chopped Synth Swell Transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell to last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Build FX Chain ===
    
    # 1. Synthesizer (ReaSynth - Rich Saw/Square Blend)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.6) # Sawtooth
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.4) # Square wave
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.7) # Extra decay

    # 2. Reverb (ReaVerbate - Placed early so reflections get chopped later)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.35) # Wet mix
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 0.8)  # Dry mix
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 2, 0.9)  # Large room size

    # 3. Volume Smoother (Used for the overall crescendo swell)
    vol_idx = RPR.RPR_TrackFX_AddByName(track, "JS: utility/volume_pan", False, -1)

    # 4. Tremolo (Rhythmic chop gate on the overall signal + reverb tail)
    trem_idx = RPR.RPR_TrackFX_AddByName(track, "JS: tremolo", False, -1)
    freq_hz = (bpm / 60.0) * 8.0 # Formula for 32nd notes synced to tempo
    # Tremolo frequency normalized (range 0 to 100Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track, trem_idx, 0, freq_hz / 100.0) 
    # Tremolo amount normalized (0.0 is -60dB -> max cut depth)
    RPR.RPR_TrackFX_SetParamNormalized(track, trem_idx, 1, 0.0) 

    # 5. Stereo Enhancer (Used to expand spatial width at the peak)
    width_idx = RPR.RPR_TrackFX_AddByName(track, "JS: LOSER/stereoEnhancer", False, -1)

    # === Step 4: Create MIDI Item & Note ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    
    note_duration_sec = bar_length_sec * bars
    tail_duration_sec = bar_length_sec * 1.5 # Allow 1.5 bars of extra time for reverb decay
    item_length_sec = note_duration_sec + tail_duration_sec

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert root pitch in mid-low register (C2 = 48)
    root_pitch = 48 + NOTE_MAP.get(key, 0)
    note_ppq_length = int(bars * beats_per_bar * 960) # 960 pulses per quarter note
    
    RPR.RPR_MIDI_InsertNote(take, False, False, 0, note_ppq_length, 0, root_pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Write Automation Envelopes ===
    
    # Volume Swell Envelope: Silence to Unity (0dB)
    # JS: utility/volume_pan parameter 0 range is -120 to +12 dB.
    # 0.90909 normalized roughly equals 0 dB.
    vol_env = RPR.RPR_GetFXEnvelope(track, vol_idx, 0, True)
    # Point 1: 0 seconds, 0.0 normalized (-120dB). Shape 3 = Slow Start (Exponential curve)
    RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 3, 0.0, False, False)
    # Point 2: Reaches peak exactly as the MIDI note ends
    RPR.RPR_InsertEnvelopePoint(vol_env, note_duration_sec, 0.90909, 0, 0.0, False, False)

    # Width Envelope: Mono (0%) to Stereo (100%)
    # JS: LOSER/stereoEnhancer parameter 0 range is 0 to 200%. 
    # 0.0 normalized = 0%, 0.5 normalized = 100%
    width_env = RPR.RPR_GetFXEnvelope(track, width_idx, 0, True)
    # Point 1: Mono at the start
    RPR.RPR_InsertEnvelopePoint(width_env, 0.0, 0.0, 3, 0.0, False, False)
    # Point 2: Explodes to full stereo width at the drop
    RPR.RPR_InsertEnvelopePoint(width_env, note_duration_sec, 0.5, 0, 0.0, False, False)

    return f"Created '{track_name}': {bars}-bar chopped synth swell in {key} {scale} at {bpm} BPM with expanding width and tail processing."
