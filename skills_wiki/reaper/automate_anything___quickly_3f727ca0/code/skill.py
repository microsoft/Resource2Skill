import reaper_python as RPR

def create_automation_pattern(
    project_name: str = "AutomateAnything",
    track_name: str = "Automated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major", # Not directly used for MIDI notes in this specific demo, but kept for parametric consistency.
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Creates a track and demonstrates volume, pan, mute, and FX parameter automation
    as shown in the "Automate Anything - Quickly" tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this specific skill).

    Returns:
        Status string, e.g., "Created 'Automated Synth' track with various automation."
    """
    RPR.Undo_BeginBlock2(0) # Begin an undo block

    # --- Music theory lookup tables (for background MIDI) ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    CHORDS = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        # Add more chord definitions if needed
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth for sound ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create a simple MIDI Item with a sustained chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_GetActiveTake(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_SetItemExt(0, 0, item, "", False))
    midi_take = RPR.RPR_GetMediaItemTake_Source(take)

    RPR.RPR_MIDI_SetItemExt_SetInitialized(midi_take, True)

    # Insert a sustained C major chord (C3, E3, G3) for the entire item length
    root_midi_note = NOTE_MAP.get(key, 0) + (3 * 12) # Octave 3 as base
    chord_intervals = CHORDS.get("major")
    
    for i, interval in enumerate(chord_intervals):
        midi_note_num = root_midi_note + interval
        note_start = 0.0
        note_end = item_length
        velocity = velocity_base - (i * 5) # Slight velocity variation
        RPR.RPR_MIDI_InsertNote(midi_take, False, False, note_start, note_end, velocity, False, midi_note_num, False)
    
    RPR.MIDI_Sort(midi_take)

    # === Step 5: Automate Volume ===
    volume_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not volume_envelope: # Should exist by default, but create if not.
        volume_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(volume_envelope, "<ENVFLAGS 0/>\nVOL", True) # Ensure it's a volume envelope
        RPR.RPR_GetSetTrackState(track, "<TRACK><ENV NAME=\"Volume\" />", True) # Ensure it's linked/visible
    
    # Set the track automation mode to 'Read' for immediate playback
    RPR.RPR_SetTrackUIAutomationMode(track, 1) # 1 = Read (play faders with armed envelopes)
    RPR.RPR_SetTrackUIDisarm(track, False) # Ensure fader is not disarmed from writing (allows read mode)

    # Draw a volume curve: start -5dB, go to -15dB, then back to -5dB
    RPR.RPR_InsertEnvelopePoint(volume_envelope, 0.0, RPR.DBToNative(-5.0), 1, 1, False, True)
    RPR.RPR_InsertEnvelopePoint(volume_envelope, item_length / 2, RPR.DBToNative(-15.0), 1, 1, False, True)
    RPR.RPR_InsertEnvelopePoint(volume_envelope, item_length, RPR.DBToNative(-5.0), 1, 1, False, True)
    RPR.RPR_Envelope_SortPoints(volume_envelope)

    # === Step 6: Automate Pan ===
    pan_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if not pan_envelope:
        pan_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(pan_envelope, "<ENVFLAGS 0/>\nPAN", True)
        RPR.RPR_GetSetTrackState(track, "<TRACK><ENV NAME=\"Pan\" />", True)

    # Draw a pan curve: full left -> center -> full right -> center
    RPR.RPR_InsertEnvelopePoint(pan_envelope, 0.0, 0.0, 1, 1, False, True) # Full left
    RPR.RPR_InsertEnvelopePoint(pan_envelope, item_length / 4, 0.5, 1, 1, False, True) # Center
    RPR.RPR_InsertEnvelopePoint(pan_envelope, item_length / 2, 1.0, 1, 1, False, True) # Full right
    RPR.RPR_InsertEnvelopePoint(pan_envelope, item_length * 3 / 4, 0.5, 1, 1, False, True) # Center
    RPR.RPR_InsertEnvelopePoint(pan_envelope, item_length, 0.5, 1, 1, False, True) # Center at end
    RPR.RPR_Envelope_SortPoints(pan_envelope)

    # === Step 7: Automate Mute ===
    mute_envelope = RPR.RPR_GetTrackEnvelopeByName(track, "Mute")
    if not mute_envelope:
        mute_envelope = RPR.RPR_CreateTrackEnvelope(track)
        RPR.RPR_SetEnvelopeStateChunk(mute_envelope, "<ENVFLAGS 0/>\nMUTE", True)
        RPR.RPR_GetSetTrackState(track, "<TRACK><ENV NAME=\"Mute\" />", True)

    # Mute/unmute sections: muted for bar 1, unmuted for bar 2, etc.
    # Mute automation points are typically 0.0 (unmute) and 1.0 (mute).
    RPR.RPR_InsertEnvelopePoint(mute_envelope, 0.0, 1.0, 1, 1, False, True) # Mute at start
    RPR.RPR_InsertEnvelopePoint(mute_envelope, bar_length_sec * 0.999, 1.0, 1, 1, False, True) # Stay mute close to bar 1
    RPR.RPR_InsertEnvelopePoint(mute_envelope, bar_length_sec * 1.0, 0.0, 1, 1, False, True) # Unmute at bar 1
    RPR.RPR_InsertEnvelopePoint(mute_envelope, bar_length_sec * 1.999, 0.0, 1, 1, False, True) # Stay unmute close to bar 2
    RPR.RPR_InsertEnvelopePoint(mute_envelope, bar_length_sec * 2.0, 1.0, 1, 1, False, True) # Mute at bar 2
    RPR.RPR_InsertEnvelopePoint(mute_envelope, bar_length_sec * 2.999, 1.0, 1, 1, False, True) # Stay mute close to bar 3
    RPR.RPR_InsertEnvelopePoint(mute_envelope, bar_length_sec * 3.0, 0.0, 1, 1, False, True) # Unmute at bar 3
    RPR.RPR_InsertEnvelopePoint(mute_envelope, item_length, 0.0, 1, 1, False, True) # Unmute at end
    RPR.RPR_Envelope_SortPoints(mute_envelope)

    # === Step 8: Automate ReaEQ Low Pass Filter Frequency ===
    eq_fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    if eq_fx_idx == -1:
        RPR.RPR_ShowConsoleMsg("Could not add ReaEQ FX.\n")
        RPR.Undo_EndBlock2(0, "Automate Anything - Failed to add ReaEQ", -1)
        return "Failed to create automation for ReaEQ (plugin not found?)"

    # Enable Band 1 and set it to Low Pass filter type
    # Band 1 is at FX index 0 for the first band in ReaEQ.
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 0, 1.0) # Enable Band 1 (param_idx 0)
    RPR.RPR_TrackFX_SetParam(track, eq_fx_idx, 11, 4.0/6.0) # Set Band 1 Type to Low Pass (param_idx 11, value 4.0/6.0)

    # Get the envelope for Band 1 Frequency (Parameter index 10)
    param_idx_lowpass_freq = 10
    fx_param_envelope = RPR.RPR_TrackFX_GetEnvelope(track, eq_fx_idx, param_idx_lowpass_freq, True)
    
    if not fx_param_envelope:
        RPR.RPR_ShowConsoleMsg("Could not create ReaEQ FX parameter envelope.\n")
        RPR.Undo_EndBlock2(0, "Automate Anything - Failed to create FX param envelope", -1)
        return "Failed to create automation for ReaEQ (envelope creation failed?)"

    # Draw a filter sweep: start high, sweep down, sweep up
    # Normalized values 0.0 to 1.0, mapping to 20Hz - 20000Hz (log scale in ReaEQ).
    RPR.RPR_InsertEnvelopePoint(fx_param_envelope, 0.0, 1.0, 1, 1, False, True) # Start at 20kHz
    RPR.RPR_InsertEnvelopePoint(fx_param_envelope, item_length / 2, 0.05, 1, 1, False, True) # Sweep down to around 100-200Hz
    RPR.RPR_InsertEnvelopePoint(fx_param_envelope, item_length, 1.0, 1, 1, False, True) # Sweep back up to 20kHz
    RPR.RPR_Envelope_SortPoints(fx_param_envelope)

    # === Step 9: Refresh UI ===
    RPR.RPR_TrackList_AdjustWindows(True)
    RPR.RPR_UpdateArrange()

    RPR.Undo_EndBlock2(0, f"Created '{track_name}' with automation", -1)
    return f"Created '{track_name}' track with Volume, Pan, Mute, and ReaEQ filter automation over {bars} bars at {bpm} BPM."

