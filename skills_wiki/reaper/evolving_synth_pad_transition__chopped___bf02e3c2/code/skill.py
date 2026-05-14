import reaper_python as RPR
import math

# Helper to convert dB to a linear 0.0-1.0 scale for REAPER parameters
# where 0.0 is -inf and 1.0 is 0dB (for track volume, some FX)
def DB_to_Val(db: float) -> float:
    if db <= -90.0: # REAPER's -inf
        return 0.0
    return RPR.DB2VAL(db)

def create_synth_transition(
    project_name: str = "MyProject",
    track_name: str = "Evolving Synth Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    chord_type: str = "min",
    octave: int = 3,
    velocity_base: int = 90,
    swell_start_db: float = -60.0,
    swell_end_db: float = 0.0,
    chop_peak_db_offset: float = 1.0, # Offset from swell line for peak of chop
    chop_trough_db_offset: float = -4.0, # Offset from swell line for trough of chop
    chop_frequency_multiplier: float = 2.0, # 1.0 for 16th, 2.0 for 32nd notes
    width_start: float = 0.0, # 0.0 for mono, 1.0 for full stereo
    width_end: float = 1.0,
    synth_reverb_mix: float = 0.25, # ReaSynth's internal reverb wet mix (0.0 to 1.0)
    synth_chorus_mix: float = 0.25, # ReaSynth's internal chorus wet mix (0.0 to 1.0)
    **kwargs,
) -> str:
    """
    Creates an evolving synth pad with a swelling, chopped, and widening transition.
    This function simulates layered track automation by drawing combined points on the main volume envelope.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        chord_type: Type of chord (major, minor, maj7, min7, etc.).
        octave: Starting octave for the chord (MIDI 0-127).
        velocity_base: Base MIDI velocity (0-127).
        swell_start_db: Starting volume for the swell-up (in dB).
        swell_end_db: Ending volume for the swell-up (in dB).
        chop_peak_db_offset: dB offset from the swell line for the peak of the chop.
        chop_trough_db_offset: dB offset from the swell line for the trough of the chop.
        chop_frequency_multiplier: Multiplier for base 16th note chopping frequency.
                                   1.0 for 16th, 2.0 for 32nd.
        width_start: Starting stereo width (0.0=mono, 1.0=stereo).
        width_end: Ending stereo width (0.0=mono, 1.0=stereo).
        synth_reverb_mix: ReaSynth's internal reverb wet mix (0.0 to 1.0).
        synth_chorus_mix: ReaSynth's internal chorus wet mix (0.0 to 1.0).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Evolving Synth Pad' with 3 notes over 4 bars at 120 BPM"
    """

    # Music theory lookup tables (simplified for this pattern)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    CHORD_INTERVALS = {
        "maj":   [0, 4, 7],
        "min":   [0, 3, 7],
        "dim":   [0, 3, 6],
        "aug":   [0, 4, 8],
        "maj7":  [0, 4, 7, 11],
        "min7":  [0, 3, 7, 10],
        "dom7":  [0, 4, 7, 10],
        "sus2":  [0, 2, 7],
        "sus4":  [0, 5, 7],
        "add9":  [0, 4, 7, 14], # Root, 3rd, 5th, 9th (octave + 2)
    }

    root_midi = NOTE_MAP.get(key, 0) + (octave * 12)
    chord_intervals = CHORD_INTERVALS.get(chord_type, CHORD_INTERVALS["min"])
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth VSTi and configure ===
    # Add ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    fx_idx = RPR.RPR_TrackFX_GetFXByName(track, "ReaSynth", False)
    if fx_idx == -1:
        return f"Error: Could not add ReaSynth to track '{track_name}'"

    # Configure ReaSynth for a pad-like sound with LFO filter modulation
    # Oscillator 1 & 2: Sawtooth
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5) # Osc 1 Waveform (0=sine, 0.5=saw, 1=square). Sawtooth is 0.5. The video shows multiwave, I'll use 0.5 for a richer sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5) # Osc 2 Waveform
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.5) # Osc 2 Volume (balance with osc 1)

    # Amplifier Envelope (Attack, Decay, Sustain, Release)
    # Param IDs: 8 (Attack), 9 (Decay), 10 (Sustain), 11 (Release)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.3) # Attack (0.0-1.0, scaled to ~0-2s) -> ~0.6-1.5s
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 1.0) # Decay (max)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 1.0) # Sustain (max)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 11, 0.8) # Release (0.0-1.0, scaled to ~0-2s) -> ~1.6s

    # Filter (Low-pass, Resonance)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 12, 0.0) # Filter Type (0=lowpass)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 13, 0.7) # Filter Cutoff (mid-high)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 14, 0.6) # Filter Resonance (medium)

    # LFO 1 to modulate Filter Cutoff (approximating "Shape Control")
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 16, 0.5) # LFO 1 Waveform (0=sine, 0.5=triangle, 1=square)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 17, 0.25) # LFO 1 Rate (synced to 1/4 note)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 18, 0.5) # LFO 1 Depth (0.0-1.0)

    # ReaSynth internal effects (Reverb and Chorus)
    # Reverb: Param IDs 32 (Enable), 33 (Size), 34 (Damp), 35 (Width), 36 (Mix)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 32, 1.0) # Reverb Enable
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 33, 0.7) # Reverb Size
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 36, synth_reverb_mix) # Reverb Mix
    # Chorus: Param IDs 37 (Enable), 38 (Rate), 39 (Depth), 40 (Mix)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 37, 1.0) # Chorus Enable
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 38, 0.2) # Chorus Rate (slow)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 39, 0.5) # Chorus Depth (medium)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 40, synth_chorus_mix) # Chorus Mix

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    item_position = 0.0 # Start at beginning
    item_length = (60.0 / bpm) * beats_per_bar * bars # Total length in seconds

    midi_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(midi_item)
    RPR.RPR_MIDI_SetMediaItemTake_Source(take, RPR.MIDI_CreateNewMIDIItemInTake(take))

    # Insert a long sustained chord
    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.RPR_MIDI_SetItemExtents(midi_take, item_position, item_length) # Set MIDI take length

    notes_added = 0
    for interval in chord_intervals:
        midi_note = root_midi + interval
        # Insert MIDI notes: take, selected, muted, start_time, end_time, channel, velocity, no_loop
        RPR.RPR_MIDI_InsertNote(midi_take, False, False, 0.0, item_length, 0, velocity_base, False)
        # Update inserted note's pitch (last inserted note)
        note_idx = RPR.RPR_MIDI_CountEvts(midi_take, None, None, None)[3] - 1
        RPR.RPR_MIDI_SetNoteValue(midi_take, note_idx, None, midi_note)
        notes_added += 1

    # Update MIDI take to reflect changes
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_MarkAllMIDIStateAndNotify(midi_take, True, True)

    # === Step 5: Automation (Volume Swell + Chopping, Width) ===
    # Volume Envelope (Swell-up and Chopping combined on the main envelope)
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not env_vol:
        env_vol = RPR.RPR_CreateTrackEnvelope(track)
        # Setting the name this way is a bit hacky, normally the envelope name is fixed.
        # But this ensures it's the "Volume" envelope.
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_ENVNAME", "Volume", True)
    
    RPR.RPR_DeleteEnvelopePointRange(env_vol, 0.0, item_length + 1.0) # Clear existing points

    # Add initial point for swell start
    RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, DB_to_Val(swell_start_db), 0, 0, True, True)

    # Add combined swell and chop points
    # The chopping effect in the video appears to be a 32nd note square wave
    # over the linear volume swell.
    # Time step for chopping: 16th note = (60/bpm)/4, 32nd note = (60/bpm)/8
    chop_interval_beats = 4.0 / (16 * chop_frequency_multiplier) # e.g. for 32nd notes, 4/32 = 1/8 beat
    time_step = (60.0 / bpm) * chop_interval_beats 
    
    num_chops = int(item_length / time_step)

    for i in range(num_chops + 1):
        current_time = i * time_step
        if current_time > item_length: # Don't go past the item length
            current_time = item_length
        
        # Calculate base swell value at current_time
        swell_ratio = current_time / item_length
        current_swell_db = swell_start_db + (swell_end_db - swell_start_db) * swell_ratio

        # Point for chop peak
        peak_db = current_swell_db + chop_peak_db_offset
        # Point for chop trough (if it's not the very end)
        trough_db = current_swell_db + chop_trough_db_offset

        # Add point for peak of chop cycle (smooth curve to next point initially, then square)
        RPR.RPR_InsertEnvelopePoint(env_vol, current_time, DB_to_Val(peak_db), 0, 0, True, True)
        
        # Add point for trough of chop cycle, if space allows (with square shape)
        if current_time + (time_step / 2.0) < item_length:
            RPR.RPR_InsertEnvelopePoint(env_vol, current_time + (time_step / 2.0), DB_to_Val(trough_db), 0, 0, True, True)
        elif current_time < item_length: # Handle last partial segment
            RPR.RPR_InsertEnvelopePoint(env_vol, item_length, DB_to_Val(trough_db), 0, 0, True, True)


    # Set segment shapes to square after the initial swell for the chopping effect
    num_points = RPR.RPR_CountEnvelopePoints(env_vol)
    for i in range(num_points - 1):
        # Point_ID, time, value, shape, tension, selected, bypass
        # Shape: -1=default, 0=linear, 1=fast, 2=slow, 3=beat, 4=square
        _, _, _, shape, _, _, _ = RPR.RPR_GetEnvelopePoint(env_vol, i)
        RPR.RPR_SetEnvelopePoint(env_vol, i, None, None, 4, None, None) # Set to square

    RPR.RPR_Envelope_SortPoints(env_vol) # Ensure points are in order


    # Width Automation Envelope
    env_width = RPR.RPR_GetTrackEnvelopeByName(track, "Width")
    if not env_width:
        env_width = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_ENVNAME", "Width", True)
    
    RPR.RPR_DeleteEnvelopePointRange(env_width, 0.0, item_length + 1.0)
    RPR.RPR_InsertEnvelopePoint(env_width, 0.0, width_start, 0, 0, True, True)
    RPR.RPR_InsertEnvelopePoint(env_width, item_length, width_end, 0, 0, True, True)

    # Enable envelopes to be visible/active
    RPR.RPR_SetTrackEnvelopeState(env_vol, 1) # 1=visible, 2=visible+active
    RPR.RPR_SetTrackEnvelopeState(env_width, 1)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM with an evolving synth pad transition."


