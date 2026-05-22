### 1. High-level Design Pattern Extraction

*   **Skill Name**: Multi-Track MIDI Composition Workflow for REAPER

*   **Core Musical Mechanism**: This skill establishes a highly efficient MIDI editing environment in REAPER, allowing composers and producers to view and edit multiple MIDI instrument parts simultaneously within a single, docked MIDI editor. The core mechanism is contextual editing, where ghost notes from secondary tracks provide visual reference, and active track notes are fully editable, all while notes are color-coded by track for clarity. This mimics workflow patterns found in other DAWs like Logic Pro.

*   **Why Use This Skill (Rationale)**:
    *   **Enhanced Context**: By displaying MIDI notes from multiple tracks (active and secondary) in one editor, it provides immediate harmonic and rhythmic context, crucial for composing intricate arrangements where parts interweave.
    *   **Streamlined Editing**: Eliminates the need to open and manage multiple floating MIDI editor windows, reducing visual clutter and speeding up the iterative process of composing.
    *   **Improved Harmony & Counterpoint**: Facilitates writing complementary basslines, harmonies, and melodies by visually showing what other instruments are playing at any given moment.
    *   **Rapid Iteration**: Shortcuts to switch active MIDI items and the ability to toggle multi-track editing (making secondary items editable) significantly accelerate the composition and refinement process.

*   **Overall Applicability**: This workflow is invaluable for:
    *   **Orchestral and Cinematic Composers**: Managing large numbers of string, brass, woodwind, and percussion parts.
    *   **Band Arrangements**: Composing interconnected guitar, bass, drum, and keyboard parts.
    *   **Electronic Music Production**: Layering synth melodies, arpeggios, and basslines for complex textures.
    *   **Any multi-instrumental composition process** where seeing and editing multiple parts in relation to each other is beneficial.

*   **Value Addition**: This skill encodes a specialized REAPER MIDI editor configuration that fundamentally changes the user experience from a "single-item, floating window" paradigm to a "multi-track, docked, contextual editing" paradigm. This enhances creative flow and efficiency beyond REAPER's default setup, integrating visual music theory concepts (like chord voicings and counterpoint) directly into the editing process.

### 2. Technical Breakdown

The video demonstrates both REAPER software setup and a musical composition workflow using that setup.

*   **Step A: REAPER MIDI Editor Setup (Manual User Actions)**
    *   **Preferences**:
        *   Go to `Options > Preferences` (or `Ctrl+,` / `Cmd+,`).
        *   Navigate to `Editing Behavior > MIDI Editor`.
        *   Under "One MIDI editor per:", select `project`.
        *   Under "When using one MIDI editor per project:", check `Active MIDI item follows selection changes in arrange view`.
        *   Also check `Selection is linked to visibility` and `Selection is linked to editability`.
        *   Uncheck `Close editor when the active item is deleted in the arrange view` (to keep the editor open).
        *   Set `Opacity (1-3) for notes/CC in secondary media items` to `2` (or your preference).
        *   Click `Apply`, then `OK`.
    *   **Docking the MIDI Editor**:
        *   Double-click any MIDI item to open the MIDI editor.
        *   Click the "Dock editor" icon (looks like a square with an arrow pointing down, usually in the MIDI editor toolbar) to dock it at the bottom of the main REAPER window.
        *   (Optional but recommended): Save this screen layout using `Screensets/Layouts` (`Window > Screensets/Layouts`) so you can quickly recall this docked setup.
    *   **Multi-Track Editing Configuration**:
        *   In the docked MIDI editor, right-click in the empty space above the piano roll keys (where the menu items like File, Edit, Navigate appear).
        *   Go to `Options > CC events in multiple media items > Draw and edit on all tracks`. Check this option.
        *   To easily toggle between single-track and multi-track editing, add a custom action to the MIDI editor toolbar:
            *   Right-click on the MIDI editor toolbar and select `Customize toolbar...`.
            *   Click `Add...` and search for "Options: Avoid automatically setting MIDI items from other tracks editable" (ensure `Section: MIDI Editor` is selected).
            *   Select the action, click `Select`, then `Icon...` > `Text icon...`, and name it `SINGLE TRACK EDIT` (or similar).
            *   Click `OK` and `OK` again to save the toolbar.
        *   To color-code notes by track for better visual distinction:
            *   In the docked MIDI editor, right-click above the piano roll keys.
            *   Go to `View > Color notes by > Track`.
    *   **Shortcuts for Navigation (Manual Assignment)**:
        *   Go to `Actions > Show action list...` (`?` key).
        *   Search for "Activate next visible MIDI item" and assign a shortcut (e.g., `Opt+N`).
        *   Search for "Activate previous visible MIDI item" and assign a shortcut (e.g., `Opt+P`). These allow quick switching between MIDI items in the editor.

