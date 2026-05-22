import reaper_python as RPR

def get_midi_note_from_key_scale(root_key_str, scale_name, degree, octave):
    """
    Calculates the MIDI note number for a given root key, scale, degree, and octave.
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
    
    root_midi = NOTE_MAP.get(root_key_str)
    if root_midi is None:
        raise ValueError(f"Invalid root key: {root_key_str}")

    scale_intervals = SCALES.get(scale_name)
    if scale_intervals is None:
        raise ValueError(f"Invalid scale name: {scale_name}")

    if not (0 <= degree < len(scale_intervals)):
        # Adjust degree to wrap around the scale if out of bounds
        degree = degree % len(scale_intervals)
        
    midi_note = (octave * 12) + root_midi + scale_intervals[degree]
    return midi_note

def create_midi_workflow_demo(
    project_name: str = "MIDI Workflow Demo",
    bpm: int = 120,
    key: str = "G",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Configures REAPER for multi-instrument MIDI workflow and creates demo music.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    RPR.Undo_BeginBlock() # Begin an undo block

    # --- User Guidance for Persistent Preferences ---
    RPR.ShowConsoleMsg(
        "\n--- REAPER MIDI Editor Workflow Setup ---\n"
        "For the best experience, please manually adjust REAPER Preferences (Options > Preferences > MIDI Editor):\n"
        "  - 'One MIDI editor per': 'Project'\n"
        "  - Check 'Active MIDI item follows selection changes in arrange view'\n"
        "  - Check 'Selection is linked to visibility'\n"
        "  - Check 'Selection is linked to editability'\n"
        "  - Uncheck 'Close editor when the active item is deleted in the arrange view'\n"
        "  - Set 'Opacity (0-3) for notes/CC in secondary media items': 2 (or your preference, 3 for maximum visibility)\n"
        "  - For easy toggling of multi-track editing, add action 'MIDI Editor: Options: Avoid automatically setting MIDI items from other tracks editable' (ID 41255) to a MIDI toolbar.\n"
        "  - For quick item switching, assign shortcuts to 'MIDI Editor: Activate next visible MIDI item' (ID 40854) and 'MIDI Editor: Activate previous visible MIDI item' (ID 40853).\n"
        "After making these changes, you may need to restart REAPER for some settings to fully apply.\n"
        "--------------------------------------------------\n"
    )

    # --- Scripted Workflow Setup (Immediate Actions) ---
    # Open the MIDI editor (if not open) and dock it
    RPR.Main_OnCommand(40053, 0) # View: MIDI editor
    RPR.Main_OnCommand(40866, 0) # MIDI Editor: Toggle dock editor (docks it if floating, undocks if docked)
    
    # Set MIDI editor to color notes by track
    RPR.Main_OnCommand(40822, 0) # MIDI Editor: View: Color notes by track

    # --- Demo Music Creation ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    track_names = ["01-MIDI Drums", "02-BASS MIDI", "03-GTR RHY MIDI", "04-GTR LEAD MIDI"]
    tracks = []
    midi_items = []
    
    # Chord progression for demo (G Major Scale: G, C, D, G)
    # Roots in MIDI notes relative to base_octave
    demo_progression_roots = [
        get_midi_note_from_key_scale(key, scale, 0, 0), # G (1st degree of G major)
        get_midi_note_from_key_scale(key, scale, 3, 0), # C (4th degree of G major)
        get_midi_note_from_key_scale(key, scale, 4, 0), # D (5th degree of G major)
        get_midi_note_from_key_scale(key, scale, 0, 0), # G (1st degree of G major)
    ]

    for i, name in enumerate(track_names):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_WNDH", 50.0) # Set track height for visibility
        tracks.append(track)
        
        # Add basic VSTi for sound, ReaSamplOmatic for drums
        if "Drums" in name:
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
        else:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_SetOpen(track, RPR.RPR_TrackFX_GetCount(track)-1, False) # Close FX window

        # Create MIDI item
        item_pos = 0.0
        item_length = bars * (60.0 / bpm) * 4 # 4 beats per bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_GetActiveTake(item) or RPR.RPR_AddTakeToMediaItem(item)
        
        RPR.RPR_MIDI_Clear(take) # Clear any default notes
        
        if "Drums" in name:
            # Basic Kick, Snare, Hi-Hat pattern
            for bar_offset in range(bars):
                # Kick (MIDI 36, C1) on 1
                RPR.RPR_MIDI_InsertNote(take, False, False, item_pos + bar_offset * 4 * (60.0/bpm), 0.25 * (60.0/bpm), 36, velocity_base, True)
                # Snare (MIDI 38, D1) on 2 and 4
                RPR.RPR_MIDI_InsertNote(take, False, False, item_pos + (bar_offset * 4 + 2) * (60.0/bpm), 0.25 * (60.0/bpm), 38, velocity_base, True)
                # Hi-hat (MIDI 42, F#1) 1/8th notes
                for beat_offset in range(8):
                    RPR.RPR_MIDI_InsertNote(take, False, False, item_pos + (bar_offset * 4 + beat_offset * 0.5) * (60.0/bpm), 0.1 * (60.0/bpm), 42, velocity_base - 20, True)
        elif "BASS" in name:
            # Simple root notes
            for bar_offset in range(bars):
                root_midi = demo_progression_roots[bar_offset % len(demo_progression_roots)]
                RPR.RPR_MIDI_InsertNote(take, False, False, item_pos + bar_offset * 4 * (60.0/bpm), 4 * (60.0/bpm), root_midi + 12*2, velocity_base + 5, True) # 2 octaves up from base
        elif "GTR RHY" in name:
            # Chords: Gmaj, Cmaj, Dmaj, Gmaj (basic triads)
            for bar_offset in range(bars):
                root_midi = demo_progression_roots[bar_offset % len(demo_progression_roots)]
                # Triad intervals (root, major 3rd, perfect 5th)
                for interval in [0, 4, 7]:
                    note_midi = root_midi + interval + 12*4 # 4 octaves up from base
                    RPR.RPR_MIDI_InsertNote(take, False, False, item_pos + bar_offset * 4 * (60.0/bpm), 4 * (60.0/bpm), note_midi, velocity_base, True)
        elif "GTR LEAD" in name:
            # Simple arpeggiated melody
            melody_intervals = [0, 4, 7, 12, 11, 7, 4, 0] # Example arpeggio pattern
            for bar_offset in range(bars):
                root_midi = demo_progression_roots[bar_offset % len(demo_progression_roots)]
                for i, interval in enumerate(melody_intervals):
                    note_midi = root_midi + interval + 12*5 # 5 octaves up from base
                    note_start = item_pos + (bar_offset * 4 + i * 0.5) * (60.0/bpm) # 1/8th notes
                    note_end = note_start + 0.4 * (60.0/bpm)
                    RPR.RPR_MIDI_InsertNote(take, False, False, note_start, note_end - note_start, note_midi, velocity_base, True)

        RPR.RPR_UpdateItemInProject(item) # Update item in project
        RPR.RPR_UpdateArrange() # Update arrange view

    # Select all created items for demonstration of multi-editing
    for item in midi_items:
        RPR.RPR_SetMediaItemSelected(item, True)
    
    RPR.Undo_EndBlock(f"Configured MIDI Workflow and created demo music", -1)
    return f"Configured MIDI Editor workflow and created '{len(tracks)}' demo tracks with MIDI items over {bars} bars at {bpm} BPM."