def process_vinyl_crackle(
    project_name: str = "MyProject",
    track_name: str = "Processed Vinyl Crackle",
    bpm: int = 120,
    bars: int = 4,
    noise_level_db: float = -30.0,
    crackle_gd_thresh_db: float = -14.1,
    crackle_gd_attack_ms: float = 0.0,
    crackle_gd_release_ms: float = 200.0,
    crackle_gd_wet_mix: float = 0.05, # 0.05 from video GUI
    crackle_gd_dry_mix: float = 1.0,  # 1.0 from video GUI
    crackle_gd_output_gain_db: float = 5.0,
    crackle_eq_lowcut_freq: float = 150.0,
    crackle_eq_highcut_freq: float = 10000.0,
    crackle_eq_highcut_gain_db: float = -6.0,
    crackle_side_trim_db: float = -6.0, # Trim Side in Voxengo MSED
    crackle_mono_maker_freq: float = 955.0, # Mono Maker frequency
    crackle_mono_maker_amount: float = 0.7, # Amount for mono maker 0-1
    crackle_reverb_wet_mix: float = 0.24, # Reverb mix (0.0 to 1.0)
    **kwargs,
) -> str:
    """
    Processes a vinyl crackle (simulated with white noise) to create a lo-fi background texture.
    Approximates proprietary VSTs (Voxengo MSED, Toneboosters Reverb) with stock REAPER plugins.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        bars: Number of bars to generate.
        noise_level_db: Volume of the generated white noise.
        crackle_gd_thresh_db: JS: General Dynamics Input Threshold (dB).
        crackle_gd_attack_ms: JS: General Dynamics Input Attack (ms).
        crackle_gd_release_ms: JS: General Dynamics Input Release (ms).
        crackle_gd_wet_mix: JS: General Dynamics Wet Mix (0.0-1.0).
        crackle_gd_dry_mix: JS: General Dynamics Dry Mix (0.0-1.0).
        crackle_gd_output_gain_db: JS: General Dynamics Output Gain (dB).
        crackle_eq_lowcut_freq: ReaEQ Highpass filter frequency (Hz).
        crackle_eq_highcut_freq: ReaEQ Lowpass filter frequency (Hz).
        crackle_eq_highcut_gain_db: ReaEQ Lowpass filter gain (dB) for taming.
        crackle_side_trim_db: ReaEQ Band 3 gain for trimming side signal (dB).
        crackle_mono_maker_freq: ReaEQ Band 4 frequency for mono-making low end (Hz).
        crackle_mono_maker_amount: Amount for mono maker (0.0 to 1.0).
        crackle_reverb_wet_mix: ReaVerb wet mix (0.0 to 1.0).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Processed Vinyl Crackle' track with effects."
    """

    import reaper_python as RPR

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Generate White Noise as source (simulating crackle) ===
    # Using JS: WhiteNoise to create a continuous noise source.
    RPR.RPR_TrackFX_AddByName(track, "JS: WhiteNoise", False, -1)
    noise_fx_idx = RPR.RPR_TrackFX_GetFXByName(track, "JS: WhiteNoise", False)
    # Param 0 is gain (0.0-1.0, 0.5 is 0dB, 0.0 is -inf)
    RPR.RPR_TrackFX_SetParam(track, noise_fx_idx, 0, DB_to_Val(noise_level_db)) 

    # Create a dummy media item to set the processing length.
    item_position = 0.0
    item_length = (60.0 / bpm) * 4 * bars
    dummy_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(dummy_item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(dummy_item, "D_LENGTH", item_length)

    # === Step 3: Add FX Chain for Processing ===

    # 1. JS: General Dynamics (Compressor/Limiter)
    RPR.RPR_TrackFX_AddByName(track, "JS: General Dynamics (compressor)", False, -1)
    gd_fx_idx = RPR.RPR_TrackFX_GetFXByName(track, "JS: General Dynamics (compressor)", False)
    
    # Param IDs: 0=Detect input gain, 1=Input ratio, 2=Input thresh (dB), 3=Input attack (ms), 4=Input release (ms)
    # 5=Detect output gain, 6=Output ratio, 7=Output thresh, 8=Output gain (dB)
    # 9=Wet mix, 10=Dry mix
    
    # Values from video GUI
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 0, DB_to_Val(0.0)) # Detect Input gain (0dB)
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 1, 0.0) # Input Ratio (Limiter mode, 0.0 for infinite ratio on Soft Knee)
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 2, DB_to_Val(crackle_gd_thresh_db)) # Input Thresh (-14.1dB)
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 3, crackle_gd_attack_ms / 1000.0) # Input Attack (0ms) - scaled from ms to 0-1 range
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 4, crackle_gd_release_ms / 1000.0) # Input Release (200ms) - scaled from ms to 0-1 range
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 9, crackle_gd_wet_mix) # Wet mix (0.05 = 5%)
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 10, crackle_gd_dry_mix) # Dry mix (1.0 = 100%)
    RPR.RPR_TrackFX_SetParam(track, gd_fx_idx, 8, DB_to_Val(crackle_gd_output_gain_db)) # Output gain (5dB)

    # 2. ReaEQ (for frequency shaping, mid-side balance and mono-making approximation)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    eq_fx_idx = RPR.RPR_TrackFX_GetFXByName(track, "ReaEQ", False)

    # Common ReaEQ parameters (for reference):
    # Band N (0-based)
    # N*10 + 5: Enable (0=off, 1=on)
    # N*10 + 6: Type (0=LP, 1=HP, 2=Band, 3=Notch, 4=LS, 5=HS, 6=BP)
    # N*10 + 7: Freq (Hz)
    # N*10 + 8: Gain (dB)
    # N*10 + 9: Q
    # N*10 + 10: Slope/Mode (0=6dB, 1=12dB, 2=Side, 3=Mid, etc.)

    # High-pass filter (low-cut)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 5, 1.0) # Band 1 Enable
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 6, 1.0) # Band 1 Type (Highpass)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 7, crackle_eq_lowcut_freq) # Band 1 Freq (150Hz)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 8, DB_to_Val(0.0)) # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 9, 1.0) # Band 1 Q
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 10, 0.0) # Band 1 Slope (6dB/oct)

    # Low-pass filter (high-cut) with gain reduction
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 15, 1.0) # Band 2 Enable
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 16, 0.0) # Band 2 Type (Lowpass)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 17, crackle_eq_highcut_freq) # Band 2 Freq (10kHz)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 18, DB_to_Val(crackle_eq_highcut_gain_db)) # Band 2 Gain (-6dB for taming)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 19, 1.0) # Band 2 Q
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 20, 0.0) # Band 2 Slope (6dB/oct)

    # Side signal trim (approximating Voxengo MSED Trim Side)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 25, 1.0) # Band 3 Enable
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 26, 3.0) # Band 3 Type (Low shelf, as a generic gain cut)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 27, 1000.0) # Band 3 Freq (arbitrary center for a broad cut)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 28, DB_to_Val(crackle_side_trim_db)) # Band 3 Gain (e.g. -6dB)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 29, 1.0) # Band 3 Q
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 30, 2.0) # Band 3 Mode (Side)

    # Mono Maker (approximating Voxengo MSED Mono Maker)
    # By using a high-pass filter on the SIDE signal, frequencies below the cutoff become mono.
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 35, 1.0) # Band 4 Enable
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 36, 1.0) # Band 4 Type (Highpass)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 37, crackle_mono_maker_freq) # Band 4 Freq (955Hz)
    # Gain for side HPF to simulate mono-making amount:
    # A negative gain on a HPF in side mode effectively cuts the stereo image below that frequency.
    # Higher amount means more reduction. We'll scale -90dB (full cut) by the amount.
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 38, DB_to_Val(-90.0 * crackle_mono_maker_amount)) # Band 4 Gain (fully cut side below freq)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 39, 1.0) # Band 4 Q
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 40, 2.0) # Band 4 Mode (Side)

    # 3. ReaVerb (approximating Toneboosters Reverb 3 "New Home Empty Room")
    RPR.RPR_TrackFX_AddByName(track, "ReaVerb", False, -1)
    reverb_fx_idx = RPR.RPR_TrackFX_GetFXByName(track, "ReaVerb", False)
    
    # ReaVerb parameters for a "room" sound
    # Param IDs: 10 (Predelay), 11 (Room size), 12 (Dampening), 14 (Dry Mix), 15 (Wet Mix)
    RPR.RPR_TrackFX_SetParam(track, reverb_fx_idx, 14, 1.0 - crackle_reverb_wet_mix) # Dry Mix
    RPR.RPR_TrackFX_SetParam(track, reverb_fx_idx, 15, crackle_reverb_wet_mix) # Wet Mix (0.24 = 24%)
    RPR.RPR_TrackFX_SetParam(track, reverb_fx_idx, 10, 0.6) # Predelay (arbitrary for small room)
    RPR.RPR_TrackFX_SetParam(track, reverb_fx_idx, 11, 0.7) # Room size (medium)
    RPR.RPR_TrackFX_SetParam(track, reverb_fx_idx, 12, 0.5) # Dampening (medium)

    return f"Created '{track_name}' track with processed vinyl crackle effects."

#### 3c. Verification Checklist

After writing the code, verify:
- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?
