import reaper_python as RPR

def get_midi_note_number(note_name: str, octave: int) -> int:
    """Converts a note name (C, C#, etc.) and octave to a MIDI note number."""
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    base_midi = NOTE_MAP.get(note_name)
    if base_midi is None:
        raise ValueError(f"Invalid note name: {note_name}")
    return base_midi + (octave + 1) * 12

def create_midi_editor_workflow_demo(
    project_name: str = "MyProject",
    track_name: str = "Piano Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Demonstrates essential MIDI editor workflow techniques in REAPER.
    Creates a new track, adds ReaSynth, inserts a C major chord pattern over 4 bars,
    with varied velocities, and adds a Pitch Bend automation lane.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). (Used for relative note calculations)
        scale: Scale type (major, minor, dorian, etc.). (Not dynamically used for chord structure in this demo)
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for the notes.
        **kwargs: Additional overrides (not used in this specific implementation).

    Returns:
        Status string, e.g., "Created 'Piano Demo' track with MIDI notes and automation."
    """
    # Music theory lookup tables (for potential future dynamic chord generation)
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        # ... other scales
    }

    # === Step 1: Set Tempo (Commented out to be additive; assumes project BPM is set) ===
    # RPR.SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.CountTracks(0)
    RPR.InsertTrackAtIndex(track_idx, True)
    track = RPR.GetTrack(0, track_idx)
    RPR.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth VSTi to the track ===
    # Using ReaSynth as a stock REAPER instrument.
    RPR.TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    time_per_beat = 60.0 / bpm
    bar_length_sec = time_per_beat * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.AddMediaItemToTrack(track)
    RPR.SetMediaItemInfo_Value(item, "D_POSITION", RPR.GetCursorPosition()) # Start at current cursor position
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.GetActiveTake(item)
    
    # Create MIDI source for the take (essential for MIDI_InsertNote)
    RPR.MIDI_SetItemExtents(item, RPR.GetMediaItemInfo_Value(item, "D_POSITION"), item_length)
    midi_take = RPR.MIDI_TakeToPtr(take)
    if not midi_take:
        return f"Failed to create MIDI source for '{track_name}'. No MIDI item created."

    # === Step 5: Insert C Major Chord Pattern and adjust velocities ===
    # Based on the visual in the tutorial, the chords are C major (C4, E4, G4).
    # 'key' parameter is used for the root of the chord for future extensibility.
    root_midi = get_midi_note_number(key, 4) # C4 as root
    chord_notes = [root_midi,  # C4
                   root_midi + 4, # E4
                   root_midi + 7] # G4

    note_duration_beats = 0.75 # Three 16th notes duration
    
    # Insert notes for all bars, simulating drawing and copy-pasting
    # Velocities are varied to demonstrate the dynamic control shown in the video.
    for bar_num in range(bars):
        bar_start_time = bar_num * bar_length_sec
        
        # Place chords on each beat of the bar (simulating a simple progression)
        # Varying velocities to demonstrate the feature from the tutorial
        for beat_in_bar in range(beats_per_bar):
            note_start_time = bar_start_time + (beat_in_bar * beat_duration)
            
            # Simple velocity variation pattern for demonstration
            current_velocity_c = max(0, min(127, velocity_base + (-10 if beat_in_bar % 2 == 0 else 5)))
            current_velocity_e = max(0, min(127, velocity_base + (5 if beat_in_bar % 2 == 0 else -5)))
            current_velocity_g = max(0, min(127, velocity_base + (-5 if beat_in_bar % 2 == 0 else 10)))

            RPR.MIDI_InsertNote(midi_take, False, False, note_start_time, note_start_time + note_duration_beats * time_per_beat, current_velocity_c, False, chord_notes[0], 0)
            RPR.MIDI_InsertNote(midi_take, False, False, note_start_time, note_start_time + note_duration_beats * time_per_beat, current_velocity_e, False, chord_notes[1], 0)
            RPR.MIDI_InsertNote(midi_take, False, False, note_start_time, note_start_time + note_duration_beats * time_per_beat, current_velocity_g, False, chord_notes[2], 0)

    RPR.MIDI_Sort(midi_take)
    # RPR.MIDI_MarkAllNotes(midi_take, True) # Optional: Select all notes in MIDI editor when opened
    RPR.MIDI_Commit(midi_take)

    # === Step 6: Add a Pitch Bend Automation Lane ===
    # This simulates the "Add Lane" feature for CC parameters in the MIDI editor.
    # Pitch Bend (MIDI CC 0x0) is often labelled "Pitch" in REAPER.
    pitch_bend_envelope = RPR.GetTrackEnvelopeByName(track, "Pitch")
    if not pitch_bend_envelope:
        pitch_bend_envelope = RPR.CreateTrackEnvelope(track)
        # Ensure the envelope is properly set up as a Pitch Bend envelope
        RPR.SetEnvelopeState(pitch_bend_envelope, "ACT 1 ENM Pitch\0") 
        # Set envelope points for demonstration of automation
        # Value ranges from -1.0 to 1.0 (full down to full up, 0.0 is center)
        RPR.InsertEnvelopePoint(pitch_bend_envelope, 0.0, 0.0, 0, 0, False, False, False)
        RPR.InsertEnvelopePoint(pitch_bend_envelope, bar_length_sec * 1.5, 0.5, 0, 0, False, False, False) # Pitch up slightly
        RPR.InsertEnvelopePoint(pitch_bend_envelope, bar_length_sec * 2.5, -0.5, 0, 0, False, False, False) # Pitch down
        RPR.InsertEnvelopePoint(pitch_bend_envelope, item_length, 0.0, 0, 0, False, False, False) # Return to center
        RPR.Envelope_SortPoints(pitch_bend_envelope)

    # === Step 7: Refresh REAPER UI ===
    RPR.UpdateArrange()
    RPR.TrackList_AdjustWindows(False) # Adjust track view to show envelope if necessary

    num_notes = RPR.MIDI_CountEvts(midi_take, None, None, None)
    return f"Created '{track_name}' with {num_notes} notes over {bars} bars at {bpm} BPM, including velocity variations and Pitch Bend automation."

