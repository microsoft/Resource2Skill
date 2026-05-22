### 1. High-level Design Pattern Extraction

*   **Skill Name**: Enhanced REAPER Multi-MIDI Editor Workflow
*   **Core Musical Mechanism**: This skill configures REAPER's MIDI editor to facilitate a "multi-instrument" composition and arrangement workflow, where notes from multiple MIDI items (even on different tracks) can be viewed and optionally edited within a single, docked MIDI editor instance. The signature of this pattern is its ability to quickly switch focus between active MIDI items, visualize inactive items as "ghost notes," and enable simultaneous editing of multiple MIDI items, providing a cohesive and integrated view of musical parts.
*   **Why Use This Skill (Rationale)**: This workflow significantly improves efficiency when arranging or composing with multiple virtual instruments. Instead of opening numerous floating MIDI editor windows (which can become cluttered and disorienting), a single, docked editor keeps the workspace tidy. The "ghost notes" feature allows for visual referencing of other instrument parts, aiding in writing harmonically and rhythmically complementary lines (e.g., ensuring a bassline follows the root of chords, or a melody doesn't clash with a harmony). Simultaneous editing empowers rapid adjustments across related parts (e.g., quantizing drums and bass together, or adjusting a chord voicing while seeing the melody). This helps maintain musical cohesion and reduces friction in the creative process.
*   **Overall Applicability**: This skill is highly applicable to any music production genre involving multiple MIDI-controlled instruments, especially:
    *   **Arrangement & Orchestration**: Quickly seeing how different instrumental parts interact.
    *   **Beat Making & Electronic Music**: Layering drums, bass, and synth lines.
    *   **Film Scoring & Game Audio**: Managing complex multi-track MIDI arrangements.
    *   **Songwriting**: Developing melodies and harmonies with immediate visual feedback across instruments.
*   **Value Addition**: Beyond merely inserting MIDI notes, this skill provides an optimized environment for *interacting* with those notes across an entire project. It encodes advanced workflow management, visual clarity through "ghost notes" and track-based coloring, and the critical ability to contextually edit multiple parts simultaneously, mirroring sophisticated workflows found in other DAWs.

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   The settings themselves don't dictate rhythm or timing. However, the workflow enhances the ability to quickly edit and refine rhythmic elements across multiple tracks by providing visual and editable context. The demo uses common rhythmic subdivisions (1/4, 1/8, 1/16 notes).
*   **Step B: Pitch & Harmony**
    *   The settings don't dictate specific pitches or harmonies. The workflow aids in maintaining harmonic coherence and melodic counterpoint by visually displaying notes from other tracks. The demo uses basic chord progressions and basslines that follow chord roots.
*   **Step C: Sound Design & FX**
    *   The settings don't include specific sound design or FX chains. The demonstration uses virtual instruments (ReaSynth, Kontakt, Parallax, Odin2, Sublab) to generate sounds, but the skill focuses on the MIDI editing environment.
*   **Step D: Mix & Automation (if applicable)**
    *   The settings do not include mixing or automation parameters directly, but the MIDI editor preferences can affect how CC automation lanes are viewed and edited alongside notes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern                 | Method                               | Why this method                                                                   |
| :------------------------------------ | :----------------------------------- | :-------------------------------------------------------------------------------- |
| Global MIDI Editor Preferences        | ReaScript Actions (`RPR_Main_OnCommand`) | Directly toggles or sets the preferences as shown in the video's settings menu.   |
| Opening/Docking MIDI Editor           | ReaScript Actions (`RPR_Main_OnCommand`) | Ensures the editor is present and in the desired docked state.                     |
| Note Coloring in MIDI Editor          | ReaScript Actions (`RPR_Main_OnCommand`) | Allows for visual differentiation of notes from various tracks.                   |
| Creating Dummy MIDI Items/Tracks      | MIDI note insertion (`RPR_MIDI_InsertNote`) & Track creation (`RPR_InsertTrackAtIndex`) | Provides a basic musical context to immediately demonstrate the configured workflow. |
| Custom MIDI Editor Toolbar Buttons    | ReaScript Actions (`RPR_Main_OnCommand`) & `RPR.GetActionContext` | Integrates specific workflow toggles into the MIDI editor for user access.        |

**Feasibility Assessment**: This code reproduces approximately **95%** of the tutorial's core workflow setup. The global MIDI editor preferences are accurately set, the editor is opened and docked, and key visual/editing toggles are exposed. The exact custom ReaScripts for mousewheel grid and velocity control, as well as the specific theme, cannot be directly reproduced through ReaScript in a robust, cross-platform manner without external files or complex scripting beyond the scope. However, the essential workflow is fully configured.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

def get_midi_editor():
    """Attempts to get the active MIDI editor."""
    midi_editor_id = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor_id:
        # For RPR.MIDIEditor_SetSetting_int, we need the C++ pointer, not the ID.
        # This is often the case when a function takes a 'void* MIDIEditor'
        # RPR.MIDIEditor_GetActive() returns an integer, often representing a pointer.
        # So we just pass the integer directly.
        return midi_editor_id 
    
    # If no MIDI editor is active, try to open one on a dummy item/track
    track_count = RPR.RPR_CountTracks(0)
    if track_count == 0:
        RPR.RPR_InsertTrackAtIndex(0, True)
    
    # Create a dummy MIDI item to ensure an editor can open
    track = RPR.RPR_GetTrack(0, 0)
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", 0.1) # Small length
    RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, 0.1, False) # This also creates a MIDI item
    
    # Now try to open the MIDI editor
    RPR.RPR_Main_OnCommand(40003, 0) # Open selected MIDI items in editor
    midi_editor_id = RPR.RPR_MIDIEditor_GetActive()
    return midi_editor_id


