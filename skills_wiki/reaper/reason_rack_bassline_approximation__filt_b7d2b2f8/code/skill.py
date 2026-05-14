import reaper_python as RPR

def create_reason_rack_bassline_approx(
    project_name: str = "MyProject",
    track_name: str = "Synth Bass (Approx)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    bass_octave: int = 2,  # MIDI Octave (C0 is 0, C1 is 1, etc.)
    filter_sweep_start_freq: float = 100.0, # Hz
    filter_sweep_end_freq: float = 5000.0,  # Hz
    **kwargs,
) -> str:
    """
    Create an approximate synth bassline pattern with a filter sweep, inspired by
    the Reason Rack Bassline Generator and filter modulation shown in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        bass_octave: MIDI octave for the bassline (e.g., 2 for C2-B2).
        filter_sweep_start_freq: Starting frequency for the low-pass filter sweep (Hz).
        filter_sweep_end_freq: Ending frequency for the low-pass filter sweep (Hz).
        **kwargs: Additional overrides (not used in this specific implementation).

    Returns:
        Status string, e.g., "Created 'Synth Bass (Approx)' with 32 notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    # Scales are not directly used for the specific melodic pattern here,
    # as the pattern uses fixed semitone offsets, but kept for extensibility.
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

    # === Step 1: Set Tempo (if different from current project tempo) ===
    # Get current project tempo, only set if different to avoid unnecessary action
    current_bpm = RPR.RPR_GetProjectBPM(0, 0, 0) # Use 0,0,0 for current project
    if abs(current_bpm - bpm) > 0.1: # Allow for minor floating point differences
        RPR.RPR_SetCurrentBPM(0, float(bpm), False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth and ReaEQ FX ===
    # Add ReaSynth (placeholder for synth bass)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    # Set ReaSynth to Saw wave for a classic synth bass sound (Parameter 4 is Osc1 Waveform, 0=Sine, 1=Saw, 2=Square, 3=Triangle)
    # Parameter 9 is Amp Envelope Decay, reduce slightly for punchier bass
    fx_synth = RPR.RPR_TrackFX_GetFX(track, 0)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 1.0) # Osc1 to Saw
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 9, 0.2) # Amp Decay reduced

    # Add ReaEQ for filtering
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)
    fx_eq = RPR.RPR_TrackFX_GetFX(track, 1) # ReaEQ is the second FX (index 1)

    # Configure ReaEQ for a Low-Pass Filter (Band 1, parameter 10 is Band 1 Enable, 11 is Band 1 Type, 12 is Freq, 13 is Q)
    # ReaEQ Band 1 parameters:
    # 0 = Band 1 Gain
    # 1 = Band 1 Freq (Hz) - this is what we'll automate
    # 2 = Band 1 Q
    # 3 = Band 1 Type (0=LP, 1=HS, 2=BP, 3=Pk, 4=HP, 5=LS, 6=Notch) - actually 1 for band 1, 0 is gain for band 1
    # Let's map parameters for ReaEQ for accuracy
    # ReaEQ param IDs:
    # Band 1: Freq (1), Q (2), Gain (3), Type (4)
    # Band 2: Freq (5), Q (6), Gain (7), Type (8)
    # ... and so on.

    # We want to use Band 1 as a Low Pass Filter.
    # Enable Band 1 (param 0 for enabled state of first band, value 1.0 = enabled)
    # Set Band 1 Type to Low-Pass (param 4, value 0.0 = Low Pass)
    # Set Band 1 Q (resonance) (param 2, value 1.0 = moderate Q)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 0, 1.0) # Enable band 1
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 4, 0.0) # Band 1 Type: Low Pass
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 2, 1.0) # Band 1 Q: 1.0 (moderate resonance)

    # === Step 4: Create MIDI Item and Insert Notes ===
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    bar_length_sec = seconds_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    item_position = 0.0

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    midi_take = RPR.RPR_MIDI_SetItemExtents(item, 0, 0, 0) # Get MIDI take for editing

    root_note_midi = NOTE_MAP.get(key.upper(), 0) + (bass_octave * 12)

    # Bassline pattern: [Root, Perfect 5th, Minor 3rd, Major 2nd] relative to root
    # Notes are triggered every 1/4th note, duration is 1/8th note.
    # Relative pitches in semitones:
    # 0 (Root), 7 (P5), 3 (m3), 2 (M2)
    relative_pitches = [0, 7, 3, 2]
    velocities = [velocity_base, int(velocity_base * 0.8), int(velocity_base * 0.8), int(velocity_base * 0.8)]
    note_duration_beats = 0.5  # 1/8th note

    notes_inserted_count = 0
    RPR.RPR_MIDI_DisableSort(midi_take) # Disable sorting for faster insertion
    for bar in range(bars):
        for i in range(len(relative_pitches)):
            position_beats = bar * beats_per_bar + (i * 1.0) # Trigger every quarter note
            note_midi = root_note_midi + relative_pitches[i]
            
            # Ensure MIDI note is within valid range (0-127)
            note_midi = max(0, min(127, note_midi))

            # RPR_MIDI_InsertNote(take, selected, muted, start_beat, end_beat, channel, velocity, pitch)
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, position_beats,
                                    position_beats + note_duration_beats,
                                    0, velocities[i], note_midi)
            notes_inserted_count += 1
    RPR.RPR_MIDI_Sort(midi_take) # Re-sort MIDI notes after insertion
    RPR.RPR_MIDI_Commit(midi_take) # Commit MIDI changes

    # === Step 5: Add Filter Automation ===
    # ReaEQ Band 1 Frequency parameter is parameter 1.
    # Parameter range for frequency is 0.0-1.0, mapping to a logarithmic scale.
    # To convert Hz to ReaEQ param value: log10(Hz/20) / log10(20000/20) for 20-20kHz range
    # Freq = 20 * 10^(param_val * 3) -> log10(Freq/20) / 3
    
    def hz_to_releq_param(hz_val):
        return (RPR.RPR_log10(hz_val / 20.0)) / (RPR.RPR_log10(20000.0 / 20.0))
    
    start_param_val = hz_to_releq_param(filter_sweep_start_freq)
    end_param_val = hz_to_releq_param(filter_sweep_end_freq)

    fx_param_idx = 1 # ReaEQ Band 1 Freq is parameter index 1
    
    # Get the envelope for the ReaEQ Band 1 Frequency
    env_name_str = RPR.RPR_TrackFX_GetParamName(track, fx_eq, fx_param_idx, "", 256)[1]
    envelope = RPR.RPR_GetTrackEnvelopeByName(track, f"FX 2 ({RPR.RPR_TrackFX_GetFXName(track, fx_eq, '', 256)[1]}): {env_name_str}")

    if not envelope:
        envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(envelope, False, f"<ENVELOPE {RPR.RPR_TrackFX_GetFXGUID(track, fx_eq)} {fx_param_idx}>", False)
        RPR.RPR_SetEnvelopeStateChunk(envelope, False, f"ACT {RPR.RPR_TrackFX_GetEnabled(track, fx_eq)}", False)

    # Clear existing points (optional, but good for clean runs)
    RPR.RPR_DeleteEnvelopePointRange(envelope, item_position, item_position + item_length)

    # Insert automation points
    RPR.RPR_InsertEnvelopePoint(envelope, item_position, start_param_val, 0, 0, True) # First point at start
    RPR.RPR_InsertEnvelopePoint(envelope, item_position + item_length, end_param_val, 0, 0, True) # Last point at end

    # Enable write mode for automation
    RPR.RPR_SetTrackSendInfo_Value(track, -1, 0, "D_AUTOMODE", 2.0) # 2.0 corresponds to Write mode (or "Trim/Read Touch Latch Write")

    RPR.RPR_UpdateArrange() # Refresh REAPER UI

    return f"Created '{track_name}' with {notes_inserted_count} notes over {bars} bars at {bpm} BPM with a filter sweep."

