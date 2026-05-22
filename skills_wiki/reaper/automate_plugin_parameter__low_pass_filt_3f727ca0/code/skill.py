import reaper_python as RPR

def create_automation_filter_sweep(
    project_name: str = "MyProject",
    track_name: str = "Automated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    synth_velocity: int = 80,
    filter_start_freq: float = 200.0, # Hz
    filter_end_freq: float = 10000.0, # Hz
    **kwargs,
) -> str:
    """
    Creates a track with ReaSynth and ReaEQ, then automates a low-pass filter sweep
    on ReaEQ to demonstrate automation in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        synth_velocity: MIDI velocity for the synth note (0-127).
        filter_start_freq: Starting frequency for the low-pass filter sweep.
        filter_end_freq: Ending frequency for the low-pass filter sweep.
        **kwargs: Additional overrides (not used in this specific implementation).

    Returns:
        Status string, e.g., "Created 'Automated Synth' with filter sweep over 4 bars at 120 BPM"
    """
    # Music theory lookup tables (for potential future expansion)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        # ... other scales
    }

    # === Step 1: Set Tempo (if not already set, it's good practice) ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This command might overwrite user's BPM. Avoid if additive.

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item with a sustained note ===
    beats_per_bar = 4
    item_position = RPR.RPR_GetCursorPosition() # Start at current cursor position
    item_length_beats = float(bars * beats_per_bar)

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_beats) # REAPER item length is in beats when setting D_LENGTH

    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_CreateNewMIDIItemInTake(take, 0.0, item_length_beats, False))

    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.RPR_MIDI_SetItemExtents(midi_take, 0.0, item_length_beats)

    # Calculate root MIDI note
    root_midi_note = NOTE_MAP.get(key.capitalize(), 0) # Default to C if key not found
    midi_note_octave = 3 # C3
    full_midi_note = root_midi_note + (midi_note_octave * 12)

    # Insert a sustained MIDI note
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 0.0, item_length_beats, synth_velocity, 0, full_midi_note, False)
    RPR.RPR_MIDI_Sort(midi_take) # Sort notes for clean MIDI data

    # === Step 4: Add FX Chain (ReaSynth and ReaEQ) ===
    # Add ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)

    # Add ReaEQ
    eq_fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)
    if eq_fx_idx == -1:
        return f"Failed to add ReaEQ to '{track_name}'"
    
    # Set the first band (index 0) to Low Pass filter type.
    # ReaEQ Band 1 Type is usually parameter 1. Type values: 0=No Band, 1=Low Shelf, 2=High Shelf, 3=Band, 4=LoPass, 5=HiPass, 6=All Pass, 7=Notch, 8=BandPass, 9=Parallel Bandpass, 10=Band (alt.2)
    # We want 4 for Low Pass.
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 1, 4.0) # Set Band 1 type to Low Pass

    # === Step 5: Automate ReaEQ Low Pass Filter Frequency ===
    # ReaEQ Band 1 Frequency is usually parameter 2 for the first band.
    # Parameter index for Band 1 Frequency is 2.
    param_idx = 2 
    
    # Get the envelope for the parameter
    env = RPR.RPR_GetTrackEnvelopeByName(track, f"JS: ReaEQ (Cockos) - Band 1 Frequency")
    if not env:
        # If not found by name, try to create it or get it by parameter index.
        # This is more robust as parameter names can sometimes change.
        # TrackFX_SetParam_Ex needs FXGUID, but RPR_TrackFX_GetParamName doesn't use GUID.
        # Let's try to add a visible envelope for the parameter
        RPR.RPR_TrackFX_SetEnvelopeState(track, eq_fx_idx, param_idx, True, True)
        env = RPR.RPR_GetTrackEnvelopeByName(track, f"JS: ReaEQ (Cockos) - Band 1 Frequency")
        if not env:
            return f"Failed to get or create automation envelope for ReaEQ Low Pass Frequency on '{track_name}'"

    # Set automation mode to Write
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_AUTOMATION_MODE", 4) # 4 = Write mode

    # Add automation points for a sweep
    # Frequency values are often 0.0-1.0 in API for logarithmic scaling.
    # ReaEQ's frequency parameter is log scaled.
    # 20Hz (0.0) to 20kHz (1.0). So 200Hz to 10kHz would be roughly (log10(200)-log10(20))/(log10(20000)-log10(20))
    # Let's use frequency values directly and REAPER will convert them.
    
    # 4 points for a sweep up and down across the item length
    # Point 1: start_freq at 0 beats
    # Point 2: end_freq at item_length_beats / 2
    # Point 3: start_freq at item_length_beats (or similar to make a full cycle if `bars` is even)
    
    # Using 4 points for a smoother sweep (start, up, down, end)
    RPR.RPR_InsertEnvelopePoint(env, item_position + 0.0, filter_start_freq, 0, 0.5, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_position + item_length_beats / 3, filter_end_freq, 0, 0.5, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_position + (item_length_beats * 2) / 3, filter_start_freq, 0, 0.5, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_position + item_length_beats, filter_start_freq, 0, 0.5, False, True)
    
    # Select the item
    RPR.RPR_SetMediaItemInfo_Value(item, "B_UISEL", True)

    # Set automation mode back to Read
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_AUTOMATION_MODE", 1) # 1 = Read mode

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with ReaSynth, ReaEQ filter sweep, and automation over {bars} bars at {bpm} BPM."

