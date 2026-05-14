import reaper_python as RPR

# Music theory lookup tables (for potential future enhancements)
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

def create_retro_synth_swell(
    project_name: str = "AgentProject",
    track_name: str = "Retro Synth Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    base_midi_note: int = 60, # C3
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a retro synth pad with layered volume swell, chopping effect,
    and stereo width automation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created synth track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        base_midi_note: The base MIDI note for the sustained pad (e.g., 60 for C3).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this simple synth).

    Returns:
        Status string describing what was created.
    """
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    ppq = 960 # Pulses per quarter note, common in REAPER MIDI

    # --- Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_RECMODE", "0", True) # Set to input off

    # --- Create MIDI Item ---
    item_pos = 0.0
    item_length = bars * (60.0 / bpm) * 4 # length in seconds (bars * beats/bar * seconds/beat)
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", "Synth Pad MIDI", True)
    
    # Insert a sustained MIDI note for the entire item length
    RPR.RPR_MIDI_SetItemExtents(item, 0, item_length)
    midi_take = RPR.RPR_MIDI_GrzNew(take) # Get MIDI Take
    
    start_time_ppq = 0
    end_time_ppq = int(item_length * (bpm / 60.0) * ppq) # Convert seconds to ppq
    
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, start_time_ppq, end_time_ppq, 0, base_midi_note, velocity_base, True)
    RPR.RPR_MIDI_Grz_Update(midi_take)
    RPR.RPR_MIDI_Grz_Free(midi_take)

    # --- Add FX Chain (ReaSynth, ReaVerb, JS: Chorus) ---
    fx_count = RPR.RPR_TrackFX_GetCount(track)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, fx_count)
    reasynt_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1

    # ReaSynth: Basic pad sound approximation (adjust for taste)
    # Osc 1 Waveform (0=sine, 0.25=saw, 0.5=square, 0.75=triangle)
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 0, 0.25) # Osc 1 Saw
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 1, 0.25) # Osc 2 Saw
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 2, 0.5)  # Osc 2 Pitch Fine (detune)
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 3, 0.05) # Osc 2 Level
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 13, 0.5) # Filter cutoff LFO rate (approx flanging)
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 14, 0.2) # Filter cutoff LFO depth
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 15, 0.8) # Amp Attack
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 16, 0.8) # Amp Decay
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 17, 0.5) # Amp Sustain
    RPR.RPR_TrackFX_SetParam(track, reasynt_fx_idx, 18, 0.8) # Amp Release

    fx_count = RPR.RPR_TrackFX_GetCount(track)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerb (Cockos)", False, fx_count)
    reaverb_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    RPR.RPR_TrackFX_SetParam(track, reaverb_fx_idx, 0, 0.4) # Wet level (adjust as needed)

    fx_count = RPR.RPR_TrackFX_GetCount(track)
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, fx_count)
    chorus_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    RPR.RPR_TrackFX_SetParam(track, chorus_fx_idx, 0, 0.5) # Delay (adjust for wider sound)
    RPR.RPR_TrackFX_SetParam(track, chorus_fx_idx, 1, 0.5) # Depth

    # --- Automation: Volume Swell (Envelope 1) ---
    vol_envelope_1 = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not vol_envelope_1:
        vol_envelope_1 = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetEnvelopeStateString(vol_envelope_1, "Volume", True) # Name it "Volume"

    RPR.RPR_Envelope_DeletePointsRange(vol_envelope_1, item_pos, item_pos + item_length)
    RPR.RPR_InsertEnvelopePoint(vol_envelope_1, item_pos, RPR.DBToNative(-4.6), 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(vol_envelope_1, item_pos + item_length, RPR.DBToNative(0.0), 0, 0, False, True)
    RPR.RPR_SetEnvelopeState(vol_envelope_1, 1) # Set to Write mode (or Touch/Latch)

    # --- Automation: Volume Chopping (Envelope 2 - on top of Envelope 1) ---
    # REAPER allows multiple automation items on the same envelope that combine.
    # We'll create a new automation item for chopping.
    
    # Create an empty automation item on the volume envelope
    RPR.RPR_AddEnvelopePoint(vol_envelope_1, 0.0, 0.0, 0, 0, False, True) # Ensure envelope is visible
    RPR.RPR_SetEnvelopeState(vol_envelope_1, 0) # Back to Read mode

    # Create an automation item. In REAPER's UI this is done by right-clicking on the envelope.
    # ReaScript doesn't have a direct function to create "automation items" on top of existing ones like the UI does.
    # The video implies creating another item that overlaps.
    # To simulate this, we'll create a new volume envelope with the chopping effect,
    # and adjust the primary envelope's base level to compensate, or we simply draw points directly.
    # The prompt implies a "stacked" automation item. The simplest way in ReaScript is to draw the points directly
    # or create a second envelope that's linked (not feasible for standard volume).
    # The video shows two separate "envelope volume" lanes. This means they are two Automation Items on the same envelope.
    # For now, I will draw the chopped automation directly onto the existing volume envelope.
    # This will overwrite the swell, but demonstrate the chopping.
    # To truly "stack" as per the video's explanation of two items combining, we need a way to
    # create automation items directly in ReaScript, which isn't directly exposed for arbitrary points on existing envelopes.
    # As a workaround, I'll create a single envelope that combines both.

    # Combined Automation: Swell + Chopping
    RPR.RPR_Envelope_DeletePointsRange(vol_envelope_1, item_pos, item_pos + item_length) # Clear existing points

    seconds_per_32nd_note = (60.0 / bpm) / 8 # A 32nd note is 1/8th of a beat (1/4th note)
    for i in range(int(bars * 4 * 8)): # Bars * 4 beats/bar * 8 32nd notes/beat
        time = item_pos + (i * seconds_per_32nd_note)
        
        # Swell base calculation
        swell_value = RPR.DBToNative(-4.6 + (4.6 / (bars * 4 * 8)) * i)
        
        # Chopping modulation
        if i % 2 == 0: # On the beat
            chopping_mod = RPR.DBToNative(1.0)
        else: # Off-beat
            chopping_mod = RPR.DBToNative(-4.0)
            
        final_volume = RPR.DBToNative(RPR.NativeToDB(swell_value) + RPR.NativeToDB(chopping_mod))
        RPR.RPR_InsertEnvelopePoint(vol_envelope_1, time, final_volume, 0, 0, True, True)

    RPR.RPR_SetEnvelopeState(vol_envelope_1, 1) # Set to Write mode (or Touch/Latch)
    RPR.RPR_SetEnvelopeState(vol_envelope_1, 0) # Back to Read mode

    # --- Automation: Stereo Width (Mono to Stereo) ---
    width_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Width")
    if not width_envelope:
        width_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetEnvelopeStateString(width_envelope, "Width", True)

    RPR.RPR_Envelope_DeletePointsRange(width_envelope, item_pos, item_pos + item_length)
    RPR.RPR_InsertEnvelopePoint(width_envelope, item_pos, 0.0, 0, 0, False, True) # 0.0 = Mono
    RPR.RPR_InsertEnvelopePoint(width_envelope, item_pos + item_length, 1.0, 0, 0, False, True) # 1.0 = Full Stereo
    RPR.RPR_SetEnvelopeState(width_envelope, 1) # Set to Write mode
    RPR.RPR_SetEnvelopeState(width_envelope, 0) # Back to Read mode

    # --- Trim Volume (for overall adjustment, not automated here) ---
    # The trim volume envelope is typically used for overall level adjustment, not automation items.
    # It exists as a separate volume envelope on the track.
    # For now, we'll just ensure it's visible.
    trim_vol_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Trim Volume")
    if not trim_vol_envelope:
        trim_vol_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetEnvelopeStateString(trim_vol_envelope, "Trim Volume", True)
    RPR.RPR_SetEnvelopeState(trim_vol_envelope, 0) # Set to Read mode

    RPR.RPR_UpdateArrange()
    return f"Created '{track_name}' track with {bars} bars of synth swell and chopping effect."


def create_lofi_crackle_fx_chain(
    project_name: str = "AgentProject",
    track_name: str = "Crackle FX (PLACEHOLDER)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    **kwargs,
) -> str:
    """
    Creates a track with a placeholder audio item and applies an FX chain
    to process it into a lo-fi crackle texture. User must replace placeholder
    item with their own vinyl crackle sample.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars for the placeholder item.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_RECMODE", "0", True) # Set to input off

    # --- Create Placeholder Audio Item ---
    item_pos = 0.0
    item_length = bars * (60.0 / bpm) * 4 # length in seconds
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    # Add an empty take for the user to replace with their audio
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", "REPLACE WITH YOUR CRACKLE SAMPLE", True)


    # --- Add FX Chain: General Dynamics, ReaEQ, ReaVerb ---
    fx_count = RPR.RPR_TrackFX_GetCount(track)

    # 1. JS: General Dynamics (for transient flattening)
    RPR.RPR_TrackFX_AddByName(track, "JS: General Dynamics (Control)", False, fx_count)
    gen_dyn_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    
    # Enable bypass on first run, user can enable after setting up sample
    RPR.RPR_TrackFX_SetEnabled(track, gen_dyn_fx_idx, True)

    # General Dynamics curve points (x, y) - normalized 0-1
    # This approximates the curve shown in the video for transient taming.
    # The actual UI drawing is more complex, but we can set points.
    # The graph axes range from -120 to +20 dB for input and output.
    # Normalized input/output parameters 12 & 13 for curve points
    # P_12 (input gain) / P_13 (output gain)

    # Clear existing points (default might have some)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 12, -1.0) # Set input gain min
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 13, -1.0) # Set output gain min
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 12, 1.0) # Set input gain max
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 13, 1.0) # Set output gain max

    # Add points for the specific curve
    # 0.0 -> 0.0 (bottom-left, linear below threshold)
    # 0.4 -> 0.4 (threshold around -40dB, linear before)
    # 0.7 -> 0.5 (compression start, around -20dB input to -15dB output)
    # 1.0 -> 0.6 (heavy limiting, around 0dB input to -5dB output)
    
    # Values are normalized 0-1.
    # dB range is -120 to +20. So 0.5 is -50dB. 0.7 is -26dB. 1.0 is +20dB.
    # To get -40dB input: 0.57 * (120+20)/120 = 0.66
    # To get -20dB input: 0.71 * (120+20)/120 = 0.82
    # To get -5dB output: (5+20)/140 = 0.17
    # This is getting very complex to map normalized to dB and back for UI points without a direct API.
    # I will simplify to normalized values that match the *shape* visually, user can fine-tune.
    
    # Threshold at ~ -30dB (input_norm = 0.64)
    # Output at ~ -20dB (output_norm = 0.71)
    
    # Use hardcoded normalized values to get a similar curve shape
    # Example normalized points (Input, Output)
    # Linear below 0.6 input (approx -40dB)
    # Above 0.6, compresses to 0.8 output (approx -20dB)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 0, 0.0) # Input Gain
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 1, 0.0) # Detect Input Gain
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 2, 0.0) # Detect rms size (ms)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 3, 0.0) # Input pre-attack (ms)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 4, 0.0) # Gain Attack (ms) (0ms as per video)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 5, 20.0) # Input Release (ms)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 6, 0.0) # Gain Release (ms)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 7, 5.0) # Wet Mix (dB) (+5dB as per video)
    
    # The drawable curve parameters are tricky to set directly via param_idx.
    # The video shows a curve with a soft knee and then a hard limit.
    # We will approximate this shape by setting specific "Detect Input Gain" and "Output Gain" points.
    # For now, let's just make sure the Gain Attack is 0ms and Wet Mix is +5dB as mentioned.
    # The curve itself is difficult without direct API for arbitrary points.
    # I will rely on the default curve and the attack/release.
    # The actual curve seen in the video is a custom "General Dynamics" shape.
    # As this is a JSFX, the curve parameters are exposed differently than typical VSTs.
    # The video implies a custom curve drawn in the UI. ReaScript cannot directly "draw" curves in the JSFX UI.
    # So, I'll set some common compressor-like settings to get a similar *effect*.
    
    # Let's try to set a simple compression curve for illustrative purposes
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 1, 0.0) # Detect Input Gain (dB)
    RPR.RPR_TrackFX_SetParam(track, gen_dyn_fx_idx, 12, 0.0) # Output Gain (dB)

    # 2. ReaEQ (for high/low pass filtering)
    fx_count = RPR.RPR_TrackFX_GetCount(track)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, fx_count)
    reaeq_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1

    # High Pass Filter (Band 0)
    RPR.RPR_TrackFX_SetParam(track, reaeq_fx_idx, 0, 1.0) # Band 1 On
    RPR.RPR_TrackFX_SetParam(track, reaeq_fx_idx, 5, 0.0) # Band 1 Type: High Pass (0=LP, 1=HP, ...)
    RPR.RPR_TrackFX_SetParam(track, reaeq_fx_idx, 1, 0.01) # Band 1 Freq (approx 100-200Hz, normalized)
                                                           # (0.01 * 20000 Hz = 200 Hz)
    # Low Pass Filter (Band 1)
    RPR.RPR_TrackFX_SetParam(track, reaeq_fx_idx, 6, 1.0) # Band 2 On
    RPR.RPR_TrackFX_SetParam(track, reaeq_fx_idx, 11, 0.0) # Band 2 Type: Low Pass (0=LP, 1=HP, ...)
    RPR.RPR_TrackFX_SetParam(track, reaeq_fx_idx, 7, 0.5) # Band 2 Freq (approx 10kHz, normalized)
                                                          # (0.5 * 20000 Hz = 10000 Hz)

    # 3. ReaVerb (for room glue, approximating Toneboosters Reverb 3)
    fx_count = RPR.RPR_TrackFX_GetCount(track)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerb (Cockos)", False, fx_count)
    reaverb_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    
    # Approximate "new home empty room" and 24% wet.
    RPR.RPR_TrackFX_SetParam(track, reaverb_fx_idx, 0, 0.24) # Wet level (24% wet)
    RPR.RPR_TrackFX_SetParam(track, reaverb_fx_idx, 1, 0.1) # Dry level (small room, mostly wet)
    RPR.RPR_TrackFX_SetParam(track, reaverb_fx_idx, 2, 0.3) # Pre-delay (short)
    RPR.RPR_TrackFX_SetParam(track, reaverb_fx_idx, 3, 0.5) # Room size
    RPR.RPR_TrackFX_SetParam(track, reaverb_fx_idx, 4, 0.7) # Damping

    # --- Stereo Width Adjustment ---
    # The video uses Voxengo Span to narrow stereo below ~955 Hz.
    # ReaScript can set the track's default width.
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_WIDTH", 0.5) # Example: set to 50% width (adjust as needed)
                                                           # This simulates narrowing the stereo image.

    RPR.RPR_UpdateArrange()
    return f"Created '{track_name}' track with FX chain. Please replace the empty item with your crackle sample."


# Example usage (for testing, will not be part of the final skill agent call)
# if __name__ == '__main__':
#     # Call the synth skill
#     status_synth = create_retro_synth_swell(bars=4, bpm=100)
#     RPR.ShowConsoleMsg(status_synth + "\n")

#     # Call the crackle skill
#     status_crackle = create_lofi_crackle_fx_chain(bars=4, bpm=100)
#     RPR.ShowConsoleMsg(status_crackle + "\n")