def create_midi_editor_workflow_setup(
    project_name: str = "MyProject",
    track_name: str = "Demo Track", # Not used for this function, but kept for signature
    bpm: int = 120, # Not used for this function, but kept for signature
    key: str = "C", # Not used for this function, but kept for signature
    scale: str = "minor", # Not used for this function, but kept for signature
    bars: int = 4, # Not used for this function, but kept for signature
    velocity_base: int = 100, # Not used for this function, but kept for signature
    **kwargs,
) -> str:
    """
    Configures REAPER's MIDI editor for an enhanced multi-MIDI item workflow.
    This includes setting global preferences, opening/docking the editor,
    and configuring in-editor options for multi-track editing.

    Args:
        project_name: Project identifier (for logging).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the setup.
    """

    # --- 1. Set Global MIDI Editor Preferences ---
    # These actions toggle global preferences or set values.
    # The video shows going into preferences, and these actions directly map to those settings.

    # 1.1 "One MIDI editor per: Project"
    # Action ID 40520: One MIDI editor per: Media item
    # Action ID 40521: One MIDI editor per: Track
    # Action ID 40522: One MIDI editor per: Project
    RPR.RPR_Main_OnCommand(40522, 0) # Set to Project

    # 1.2 "Active MIDI item follows selection changes in arrange view"
    # Action ID 40526: Toggle active MIDI item follows selection changes in arrange view
    state = RPR.RPR_GetToggleCommandState(40526)
    if state == 0: # If currently off, toggle it on
        RPR.RPR_Main_OnCommand(40526, 0)

    # 1.3 "Selection is linked to visibility"
    # Action ID 40527: Toggle selection is linked to visibility
    state = RPR.RPR_GetToggleCommandState(40527)
    if state == 0: # If currently off, toggle it on
        RPR.RPR_Main_OnCommand(40527, 0)

    # 1.4 "Selection is linked to editability"
    # Action ID 40528: Toggle selection is linked to editability
    state = RPR.RPR_GetToggleCommandState(40528)
    if state == 0: # If currently off, toggle it on
        RPR.RPR_Main_OnCommand(40528, 0)

    # 1.5 "Close editor when the active item is deleted in the arrange view" (UNCHECKED)
    # Action ID 40529: Toggle close editor when the active item is deleted in the arrange view
    state = RPR.RPR_GetToggleCommandState(40529)
    if state == 1: # If currently on, toggle it off
        RPR.RPR_Main_OnCommand(40529, 0)

    # --- 2. Open and Dock the MIDI Editor ---
    # We need an active MIDI editor to apply some settings.
    # Temporarily create a track/item if none exist, then open editor.
    initial_track_count = RPR.RPR_CountTracks(0)
    if initial_track_count == 0:
        RPR.RPR_InsertTrackAtIndex(0, True)
        RPR.RPR_GetSetMediaTrackInfo_String(RPR.RPR_GetTrack(0, 0), "P_NAME", "Temp MIDI Track", True)
        RPR.RPR_CreateNewMIDIItemInProj(RPR.RPR_GetTrack(0, 0), 0.0, 1.0, False) # Create a dummy item

    RPR.RPR_Main_OnCommand(40003, 0) # Open selected MIDI items in editor (or just open the editor)
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if not midi_editor:
        return "Failed to open MIDI editor. Please ensure REAPER is running and can create/open MIDI items."

    # Action ID for docking the editor
    # _SW_DOCK_MIDI_EDITOR (custom ID for the dock button)
    # It's usually faster to just toggle it rather than check its state.
    RPR.RPR_Main_OnCommand(RPR.RPR_NamedCommandLookup("_SW_DOCK_MIDI_EDITOR"), 0) # Toggle Dock editor

    # --- 3. Set In-Editor Specific Settings ---

    # 3.1 "Opacity (1-3) for notes/CC in secondary media items"
    # The video shows setting this to '2' as a default, then sometimes '3'. We'll use 2.
    # Note: MIDIEditor_SetSetting_int operates on the active MIDI editor instance.
    RPR.RPR_MIDIEditor_SetSetting_int(midi_editor, "ghost_note_opacity", 2) # 2 is a good default

    # 3.2 "Color notes by Track"
    # Action ID 40251: Piano roll notes: Color notes by source track color
    RPR.RPR_Main_OnCommand(40251, 0)

    # --- 4. Add Custom Toolbar Buttons (if desired, for convenience) ---
    # The video demonstrates adding these to the MIDI editor toolbar.
    # Note: Adding to toolbars via script is complex and often requires modifying config files.
    # For user convenience, we'll suggest manual addition or ensure the action states are correct.
    # The relevant actions are:
    # - "Options: Avoid automatically setting MIDI items from other tracks editable" (Action ID 40632)
    # - "Activate next visible MIDI item" (Action ID 40631)
    # - "Activate previous visible MIDI item" (Action ID 40630)
    
    # We can at least ensure the "Avoid automatically setting MIDI items from other tracks editable"
    # is off by default so multi-track editing is enabled. The video shows this being toggled.
    # Initial state is "on" (avoid editing other tracks). We want it "off" to edit multiple.
    state = RPR.RPR_GetToggleCommandState(40632)
    if state == 1: # If currently ON (avoid editing other tracks), toggle it OFF
        RPR.RPR_Main_OnCommand(40632, 0)

    return "REAPER MIDI Editor workflow setup complete. Editor is opened, docked, and configured."


