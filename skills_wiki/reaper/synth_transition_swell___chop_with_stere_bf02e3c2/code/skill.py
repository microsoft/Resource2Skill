import reaper_python as RPR

def create_synth_transition_swell_chop(
    project_name: str = "SynthTransitionProject",
    track_name: str = "Synth Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    synth_waveform: str = "saw", # "saw", "sine", "square", "triangle"
    chop_start_bar: int = 2,
    trim_volume_db: float = -13.6,
    **kwargs,
) -> str:
    """
    Create an evolving synth pad with layered volume automation (swell and choppy),
    stereo width expansion, and effects, ideal for transitions.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, etc.).
        bars: Number of bars to generate the transition over.
        velocity_base: Base MIDI velocity (0-127).
        synth_waveform: Waveform for ReaSynth (e.g., "saw", "sine").
        chop_start_bar: The bar number where the choppy volume automation begins.
        trim_volume_db: Overall trim volume for the track in dB.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Synth Transition' with 3 notes over 4 bars at 120 BPM"
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
    
    # Ensure chop_start_bar is within valid range
    chop_start_bar = max(1, min(chop_start_bar, bars))

    # === Step 1: Set Tempo ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This command might interfere with other scripts, better to leave it to the calling agent

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    # Calculate root note and chord notes
    root_midi_note = NOTE_MAP.get(key.capitalize(), 0) + 48 # C3 as base
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # Create a basic minor triad in root position
    midi_notes_to_add = [
        root_midi_note,
        root_midi_note + scale_intervals[2], # Minor third
        root_midi_note + scale_intervals[4]  # Perfect fifth
    ]

    beats_per_bar = 4
    item_length_beats = beats_per_bar * bars
    
    # Add MIDI item to track
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats))
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_AllocMidiTake(take))
    midi_take = RPR.RPR_GetMediaItemTake_Source(take)

    RPR.RPR_MIDI_SetItemExtents(midi_take, 0.0, item_length_beats)

    # Insert MIDI notes for the sustained chord
    RPR.RPR_MIDI_DisableGridSnapIn(midi_take)
    for note_num in midi_notes_to_add:
        RPR.RPR_MIDI_InsertNote(midi_take, 0, 0, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats), note_num, velocity_base, True, True)
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_MarkAllNotes(midi_take, True)
    RPR.RPR_MIDI_SetAllNotesVelocities(midi_take, velocity_base, True)
    RPR.RPR_MIDI_UpdateBlock(midi_take)
    RPR.RPR_MIDI_SetItemExtents(midi_take, 0.0, item_length_beats)
    RPR.RPR_UpdateArrange()

    # === Step 4: Add FX Chain ===
    # ReaSynth (as Hybrid 3 alternative)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    synth_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    # Set waveform (ReaSynth param 1 is Osc 1 waveform, 0=sine, 1=saw, 2=square, 3=tri)
    waveform_map = {"sine": 0.0, "saw": 0.333, "square": 0.666, "triangle": 1.0}
    RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 1, waveform_map.get(synth_waveform.lower(), 0.333)) # Osc 1 waveform
    # Basic Amp Env for pad
    RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 2, 0.05) # Attack (s)
    RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 3, 0.5)  # Decay (s)
    RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 4, 0.7)  # Sustain (level)
    RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 5, 1.0)  # Release (s)

    # ReaVerb (as Hall Reverb alternative)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerb", False, -1)
    reverb_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    RPR.RPR_TrackFX_SetParam(track, reverb_fx_idx, 10, 0.30) # Wet Mix roughly 30%

    # JS: LOSER/stereo_chorus (as Chorus alternative)
    RPR.RPR_TrackFX_AddByName(track, "JS: LOSER/stereo_chorus", False, -1)
    chorus_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
    RPR.RPR_TrackFX_SetParam(track, chorus_fx_idx, 0, 0.5) # Rate
    RPR.RPR_TrackFX_SetParam(track, chorus_fx_idx, 1, 0.5) # Depth
    RPR.RPR_TrackFX_SetParam(track, chorus_fx_idx, 2, 0.5) # Mix


    # === Step 5: Create Volume Automation (Layered) ===
    # Envelope 1: Smooth Volume Swell
    vol_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not vol_envelope:
        vol_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetObjectState(vol_envelope, "Volume Envelope", True)

    RPR.RPR_DeleteEnvelopePointRange(vol_envelope, 0.0, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats))
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 0.0, RPR.RPR_DBToNormalized(0.0), 0, 0.0, False, True) # Start at 0dB (for now)
    RPR.RPR_InsertEnvelopePoint(vol_envelope, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats), RPR.RPR_DBToNormalized(0.0), 0, 0.0, False, True)
    
    # Create an automation item for the initial swell
    swell_item_start_time = 0.0
    swell_item_end_time = RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats)
    swell_auto_item = RPR.RPR_AddTakeEnvelopeFX(take, "Volume", swell_item_start_time, swell_item_end_time)
    
    # Get the envelope inside the automation item
    env_in_auto_item = RPR.RPR_GetTakeEnvelope(swell_auto_item, 0)
    RPR.RPR_DeleteEnvelopePointRange(env_in_auto_item, 0.0, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats))
    
    # Start at -4.6dB (normalized)
    RPR.RPR_InsertEnvelopePoint(env_in_auto_item, swell_item_start_time, RPR.RPR_DBToNormalized(-4.6), 1, 0.0, False, True) # Linear curve for swell
    # End at 0dB (normalized)
    RPR.RPR_InsertEnvelopePoint(env_in_auto_item, swell_item_end_time, RPR.RPR_DBToNormalized(0.0), 1, 0.0, False, True)
    RPR.RPR_SetMediaItemInfo_Value(swell_auto_item, "D_VOL", 1.0) # Set item volume to 0db to properly layer


    # Envelope 2: Chopping Effect Automation Item (stacked on top)
    chop_start_time = RPR.RPR_TimeMap_QNToTime(0.0, beats_per_bar * chop_start_bar)
    chop_end_time = RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats)
    chop_auto_item = RPR.RPR_AddTakeEnvelopeFX(take, "Volume", chop_start_time, chop_end_time)
    
    env_in_chop_item = RPR.RPR_GetTakeEnvelope(chop_auto_item, 0)
    RPR.RPR_DeleteEnvelopePointRange(env_in_chop_item, 0.0, chop_end_time - chop_start_time)
    
    # Create 32nd note chopping pattern
    time_quant = 1.0 / 8.0 # 32nd note in quarter notes (0.125 beats)
    num_chop_points = int(((chop_end_time - chop_start_time) / (60.0 / bpm)) * (beats_per_bar / time_quant)) * 2
    
    for i in range(num_chop_points):
        point_time = (i * time_quant) / beats_per_bar * (chop_end_time - chop_start_time) # Relative time within auto item
        if i % 2 == 0: # Up point (+1 dB)
            RPR.RPR_InsertEnvelopePoint(env_in_chop_item, point_time, RPR.RPR_DBToNormalized(1.0), 0, 0.0, False, True)
        else: # Down point (-4 dB)
            RPR.RPR_InsertEnvelopePoint(env_in_chop_item, point_time, RPR.RPR_DBToNormalized(-4.0), 0, 0.0, False, True)
    RPR.RPR_SetMediaItemInfo_Value(chop_auto_item, "D_VOL", 1.0) # Set item volume to 0db to properly layer


    # === Step 6: Create Width Automation ===
    width_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Width")
    if not width_envelope:
        width_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetObjectState(width_envelope, "Width Envelope", True)

    RPR.RPR_DeleteEnvelopePointRange(width_envelope, 0.0, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats))
    RPR.RPR_InsertEnvelopePoint(width_envelope, 0.0, 0.0, 1, 0.0, False, True) # Start at 0% (mono)
    RPR.RPR_InsertEnvelopePoint(width_envelope, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats), 1.0, 1, 0.0, False, True) # End at 100% (stereo)


    # === Step 7: Apply Trim Volume ===
    trim_volume_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Trim Volume")
    if not trim_volume_envelope:
        trim_volume_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_GetSetObjectState(trim_volume_envelope, "Trim Volume Envelope", True)
    
    # Set the trim volume as a static value over the entire duration
    RPR.RPR_DeleteEnvelopePointRange(trim_volume_envelope, 0.0, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats))
    norm_trim_vol = RPR.RPR_DBToNormalized(trim_volume_db)
    RPR.RPR_InsertEnvelopePoint(trim_volume_envelope, 0.0, norm_trim_vol, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(trim_volume_envelope, RPR.RPR_TimeMap_QNToTime(0.0, item_length_beats), norm_trim_vol, 0, 0.0, False, True)


    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {len(midi_notes_to_add)} notes over {bars} bars at {bpm} BPM with swell, chop, and width automation."

