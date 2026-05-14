import reaper_python as RPR
import math

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an evolving synth transition and a processed lo-fi crackle texture in REAPER.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides for specific parameters.

    Returns:
        Status string describing what was created.
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

    root_midi = NOTE_MAP.get(key, 0) # Default to C if key not found
    current_scale = SCALES.get(scale, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4.0 # Assuming 4/4 time signature
    seconds_per_beat = 60.0 / bpm
    bar_length_sec = seconds_per_beat * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # --- Synth Transition Track ---
    synth_track_name = "Synth Pad Transition"
    synth_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(synth_track_idx, True)
    synth_track = RPR.RPR_GetTrack(0, synth_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", synth_track_name, True)

    # === Step 2: Create MIDI Item for Synth ===
    synth_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_LENGTH", total_length_sec)
    synth_take = RPR.RPR_AddTakeToMediaItem(synth_item)

    RPR.MIDI_SetItemExtents(synth_item, 0.0, total_length_sec) # Set MIDI item length

    # Insert a sustained C major chord as a pad
    # C3, E3, G3, C4
    base_octave = 3
    midi_notes = [
        root_midi + base_octave * 12 + current_scale[0],  # C3
        root_midi + base_octave * 12 + current_scale[2],  # E3
        root_midi + base_octave * 12 + current_scale[4],  # G3
        root_midi + (base_octave + 1) * 12 + current_scale[0] # C4
    ]

    RPR.MIDI_SetItemExtents(synth_item, 0.0, total_length_sec)
    RPR.MIDI_ClearEvts(synth_take)
    RPR.MIDI_SetItemExtents(synth_item, 0.0, total_length_sec) # Re-set extents after clearing

    # Calculate MIDI item's end time in beats for MIDI_InsertNote
    item_end_beat = RPR.MIDI_GetItemDuration(synth_item) / seconds_per_beat

    for note in midi_notes:
        RPR.MIDI_InsertNote(
            synth_take, False, False, 0.0, item_end_beat,
            0, note, velocity_base, True
        )

    RPR.MIDI_Sort(synth_take)
    RPR.MIDI_MarkAll(synth_take)
    RPR.MIDI_SetCC(synth_take, False, False, 0, 7, -1, -1, 100, True) # Set default volume CC

    # === Step 3: Add FX Chain for Synth ===
    # ReaSynth (basic synth pad)
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth (Cockos)", False, -1)
    # To approximate LFO mod: Set some ReaSynth parameters that LFO might modulate
    # LFO rate (param 19), LFO depth (param 20), Filter Cutoff (param 9)
    # These are illustrative, exact mapping from Hybrid 3 is not direct.
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 19, 0.25) # LFO Rate
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 20, 0.5)  # LFO Depth
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 9, 0.7)   # Filter Cutoff

    # ReaVerb (Hall Reverb)
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaVerb (Cockos)", False, -1)
    # Set to a hall-like preset (parameter indices are often heuristic without direct API for presets)
    RPR.RPR_TrackFX_SetParam(synth_track, 1, 0, 0.25) # Wet gain
    RPR.RPR_TrackFX_SetParam(synth_track, 1, 1, 0.75) # Dry gain
    RPR.RPR_TrackFX_SetParam(synth_track, 1, 2, 0.8)  # Room size

    # ReaDelay (Chorus-like effect)
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaDelay (Cockos)", False, -1)
    # For chorus, use short, modulated delays
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 0, 0.15) # Wet mix
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 1, 0.85) # Dry mix
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 2, 0.03) # Delay 1 Time (short)
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 5, 0.025) # Delay 2 Time (slightly different)
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 8, 0.3)  # Feedback 1
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 11, 0.3) # Feedback 2
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 14, 0.02) # LFO rate (for modulation)
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 15, 0.1)  # LFO depth

    # === Step 4: Add Automation for Synth ===
    # Volume Automation (layered items)
    volume_env = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_WND", 1) # Ensure envelope lane is visible

    # Automation Item 1: Swell Up
    RPR.RPR_AddEnvelopePoint(volume_env, 0.0, RPR.DB2VAL(-4.6), 0, 0, False, True)
    RPR.RPR_AddEnvelopePoint(volume_env, total_length_sec, RPR.DB2VAL(0.0), 0, 0, False, True)
    
    # Automation Item 2: Choppy/Gate Effect (created as a separate item, but on the same envelope lane)
    # This simulates a square wave gating.
    # The actual graphical envelope will show the combined effect.
    chop_start_time = total_length_sec / 4 # Start chopping after 1/4 of the transition
    chop_end_time = total_length_sec
    chop_interval_sec = seconds_per_beat / 8 # 32nd notes
    
    # Define points for the choppy effect
    for t in range(int(chop_start_time / chop_interval_sec), int(chop_end_time / chop_interval_sec)):
        current_time = t * chop_interval_sec
        # Peak
        RPR.RPR_AddEnvelopePoint(volume_env, current_time, RPR.DB2VAL(1.0), 1, 0, False, True)
        # Trough
        RPR.RPR_AddEnvelopePoint(volume_env, current_time + chop_interval_sec / 2, RPR.DB2VAL(-4.0), 1, 0, False, True)

    # Width Automation (Mono to Stereo)
    width_env = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Stereo width")
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_WND", 1) # Ensure envelope lane is visible
    RPR.RPR_AddEnvelopePoint(width_env, 0.0, 0.0, 0, 0, False, True) # 0% width (mono) at start
    RPR.RPR_AddEnvelopePoint(width_env, total_length_sec, 1.0, 0, 0, False, True) # 100% width (stereo) at end


    # --- Lo-Fi Crackle Track ---
    crackle_track_name = "Lo-Fi Crackle"
    crackle_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(crackle_track_idx, True)
    crackle_track = RPR.RPR_GetTrack(0, crackle_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(crackle_track, "P_NAME", crackle_track_name, True)

    # === Create Placeholder Audio Item for Crackle ===
    # Note: The actual crackle sound file is NOT included. User must drop their own.
    crackle_item = RPR.RPR_AddMediaItemToTrack(crackle_track)
    RPR.RPR_SetMediaItemInfo_Value(crackle_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(crackle_item, "D_LENGTH", total_length_sec)
    # Optional: Fill with silence or a basic noise generator if available and scriptable
    # For simplicity, leaving it as an empty item where user can later drop their sample.

    # === Add FX Chain for Crackle ===
    # 1. JS: General Dynamics (Control) - For transient flattening/limiting
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: General Dynamics (Control) (Cockos)", False, -1)
    # Parameters for JS: General Dynamics
    # Parameter indices are often generic for JSFX or vary. This is an approximation.
    # The graph shown in the video is complex to reproduce exactly via ReaScript's
    # general parameter setting functions. We'll set attack/release and wet mix.
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 0, 0.0)   # Detect input gain (0 dB)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 1, 0.0)   # Detect RMS size (0 ms for fastest)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 2, 0.0)   # Input Attack (0 ms)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 3, 20.0)  # Input Release (20 ms)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 4, 0.0)   # Input Precomp (0 ms)
    # The actual curve is params 5 to 70 for 65 points. We cannot easily draw the curve directly.
    # Set wet mix to approximate impact on peaks.
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 71, 0.5)  # Dry mix (approximate)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 72, 0.05) # Wet mix (approximate 5%)

    # 2. JS: Volume/Pan/Stereo - For stereo balance, mid-side trim, mono-maker
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: Utility/volume/pan/stereo (Cockos)", False, -1)
    # To approximate VUMT: Trim right by ~4.4dB (assuming source imbalance)
    RPR.RPR_TrackFX_SetParam(crackle_track, 1, 1, RPR.DB2VAL(-4.4)) # Right Gain
    # Mono-making below ~955 Hz & side trim: use stereo width control as an approximation
    # 0 = mono, 1 = stereo. Value < 1 will narrow stereo.
    RPR.RPR_TrackFX_SetParam(crackle_track, 1, 3, 0.70) # Stereo width to ~70%
    # This JSFX doesn't have a frequency-dependent mono maker. This is a limitation.

    # 3. ReaEQ - High/Low-pass filtering
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaEQ (Cockos)", False, -1)
    # Band 1: Highpass
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 0, 3.0)   # Band 1 enabled
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 1, 0.0)   # Band 1 gain (0 dB)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 2, 150.0) # Band 1 freq (150 Hz)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 3, 6.0)   # Band 1 Q (slope)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 5, 0.0)   # Band 1 type (High Pass)

    # Band 2: Lowpass
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 6, 3.0)   # Band 2 enabled
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 7, 0.0)   # Band 2 gain (0 dB)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 8, 7000.0) # Band 2 freq (7 kHz)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 9, 6.0)   # Band 2 Q (slope)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 11, 1.0)  # Band 2 type (Low Pass)

    # 4. ReaVerb (subtle room ambiance)
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaVerb (Cockos)", False, -1)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 0, 0.24) # Wet gain (~24%)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 1, 0.76) # Dry gain (~76%)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 2, 0.5) # Room size (medium)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 3, 0.6) # Damping

    RPR.RPR_UpdateArrange()

    return f"Created '{synth_track_name}' and '{crackle_track_name}' with evolving effects over {bars} bars at {bpm} BPM."

