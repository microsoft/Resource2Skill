import reaper_python as RPR

def get_scale_midi_notes(root_note_midi: int, scale_type: str, octaves: int = 1) -> list:
    """Helper to generate MIDI notes for a given scale and root."""
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10], # Natural minor
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    scale_intervals = SCALES.get(scale_type, SCALES["major"])
    notes = []
    for octave in range(octaves):
        for interval in scale_intervals:
            notes.append(root_note_midi + (octave * 12) + interval)
    return notes

def get_midi_root_from_key(key: str, octave: int = 3) -> int:
    """Helper to convert key string to MIDI root note."""
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    base_midi_note = NOTE_MAP.get(key.upper(), 0) # Default to C
    return base_midi_note + (octave * 12) # C3 = 48 (MIDI note number for C in octave 3)


def automate_anything_quickly(
    project_name: str = "MyProject",
    track_name: str = "Automated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Demonstrates how to quickly automate various parameters (Volume, Pan, Mute, FX parameters) in REAPER.

    The script creates a new track with a ReaSynth playing a sustained note
    and adds automation envelopes for volume, pan, mute, and a ReaEQ low-pass filter.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this specific skill but included for composability).

    Returns:
        Status string, e.g., "Created 'Automated Synth' track with automation examples."
    """

    # --- Step 1: Set Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Step 2: Create Track ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Set default track automation mode to Trim/Read (0).
    # Other modes: 1=Read, 2=Touch, 3=Latch, 4=Write, 5=Latch Preview
    RPR.RPR_GetSetMediaTrackInfo_Value(track, "I_AUTOMODE", 0) 

    # --- Step 3: Add ReaSynth and a simple MIDI item ---
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    
    # Create a MIDI item on the track
    item_start_time = 0.0
    item_length = bars * (60.0 / bpm) * 4 # duration in seconds for 'bars' bars (assuming 4 beats/bar)
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Create a blank MIDI source for the take
    RPR.RPR_MIDI_SetItemExtents(RPR.RPR_GetMediaItemTake_Item(take), 0.0, item_length, True)

    # Insert a sustained MIDI note at the root of the chosen key for the item's duration
    midi_root_note = get_midi_root_from_key(key, octave=3) # Default to C3
    RPR.MIDI_InsertNote(RPR.RPR_GetMediaItemTake_Source(take), False, False, 0.0, item_length, 0, velocity_base, midi_root_note, False)
    RPR.RPR_MIDI_Sort(RPR.RPR_GetMediaItemTake_Source(take))
    RPR.RPR_MarkAllMIDIItemsDirty(RPR.RPR_GetMediaItemTake_Item(take))
    
    # --- Step 4: Add Automation Envelopes ---
    # Automation Envelope Point Shape Constants:
    # 0 = normal (linear)
    # 1 = fast start (slow end)
    # 2 = slow start (fast end)
    # 3 = smooth (bezier)
    # 4 = square

    # Helper to set envelope visibility and arming
    def set_envelope_state(env_obj, visible=True, armed=True):
        if env_obj:
            vis_str = "VISIBLE 1" if visible else "VISIBLE 0"
            arm_str = "ARMED 1" if armed else "ARMED 0"
            RPR.RPR_SetEnvelopeStateChunk(env_obj, f"<ENVCHUNK_START> {vis_str} {arm_str} <ENVCHUNK_END>", True)

    # 4a. Volume Automation
    volume_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not volume_env: # Create if it doesn't exist
        volume_env = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(volume_env, "VOL", True) # Make it a volume envelope
    set_envelope_state(volume_env) # Make visible and armed
    
    RPR.RPR_DeleteEnvelopePointRange(volume_env, 0.0, item_length) # Clear existing points
    RPR.RPR_InsertEnvelopePoint(volume_env, 0.0, RPR.RPR_DB2SL(-12.0), 3, 0.0, True, False) # Start at -12dB
    RPR.RPR_InsertEnvelopePoint(volume_env, item_length / 2, RPR.RPR_DB2SL(0.0), 3, 0.0, True, False) # Mid at 0dB
    RPR.RPR_InsertEnvelopePoint(volume_env, item_length, RPR.RPR_DB2SL(-12.0), 3, 0.0, True, False) # End at -12dB

    # 4b. Pan Automation
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if not pan_env: # Create if it doesn't exist
        pan_env = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(pan_env, "PAN", True) # Make it a pan envelope
    set_envelope_state(pan_env) # Make visible and armed
    
    RPR.RPR_DeleteEnvelopePointRange(pan_env, 0.0, item_length) # Clear existing points
    RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, 0.0, 3, 0.0, True, False) # Left (-100%)
    RPR.RPR_InsertEnvelopePoint(pan_env, item_length / 4, 1.0, 3, 0.0, True, False) # Right (+100%)
    RPR.RPR_InsertEnvelopePoint(pan_env, item_length / 2, 0.5, 3, 0.0, True, False) # Center (0%)
    RPR.RPR_InsertEnvelopePoint(pan_env, 3 * item_length / 4, 0.0, 3, 0.0, True, False) # Left (-100%)
    RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.5, 3, 0.0, True, False) # Center (0%)

    # 4c. Mute Automation
    mute_env = RPR.RPR_GetTrackEnvelopeByName(track, "Mute")
    if not mute_env: # Create if it doesn't exist
        mute_env = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(mute_env, "MUTE", True) # Make it a mute envelope
    set_envelope_state(mute_env) # Make visible and armed
    
    RPR.RPR_DeleteEnvelopePointRange(mute_env, 0.0, item_length) # Clear existing points
    # Mute values are 0.0 (unmuted) or 1.0 (muted)
    RPR.RPR_InsertEnvelopePoint(mute_env, 0.0, 0.0, 4, 0.0, True, False) # Unmuted
    RPR.RPR_InsertEnvelopePoint(mute_env, item_length / 2 - 0.01, 0.0, 4, 0.0, True, False) # Unmuted
    RPR.RPR_InsertEnvelopePoint(mute_env, item_length / 2, 1.0, 4, 0.0, True, False) # Muted
    RPR.RPR_InsertEnvelopePoint(mute_env, item_length - 0.01, 1.0, 4, 0.0, True, False) # Muted
    RPR.RPR_InsertEnvelopePoint(mute_env, item_length, 0.0, 4, 0.0, True, False) # Unmuted


    # 4d. FX Parameter Automation (ReaEQ Low Pass Filter Frequency)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)
    eq_fx_idx = RPR.RPR_TrackFX_GetFXIdx(track, RPR.RPR_TrackFX_GetCount(track) - 1)

    # Set Band 1 to Low Pass filter type (Parameter 2 for band type, value 0.0 for Low Pass)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 2, 0.0) 

    # Parameter ID 3 for Band 1 Frequency (ReaEQ)
    # The name for the envelope will be "ReaEQ: Low-pass filter (band 1) Frequency"
    freq_env_name = "ReaEQ: Low-pass filter (band 1) Frequency"
    
    # It's good practice to ensure the parameter is touched/revealed for automation if getting by name
    # We can briefly set its value to ensure the envelope is creatable/retrievable
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 3, 0.5) # Set initial frequency (normalized 0-1)

    freq_env = RPR.RPR_GetTrackEnvelopeByName(track, freq_env_name)

    if freq_env:
        set_envelope_state(freq_env) # Make visible and armed
        RPR.RPR_DeleteEnvelopePointRange(freq_env, 0.0, item_length) # Clear existing points
        # ReaEQ frequency parameter values are normalized 0-1, mapping to its frequency range.
        RPR.RPR_InsertEnvelopePoint(freq_env, 0.0, 0.1, 3, 0.0, True, False) # Start freq low
        RPR.RPR_InsertEnvelopePoint(freq_env, item_length / 2, 0.9, 3, 0.0, True, False) # Mid freq high
        RPR.RPR_InsertEnvelopePoint(freq_env, item_length, 0.1, 3, 0.0, True, False) # End freq low
    else:
        RPR.RPR_ShowConsoleMsg("Could not create/retrieve ReaEQ Frequency envelope. Ensure the parameter is revealed for automation in the FX window.\n")
        
    RPR.RPR_UpdateArrange() # Refresh REAPER UI to show envelopes

    return f"Created '{track_name}' track with automation examples (Volume, Pan, Mute, ReaEQ LP Freq) over {bars} bars."
