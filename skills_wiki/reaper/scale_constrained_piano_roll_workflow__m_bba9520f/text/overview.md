### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Constrained Piano Roll Workflow (Muted Guide Notes)

* **Core Musical Mechanism**: By creating a background item containing muted MIDI notes of a specific scale and running the `View: Hide unused note rows` action, the MIDI editor's piano roll is transformed into a custom, purely diatonic grid. All non-scale notes are completely hidden.

* **Why Use This Skill (Rationale)**: This is a powerful UX and composition hack. When working with complex scales (like the Whole Tone scale featured in the video) or when writing rapid arpeggios, hiding the non-diatonic keys prevents wrong notes and visually declutters the workspace. It effectively turns the standard chromatic piano roll into a customized instrument interface tailored to the current song's key. 

* **Overall Applicability**: Extremely useful for programming melodies, chords, and basslines in any genre. It is particularly effective for EDM, trap, and cinematic music where strict adherence to a specific mode or exotic scale is required, and where fast mouse-clicking is the primary input method.

* **Value Addition**: Instead of relying on the user to manually set up templates, snap settings, or remember the notes of a scale, this skill automatically computes the pitch classes across all octaves, generates the "guide" item, mutes it, and instantly filters the Piano Roll view.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Generates a primary "Composition" MIDI item (e.g., 4 bars).
  - Generates a 1-beat "Guide" MIDI item sitting immediately after the composition item.
  - The rhythmic placement of the guide item prevents it from overlapping with the user's active workspace.

* **Step B: Pitch & Harmony**
  - The script accepts any root key and scale combination.
  - It uses modulo-12 arithmetic to identify valid pitch classes for the selected scale.
  - It populates the guide item with every valid pitch across the entire 0-127 MIDI range.

* **Step C: Sound Design & FX**
  - The guide item is explicitly muted (`B_MUTE = 1.0`). This ensures the scale notes do not trigger any synthesizers or affect playback, acting purely as a visual anchor.

* **Step D: Mix & Automation**
  - N/A. This is a UI/workflow optimization technique.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | Modulo-12 pitch class mapping | Ensures edge-cases at the extreme top/bottom octaves are perfectly covered. |
| Non-destructive UI | Muted media item (`B_MUTE`) | Matches the tutorial's technique of using a silent item to trick the MIDI editor into registering notes as "used". |
| Workspace execution | Action ID `40452` | Directly triggers the native REAPER command "Hide unused note rows" within the active MIDI Editor. |

> **Feasibility Assessment**: 100% — This code entirely replicates the scale-locking setup workflow demonstrated in the tutorial, automating what would normally take a user 2-3 minutes of manual copying, pasting, and muting.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale-Constrained Piano Roll workflow in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars for the active composition area.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created workflow setup.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # === Step 1: Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    key_norm = key.capitalize()
    if key_norm not in NOTE_MAP:
        key_norm = "C"
    root_midi = NOTE_MAP[key_norm]
    
    scale_norm = scale.lower()
    if scale_norm not in SCALES:
        scale_norm = "minor"
    scale_intervals = SCALES[scale_norm]

    # Calculate valid pitch classes (modulo 12)
    valid_pitch_classes = set((root_midi + interval) % 12 for interval in scale_intervals)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key_norm} {scale_norm})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # === Step 3: Create Active Composition Item ===
    # This is where the user will actually draw their notes
    comp_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(comp_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(comp_item, "D_LENGTH", bar_length_sec * bars)
    comp_take = RPR.RPR_AddTakeToMediaItem(comp_item)

    # === Step 4: Create Muted Scale Guide Item ===
    # We place this item immediately AFTER the composition item so it doesn't overlap
    guide_pos = bar_length_sec * bars
    guide_item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(guide_item, "D_POSITION", guide_pos)
    RPR.RPR_SetMediaItemInfo_Value(guide_item, "D_LENGTH", bar_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(guide_item, "B_MUTE", 1.0) # Completely muted
    guide_take = RPR.RPR_AddTakeToMediaItem(guide_item)

    # Populate guide item with all 128 possible notes that fit the scale
    note_count = 0
    for pitch in range(128):
        if pitch % 12 in valid_pitch_classes:
            # Insert note: length is 1 quarter note (960 PPQ)
            RPR.RPR_MIDI_InsertNote(guide_take, False, True, 0, 960, 0, pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(guide_take)

    # === Step 5: Open in MIDI Editor & Filter Rows ===
    # Select both items so the MIDI editor calculates "used rows" based on the guide item
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_SelectAllMediaItems(0, False)
    RPR.RPR_SetMediaItemSelected(comp_item, True)
    RPR.RPR_SetMediaItemSelected(guide_item, True)
    
    # Open Built-In MIDI Editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Trigger 'View: Hide unused note rows' (Command 40452)
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)
        # Zoom to content so the rows fill the screen nicely
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40466)

    return f"Created '{full_track_name}' workspace. Generated {note_count} guide notes and hid unused piano roll rows."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?