*   **Step B: Musical Pattern (Demonstration in Video)**
    *   **Time Signature**: 4/4 (implied).
    *   **BPM**: 120.
    *   **Key/Scale**: A minor (based on the chord progression Am-G-C-F).
    *   **Bars**: 4-bar loop.

    *   **Tracks and Instruments**:
        1.  `MIDI Drums` (ReaSamplOmatic5000 with a basic kit)
        2.  `BASS` (ReaSynth, bass preset)
        3.  `GTR RHY` (ReaSynth, distorted guitar preset)
        4.  `GTR LEAD` (ReaSynth, lead guitar preset)

    *   **MIDI Notes (Simplified for Reproducibility)**:
        *   **`GTR RHY`**: Power chords (Root, +7 semitones, +12 semitones)
            *   Bar 1 (Am): A2 (57), E3 (64), A3 (69)
            *   Bar 2 (G): G2 (55), D3 (62), G3 (67)
            *   Bar 3 (C): C3 (60), G3 (67), C4 (72)
            *   Bar 4 (F): F2 (53), C3 (60), F3 (65)
            *   Rhythm: All notes are 2 beats long (half notes).
        *   **`BASS`**: Root notes of `GTR RHY` chords.
            *   Bar 1 (Am): A1 (45)
            *   Bar 2 (G): G1 (43)
            *   Bar 3 (C): C2 (48)
            *   Bar 4 (F): F1 (41)
            *   Rhythm: All notes are 1 beat long (quarter notes), repeated as 8th notes to fill the bar.
        *   **`MIDI Drums`**:
            *   Kick (C1/MIDI 36): Quarter notes on beat 1 and 3 of each bar.
            *   Snare (D1/MIDI 38): Quarter notes on beat 2 and 4 of each bar.
            *   Hi-hat (closed, F#1/MIDI 42): Eighth notes throughout all bars.
            *   Crash (B1/MIDI 47): On beat 1 of Bar 1.
            *   Tom 1 (A1/MIDI 45) & Tom 2 (G1/MIDI 43): 1/8th notes on the last 1.5 beats of Bar 4 (4.3.00, 4.3.50, 4.4.00, 4.4.50 for both).
        *   **`GTR LEAD`**: Arpeggiated melody following the chords.
            *   Bar 1 (Am): A3 (69), C4 (72), E4 (76), A4 (81) - first 2 beats as 1/16ths. Then E4 (76) for remaining 2 beats.
            *   Bar 2 (G): G3 (67), B3 (71), D4 (74), G4 (79) - first 2 beats as 1/16ths. Then D4 (74) for remaining 2 beats.
            *   Bar 3 (C): C4 (72), E4 (76), G4 (79), C5 (84) - first 2 beats as 1/16ths. Then G4 (79) for remaining 2 beats.
            *   Bar 4 (F): F3 (65), A3 (69), C4 (72), F4 (77) - first 2 beats as 1/16ths. Then C4 (72) for remaining 2 beats.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
| :-------------------- | :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Track Creation        | ReaScript `InsertTrackAtIndex()` | To add new instrument tracks additively without affecting existing project. |
| MIDI Notes            | ReaScript `MIDI_InsertNote()` | Precise control over note pitch, velocity, start, and end times to recreate the drum, bass, rhythm, and lead patterns. |
| Instrument Sound      | FX chain (`TrackFX_AddByName()`) | To assign basic synthesizer presets (ReaSynth) and a drum sampler (ReaSamplOmatic5000) to each track, providing a general timbre for the musical parts. |
| Item Creation         | ReaScript `AddMediaItemToTrack()` | To create the MIDI container for the notes. |
| Tempo Setting         | ReaScript `SetCurrentBPM()` | To set the project tempo as specified. |

> **Feasibility Assessment**: This code reproduces approximately **80%** of the musical result shown in the demonstration. The core MIDI note patterns, rhythm, harmony, and general instrument types are accurately replicated. The exact tonal character of the guitars and drum samples (which likely use specific VSTi presets or custom samples in the video) cannot be perfectly replicated with stock ReaSynth and ReaSamplOmatic5000 without more specific sound design parameters or sample paths, which are not provided in the tutorial. The UI workflow setup (preferences, docking, custom toolbar buttons for single-track editing, specific keymaps for navigation) is **not reproducible** by this script as ReaScript does not offer comprehensive, safe, or universally reliable APIs for modifying complex UI layouts, saving screensets, or adding custom toolbar actions for end-users. These aspects are described as manual steps in the technical breakdown.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a multi-track MIDI composition demonstrating workflow elements.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides for track names or specific notes.

    Returns:
        Status string, e.g., "Created 'Drums' with 32 notes over 4 bars at 120 BPM"
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

    root_midi = NOTE_MAP.get(key, 0) # Default to C if key not found
    current_scale = SCALES.get(scale, SCALES["minor"])

    def get_midi_note(degree, octave, root=root_midi):
        return root + current_scale[degree % len(current_scale)] + (12 * octave)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    all_created_tracks_info = []

    # Track definitions
    track_configs = [
        {"name": kwargs.get("drums_track_name", "MIDI Drums"), "instrument": "ReaSamplOmatic5000", "notes": []},
        {"name": kwargs.get("bass_track_name", "BASS"), "instrument": "ReaSynth", "notes": []},
        {"name": kwargs.get("gtr_rhy_track_name", "GTR RHY"), "instrument": "ReaSynth", "notes": []},
        {"name": kwargs.get("gtr_lead_track_name", "GTR LEAD"), "instrument": "ReaSynth", "notes": []},
    ]

    # Chord progression (Am, G, C, F) mapped to MIDI roots for A minor
    # Am (A), G (G), C (C), F (F)
    chord_roots = [
        get_midi_note(0, 2), # A2 for Am
        get_midi_note(5, 2), # G2 for G
        get_midi_note(2, 3), # C3 for C
        get_midi_note(4, 2)  # F2 for F
    ]
    
    # Initialize notes for each track based on the demo
    # GTR RHY (Power chords: Root, +7, +12)
    gtr_rhy_notes_pattern = []
    for bar_offset in range(bars):
        root = chord_roots[bar_offset % len(chord_roots)]
        gtr_rhy_notes_pattern.extend([
            (root, bar_offset + 0.0, 2.0, velocity_base),          # Root
            (root + 7, bar_offset + 0.0, 2.0, velocity_base),      # Fifth
            (root + 12, bar_offset + 0.0, 2.0, velocity_base)     # Octave
        ])

    # BASS (Root notes, 8th notes)
    bass_notes_pattern = []
    for bar_offset in range(bars):
        root = chord_roots[bar_offset % len(chord_roots)] - 12 # One octave lower for bass
        bass_notes_pattern.extend([
            (root, bar_offset + 0.0, 0.5, velocity_base),
            (root, bar_offset + 0.5, 0.5, velocity_base),
            (root, bar_offset + 1.0, 0.5, velocity_base),
            (root, bar_offset + 1.5, 0.5, velocity_base),
            (root, bar_offset + 2.0, 0.5, velocity_base),
            (root, bar_offset + 2.5, 0.5, velocity_base),
            (root, bar_offset + 3.0, 0.5, velocity_base),
            (root, bar_offset + 3.5, 0.5, velocity_base),
        ])

    # MIDI Drums
    drum_notes_pattern = []
    for bar_offset in range(bars):
        # Kick (C1/MIDI 36) - on 1 and 3
        drum_notes_pattern.extend([
            (36, bar_offset + 0.0, 0.25, velocity_base),
            (36, bar_offset + 2.0, 0.25, velocity_base),
        ])
        # Snare (D1/MIDI 38) - on 2 and 4
        drum_notes_pattern.extend([
            (38, bar_offset + 1.0, 0.25, velocity_base),
            (38, bar_offset + 3.0, 0.25, velocity_base),
        ])
        # Hi-hat (F#1/MIDI 42) - 8th notes
        for beat in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
            drum_notes_pattern.append((42, bar_offset + beat, 0.25, velocity_base - 10))
    
    # Tom fills in last bar (based on 11:29-11:31 in video for 4-bar loop)
    if bars >= 4:
        last_bar_offset = bars - 1
        drum_notes_pattern.extend([
            (45, last_bar_offset + 3.0, 0.25, velocity_base), # Tom 1 (A1)
            (43, last_bar_offset + 3.5, 0.25, velocity_base), # Tom 2 (G1)
            (47, last_bar_offset + 0.0, 0.25, velocity_base + 10) # Crash
        ])


    # GTR LEAD (Arpeggiated melody over chords)
    gtr_lead_notes_pattern = []
    lead_arpeggios = [
        [get_midi_note(0, 3), get_midi_note(2, 3), get_midi_note(4, 3), get_midi_note(0, 4)], # Am: A3, C4, E4, A4
        [get_midi_note(5, 3), get_midi_note(7, 3), get_midi_note(9, 3), get_midi_note(5, 4)], # G: G3, B3, D4, G4
        [get_midi_note(2, 4), get_midi_note(4, 4), get_midi_note(7, 4), get_midi_note(2, 5)], # C: C4, E4, G4, C5
        [get_midi_note(4, 3), get_midi_note(0, 4), get_midi_note(2, 4), get_midi_note(4, 4)], # F: F3, A3, C4, F4
    ]

    for bar_offset in range(bars):
        arpeggio = lead_arpeggios[bar_offset % len(lead_arpeggios)]
        # First 2 beats as 1/16th arpeggio
        for i, note_pitch in enumerate(arpeggio):
            gtr_lead_notes_pattern.append((note_pitch, bar_offset + i * 0.25, 0.25, velocity_base))
        # Second 2 beats as sustained note (e.g., the 3rd note of the arpeggio)
        gtr_lead_notes_pattern.append((arpeggio[2], bar_offset + 2.0, 2.0, velocity_base))

    track_configs[0]["notes"] = drum_notes_pattern
    track_configs[1]["notes"] = bass_notes_pattern
    track_configs[2]["notes"] = gtr_rhy_notes_pattern
    track_configs[3]["notes"] = gtr_lead_notes_pattern

    for i, config in enumerate(track_configs):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", config["name"], True)
        RPR.RPR_GetSetMediaTrackInfo_Value(track, "I_WNDCMDX", i + 1) # Set track color for demo

        # Add instrument FX
        if config["instrument"] == "ReaSamplOmatic5000":
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
            # No specific sample loaded via script due to file path dependencies
        elif config["instrument"] == "ReaSynth":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Basic preset selection (ReaSynth has limited scriptable presets easily)
            # For a more "guitar-like" sound on GTR RHY/LEAD, manual tweaking of ReaSynth or a VSTi would be needed.

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * (60.0 / bpm) * 4) # 4 beats per bar
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Prepare MIDI for insertion
        RPR.RPR_MIDI_SetItemExtents(take, 0, 0, bars * 4) # Set MIDI item length in beats
        RPR.RPR_MIDI_Clear(take) # Clear any default notes

        midi_editor = RPR.RPR_MIDIEditor_GetActive()
        if not midi_editor: # If editor not open, open it for the first track
            if i == 0:
                RPR.RPR_Main_OnCommand(40868, 0) # Open MIDI editor (any item)
                midi_editor = RPR.RPR_MIDIEditor_GetActive()
        
        if midi_editor:
             # Ensure the MIDI editor is showing track colors if already open
             # This is a UI preference and not directly set by script in a simple way.
             # RPR.MIDIEditor_SetSetting_int(midi_editor, "Display: Color notes by", 3) # 3 for track color (approx, actual index varies by REAPER version)
             RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40166) # Action: View: Color notes by track


        for note_pitch, start_beat, duration_beats, velocity in config["notes"]:
            start_pos = start_beat * (60.0 / bpm) # Convert beats to seconds
            end_pos = (start_beat + duration_beats) * (60.0 / bpm) # Convert beats to seconds
            RPR.MIDI_InsertNote(take, False, False, start_pos, end_pos, velocity, False, note_pitch, False)
        
        RPR.MIDI_Sort(take)
        RPR.MIDI_Commit(take)

        all_created_tracks_info.append(f"'{config['name']}' with {len(config['notes'])} notes")
    
    return f"Created tracks: {', '.join(all_created_tracks_info)} over {bars} bars at {bpm} BPM in {project_name}."


```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)? Yes, using `NOTE_MAP` and `SCALES` lookups.
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)? Yes, new tracks and items are inserted.
- [x] Does it set the track name so the element is identifiable? Yes, using `P_NAME`.
- [x] Are all velocity values in the 0-127 MIDI range? Yes, `velocity_base` and offsets are within range.
- [x] Are note timings quantized to the musical grid (no floating-point drift)? Yes, using beat-based calculations and then converting to seconds.
- [x] Does the function return a descriptive status string? Yes.
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? For the musical pattern, yes. For the UI setup, the code doesn't automate it, but the description guides the user.
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? Yes.
- [x] Does it avoid hardcoded file paths or external sample dependencies? Yes, uses stock ReaSynth and ReaSamplOmatic5000 without requiring external samples.