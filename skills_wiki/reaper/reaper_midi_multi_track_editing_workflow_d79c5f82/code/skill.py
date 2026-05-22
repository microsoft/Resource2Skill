import reaper_python as RPR

# Music theory lookup tables (for demonstration MIDI only)
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
CHORDS = {
    "C_major_triad": [0, 4, 7],
    "G_major_triad": [7, 11, 14],
    "A_minor_triad": [9, 12, 16],
    "F_major_triad": [5, 9, 12],
}

def get_midi_note(root_key_name: str, scale_degree: int, octave: int = 4) -> int:
    """Calculates the MIDI note number for a given root key, scale degree, and octave."""
    root_midi = NOTE_MAP.get(root_key_name, 0)
    scale_intervals = SCALES.get("major") # Using major for simple demo chords
    if not scale_intervals: return 0
    
    # Calculate midi note for the scale degree
    midi_note = root_midi + scale_intervals[scale_degree % len(scale_intervals)] + (octave * 12)

    # Adjust octave based on scale degree wrap-around
    if scale_degree >= len(scale_intervals):
        midi_note += ((scale_degree // len(scale_intervals)) * 12)

    return midi_note

def create_midi_item_with_notes(track, start_time, duration, notes_data, is_drum_track=False):
    """Creates a MIDI item and inserts notes."""
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_SetItemExt(item, True, False, 0, 0, 0, False))

    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.RPR_MIDI_SetItemExt(item, True, False, 0, 0, 0, False) # Ensure MIDI source is created

    for note_info in notes_data:
        pitch, start, end, velocity = note_info
        if is_drum_track: # Drum notes are fixed pitches for specific drum sounds
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, start, end, True, pitch, velocity, False)
        else: # Regular melodic/harmonic notes
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, start, end, True, pitch, velocity, False)
    
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_UpdateArrange()
    return item

