import reaper_python as RPR
import math

# Music theory lookup tables (already provided in the template)
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

def get_midi_note(key, scale, degree, octave=4):
    """Calculates MIDI note number for a given key, scale, degree, and octave."""
    if key not in NOTE_MAP:
        raise ValueError(f"Invalid key: {key}. Must be one of {list(NOTE_MAP.keys())}")
    if scale not in SCALES:
        raise ValueError(f"Invalid scale: {scale}. Must be one of {list(SCALES.keys())}")
    if not (1 <= degree <= len(SCALES[scale])): # Basic check for degree
        # Adjust degree to wrap around the scale for higher/lower notes if needed
        pass # The logic below handles this

    root_midi = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    
    num_scale_notes = len(scale_intervals)
    octave_offset = (degree - 1) // num_scale_notes
    scale_degree_index = (degree - 1) % num_scale_notes
    
    interval = scale_intervals[scale_degree_index]
    
    midi_note = root_midi + interval + (octave + octave_offset) * 12
    return midi_note

def db_to_reaper_vol(db_val):
    """Converts a dB value to REAPER's linear volume scale (0.0 to 1.0)."""
    if db_val <= -144: # REAPER's minimum dB value (effectively mute)
        return 0.0
    return math.pow(10, db_val / 20.0)

