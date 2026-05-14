### 1. High-level Design Pattern Extraction

> **Skill Name**: Auto-Generate Scale Guide & Restrict Piano Roll

* **Core Musical Mechanism**: The tutorial demonstrates a workflow technique rather than a specific song pattern: constraining the REAPER MIDI Editor to *only* display rows for notes that belong to a specific scale. This is achieved by populating a MIDI item with the desired scale's notes across all octaves, and then triggering the `Hide unused note rows` action. 

* **Why Use This Skill (Rationale)**: This technique creates a "diatonic sandbox." By collapsing the piano roll to only show notes in your target scale (e.g., G Major, C Dorian, or Whole Tone), it becomes visually impossible to click a wrong note. This is incredibly useful for producers who do not have extensive music theory knowledge, or when composing fast, complex arpeggios and melodies where visual clutter slows down the workflow. 

* **Overall Applicability**: This skill shines when starting a new project or section. Instead of maintaining a folder of "MIDI scale templates" (as suggested in the video), this code programmatically generates the requested scale across all octaves on the fly, mutes the notes (so they don't interfere with audio), and automatically restricts the MIDI editor view.

* **Value Addition**: Compared to a blank MIDI clip, this script mathematically calculates all notes in a given mode/scale across the entire 128-note MIDI spectrum, builds the scaffolding, and executes REAPER UI commands to transform the Piano Roll into a custom-tailored interface for that specific musical key.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Duration**: The notes span the entire duration of the generated item (default 1 bar).
  - **Velocity/Playback**: The notes are explicitly created as **muted** (`muted=True`). This ensures they serve purely as a structural UI guide and will not trigger VST synths if the user drops an instrument onto the track.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Accepts standard root notes (C, C#, D...) and extrapolates scales based on interval mappings (Major, Minor, Dorian, Whole Tone, Pentatonics).
  - **Octave Spanning**: The pattern loops the scale intervals from MIDI note 0 to 127 to cover every playable octave.

* **Step C: Sound Design & FX**
  - **Instrument**: None required. This is a MIDI/UI structural setup.

* **Step D: Mix & Automation**
  - **UI Automation**: Uses REAPER's Action API to unselect other items, open the newly created scale guide in the active MIDI Editor (`Command 40153`), and trigger the MIDI Editor action "View: Hide unused note rows" (`Command 40454`).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | Python Dictionary & MIDI Math | Automatically calculates correct pitches without needing manual entry or external files. |
| Note population | `RPR_MIDI_InsertNote` | Precise programmatic placement of muted notes across octaves 0-10. |
| Restricting the Piano Roll | `RPR_MIDIEditor_OnCommand` | Directly triggers the REAPER action shown in the video (`40454: Hide unused note rows`). |

> **Feasibility Assessment**: 100%. The script perfectly automates the entire 4-minute manual process shown in the video into a single, parametric function call, resulting in an instantly restricted piano roll for any chosen key and scale.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "G",
    scale: str = "major",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Scale Guide' track that auto-restricts the MIDI Piano Roll
    to only show notes from the selected key and scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, pentatonic_minor, etc.).
        bars: Number of bars to generate for the guide block.
        velocity_base: Base MIDI velocity (0-127). Not highly relevant as notes are muted.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]  # Specifically highlighted in tutorial
    }

    # Normalize inputs
    key_upper = key.upper()
    root_pitch = NOTE_MAP.get(key_upper, 0)
    scale_lower = scale.lower()
    intervals = SCALES.get(scale_lower, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{key_upper} {scale_lower.capitalize()} Guide", True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Convert start and end to PPQ
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Populate Scale Notes Across All Octaves ===
    note_count = 0
    # MIDI ranges from 0 to 127
    for oct_multiplier in range(-1, 10):
        for interval in intervals:
            pitch = (oct_multiplier * 12) + root_pitch + interval
            if 0 <= pitch <= 127:
                # Insert note: muted=True so it acts purely as a UI layout map
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate MIDI Editor UI commands ===
    # Unselect all items in the project first to ensure we open only our new item
    RPR.RPR_Main_OnCommand(40289, 0) 
    
    # Select our new item
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Get active MIDI editor pointer and run 'Hide unused note rows' (ID: 40454)
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40454)

    return f"Created guide track for {key_upper} {scale_lower} with {note_count} muted notes. MIDI Editor restricted to scale rows."
```