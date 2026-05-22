def create_pattern(
    project_name: str = "MyProject",
    base_track_name: str = "Original Item Track",
    new_track_name: str = "Moved Item Track",
    bpm: int = 120,
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Demonstrates REAPER's customization capabilities by setting up tracks/items
    and illustrating the effect of a custom action ("Split and put item above").

    Args:
        project_name: Project identifier (for logging).
        base_track_name: Name for the initial track with the media item.
        new_track_name: Name for the track above, to which an item will be moved.
        bpm: Tempo in BPM.
        bars: Number of bars for the initial media item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the setup and instructions for customization.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    # Create the 'Moved Item Track' first, so 'Original Item Track' is below it.
    # The 'Move to track above' action needs an existing track above.
    track_idx_new = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_new, True)
    track_new = RPR.RPR_GetTrack(0, track_idx_new)
    RPR.RPR_GetSetMediaTrackInfo_String(track_new, "P_NAME", new_track_name, True)

    track_idx_base = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_base, True)
    track_base = RPR.RPR_GetTrack(0, track_idx_base)
    RPR.RPR_GetSetMediaTrackInfo_String(track_base, "P_NAME", base_track_name, True)

    # === Step 3: Create a Sample MIDI Item on the base track ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track_base)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_MIDI_SetItemExtents(take, 0, item_length) # Set MIDI item length

    # Add a simple MIDI note to make it visible
    RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, 0.5 * bar_length_sec, velocity_base, 60, 0)
    RPR.RPR_MIDI_InsertNote(take, False, False, 1.0 * bar_length_sec, 1.5 * bar_length_sec, velocity_base, 62, 0)
    RPR.RPR_MIDI_InsertNote(take, False, False, 2.0 * bar_length_sec, 2.5 * bar_length_sec, velocity_base, 64, 0)
    RPR.RPR_MIDI_InsertNote(take, True, True, 3.0 * bar_length_sec, 3.5 * bar_length_sec, velocity_base, 65, 0)

    # === Step 4: Illustrate the "Split and put item above" custom action effect ===
    # For demonstration, we'll select the item created and place the edit cursor
    # around 1/4 into the item for splitting.
    RPR.RPR_SetMediaItemInfo_Value(item, "B_UISEL", 1) # Select the item
    split_pos = item_length / 4.0
    RPR.RPR_SetEditCurPos(split_pos, True, True) # Place edit cursor

    # --- Actions that simulate the custom action ---
    # Action 1: Split items at edit cursor (Action ID 40071)
    # This splits the selected item where the edit cursor is.
    RPR.RPR_Main_OnCommand(40071, 0)

    # Action 2: Select next item (Action ID 40049)
    # After splitting, the right-hand part is usually selected. Let's ensure the new item is selected.
    # Note: RPR_Main_OnCommand(40289, 0) (Item: Select last touched item) could also work
    RPR.RPR_Main_OnCommand(40049, 0) 
    
    # Action 3: Move selected items to track above (Action ID 40224)
    # Moves the newly selected item to the track directly above it.
    RPR.RPR_Main_OnCommand(40224, 0)

    # --- Instructions for user about creating the custom action manually ---
    instructions = (
        "\n--- REAPER Customization Tips (from the video) ---\n"
        "1. To truly create the 'Split and put item above' custom action:\n"
        "   - Press '?' to open the Actions list.\n"
        "   - Click 'New action' -> 'New custom action'.\n"
        "   - Name it, e.g., 'Split and put item above'.\n"
        "   - Search for and drag these actions to the right side (in order):\n"
        "     - 'Item: Split items at edit cursor' (Action ID 40071)\n"
        "     - 'Item: Select next item' (Action ID 40049)\n" # Using 'Select next item' because 'select item under mouse' can't be guaranteed.
        "     - 'Track: Move selected items to track above' (Action ID 40224)\n"
        "   - Assign a shortcut to your custom action (e.g., Ctrl+E).\n"
        "   - Now, select an item, place your edit cursor, and try your new shortcut!\n"
        "\n"
        "2. For general workflow optimization (as discussed in the video):\n"
        "   - Explore REAPER Preferences (Options -> Preferences) to adapt settings to your needs.\n"
        "   - Right-click on almost any element in REAPER to discover context-specific menus and options.\n"
        "   - Create and save custom screen layouts (View -> Screen sets/layouts -> Save current screen set) for different tasks (mixing, recording, editing, songwriting)."
    )

    return (
        f"Created '{base_track_name}' and '{new_track_name}' tracks, "
        f"and demonstrated a custom action effect (split and move item) "
        f"at {bpm} BPM. An item was created on '{base_track_name}', "
        f"split, and part of it moved to '{new_track_name}'.\n"
        f"{instructions}"
    )

