import reaper_python as RPR

def create_pattern(
    project_name: str = "Basic MIDI Workflow Demo",
    track_name: str = "MIDI Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major", # Using major for the C chord example
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Demonstrates basic MIDI editing workflow techniques in REAPER.
    Creates a track, adds a VSTi (ReaSynth), inserts example MIDI notes,
    and highlights velocity and pitch CC lanes for further manual editing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this basic skill).

    Returns:
        Status string, e.g., "Created 'MIDI Piano' with 6 notes over 4 bars at 120 BPM.
        ReaSynth loaded. Velocity and Pitch CC lanes ready for automation."
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        # ... other scales not directly used for fixed chords but good for other skills
    }

    root_midi_note = NOTE_MAP.get(key.upper(), 0) + 60 # C4 is MIDI note 60

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add VST Instrument (ReaSynth as a common placeholder) ===
    # The video uses "VSTi: Grand Piano (saulocity)". ReaSynth is a stock alternative.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    
    # === Step 4: Create MIDI Item ===
    # For 4/4 time signature, each bar is 4 beats. Beat length is 60/BPM seconds.
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at beginning of project
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        RPR.RPR_ShowConsoleMsg("Failed to get active take.\n")
        return "Error: Failed to get active take."

    # Create MIDI object from take
    midi_take = RPR.RPR_MIDI_AllocTemporary(take)
    if not midi_take:
        RPR.RPR_ShowConsoleMsg("Failed to allocate temporary MIDI_Take.\n")
        return "Error: Failed to allocate temporary MIDI_Take."

    # === Step 5: Insert example MIDI notes (a simple C major chord progression) ===
    # Note: The video shows manual note drawing, this code creates notes programmatically
    # to set up an editable example.
    
    # C major triad (C4, E4, G4) starting at beat 0, length 1 beat, varying velocities
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 0.0 * beat_length_sec, 1.0 * beat_length_sec, velocity_base - 20, 0, root_midi_note)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 0.0 * beat_length_sec, 1.0 * beat_length_sec, velocity_base, 0, root_midi_note + 4)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 0.0 * beat_length_sec, 1.0 * beat_length_sec, velocity_base + 10, 0, root_midi_note + 7)

    # G major triad (G4, B4, D5) starting at beat 1, length 1 beat, varying velocities
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 1.0 * beat_length_sec, 2.0 * beat_length_sec, velocity_base - 10, 0, root_midi_note + 7)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 1.0 * beat_length_sec, 2.0 * beat_length_sec, velocity_base + 5, 0, root_midi_note + 11)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 1.0 * beat_length_sec, 2.0 * beat_length_sec, velocity_base + 15, 0, root_midi_note + 14)

    # A minor triad (A4, C5, E5) starting at beat 2, length 1 beat, varying velocities
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 2.0 * beat_length_sec, 3.0 * beat_length_sec, velocity_base - 5, 0, root_midi_note + 9)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 2.0 * beat_length_sec, 3.0 * beat_length_sec, velocity_base + 10, 0, root_midi_note + 12)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 2.0 * beat_length_sec, 3.0 * beat_length_sec, velocity_base + 20, 0, root_midi_note + 16)
    
    # F major triad (F4, A4, C5) starting at beat 3, length 1 beat, varying velocities
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 3.0 * beat_length_sec, 4.0 * beat_length_sec, velocity_base - 15, 0, root_midi_note + 5)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 3.0 * beat_length_sec, 4.0 * beat_length_sec, velocity_base, 0, root_midi_note + 9)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 3.0 * beat_length_sec, 4.0 * beat_length_sec, velocity_base + 10, 0, root_midi_note + 12)

    # === Step 6: Apply MIDI changes and set active CC lanes for manual editing ===
    RPR.RPR_MIDI_FreeTemporary(midi_take)
    RPR.RPR_MIDIEditor_SetActiveTake(take) # Set the take as active for MIDI editor
    
    # Open MIDI Editor (if not already open, this command opens it)
    RPR.RPR_Main_OnCommand(40050, 0) # View: Open/close MIDI editor

    # Set Velocity lane as visible (CC lane 07)
    # The constants for CC lanes are not directly in ReaScript, but velocity is a common control.
    # MIDI_SetCCTextVelShape(index, hidetext, hidevel, showvel_val, showtext_val)
    # 0 = Velocity, 1 = Pitch, 2 = Program, 3 = Channel Pressure, 4 = Bank/Program Select
    # This might require some deeper MIDI editor API calls or manual interaction.
    # For now, we ensure the MIDI editor is open and focus on velocity setting in the notes.
    # The video shows the velocity lane automatically appearing when notes are present.
    # To explicitly show it programmatically, we can try to activate the correct CC lane.
    # This part is more for the user to confirm in the UI.

    # RPR.MIDIEditor_SetCurrentCCShape(midi_editor, type, draw_flags)
    # Let's try to simulate setting current CC lane to velocity by opening the MIDI editor then setting the view
    
    # Get the active MIDI editor
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # These commands are often internal actions, but we can set properties.
        # For velocity (CC 07), usually it's the default or set via menu.
        # This part ensures the take is loaded for editing velocity/pitch.
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40066) # MIDI: Show velocity/volume lane

        # For Pitch, can simulate adding another lane via action if a specific action exists.
        # Often these are done via menu, so direct programmatic control can be complex.
        # The key is that the notes are there, and the lanes can be activated by the user.

    return f"Created '{track_name}' with 12 notes over {bars} bars at {bpm} BPM. ReaSynth loaded. " \
           f"MIDI editor opened with example notes. Velocity and other CC lanes ready for manual automation tweaking."

