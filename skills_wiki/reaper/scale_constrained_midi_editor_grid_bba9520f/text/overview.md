### 1. High-level Design Pattern Extraction

**Skill Name**: Scale-Constrained MIDI Editor Grid

* **Core Musical Mechanism**: This technique uses full-length, muted "guide notes" spanning multiple octaves combined with REAPER's "Hide unused note rows" action. This effectively collapses the piano roll, removing all non-diatonic keys and turning the MIDI editor into a custom, scale-locked compositional grid.
* **Why Use This Skill (Rationale)**: By removing out-of-scale notes from the visual interface, you eliminate the cognitive load of remembering scale intervals. Musically, this accelerates diatonic chord building (since stacking thirds visually becomes just "skip one visible row") and prevents accidental dissonances. It is especially useful when experimenting with symmetrical or exotic scales (like the Whole Tone scale mentioned in the video), which lack the familiar visual anchor of the standard major/minor white-and-black key layout.
* **Overall Applicability**: Perfect for rapid beatmaking, composing complex orchestral runs, writing melodies in unfamiliar modes (Dorian, Phrygian), or quickly drawing dense chord progressions without hitting "wrong" notes.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes pure music theory into the UI. It transforms the physical workspace to match the harmonic context, acting as a foolproof template for diatonic composition.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythmic constraints do not apply to the guide notes themselves; they span the entire length of the item to ensure the note rows remain "used" and visible anywhere in the clip.
  - The generated template can be any length (e.g., 4 or 8 bars).

* **Step B: Pitch & Harmony**
  - The script calculates every valid note for a chosen Root Key (e.g., C) and Scale (e.g., minor, major, whole_tone) across all 128 MIDI pitches.
  - Symmetrical scales like the Whole Tone scale (intervals: 0, 2, 4, 6, 8, 10) have an uneven, dreamy sound heavily used in film scores and jazz, which the tutorial specifically highlights.

* **Step C: Sound Design & FX**
  - No active synthesizers are required for the template itself.
  - **Crucial Technique**: The generated guide notes are explicitly set to **muted** (`muted=True`). This ensures they don't produce sound or trigger synths, acting purely as silent UI elements to hold the piano roll rows open.

* **Step D: Mix & Automation**
  - **Action Automation**: The script programmatically opens the MIDI editor and triggers Action ID `40452` ("View: Hide unused note rows") to instantly snap the visual grid into the target scale.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale interval calculation | Music theory mapping | Allows generating any scale/mode dynamically across 10 octaves. |
| Scale UI generation | `RPR_MIDI_InsertNote` with `muted=True` | Matches the tutorial's technique of using silent notes as row placeholders. |
| Collapsing the Piano Roll | `RPR_MIDIEditor_OnCommand(40452)` | Automates the exact REAPER UI action demonstrated in the video to hide non-scale rows. |

> **Feasibility Assessment**: 100% reproduction. The script fully automates the entire 4-minute tutorial workflow (calculating scale degrees, copying across octaves, muting notes, and filtering the MIDI editor view) into a single execution step.

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
    Create a Scale-Constrained MIDI Editor Grid in the current REAPER project.
    Generates muted guide notes across all octaves and collapses the piano roll
    to only show the notes in the requested scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars for the template item.
        velocity_base: Base MIDI velocity (not used audibly, as notes are muted).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]  # Featured in the tutorial
    }

    key_base = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    # We create a dedicated track for the scale guide to keep it non-destructive
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    target_track_name = f"{track_name} ({key} {scale})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", target_track_name, True)

    # === Step 3: Create MIDI Item ===
    # Calculate lengths and positions
    cursor_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Deselect all items first so we can exclusively open our new item
    RPR.RPR_SelectAllMediaItems(0, False)

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    RPR.RPR_SetMediaItemSelected(item, True)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos + item_length)

    # === Step 4: Generate Muted Scale Notes ===
    # Loop through all 10 octaves to populate the entire piano roll
    note_count = 0
    for octave in range(11):
        for interval in intervals:
            pitch = (octave * 12) + key_base + interval
            if pitch <= 127:
                # Insert note: muted=True is the key to making this a UI guide
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    True,           # MUTED (Acts as silent guide)
                    start_ppq,      # start time
                    end_ppq,        # end time (spans the whole item)
                    0,              # channel
                    pitch,          # calculated MIDI pitch
                    velocity_base,  # velocity
                    True            # noSort (we'll sort at the end)
                )
                note_count += 1

    # Sort MIDI after bulk insertion for performance
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate the MIDI Editor View ===
    # 40153: Main context - "Item: Open in built-in MIDI editor"
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Get the newly opened MIDI editor
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    
    if midi_editor:
        # Command 40452 in MIDI Editor: "View: Hide unused note rows"
        # We check the toggle state so we don't accidentally un-hide it if already active
        # 32060 is the section ID for the MIDI Editor
        state = RPR.RPR_GetToggleCommandStateEx(32060, 40452)
        if state == 0:
            RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)

    return f"Created scale guide '{target_track_name}' with {note_count} muted notes. Piano roll collapsed to diatonic rows."
```