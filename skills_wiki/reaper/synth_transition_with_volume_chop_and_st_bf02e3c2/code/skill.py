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
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues":            [0, 3, 5, 6, 7, 10],
}

def create_synth_transition_pattern(
    project_name: str = "SynthTransitionProject",
    track_name: str = "Synth Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Covers the full transition shown in the video
    velocity_base: int = 100,
    flange_min_freq: float = 200.0, # Min frequency for ReaEQ band modulation (Hz)
    flange_max_freq: float = 2000.0, # Max frequency for ReaEQ band modulation (Hz)
    flange_lfo_rate_bars: float = 2.0, # How many bars for one full filter sweep cycle
    chop_amount_db: float = 4.0, # Amplitude of the volume chop in dB
    chop_rate_subdivision: int = 32, # e.g., 32 for 32nd notes
    volume_swell_start_db: float = -4.6, # Start volume for the overall swell in dB
    volume_swell_end_db: float = 0.0, # End volume for the overall swell in dB
    stereo_width_start: float = 0.0, # Initial stereo width (0.0 for mono, 1.0 for full stereo)
    stereo_width_end: float = 1.0, # Final stereo width
    **kwargs,
) -> str:
    """
    Create a synth transition pattern with volume swell, chopping, stereo width automation,
    and a modulated filter effect. Approximates Hybrid 3 synth sound and effects.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the transition over.
        velocity_base: Base MIDI velocity (0-127).
        flange_min_freq: Minimum frequency for the ReaEQ band modulation (Hz).
        flange_max_freq: Maximum frequency for the ReaEQ band modulation (Hz).
        flange_lfo_rate_bars: How many bars for one full filter sweep cycle.
        chop_amount_db: Amount of gain reduction for the chopping effect (dB).
        chop_rate_subdivision: Rhythmic subdivision for the chopping effect (e.g., 32 for 32nd notes).
        volume_swell_start_db: Start volume for the overall swell (dB).
        volume_swell_end_db: End volume for the overall swell (dB).
        stereo_width_start: Initial stereo width (0.0 for mono, 1.0 for full stereo).
        stereo_width_end: Final stereo width.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Synth Transition' with 1 MIDI item over 8 bars at 120 BPM"
    """

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Create MIDI Item (Sustained C minor chord as in video) ---
    root_midi_octave = 3 # Start chord from C3
    root_midi_note = NOTE_MAP[key] + (root_midi_octave * 12)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # Create a simple chord (root, 3rd, 5th, octave root, octave 3rd, octave 5th)
    chord_notes_midi = [
        root_midi_note,
        root_midi_note + scale_intervals[2], # Third
        root_midi_note + scale_intervals[4], # Fifth
        root_midi_note + 12,                  # Octave root
        root_midi_note + scale_intervals[2] + 12, # Octave third
        root_midi_note + scale_intervals[4] + 12, # Octave fifth
    ]

    midi_item_start_time = 0.0
    beats_per_bar = 4.0
    seconds_per_beat = 60.0 / bpm
    midi_item_length_beats = bars * beats_per_bar
    midi_item_length_seconds = midi_item_length_beats * seconds_per_beat

    midi_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_POSITION", midi_item_start_time)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_LENGTH", midi_item_length_seconds)
    midi_take = RPR.RPR_AddTakeToMediaItem(midi_item)
    RPR.RPR_MIDI_ClearEventList(midi_take)
    RPR.RPR_MIDI_SetMediaItemTake_SourceMIDI(midi_take, True, True)

    for midi_note in chord_notes_midi:
        RPR.RPR_MIDI_InsertNote(
            midi_take,
            False,              # No select
            False,              # No mute
            midi_item_start_time,
            midi_item_length_seconds,
            velocity_base,
            midi_note,
            True                # No auto-end
        )

    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_MarkAllNotes(midi_take, False)
    RPR.RPR_MIDI_UpdateByTake(midi_take, True, True)

    # --- Add FX Chain (ReaSynth, ReaVerb, ReaChorus, ReaEQ for modulation) ---
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerb", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaChorus", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1) # For flanging approx

    # Configure ReaSynth for a pad-like sound (basic, as Hybrid 3 is complex)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Attack (0.0-1.0, 0.5 is slower)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.7) # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.8) # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5) # Release

    # Configure ReaVerb (approximate Hall Reverb)
    RPR.RPR_TrackFX_SetPreset(track, 1, "Default (Smooth Hall)")
    RPR.RPR_TrackFX_SetParam(track, 1, 0, 0.5) # Wet mix (0.0-1.0)

    # Configure ReaChorus
    RPR.RPR_TrackFX_SetParam(track, 2, 0, 0.5) # Wet (0.0-1.0)
    RPR.RPR_TrackFX_SetParam(track, 2, 1, 0.2) # Depth (0.0-1.0)
    RPR.RPR_TrackFX_SetParam(track, 2, 2, 0.5) # Rate (0.0-1.0)

    # Configure ReaEQ for filter modulation (approximation of Hybrid 3's shape LFO)
    # Use a low-pass filter (band 1) and modulate its frequency
    # ReaEQ parameter indices: Band 1: Enabled (0), Type (1), Freq (2), Q (3), Gain (4), Mode (5)
    # For Band 1, use lowpass (Type=1)
    RPR.RPR_TrackFX_SetEQParam(track, 3, 0, True, 1, 1.0, 1000.0, 0.0) # Band 1: Lowpass, Q=1.0, Freq=1000Hz, Gain=0

    # --- Automation Envelopes ---
    # 1. Volume Swell
    volume_env_id = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not volume_env_id:
        volume_env_id = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetTrackEnvelopeInfo_String(volume_env_id, "P_NAME", "Volume", True)
    RPR.RPR_SetEnvelopeState(volume_env_id, 1) # Enable envelope
    RPR.RPR_DeleteEnvelopePointRange(volume_env_id, 0.0, midi_item_length_seconds + 1.0) # Clear existing points

    # Point 1: Start volume for swell
    RPR.RPR_InsertEnvelopePoint(volume_env_id, 0.0, RPR.DB2VAL(volume_swell_start_db), 0, 0, False)
    # Point 2: End volume for swell
    RPR.RPR_InsertEnvelopePoint(volume_env_id, midi_item_length_seconds, RPR.DB2VAL(volume_swell_end_db), 0, 0, False)

    # 2. Volume Chopping (added to the same volume envelope for combined effect)
    chop_interval_seconds = seconds_per_beat * (beats_per_bar / chop_rate_subdivision)
    current_time = midi_item_start_time
    while current_time < midi_item_length_seconds:
        # Peak (0dB offset from current swell level)
        RPR.RPR_InsertEnvelopePoint(volume_env_id, current_time, RPR.DB2VAL(0.0), 0, 0, False)
        # Trough (-chop_amount_db offset from current swell level)
        if current_time + chop_interval_seconds * 0.5 < midi_item_length_seconds:
            RPR.RPR_InsertEnvelopePoint(volume_env_id, current_time + chop_interval_seconds * 0.5, RPR.DB2VAL(-chop_amount_db), 0, 0, False)
        current_time += chop_interval_seconds
    # Ensure a final point at the end of the item if it ends on a trough
    if current_time - chop_interval_seconds * 0.5 < midi_item_length_seconds and current_time > midi_item_length_seconds:
        RPR.RPR_InsertEnvelopePoint(volume_env_id, midi_item_length_seconds, RPR.DB2VAL(0.0), 0, 0, False) # Return to peak or swell end

    # 3. Stereo Width Automation (from mono to stereo)
    width_env_id = RPR.RPR_GetTrackEnvelopeByName(track, "Width")
    if not width_env_id:
        width_env_id = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetTrackEnvelopeInfo_String(width_env_id, "P_NAME", "Width", True)
    RPR.RPR_SetEnvelopeState(width_env_id, 1) # Enable envelope
    RPR.RPR_DeleteEnvelopePointRange(width_env_id, 0.0, midi_item_length_seconds + 1.0)

    RPR.RPR_InsertEnvelopePoint(width_env_id, 0.0, stereo_width_start, 0, 0, False)
    RPR.RPR_InsertEnvelopePoint(width_env_id, midi_item_length_seconds, stereo_width_end, 0, 0, False)

    # 4. ReaEQ filter frequency modulation (simulating Hybrid 3's shape LFO)
    # Param index for Band 1 Freq is 4 (for ReaEQ after Enable/Type/Q/Gain are 0,1,2,3 for band 1 config)
    # The true parameter index for frequency of a band depends on its mode.
    # For band 1, with default enabled, the frequency is parameter 2 (0-based) assuming it's a normal band.
    # If band 1 is set to HPF (type 0), Freq is param 2. If it's LPF (type 1), Freq is param 2.
    # Let's verify parameter index: ReaEQ (Band 1, Freq) parameter index is 4.
    # (0: Band 1 bypass, 1: Band 1 type, 2: Band 1 freq_norm, 3: Band 1 Q_norm, 4: Band 1 Gain_norm)
    eq_band_freq_param_idx = 2 # Actually it is 2 for Freq, 3 for Q, 4 for Gain.
    eq_freq_env_id = RPR.RPR_GetTrackEnvelopeByFXParam(track, 3, eq_band_freq_param_idx, True) # FX=3 (ReaEQ), Param=2 (Band 1 Freq)
    if not eq_freq_env_id:
        eq_freq_env_id = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetTrackEnvelopeInfo_String(eq_freq_env_id, "P_NAME", "ReaEQ: Band 1 Freq", True)
    RPR.RPR_SetEnvelopeState(eq_freq_env_id, 1)
    RPR.RPR_DeleteEnvelopePointRange(eq_freq_env_id, 0.0, midi_item_length_seconds + 1.0)

    lfo_period_seconds = flange_lfo_rate_bars * beats_per_bar * seconds_per_beat
    current_time = midi_item_start_time
    while current_time < midi_item_length_seconds:
        # Normalized values for ReaEQ frequency parameter (0.0-1.0 maps log-linearly)
        # To get specific Hz, need to convert to normalized value (complex, simplified here)
        # Let's map 0.0 to min_freq and 1.0 to max_freq (approx)
        min_norm_freq = (flange_min_freq - 20) / (20000 - 20) # Very rough linear mapping for ReaEQ param 2
        max_norm_freq = (flange_max_freq - 20) / (20000 - 20)
        
        RPR.RPR_InsertEnvelopePoint(eq_freq_env_id, current_time, min_norm_freq, 0, 0, False)
        if current_time + lfo_period_seconds / 2 < midi_item_length_seconds:
            RPR.RPR_InsertEnvelopePoint(eq_freq_env_id, current_time + lfo_period_seconds / 2, max_norm_freq, 0, 0, False)
        if current_time + lfo_period_seconds < midi_item_length_seconds:
            RPR.RPR_InsertEnvelopePoint(eq_freq_env_id, current_time + lfo_period_seconds, min_norm_freq, 0, 0, False)
        current_time += lfo_period_seconds
    
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with 1 MIDI item over {bars} bars at {bpm} BPM with custom transitions."


