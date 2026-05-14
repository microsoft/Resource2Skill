def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Synth Filter Sweep",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    filter_start_freq: float = 200.0, # Hz
    filter_end_freq: float = 12000.0, # Hz
    **kwargs,
) -> str:
    """
    Create a synth track with a basic chord progression and a low-pass filter
    automation sweep in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (minimum 2 for a sweep).
        velocity_base: Base MIDI velocity (0-127).
        filter_start_freq: Starting frequency for the low-pass filter sweep (Hz).
        filter_end_freq: Ending frequency for the low-pass filter sweep (Hz).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Synth Filter Sweep' with automation over 4 bars at 120 BPM"
    """
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
    
    # Chord degrees relative to scale root
    CHORDS = {
        "major": [(0, 4, 7)],
        "minor": [(0, 3, 7)],
        "dom7":  [(0, 4, 7, 10)],
        "maj7":  [(0, 4, 7, 11)],
        "min7":  [(0, 3, 7, 10)],
    }

    import reaper_python as RPR

    RPR.Undo_BeginBlock2(0) # Begin undo block

    try:
        # === Step 1: Set Tempo ===
        # The tutorial shows a manual tempo change, let's ensure it's set
        RPR.RPR_SetCurrentBPM(0, bpm, False)

        # === Step 2: Create Track ===
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

        # === Step 3: Create MIDI Item ===
        root_midi_note = NOTE_MAP.get(key, 0) + 60 # C4 as base
        selected_scale = SCALES.get(scale, SCALES["major"])

        beats_per_bar = 4
        item_length = float(bars) # Length in bars
        
        # Create MIDI item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at bar 0
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_TakeFX_AddByName(take, "MIDI_editor", 0) # Add MIDI editor to take

        midi_take = RPR.RPR_MIDI_SetItemExtents(take, 0, 0)
        
        # Simple I-IV-V-I progression (adjust for scale if not major)
        # For simplicity and to focus on filter, use major triads, adjust notes for minor key
        chord_degrees = [(0, 4, 7), (5, 9, 12), (7, 11, 14), (0 + 12, 4 + 12, 7 + 12)] # I-IV-V-I in C
        
        if scale == "minor":
            chord_degrees = [(0, 3, 7), (5, 8, 12), (7, 10, 14), (0 + 12, 3 + 12, 7 + 12)] # i-iv-V-i in C minor
        
        # Insert MIDI notes (one chord per bar for a sustained effect)
        for bar_num in range(bars):
            for i, degree in enumerate(chord_degrees[bar_num % len(chord_degrees)]):
                pitch = root_midi_note + degree
                start_time = bar_num * beats_per_bar
                end_time = (bar_num + 1) * beats_per_bar - 0.1 # Sustain almost whole bar
                RPR.MIDI_InsertNote(midi_take, 0, 0, start_time, end_time, velocity_base, True, pitch, True)

        RPR.MIDI_Sort(midi_take)
        RPR.MIDI_SetItemExtents(take, 0.0, item_length, True) # Finalize MIDI item
        RPR.RPR_UpdateArrange()


        # === Step 4: Add FX Chain (ReaSynth + ReaEQ) ===
        # ReaSynth (Basic synth for the sound)
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
        # No specific parameter changes for ReaSynth, relying on default for a basic pad sound

        # ReaEQ (Low-pass filter)
        eq_fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)
        
        # Configure ReaEQ for Low Pass filter (Band 1)
        # Band 1 parameters: [enabled, type, freq, gain, bandwidth]
        # Type: 5 = Low Pass, 6 = High Pass, 0 = Band, etc.
        # Param 0: Band 1 Enabled (0.0=off, 1.0=on)
        # Param 1: Band 1 Type (0=LP Shelf, 1=HP Shelf, 2=Band, 3=Notch, 4=BP, 5=LP, 6=HP)
        # Param 2: Band 1 Freq (Hz)
        # Param 3: Band 1 Gain (dB)
        # Param 4: Band 1 Q (bandwidth in octaves if type is band/LP/HP)
        
        # Disable all bands initially and configure band 1 as low pass
        for band in range(4): # ReaEQ has 4 bands by default
            RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, band * 5 + 0, 0.0) # Disable band
        
        RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 0, 1.0) # Enable Band 1
        RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 1, 5.0) # Set Band 1 Type to Low Pass
        RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 4, 0.85) # Set Band 1 Q (bandwidth)
        # Frequency and Gain will be set via automation

        # === Step 5: Automate ReaEQ Frequency ===
        # The Low Pass Frequency for Band 1 in ReaEQ is parameter index 2
        # Param 0: Band 1 Enabled
        # Param 1: Band 1 Type
        # Param 2: Band 1 Freq (Hz) --> This is what we automate
        # Param 3: Band 1 Gain
        # Param 4: Band 1 Q

        # Get the envelope for ReaEQ Band 1 Frequency (parameter index 2)
        # RPR_GetTrackFXParameterString provides parameter name "Low Pass 1 Frequency"
        param_idx = 2 # Parameter index for Band 1 Frequency
        envelope = RPR.RPR_TrackFX_GetEnvelope(track, eq_fx_idx, param_idx, True)

        # Clear existing points to avoid conflicts with previous runs
        RPR.RPR_DeleteEnvelopePointRange(envelope, 0.0, item_length)

        # Insert automation points for a linear sweep
        # Point 1: Start of item, low frequency
        RPR.RPR_InsertEnvelopePoint(envelope, 0.0, filter_start_freq, 0, 0, False, True)
        
        # Point 2: End of item, high frequency
        RPR.RPR_InsertEnvelopePoint(envelope, item_length, filter_end_freq, 0, 0, False, True)
        
        # Ensure automation mode is "Read"
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_AUTOMODE", 1.0) # 1 = Read mode

        RPR.RPR_TrackList_AdjustWindows(False) # Refresh track list display
        RPR.RPR_UpdateArrange() # Update REAPER arrange view

        return f"Created '{track_name}' with {bars} bars of synth and low-pass filter automation from {filter_start_freq}Hz to {filter_end_freq}Hz at {bpm} BPM."

    except Exception as e:
        return f"Error creating pattern: {e}"
    finally:
        RPR.Undo_EndBlock2(0, "Create Synth Filter Sweep Pattern", -1) # End undo block
