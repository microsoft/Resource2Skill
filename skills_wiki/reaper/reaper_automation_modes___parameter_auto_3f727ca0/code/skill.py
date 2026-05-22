import reaper_python as RPR

def create_automation_demonstration(
    project_name: str = "ReaperAutomationDemo",
    track_name: str = "Automated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a synth track with a sustained chord and demonstrates various
    automation types (Volume, Pan, Mute, ReaEQ Low-Pass Filter) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate automation over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this skill but for composability).

    Returns:
        Status string, e.g., "Created 'Automated Synth' with volume, pan, mute, and EQ automation over 4 bars."
    """
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

    # --- Setup Project ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # --- Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- MIDI Item (Sustained Chord) ---
    beats_per_bar = 4
    item_position = 0.0
    item_length = float(bars * beats_per_bar) # Length in beats
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)
    
    midi_take = RPR.RPR_MIDI_SetItemExtents(item, 0, 0) # Ensure it's a MIDI take

    root_midi = NOTE_MAP.get(key.capitalize(), 0) + 60 # C4 as base octave
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Create a simple major triad (root, 3rd, 5th) and octave
    chord_notes_intervals = [scale_intervals[0], scale_intervals[2], scale_intervals[4], scale_intervals[0] + 12]
    
    for interval in chord_notes_intervals:
        pitch = root_midi + interval
        RPR.RPR_MIDI_InsertNote(midi_take, True, False, 0.0, item_length, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_UpdateArrange()

    # --- Add FX (ReaSynth and ReaEQ) ---
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)
    
    # --- Setup Automation Envelopes ---

    # Volume Envelope (param ID 0)
    # The first envelope is usually Volume, but we can explicitly get it.
    vol_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not vol_envelope:
        RPR.RPR_TrackFX_AddByName(track, "Volume", True, -1) # Ensure Volume envelope is visible/created
        vol_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    RPR.RPR_SetEnvelopeState(vol_envelope, True) # Make sure it's visible
    RPR.RPR_Envelope_SetChunk(vol_envelope, '', True) # Clear existing points for demo
    
    # Simple volume fade/swell
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 0.0, 1.0, 0, 0, 0, True) # Start at 0dB (1.0 = 0dB)
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 0.5 * item_length, 0.2, 0, 0, 0, True) # Dip to -14dB (approx 0.2)
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 0.75 * item_length, 1.0, 0, 0, 0, True) # Back to 0dB
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 1.0 * item_length, 0.0, 0, 0, 0, True) # Fade out to -inf (0.0)

    # Pan Envelope (param ID 1)
    pan_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if not pan_envelope:
        RPR.RPR_TrackFX_AddByName(track, "Pan", True, -1)
        pan_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")

    RPR.RPR_SetEnvelopeState(pan_envelope, True)
    RPR.RPR_Envelope_SetChunk(pan_envelope, '', True) # Clear existing points
    
    # Simple pan sweep (0.5 = center, 0.0 = full left, 1.0 = full right)
    RPR.RPR_InsertEnvelopePoint(pan_envelope, 0.0, 0.0, 0, 0, 0, True) # Full Left
    RPR.RPR_InsertEnvelopePoint(pan_envelope, 0.5 * item_length, 1.0, 0, 0, 0, True) # Full Right
    RPR.RPR_InsertEnvelopePoint(pan_envelope, 1.0 * item_length, 0.0, 0, 0, 0, True) # Full Left

    # Mute Envelope (param ID 2)
    mute_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Mute")
    if not mute_envelope:
        RPR.RPR_TrackFX_AddByName(track, "Mute", True, -1)
        mute_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Mute")

    RPR.RPR_SetEnvelopeState(mute_envelope, True)
    RPR.RPR_Envelope_SetChunk(mute_envelope, '', True) # Clear existing points
    
    # Mute/Unmute pattern (0.0 = unmute, 1.0 = mute)
    for i in range(bars * 2): # Two points per bar (on/off)
        pos = i * (item_length / (bars * 2))
        val = 0.0 if (i % 2 == 0) else 1.0 # Unmute, then Mute
        RPR.RPR_InsertEnvelopePoint(mute_envelope, pos, val, 0, 0, 0, True)
    RPR.RPR_InsertEnvelopePoint(mute_envelope, item_length, 0.0, 0, 0, 0, True) # Ensure ends unmute

    # ReaEQ Low-Pass Frequency Automation (FX index 1, param ID 1 for freq band 1)
    # Get ReaEQ index (assuming it's the second FX)
    fx_idx = -1
    for i in range(RPR.RPR_TrackFX_GetCount(track)):
        fx_name = RPR.RPR_TrackFX_GetFXName(track, i, '', 1024)[2]
        if "ReaEQ" in fx_name:
            fx_idx = i
            break
    
    if fx_idx != -1:
        # Enable 1st band (low-pass filter) on ReaEQ if not already
        # Param 0 is Enabled state, 1 is Type for band 1, 2 is Frequency for band 1
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 1.0) # Enable band 1
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Set band 1 to Lowpass (0.0 for lowpass type)
        
        # Get parameter envelope for Lowpass Frequency (parameter ID 2 for band 1 freq)
        eq_freq_envelope = RPR.RPR_GetFXEnvelope(track, fx_idx, 2, True)
        RPR.RPR_SetEnvelopeState(eq_freq_envelope, True)
        RPR.RPR_Envelope_SetChunk(eq_freq_envelope, '', True) # Clear existing points

        # Automate low-pass frequency (0.0 to 1.0 range, maps to Hz)
        # Assuming ReaEQ freq range maps roughly: 0.0=20Hz, 1.0=20000Hz (need to know exact scaling for precision)
        # Using approximated values for a sweep
        RPR.RPR_InsertEnvelopePoint(eq_freq_envelope, 0.0, 1.0, 0, 0, 0, True) # Start open (20kHz)
        RPR.RPR_InsertEnvelopePoint(eq_freq_envelope, 0.25 * item_length, 0.2, 0, 0, 0, True) # Sweep down (approx 200Hz)
        RPR.RPR_InsertEnvelopePoint(eq_freq_envelope, 0.75 * item_length, 0.8, 0, 0, 0, True) # Sweep up (approx 8kHz)
        RPR.RPR_InsertEnvelopePoint(eq_freq_envelope, 1.0 * item_length, 1.0, 0, 0, 0, True) # End open (20kHz)
    else:
        return "ERROR: ReaEQ not found on track."

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with volume, pan, mute, and EQ automation over {bars} bars."