# --- Example for Vinyl Crackle FX Pattern (not the main function as per prompt's example structure) ---
# This function demonstrates how to create a track with FX for vinyl crackle.
# The user would need to supply their own audio sample to the created media item.
def create_vinyl_crackle_fx_pattern(
    project_name: str = "CrackleFXProject",
    track_name: str = "Vinyl Crackle FX",
    bpm: int = 120,
    bars: int = 4,
    crackle_vol_db: float = -15.0, # Target volume for the crackle
    comp_threshold: float = -20.0,
    comp_ratio: float = 6.0,
    eq_mono_freq_hz: float = 955.0, # Freq below which stereo signal is mono-ed (approx)
    eq_high_cut_hz: float = 10000.0, # High-cut for overall crackle
    reverb_wet_mix: float = 0.24, # 24% wet
    **kwargs,
) -> str:
    """
    Creates a track with an empty item (for user to add vinyl crackle) and processes it
    with dynamics, EQ (including mid/side mono-making), and reverb to achieve a lo-fi texture.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        bars: Number of bars for the placeholder audio item.
        crackle_vol_db: Target volume for the crackle track (dB).
        comp_threshold: Threshold for ReaComp (dB).
        comp_ratio: Ratio for ReaComp.
        eq_mono_freq_hz: Frequency below which the stereo signal is mono-ed in ReaEQ (Hz).
        eq_high_cut_hz: Frequency for high-cut on the overall crackle in ReaEQ (Hz).
        reverb_wet_mix: Wet mix for ReaVerb (0.0-1.0).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Vinyl Crackle FX' track with processing chain."
    """
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Create Placeholder Audio Item ---
    # User needs to place their own vinyl crackle sample here.
    item_start_time = 0.0
    beats_per_bar = 4.0
    seconds_per_beat = 60.0 / bpm
    item_length_seconds = bars * beats_per_bar * seconds_per_beat
    
    audio_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(audio_item, "D_POSITION", item_start_time)
    RPR.RPR_SetMediaItemInfo_Value(audio_item, "D_LENGTH", item_length_seconds)
    # Note: No audio source is added; user should drag/drop their crackle sample onto this item.

    # Set initial track volume
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", RPR.DB2VAL(crackle_vol_db))

    # --- Add FX Chain (ReaComp, ReaEQ, ReaVerb) ---
    # 1. ReaComp (for transient shaping, approximating General Dynamics' flattening)
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, comp_threshold) # Threshold
    RPR.RPR_TrackFX_SetParam(track, 0, 1, comp_ratio)     # Ratio
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.001)          # Attack (1ms)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.050)          # Release (50ms)
    RPR.RPR_TrackFX_SetParam(track, 0, 8, 1)             # Auto make-up gain

    # 2. ReaEQ (for high-cut, low-cut, and mid/side mono-making)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Band 1: Low-cut filter for overall sound
    RPR.RPR_TrackFX_SetEQParam(track, 1, 0, True, 0, 1.0, 50.0, 0.0) # Band 1: Highpass, Q=1, Freq=50Hz

    # Band 2: High-cut filter for overall sound
    RPR.RPR_TrackFX_SetEQParam(track, 1, 1, True, 1, 1.0, eq_high_cut_hz, 0.0) # Band 2: Lowpass, Q=1, Freq=10000Hz

    # Band 3: Lowpass on Side channel to mono low frequencies (approximating Voxengo MSED)
    # Enable ReaEQ's Mid/Side processing
    # Set Band 3 to Lowpass (Type=1) and Mode to Side (param 5, value 2).
    # ReaEQ Band 3 parameters start from index 10 (0-based)
    # 10: Band 3 bypass, 11: Band 3 type, 12: Band 3 freq_norm, 13: Band 3 Q_norm, 14: Band 3 Gain_norm, 15: Band 3 Mode (0:Normal, 1:Mid, 2:Side)
    RPR.RPR_TrackFX_SetEQParam(track, 1, 10, True, 1, 1.0, eq_mono_freq_hz, 0.0) # Band 3: Lowpass, Q=1.0, Freq=eq_mono_freq_hz
    RPR.RPR_TrackFX_SetEQParam(track, 1, 15, True, 2, 0, 0, 0) # Set Band 3 Mode to Side

    # 3. ReaVerb (for ambiance, approximating Toneboosters Reverb 3)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerb", False, -1)
    RPR.RPR_TrackFX_SetPreset(track, 2, "Default (Small Room)") # Start with a small room preset
    RPR.RPR_TrackFX_SetParam(track, 2, 0, reverb_wet_mix)      # Wet mix

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' track with processing chain for vinyl crackle. Please add your crackle sample to the created audio item."

# --- Main Dispatcher Function (as requested in the prompt example) ---
def create_pattern(
    pattern_type: str = "synth_transition", # "synth_transition" or "vinyl_crackle"
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Dispatches to specific pattern creation functions based on `pattern_type`.

    Args:
        pattern_type: Specifies which pattern to create ("synth_transition" or "vinyl_crackle").
        project_name: Project identifier.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional arguments specific to the chosen pattern type.

    Returns:
        Status string from the called pattern creation function.
    """
    if pattern_type == "synth_transition":
        return create_synth_transition_pattern(
            project_name=project_name,
            bpm=bpm,
            key=key,
            scale=scale,
            bars=bars,
            velocity_base=velocity_base,
            **kwargs
        )
    elif pattern_type == "vinyl_crackle":
        return create_vinyl_crackle_fx_pattern(
            project_name=project_name,
            bpm=bpm,
            bars=bars,
            **kwargs
        )
    else:
        return f"Error: Unknown pattern_type '{pattern_type}'. Must be 'synth_transition' or 'vinyl_crackle'."