def create_synth_transition_and_crackle_fx(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    synth_velocity: int = 100,
    crackle_volume_db: float = -18.0, # dB
    **kwargs,
) -> str:
    """
    Creates a synth track with a transitional flanging/chopping/width effect
    and a background vinyl crackle track with lo-fi processing.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        synth_velocity: MIDI velocity for the synth note (0-127).
        crackle_volume_db: Base volume for the crackle track in dB.
        **kwargs: Additional overrides (not used directly in this function but for future compatibility).

    Returns:
        Status string, e.g., "Created synth transition and crackle FX over 8 bars."
    """
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_item_length = bar_length_sec * bars
    
    # Automation envelopes often extend slightly beyond the item length to catch reverb tails.
    automation_end_time = total_item_length + bar_length_sec 

    # --- SYNTH TRANSITION TRACK ---
    synth_track_name = "Synth Transition"
    synth_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(synth_track_idx, True)
    synth_track = RPR.RPR_GetTrack(0, synth_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", synth_track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "D_VOL", db_to_reaper_vol(-5.0)) # Trim Volume -5dB

    # Add ReaSynth
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth (Cockos)", False, -1)
    
    # MIDI Item and Note (sustained for the whole duration)
    midi_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_LENGTH", total_item_length)
    midi_take = RPR.RPR_GetActiveTake(midi_item)
    
    synth_note_midi = get_midi_note(key, scale, 1, 3) # First degree of the scale, octave 3
    RPR.MIDI_SetItemExtents(midi_item, 0.0, total_item_length) 
    RPR.MIDI_InsertNote(midi_take, False, False, 0.0, total_item_length, False, synth_note_midi, synth_velocity, 0)
    RPR.MIDI_Sort(midi_take)
    RPR.MIDI_UpdateItemInProject(midi_item)

    # ReaSynth Filter Cutoff Automation (to simulate LFO on shape / flanging)
    # Automate ReaSynth's filter cutoff (param 16) with an LFO-like curve
    rs_fx_idx = RPR.RPR_TrackFX_GetFXByName(synth_track, "ReaSynth", False)
    cutoff_param_idx = 16 # Filter Cutoff
    
    RPR.RPR_TrackFX_SetParam(synth_track, rs_fx_idx, cutoff_param_idx, 0.5) # Set initial value
    RPR.RPR_TrackFX_SetEnvelopeParam(synth_track, rs_fx_idx, cutoff_param_idx, True, True, True)
    cutoff_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "ReaSynth(1) VSTi: Filter Cutoff")
    RPR.RPR_DeleteEnvelopePointRange(cutoff_envelope, 0.0, automation_end_time)

    # Simulate slow LFO on filter cutoff from ~40% to ~70%
    num_points = bars * 8 # 8 points per bar for a smooth LFO
    for i in range(num_points + 1):
        time = i * (automation_end_time / num_points)
        value = 0.55 + 0.15 * math.sin(i * 2 * math.pi / (num_points / (bars / 2))) # 2 cycles over 4 bars
        RPR.RPR_InsertEnvelopePoint(cutoff_envelope, time, value, 0, 0.5, False, False)
    
    # Track Volume Automation (Swell Up + Chopping)
    vol_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")
    if not vol_envelope:
        RPR.RPR_SetMediaTrackInfo_Value(synth_track, "C_SHOWSVOLPAN", 1) 
        vol_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")

    RPR.RPR_DeleteEnvelopePointRange(vol_envelope, 0.0, automation_end_time)
    
    initial_swell_db = -4.6
    final_swell_db = 0.0
    chop_high_offset_db = 1.0 # chop peak relative to swell
    chop_low_offset_db = -4.0 # chop trough relative to swell
    
    start_chop_bar = 1 # Chop starts from the second bar in the video
    chop_start_time = bar_length_sec * start_chop_bar
    
    # Points for the swell
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 0.0, db_to_reaper_vol(initial_swell_db), 0, 0.5, False, False)
    RPR.RPR_InsertEnvelopePoint(vol_envelope, chop_start_time, db_to_reaper_vol(initial_swell_db + (chop_high_offset_db + chop_low_offset_db)/2), 0, 0.5, False, False)

    # Combined swell and chop automation
    num_chop_intervals = int((automation_end_time - chop_start_time) / (bar_length_sec / 8)) # 32nd note intervals
    for i in range(num_chop_intervals + 1):
        time = chop_start_time + i * (bar_length_sec / 8)
        time = min(time, automation_end_time) # Ensure time does not exceed max
        
        # Calculate base swell volume at this time
        swell_range = final_swell_db - initial_swell_db
        swell_progress = (time / automation_end_time) # Normalized progress over total duration
        current_base_swell_db = initial_swell_db + (swell_range * swell_progress)
        
        # Apply chop offset
        chop_offset_db = chop_high_offset_db if (i % 2 == 0) else chop_low_offset_db
        final_vol_db = current_base_swell_db + chop_offset_db
        
        RPR.RPR_InsertEnvelopePoint(vol_envelope, time, db_to_reaper_vol(final_vol_db), 0, 0.5, False, False)


    # Track Width Automation (Mono to Stereo)
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_PANMODE", 1) # Set track to Stereo Pan mode
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "C_SHOWSWIDTH", 1) # Show width envelope
    width_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Width")
    
    RPR.RPR_DeleteEnvelopePointRange(width_envelope, 0.0, automation_end_time)
    RPR.RPR_InsertEnvelopePoint(width_envelope, 0.0, 0.0, 0, 0.5, False, False) # Mono (0.0)
    RPR.RPR_InsertEnvelopePoint(width_envelope, automation_end_time, 1.0, 0, 0.5, False, False) # Stereo (1.0)


    # --- CRACKLE FX TRACK ---
    crackle_track_name = "Vinyl Crackle FX"
    crackle_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(crackle_track_idx, True)
    crackle_track = RPR.RPR_GetTrack(0, crackle_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(crackle_track, "P_NAME", crackle_track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(crackle_track, "D_VOL", db_to_reaper_vol(crackle_volume_db))

    # Add JS: Pink Noise as source (no item needed, JSFX generates continuously)
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: Pink Noise (Cockos)", False, -1)
    
    # Add JS: General Dynamics (to compress transients)
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: General Dynamics (Cockos)", False, -1)
    gd_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "JS: General Dynamics", False)
    
    # Set General Dynamics parameters based on video (approximation)
    # Detect input gain (dB): 0.0 (param 0)
    # Input response (ms): 0.0 (fast attack) (param 3)
    # Ratio: ~0.9 (high compression/limiting) (param 4)
    # Threshold: ~-20dB (param 5 maps 0-1 to -60-0dB, so 40/60 = 0.66)
    # Wet mix (dB): 5.0 (output boost) (param 8)
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 0, 0.0)    # Detect input gain 0dB
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 3, 0.0)    # Input response 0ms (fast attack)
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 4, 0.9)    # Ratio approx 0.9 (high compression)
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 5, 0.66)   # Threshold approx -20dB
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 8, db_to_reaper_vol(5.0)) # Wet mix +5dB (ReaScript expects linear for this param)

    # Add JS: Stereo Field Manipulator (for mid-side balance and mono maker)
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: Stereo Field Manipulator (Cockos)", False, -1)
    sfm_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "JS: Stereo Field Manipulator", False)
    
    # Trim Left (-6.0dB) and Right (+4.4dB) for balance (param 0 & 1)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 0, db_to_reaper_vol(-6.0)) # Input L trim (linear value)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 1, db_to_reaper_vol(4.4))  # Input R trim (linear value)

    # Trim Side Signal (-6dB, using Mid-Side mode) (param 3)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 3, db_to_reaper_vol(-6.0)) # Gain (Side) (linear value)
    
    # Mono Maker at 955 Hz, amount 70% (param 2 for mix, param 6 for freq)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 2, 0.70) # Mono mix 70% (0.0 to 1.0)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 6, 955.0/1000.0) # Mono frequency 955Hz (scaled 0-1 for 0-10000Hz)

    # Add ReaEQ (high-pass and low-pass filtering)
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaEQ (Cockos)", False, -1)
    req_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "ReaEQ", False)

    # Band 1: High Pass (LPF in ReaEQ terms, but for filtering lows)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 0, 1.0) # Band 1 On
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 1, 0.0) # Band 1 Type: High Pass (LPF)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 2, 200.0) # Band 1 Freq: 200Hz
    
    # Band 2: Low Pass (HPF in ReaEQ terms, but for filtering highs)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 5, 1.0) # Band 2 On
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 6, 1.0) # Band 2 Type: Low Pass (HPF)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 7, 10000.0) # Band 2 Freq: 10kHz
    
    # Band 3: Mid-dip at 1kHz (subtle)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 10, 1.0) # Band 3 On
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 11, 2.0) # Band 3 Type: Band (Shelf)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 12, 1000.0) # Band 3 Freq: 1kHz
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 13, db_to_reaper_vol(-1.0)) # Band 3 Gain: -1dB (linear value)


    # Add ReaVerb (for subtle room sound)
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaVerb (Cockos)", False, -1)
    rv_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "ReaVerb", False)
    
    # Set ReaVerb parameters for a subtle room (approximation of "New Home Empty Room")
    # Parameter 10 is Dry/Wet mix (0.0 to 1.0)
    RPR.RPR_TrackFX_SetParam(crackle_track, rv_fx_idx, 10, 0.24) # Dry/Wet (Wet) 24%

    RPR.RPR_UpdateArrange()
    
    return f"Created '{synth_track_name}' and '{crackle_track_name}' over {bars} bars at {bpm} BPM."