def reaper_midi_workflow_setup(
    project_name: str = "MIDI Workflow Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Sets up REAPER's MIDI editor for better multi-track editing workflow and demonstrates it.

    Args:
        project_name: Project identifier (for logging, not directly used in script for project name).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate for demonstration.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this configuration skill).

    Returns:
        Status string describing the setup and created items.
    """
    RPR.Undo_BeginBlock()

    # === Step 1: Initial REAPER Preferences (Manual Setup Recommended) ===
    # These preferences are persistent and often require a REAPER restart or UI reload
    # to take full effect immediately. It is recommended that the user sets these manually once:
    # Go to Options -> Preferences -> MIDI Editor:
    # 1. "One MIDI editor per:" set to "project"
    # 2. "Active MIDI item follows selection changes in arrange view:" CHECKED
    # 3. "Selection is linked to visibility:" CHECKED
    # 4. "Selection is linked to editability:" CHECKED
    # 5. "Close editor when the active item is deleted in the arrange view:" UNCHECKED (optional)
    # 6. "Opacity (1-3) for notes/CC in secondary media items:" set to 2 or 3 (optional, visual preference)
    #
    # The script will proceed assuming these are set for optimal demonstration.

    # === Step 2: Create Demonstration Tracks ===
    track_names = ["MIDI Drums", "MIDI Bass", "MIDI GTR RHY", "MIDI GTR LEAD"]
    tracks = []
    for i, name in enumerate(track_names):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        # Set track colors for better visibility
        color_val = 0x00FF0000 | (0x0000FF00 * (i % 4)) | (0x000000FF * ((i+1) % 4)) # Simple color cycling
        RPR.RPR_SetTrackColor(track, color_val)
        tracks.append(track)

    # === Step 3: Create Demonstration MIDI Items ===
    beats_per_bar = 4
    bar_length_beats = float(beats_per_bar)
    seconds_per_beat = 60.0 / bpm

    # Create empty MIDI items first
    midi_items = []
    for track in tracks:
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * bar_length_beats * seconds_per_beat)
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_SetItemExt(item, True, False, 0, 0, 0, False))
        midi_items.append(item)

    # Populate MIDI items with simple notes for demonstration
    # MIDI Drums (General MIDI drum map for simplicity)
    drum_notes = [
        # Kick on 1 and 3
        (36, 0.0, 0.9, 120), (36, 2.0, 2.9, 120),
        (36, 4.0, 4.9, 120), (36, 6.0, 6.9, 120),
        # Snare on 2 and 4
        (38, 1.0, 1.9, 110), (38, 3.0, 3.9, 110),
        (38, 5.0, 5.9, 110), (38, 7.0, 7.9, 110),
        # Hi-hats 1/8th notes
        (42, 0.0, 0.4, 90), (42, 0.5, 0.9, 90), (42, 1.0, 1.4, 90), (42, 1.5, 1.9, 90),
        (42, 2.0, 2.4, 90), (42, 2.5, 2.9, 90), (42, 3.0, 3.4, 90), (42, 3.5, 3.9, 90),
        (42, 4.0, 4.4, 90), (42, 4.5, 4.9, 90), (42, 5.0, 5.4, 90), (42, 5.5, 5.9, 90),
        (42, 6.0, 6.4, 90), (42, 6.5, 6.9, 90), (42, 7.0, 7.4, 90), (42, 7.5, 7.9, 90),
    ]
    create_midi_item_with_notes(tracks[0], 0.0, bars * bar_length_beats * seconds_per_beat, drum_notes, is_drum_track=True)

    # MIDI Bass (root notes of chords)
    bass_notes = [
        (get_midi_note(key, 0, 2), 0.0, 1.9, 100), # C2
        (get_midi_note(key, 5, 2), 2.0, 3.9, 100), # F2
        (get_midi_note(key, 7, 2), 4.0, 5.9, 100), # G2
        (get_midi_note(key, 9, 2), 6.0, 7.9, 100), # A2
    ]
    create_midi_item_with_notes(tracks[1], 0.0, bars * bar_length_beats * seconds_per_beat, bass_notes)

    # MIDI GTR RHY (simple chords)
    gtr_rhy_notes = [
        # C Major Triad
        (get_midi_note(key, 0, 3), 0.0, 0.9, 95), (get_midi_note(key, 2, 3), 0.0, 0.9, 95), (get_midi_note(key, 4, 3), 0.0, 0.9, 95),
        # F Major Triad
        (get_midi_note(key, 5, 3), 2.0, 2.9, 95), (get_midi_note(key, 9, 3), 2.0, 2.9, 95), (get_midi_note(key, 0, 4), 2.0, 2.9, 95),
        # G Major Triad
        (get_midi_note(key, 7, 3), 4.0, 4.9, 95), (get_midi_note(key, 11, 3), 4.0, 4.9, 95), (get_midi_note(key, 2, 4), 4.0, 4.9, 95),
        # A Minor Triad
        (get_midi_note(key, 9, 3), 6.0, 6.9, 95), (get_midi_note(key, 0, 4), 6.0, 6.9, 95), (get_midi_note(key, 3, 4), 6.0, 6.9, 95),
    ]
    create_midi_item_with_notes(tracks[2], 0.0, bars * bar_length_beats * seconds_per_beat, gtr_rhy_notes)

    # MIDI GTR LEAD (simple melody/arpeggio)
    gtr_lead_notes = [
        (get_midi_note(key, 4, 4), 0.0, 0.5, 105), (get_midi_note(key, 5, 4), 0.5, 1.0, 105),
        (get_midi_note(key, 7, 4), 1.0, 1.5, 105), (get_midi_note(key, 9, 4), 1.5, 2.0, 105),
        (get_midi_note(key, 11, 4), 2.0, 2.5, 105), (get_midi_note(key, 12, 4), 2.5, 3.0, 105),
        (get_midi_note(key, 14, 4), 3.0, 3.5, 105), (get_midi_note(key, 16, 4), 3.5, 4.0, 105),
        # Repeat roughly
        (get_midi_note(key, 4, 4), 4.0, 4.5, 105), (get_midi_note(key, 5, 4), 4.5, 5.0, 105),
        (get_midi_note(key, 7, 4), 5.0, 5.5, 105), (get_midi_note(key, 9, 4), 5.5, 6.0, 105),
        (get_midi_note(key, 11, 4), 6.0, 6.5, 105), (get_midi_note(key, 12, 4), 6.5, 7.0, 105),
        (get_midi_note(key, 14, 4), 7.0, 7.5, 105), (get_midi_note(key, 16, 4), 7.5, 8.0, 105),
    ]
    create_midi_item_with_notes(tracks[3], 0.0, bars * bar_length_beats * seconds_per_beat, gtr_lead_notes)

    # Select all tracks and MIDI items for demonstration
    for track in tracks:
        RPR.RPR_SetTrackSelected(track, True)
    for item in midi_items:
        RPR.RPR_SetMediaItemSelected(item, True)

    # === Step 4: Open and Dock MIDI Editor ===
    # Action: View: Toggle show MIDI Editor windows (main window)
    RPR.RPR_Main_OnCommand(40879, 0)
    # Find the MIDI editor window and dock it (requires the window to be open)
    # This part can be tricky via ReaScript as window handles are dynamic.
    # The video shows clicking a specific icon in the MIDI editor toolbar.
    # The action ID for 'Dock editor (toggle)' within the MIDI Editor is 40049.
    # This might need to be triggered while the MIDI Editor is the focused window.
    # For a general script, it's often easier to guide the user to dock it manually once.
    # Let's try to assume it's open and run the dock action, which might fail if it's not focused.
    # A more robust solution might involve iterating through windows, but for simplicity:
    # RPR.RPR_Main_OnCommand(40049, 0) # This ID is for the main action list, not MIDI editor's specific action.

    # === Step 5: Apply MIDI Editor Settings via Actions ===
    # Action: Options: Draw and edit CC events in multiple media items (all tracks)
    # This enables editing ghost notes.
    RPR.RPR_Main_OnCommand(40162, 0) 
    
    # Action: View: Piano roll notes: Color notes by track
    # This colors ghost notes and active notes according to their track color.
    RPR.RPR_Main_OnCommand(40578, 0)

    # Action: Options: Avoid automatically setting MIDI items from other tracks editable (toggle)
    # This action needs to be added to the MIDI editor toolbar by the user for quick access.
    # It toggles between "single track edit" and "multi-track edit with ghost notes editable"
    # Action ID: 40484. The script toggles it off (multi-track edit mode) initially.
    if RPR.RPR_GetToggleCommandState(40484) == 1: # If single track edit is ON
        RPR.RPR_Main_OnCommand(40484, 0) # Toggle it OFF to enable multi-track editing

    # === Step 6: Recommend Shortcuts ===
    RPR.RPR_ShowConsoleMsg("\n--- MIDI Editor Workflow Setup Complete! ---")
    RPR.RPR_ShowConsoleMsg("1. Please ensure your MIDI Editor is set to 'One MIDI editor per: project' in REAPER Preferences (Options -> Preferences -> MIDI Editor).")
    RPR.RPR_ShowConsoleMsg("2. Also ensure 'Active MIDI item follows selection changes in arrange view', 'Selection is linked to visibility', and 'Selection is linked to editability' are CHECKED in the same preferences window.")
    RPR.RPR_ShowConsoleMsg("3. The MIDI Editor should now be open, displaying notes for all selected items, with unselected items appearing as ghost notes.")
    RPR.RPR_ShowConsoleMsg("4. 'Draw and edit on all tracks' is ENABLED, allowing you to edit ghost notes.")
    RPR.RPR_ShowConsoleMsg("5. 'Color notes by track' is ENABLED for better visual differentiation.")
    RPR.RPR_ShowConsoleMsg("6. To quickly toggle between editing only the active item and editing all editable items (ghost notes included), consider adding Action ID 40484 ('Options: Avoid automatically setting MIDI items from other tracks editable (toggle)') to your MIDI editor toolbar via 'Options -> Customize menus/toolbars...'.")
    RPR.RPR_ShowConsoleMsg("7. For seamless navigation between MIDI items, map keyboard shortcuts to 'MIDI Editor: Activate next visible MIDI item' (e.g., Opt+N) and 'MIDI Editor: Activate previous visible MIDI item' (e.g., Opt+Shift+N) in the Actions list.\n")
    RPR.RPR_ShowConsoleMsg("Feel free to edit the generated MIDI items to see the workflow in action!")
    
    RPR.Undo_EndBlock("REAPER MIDI Workflow Setup", -1)
    
    return f"Configured MIDI editor workflow and created demonstration tracks for '{project_name}'."

