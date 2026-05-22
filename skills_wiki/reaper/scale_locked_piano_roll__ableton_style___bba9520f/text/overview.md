### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Locked Piano Roll (Ableton-Style "Fold")

* **Core Musical Mechanism**: This technique forces the REAPER MIDI Editor to exclusively display notes that belong to a specific musical scale. By generating a "guide" MIDI item containing all the valid notes across multiple octaves, muting it, and triggering the "Hide unused note rows" action, the piano roll "folds" into a custom diatonic (or exotic) grid where wrong notes physically cannot be clicked.

* **Why Use This Skill (Rationale)**: This workflow hack effectively turns REAPER into an isomorphic keyboard/grid. It removes the mental friction of remembering scale formulas (like Whole Tone, Harmonic Minor, or Dorian) during composition. By collapsing the visual grid to only the in-scale notes, producers can easily draw complex extended chords, fast arpeggios, and melodic runs without accidentally placing out-of-key dissonances. 

* **Overall Applicability**: Essential for rapid MIDI sequencing, creating complex diatonic chord progressions, writing fast trap/EDM melodies, or experimenting with unfamiliar scales (like the Whole Tone scale used for "dreamy, flashback" sequences as noted in the tutorial).

* **Value Addition**: Instead of manually clicking notes and duplicating them up octaves as shown in the video, this encoded skill instantly generates the mathematical scale lattice and automatically folds the MIDI editor UI in one action.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Rhythm**: Rhythm is irrelevant for the "guide" item. We simply place all scale notes at the very beginning of the item (`0` PPQ to `960` PPQ).
  - **Playback**: The generated MIDI item is hard-muted so it does not trigger any synthesizers or interfere with the actual composition.

* **Step B: Pitch & Harmony**
  - **Scale Logic**: Notes are calculated using a base MIDI note (e.g., C = 0) plus the intervals of the selected scale, repeated across all visible octaves (octaves 1 through 7).
  - **Tutorial Specifics**: The tutorial specifically demonstrates the G Major scale and the C Whole Tone scale.

* **Step C: Sound Design & FX**
  - No audio FX are used. This is purely a MIDI workspace/UI configuration technique.

* **Step D: Mix & Automation (if applicable)**
  - The item's `B_MUTE` value is set to `1.0` (Muted) so the guide notes never reach the audio engine.
  - The script automates REAPER's UI by opening the item in the built-in MIDI editor (Command `40153`) and immediately firing "View: Hide unused note rows" (Command `40452`).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale Note Generation | MIDI note insertion | Generates the structural guide notes needed for the UI hack across 7 octaves. |
| Non-destructive playback | Item Property (`B_MUTE`) | Mutes the item so the guide notes don't trigger the track's virtual instruments. |
| "Fold" effect | MIDI Editor Command automation | Programmatically triggers "Hide unused note rows" (`40452`) exactly as demonstrated in the tutorial. |

> **Feasibility Assessment**: 100% reproducible. The script bypasses the manual drawing shown in the video and goes straight to generating the guide item and collapsing the piano roll.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a muted "Scale Guide" MIDI item and folds the MIDI editor to show 
    only the notes in the chosen scale (Ableton-style "Fold").

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created guide track.
    """
    import reaper_python as RPR

    # Music theory lookup tables
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Highlighted in tutorial
    }

    # Validate inputs
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name track descriptively so the user knows what scale grid is locked
    full_track_name = f"{track_name} ({key} {scale})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 2: Create MIDI Item ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Mute the item so it functions strictly as a UI guide, not as playable audio
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Populate Guide Notes (Octaves 1 to 7) ===
    start_ppq = 0.0
    end_ppq = 960.0 # 1 quarter note length is enough to register in the UI
    note_count = 0

    for octave in range(1, 8):
        base_midi = (octave * 12) + root_val
        for interval in scale_intervals:
            pitch = base_midi + interval
            if pitch <= 127:
                # Insert notes (muted=True as an extra precaution)
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, False)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Fold the MIDI Editor ===
    # Deselect all items first, then select our guide item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open selected item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Get active MIDI editor pointer and trigger the "Hide unused note rows" action
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        RPR.RPR_MIDIEditor_OnCommand(editor, 40452) # View: Hide unused note rows

    return f"Created scale guide for {key} {scale} ({note_count} guide notes). MIDI Editor folded to scale."
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