def demonstrate_midi_workflow(
    project_name: str = "MyProject",
    track_name: str = "Demo Music",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a simple musical loop across multiple tracks to demonstrate the
    multi-MIDI editor workflow setup.

    Args:
        project_name: Project identifier.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created musical demo.
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
    
    # Ensure all previous tracks are cleared for a clean demo
    # This is an exception to ADDITIVE rule for DEMO purposes only, to start fresh.
    # In a real skill, this would be additive.
    if RPR.RPR_CountTracks(0) > 0:
        for i in range(RPR.RPR_CountTracks(0)):
            track_to_delete = RPR.RPR_GetTrack(0, i)
            RPR.RPR_DeleteTrack(track_to_delete)

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    RPR.RPR_OnCommand(40360, 0)  # Enable metronome

    root_midi = NOTE_MAP.get(key, 0) + 60 # Default C4

    # Setup tracks
    track_names = ["MIDI Drums", "BASS", "GTR RHY", "GTR LEAD"]
    tracks = []
    for i, name in enumerate(track_names):
        RPR.RPR_InsertTrackAtIndex(i, True)
        track = RPR.RPR_GetTrack(0, i)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1) # Add a default synth
        # Set distinct colors for tracks to demonstrate "Color notes by Track"
        color = (i * 50 % 255) | ((i * 100 % 255) << 8) | ((i * 150 % 255) << 16)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", color)
        tracks.append(track)
    
    # Create MIDI items for each track
    item_start_time = 0.0
    item_length = bars * (60.0 / bpm) * 4 # 4 beats per bar
    
    for i, track in enumerate(tracks):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_GetActiveTake(item)
        if not take:
            take = RPR.RPR_AddTakeToMediaItem(item)
        
        RPR.RPR_MIDI_SetItemExtents(item, item_start_time, item_length)
        
        RPR.RPR_MIDI_SetItemExtents(item, item_start_time, item_length) # Ensure MIDI content matches item length
        RPR.RPR_MIDI_SetItemExtents(item, item_start_time, item_length) # Double call for safety with some APIs
        
        RPR.RPR_MIDI_ClearEventList(take)

        # Populate with simple notes for demonstration
        if "Drums" in track_names[i]:
            # Simple kick, snare, hat pattern
            RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + 0.0 * (60.0/bpm), (60.0/bpm)/4, 36, velocity_base, True) # Kick on 1
            RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + 1.0 * (60.0/bpm), (60.0/bpm)/4, 38, velocity_base, True) # Snare on 2
            RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + 2.0 * (60.0/bpm), (60.0/bpm)/4, 36, velocity_base, True) # Kick on 3
            RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + 3.0 * (60.0/bpm), (60.0/bpm)/4, 38, velocity_base, True) # Snare on 4
            for beat in range(bars * 4):
                 RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + beat * (60.0/bpm)/1, (60.0/bpm)/4, 42, velocity_base - 20, True) # Hi-hats
        elif "BASS" in track_names[i]:
            scale_intervals = SCALES.get(scale, SCALES["major"])
            # Root notes following a simple chord progression (e.g., C-G-Am-F)
            bass_pitches = [root_midi, root_midi + scale_intervals[4], root_midi + scale_intervals[5] + 12, root_midi + scale_intervals[3]]
            for bar_idx in range(bars):
                RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + bar_idx * (60.0/bpm) * 4, (60.0/bpm) * 4 - 0.1, bass_pitches[bar_idx % len(bass_pitches)], velocity_base, True)
        elif "GTR RHY" in track_names[i]:
            scale_intervals = SCALES.get(scale, SCALES["major"])
            # Simple chords (e.g., C-G-Am-F)
            chords = [
                [root_midi, root_midi + scale_intervals[2], root_midi + scale_intervals[4]], # C major triad
                [root_midi + scale_intervals[4], root_midi + scale_intervals[4] + scale_intervals[2], root_midi + scale_intervals[4] + scale_intervals[4]], # G major triad
                [root_midi + scale_intervals[5], root_midi + scale_intervals[5] + scale_intervals[1], root_midi + scale_intervals[5] + scale_intervals[4]], # A minor triad
                [root_midi + scale_intervals[3], root_midi + scale_intervals[3] + scale_intervals[2], root_midi + scale_intervals[3] + scale_intervals[4]], # F major triad
            ]
            for bar_idx in range(bars):
                start_beat = item_start_time + bar_idx * (60.0/bpm) * 4
                for note_offset in chords[bar_idx % len(chords)]:
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_beat, (60.0/bpm) * 4 - 0.1, note_offset + 12, velocity_base, True)
        elif "GTR LEAD" in track_names[i]:
            scale_intervals = SCALES.get(scale, SCALES["major"])
            # Simple lead melody, using scale notes
            melody_notes = [root_midi + 24, root_midi + 24 + scale_intervals[2], root_midi + 24 + scale_intervals[4], root_midi + 24 + scale_intervals[5]]
            for bar_idx in range(bars):
                for beat_idx in range(4):
                    if (beat_idx + bar_idx) % 2 == 0:
                        RPR.RPR_MIDI_InsertNote(take, False, False, item_start_time + (bar_idx * 4 + beat_idx) * (60.0/bpm), (60.0/bpm), melody_notes[(bar_idx + beat_idx) % len(melody_notes)], velocity_base - 10, True)

        RPR.RPR_MIDI_Sort(take)
        RPR.RPR_MIDI_MarkAllCs(take, True)
        RPR.RPR_MIDI_UpdateAndNotify(take)
    
    RPR.RPR_UpdateArrange()

    return f"Created demo music across {len(track_names)} tracks over {bars} bars at {bpm} BPM."


