import reaper_python as RPR

def create_massivex_bleass_granular_pattern(
    project_name: str = "MassiveX & BLEASS Granular Demo",
    track_name: str = "Synth Pluck with Granular FX",
    bpm: int = 120,
    key: str = "C", # Key is not explicitly set for MIDI, but kept for consistency
    scale: str = "major", # Scale is not explicitly set for MIDI, but kept for consistency
    bars: int = 4,
    velocity_base: int = 90, # Velocity for the placeholder MIDI item
    octave: int = 4, # Octave for the placeholder MIDI item
    **kwargs,
) -> str:
    """
    Creates a track with Native Instruments Massive X, Reason Rack Plugin (for Beat Map),
    and BLEASS Granular, along with a placeholder MIDI item.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B) - used for placeholder MIDI item.
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.) - used for placeholder MIDI item.
        bars: Number of bars for the MIDI item.
        velocity_base: Base MIDI velocity (0-127) for the placeholder MIDI item.
        octave: Starting octave for the placeholder MIDI item.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Synth Pluck with Granular FX' track with VSTs and a placeholder MIDI item."
    """
    # Music theory lookup tables (used for placeholder MIDI, not for actual Beat Map output)
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

    RPR.Undo_BeginBlock2(0) # Begin undo block

    try:
        # === Step 1: Set Tempo ===
        RPR.RPR_SetCurrentBPM(0, bpm, False)

        # === Step 2: Create Track ===
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

        # === Step 3: Add Massive X VSTi ===
        # Note: Specific preset "Retro Pluck" cannot be loaded programmatically for VSTs.
        # User will need to load it manually from Massive X UI.
        massive_x_added = RPR.RPR_TrackFX_AddByName(track, "Massive X (Native Instruments)", False, -1)
        if not massive_x_added:
            return "Failed to add Massive X. Please ensure it is installed and correctly scanned by REAPER."
        
        # === Step 4: Add Reason Rack Plugin (to host Beat Map) ===
        reason_rack_added = RPR.RPR_TrackFX_AddByName(track, "Reason Rack Plugin (Propellerhead)", False, -1)
        if not reason_rack_added:
            return "Failed to add Reason Rack Plugin. Please ensure it is installed and correctly scanned by REAPER."
        # User needs to manually load 'Beat Map' inside Reason Rack Plugin and configure its routing to Massive X.

        # === Step 5: Add BLEASS Granular VST3 Effect ===
        bleass_granular_added = RPR.RPR_TrackFX_AddByName(track, "BLEASS Granular (BLEASS)", False, -1)
        if not bleass_granular_added:
            return "Failed to add BLEASS Granular. Please ensure it is installed and correctly scanned by REAPER."
        # The video shows adjustment of the 'Mix' knob. Its parameter ID is VST-specific and not visible in the video.
        # User needs to manually adjust its parameters.

        # === Step 6: Create Placeholder MIDI Item ===
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_length_sec * bars
        
        # Get current project time to place the item
        current_time = RPR.RPR_GetPlayPosition(0)

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        
        take = RPR.RPR_GetActiveTake(item)
        if not take:
            take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Add a single C4 note as a placeholder to make the MIDI item non-empty
        # This will be replaced by the MIDI output from Reason Rack Plugin/Beat Map
        # or by user-entered notes.
        placeholder_midi_note = (NOTE_MAP.get(key, 0) + (octave * 12)) 
        RPR.MIDI_InsertNote(take, False, False, 0.0, 0.5, velocity_base, False, placeholder_midi_note, True)
        
        RPR.MIDI_Sort(take)
        RPR.MIDI_SetItemExtents(item, True, True) # Adjust item length to content
        
        RPR.RPR_UpdateArrange()
        # RPR.RPR_Main_OnCommand(40050, 0) # Item navigation: move cursor to start of selected items (optional)

        return (
            f"Created '{track_name}' track with Massive X, Reason Rack Plugin, and BLEASS Granular VSTs.\n"
            "**Manual steps required:**\n"
            "1. Load 'Retro Pluck' preset in Massive X.\n"
            "2. Open Reason Rack Plugin, add 'Beat Map' player, and route its MIDI output to Massive X.\n"
            "3. Adjust parameters (e.g., 'Mix' knob) in BLEASS Granular to taste.\n"
            "4. The included MIDI item has a placeholder note. You can delete it and use Beat Map, or add your own MIDI."
        )

    finally:
        RPR.Undo_EndBlock2(0, "Create Massive X + BLEASS Granular Pattern Setup", -1)

