import reaper_python as RPR

def create_massive_x_reason_rack_chain(
    project_name: str = "MyProject",
    track_name: str = "Complex VST Chain",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor", # Not directly used for this pattern, but kept for consistency
    bars: int = 4,
    velocity_base: int = 100,
    trigger_note: int = 60, # MIDI note C3
    **kwargs,
) -> str:
    """
    Create a REAPER track with a complex VST chain including Massive X, Reason Rack Plugin,
    BLASS Synthesizer, BLASS Dreamer, BLASS Clap, and BLASS Reverb, along with a
    simple MIDI trigger.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Not directly used for this pattern.
        scale: Scale type (major, minor, dorian, etc.). Not directly used for this pattern.
        bars: Number of bars to generate the MIDI trigger.
        velocity_base: Base MIDI velocity (0-127).
        trigger_note: MIDI note number for the repeating trigger (e.g., 60 for C3).
        **kwargs: Additional overrides (not used in this specific skill).

    Returns:
        Status string, e.g., "Created 'Complex VST Chain' with VSTs and MIDI trigger over 4 bars"
    """
    # Music theory lookup tables (not extensively used for this skill but kept for standard)
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add VST FX Chain ===
    # IMPORTANT: These VSTs are third-party and must be installed on the system
    # for the skill to produce the intended sound. If not installed, REAPER
    # may display a prompt or load a blank plugin.

    vst_plugins = [
        "Massive X (Native Instruments)",
        "Reason Rack Plugin (Propellerhead Software AB)",
        "BLASS Synthesizer (CHONE)",
        "BLASS Dreamer (CHONE)",
        "BLASS Clap (CHONE)",
        "BLASS Reverb (CHONE)",
    ]

    for plugin_name in vst_plugins:
        # Add VSTi: prefix for instruments, otherwise VST:
        is_instrument = "VSTi" in plugin_name # Simple heuristic
        RPR.RPR_TrackFX_AddByName(track, plugin_name, is_instrument, -1)
        # Note: Internal VST parameters (like "Retro Pluck" preset for Massive X,
        # or Donbeat player configuration within Reason Rack) are not set here
        # and would require manual configuration within the VST's UI.

    # === Step 4: Create MIDI Item with Trigger Notes ===
    # This MIDI item will provide a continuous trigger for the generative VSTs (e.g., Donbeat).
    beats_per_bar = 4
    item_length_beats = beats_per_bar * bars
    item_length_sec = (60.0 / bpm) * item_length_beats

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", "MIDI Trigger", True)

    midi_take = RPR.RPR_MIDI_SetItemExtents(take, 0) # Create MIDI take

    # Insert repeating quarter notes for triggering
    for beat in range(item_length_beats):
        position = beat * (60.0 / bpm) # Start of the beat
        note_length = (60.0 / bpm) - 0.01 # Slightly shorter than a beat
        
        # RPR_MIDI_InsertNote(MIDI_take, selected, muted, start_time_beats, end_time_beats, chan, note, velocity, no_cc_reset)
        # Using RPR_MIDI_InsertNote(MIDI_take, selected, muted, start_time, end_time, channel, pitch, velocity, no_cc_reset)
        # start_time and end_time are in MIDI quarter notes. Need to convert seconds to quarter notes.
        
        # Calculate start and end time in REAPER's internal MIDI quarter note format
        # Each beat is 1.0 quarter note in MIDI time
        midi_qtr_start = float(beat)
        midi_qtr_end = float(beat + 1) - 0.01 # Slightly shorter

        RPR.RPR_MIDI_InsertNote(midi_take, False, False, midi_qtr_start, midi_qtr_end, 0, trigger_note, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_Commit(midi_take)

    # Refresh REAPER
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with VSTs: {', '.join(vst_plugins)} and MIDI trigger over {bars} bars at {bpm} BPM."