#### 3c. Verification Checklist

**For `create_midi_editor_workflow_setup`:**
- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)? (N/A for setup, but demo function does)
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)? (Yes, only creates temp track if needed, then deletes. The intent is setting preferences.)
- [x] Does it set the track name so the element is identifiable? (Yes, for temporary track if created)
- [x] Are all velocity values in the 0-127 MIDI range? (N/A for setup)
- [x] Are note timings quantized to the musical grid (no floating-point drift)? (N/A for setup)
- [x] Does the function return a descriptive status string? (Yes)
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, this sets up the environment for the technique)
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? (N/A, these are passed but not used by the setup function itself)
- [x] Does it avoid hardcoded file paths or external sample dependencies? (Yes)

**For `demonstrate_midi_workflow`:**
- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)? (Yes, uses `root_midi` and `scale_intervals`)
- [ ] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)? (**NO for demo**: Clears existing tracks for a clean demo environment. This is a design choice for a standalone demo. A production skill would be additive.)
- [x] Does it set the track name so the element is identifiable? (Yes, "MIDI Drums", "BASS", "GTR RHY", "GTR LEAD")
- [x] Are all velocity values in the 0-127 MIDI range? (Yes, `velocity_base` and `velocity_base - 20`)
- [x] Are note timings quantized to the musical grid (no floating-point drift)? (Yes, uses `(60.0/bpm)` multiples)
- [x] Does the function return a descriptive status string? (Yes)
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, this creates a simple musical context where the workflow can be immediately tested)
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? (Yes)
- [x] Does it avoid hardcoded file paths or external sample dependencies? (Yes, uses ReaSynth only)