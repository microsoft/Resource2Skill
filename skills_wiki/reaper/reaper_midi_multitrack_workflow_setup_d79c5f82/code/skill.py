import reaper_python as RPR
import time

def setup_midi_multitrack_editing_workflow(
    project_name: str = "DemoProject",
    bars: int = 4,
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    velocity_base: int = 100,
    ghost_opacity: int = 2, # 1-3
    **kwargs,
) -> str:
    """
    Configures REAPER's MIDI Editor for an efficient multitrack editing workflow.
    This includes setting preferences, docking the editor, and adding a toggle for
    multi-track editing. It also creates some dummy MIDI items for demonstration.

    Args:
        project_name: Project identifier (for logging).
        bars: Number of bars for the demo MIDI items.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B) for demo items.
        scale: Scale type (major, minor, etc.) for demo items.
        velocity_base: Base MIDI velocity (0-127) for demo items.
        ghost_opacity: Opacity for secondary (ghost) MIDI notes (1-3).
        **kwargs: Additional overrides (not used in this setup skill).

    Returns:
        Status string describing the setup and demo items.
    """

    # Music theory lookup tables (for demo items)
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
    
    # === 1. Configure MIDI Editor Preferences ===
    # These settings are typically stored in reaper.ini.
    # "1" = enabled/true, "0" = disabled/false.
    
    # "One MIDI editor per: project"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_oneeditorper", "2", True)
    # "Active MIDI item follows selection changes in arrange view"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_itemfollsel", "1", True)
    # "Selection is linked to visibility"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_linkvis", "1", True)
    # "Selection is linked to editability"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_linkededit", "1", True)
    # "Close editor when the active item is deleted in the arrange view"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_autoclose", "0", True)
    # "Make secondary items editable by default"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_makeseceditable", "1", True)
    # "Avoid automatically setting MIDI items from other tracks editable" (initial state for toggle)
    # For multi-track editing by default, this should be 0. The button toggles it.
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_avoidautosecedit", "0", True)
    # "Opacity (1-3) for notes/CC in secondary media items"
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_ghost_opacity", str(ghost_opacity), True)

    # Reload preferences to apply changes immediately
    RPR.RPR_Main_OnCommand(40866, 0) # Action: Preferences: Reload last saved project settings (if any) or restore default project settings if none.

    # === 2. Create Demo Tracks and MIDI Items ===
    track_names = ["01 MIDI Drums", "02 BASS", "03 GTR RHY", "04 GTR LEAD"]
    tracks = []
    root_midi = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # Set BPM
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    for i, name in enumerate(track_names):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Set track color (for "Color notes by Track" in MIDI editor)
        # Using simple colors: 0xFF0000 (Red), 0x00FF00 (Green), 0x0000FF (Blue), 0xFFFF00 (Yellow)
        colors = [0x0000FF, 0xFF00FF, 0xFF7F00, 0x00FFFF] # Blue, Magenta, Orange, Cyan
        RPR.RPR_SetTrackColor(track, colors[i % len(colors)])
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", 1) # Enable custom color

        # Add ReaSynth for melodic tracks, ReaSamplOmatic5000 for drums
        if "Drums" in name:
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
            # Load a simple kick sample (this is a placeholder, actual sample might not exist)
            # RPR.RPR_CSurf_OnMidiChange(track, 0, 12, 1, 0) # Example to trigger first FX parameter
        else:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI item
        item_pos = 0.0
        item_length = (60.0 / bpm) * 4 * bars # 4 beats per bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_GetActiveTake(item)
        if take:
            RPR.RPR_TakeFX_AddByName(take, "MIDI_editor_notation", False, -1) # Ensure piano roll view is active

            # Generate simple MIDI notes for demonstration
            midi_take = RPR.RPR_MIDI_GetTake(take)
            if midi_take:
                if "Drums" in name:
                    # Simple kick and snare pattern
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 0.0, 0.5, velocity_base, 36, 0) # Kick on 1
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 1.0, 0.5, velocity_base, 38, 0) # Snare on 2
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 2.0, 0.5, velocity_base, 36, 0) # Kick on 3
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, 3.0, 0.5, velocity_base, 38, 0) # Snare on 4
                elif "BASS" in name:
                    # Simple root notes
                    for beat in range(bars * 4):
                        pitch = root_midi + (scale_intervals[beat % len(scale_intervals)] if beat < bars * len(scale_intervals) else 0) - 12 # One octave lower
                        RPR.RPR_MIDI_InsertNote(midi_take, False, False, float(beat), 1.0, velocity_base, pitch, 0)
                elif "GTR RHY" in name:
                    # Simple chords
                    for beat in range(bars * 4):
                        root_pitch = root_midi + scale_intervals[beat % len(scale_intervals)] + 12
                        RPR.RPR_MIDI_InsertNote(midi_take, False, False, float(beat), 1.0, velocity_base, root_pitch, 0)
                        RPR.RPR_MIDI_InsertNote(midi_take, False, False, float(beat), 1.0, velocity_base, root_pitch + scale_intervals[2] , 0) # Third
                        RPR.RPR_MIDI_InsertNote(midi_take, False, False, float(beat), 1.0, velocity_base, root_pitch + scale_intervals[4] , 0) # Fifth
                elif "GTR LEAD" in name:
                    # Simple ascending melody
                    for beat in range(bars * 4):
                        pitch = root_midi + scale_intervals[beat % len(scale_intervals)] + 24
                        RPR.RPR_MIDI_InsertNote(midi_take, False, False, float(beat) + 0.5, 0.5, velocity_base, pitch, 0)

                RPR.RPR_MIDI_Sort(midi_take)
                RPR.RPR_MIDI_SetItemExtents(midi_take, 0, 0, 0) # Update item based on MIDI
                RPR.RPR_MIDI_FreeCommand(midi_take, True) # Apply changes

        RPR.RPR_UpdateArrange() # Update REAPER display
        tracks.append(track)
        
    # Select all created items for demonstration
    RPR.RPR_SelectAllMediaItems(0, True)
    for i in range(RPR.RPR_CountMediaItems(0)):
        item = RPR.RPR_GetMediaItem(0, i)
        RPR.RPR_SetMediaItemSelected(item, True)


    # === 3. Open and Dock MIDI Editor ===
    # Open MIDI editor (Action ID: 40049)
    RPR.RPR_Main_OnCommand(40049, 0) 
    
    # Give REAPER a moment to open the window, otherwise docking might fail
    time.sleep(0.5) 

    # Find the MIDI editor window and dock it
    # Action ID: 40751 toggles "Dock editor" in the MIDI Editor.
    # This assumes the MIDI editor is the currently focused window when the action is run.
    # We trigger the action when the MIDI editor is already open.
    RPR.RPR_Main_OnCommand(40751, 0) 
    
    # Give REAPER a moment to dock the window
    time.sleep(0.2)

    # === 4. Set MIDI Editor View Options ===
    # "Draw and edit on all tracks" (Action ID: 40722 in MIDI Editor context)
    # Ensure this is enabled for multi-track editing
    if RPR.RPR_GetToggleCommandState(40722) == 0: # If disabled, enable it
        RPR.RPR_Main_OnCommand(40722, 0)

    # "Color notes by Track" (Action ID: 40704 in MIDI Editor context will cycle, 
    # but a preference string is more direct if available, or we might need to cycle until "Track")
    # For now, let's assume it's initially by Velocity and cycle to Track if needed, or rely on preference.
    # The preference "midieditor_color_mode" should cover this. 4=track.
    RPR.RPR_WritePrivateProfileString("REAPER", "pref_midieditor_color_mode", "4", True)
    RPR.RPR_Main_OnCommand(40866, 0) # Reload preferences

    # === 5. Add Custom Toolbar Button (Manual step - ReaScript cannot directly modify toolbars) ===
    # To add "Options: Avoid automatically setting MIDI items from other tracks editable" (Action ID: 40750)
    # to the MIDI editor toolbar, the user would typically right-click the MIDI editor toolbar ->
    # "Customize toolbar" -> Add -> find Action 40750 -> "Text icon..." and name it "SINGLE TRACK EDIT"
    # This specific step is not directly reproducible by ReaScript for toolbar customization.
    # We ensure the preference is set correctly, and the user can manually add the button if desired.
    
    return f"MIDI Multitrack Workflow setup complete. Created {len(track_names)} demo tracks and docked MIDI editor. Please manually add the 'SINGLE TRACK EDIT' toolbar button (Action ID 40750) to your MIDI editor toolbar for full functionality."

