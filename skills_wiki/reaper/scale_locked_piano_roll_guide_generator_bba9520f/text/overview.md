### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Locked Piano Roll Guide Generator

* **Core Musical Mechanism**: Constraining the MIDI editor's piano roll display to *only* show the diatonic notes of a specific scale (e.g., C Minor, G Whole Tone), hiding all out-of-scale rows. 
* **Why Use This Skill (Rationale)**: By visualizing only the valid notes within a chosen scale, the producer completely eliminates the possibility of drawing "wrong" notes. It removes the cognitive load of remembering key signatures or visualizing scale formulas, speeding up the composition of complex melodies and dense chord progressions.
* **Overall Applicability**: Essential for songwriting, melody creation, and programming dense MIDI (orchestral, EDM, jazz) where strictly adhering to a scale or specific mode is desired. It's particularly useful for newer producers learning music theory.
* **Value Addition**: In the tutorial, the instructor manually finds the root note, duplicates it diatonically, copies it across all octaves, saves it as a template file, imports the file, and then triggers the "Hide unused note rows" action. This script proceduralizes that entire workflow—instantly generating a muted background track populated with all notes of the requested key/scale, and automatically configuring the MIDI Editor to hide non-scale rows.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: The notes span the entire requested duration of the generated item (e.g., a solid block spanning 4 bars) so they are persistently visible as a background scaffolding.
* **Step B: Pitch & Harmony**
  - **Key & Scale**: Takes user parameters (e.g., "C", "minor") and mathematically generates every diatonic interval across the entire MIDI spectrum (octaves 0 to 10, pitches 0-127).
  - **Supported Scales**: Major, Minor, Harmonic Minor, Dorian, Mixolydian, Pentatonics, Blues, and the Whole Tone scale (which was explicitly highlighted as a bonus tip in the video).
* **Step C: Sound Design & FX**
  - **Silent Scaffolding**: No audio is produced. The generated track is explicitly muted. It serves purely as a structural visual guide for the REAPER MIDI Editor.
* **Step D: Mix & Automation**
  - The script utilizes REAPER's GUI automation `RPR_MIDIEditor_OnCommand(editor, 40452)` to programmatically trigger the "View: Hide unused note rows" action once the notes are generated.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Procedural Scale Generation | `RPR_MIDI_InsertNote` with Theory tables | Matches the video's requirement to have MIDI items containing all octaves of a scale. |
| Non-destructive Guide | `RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1)` | Prevents the guide notes from accidentally triggering VSTs while still acting as a visual anchor. |
| Piano Roll Modification | `RPR_MIDIEditor_OnCommand(40452)` | Directly reproduces the tutorial's core hack: triggering the "Hide unused note rows" action automatically. |

> **Feasibility Assessment**: 100% reproduction. The code completely automates the tedious manual setup shown in the video, delivering the exact "scale-locked" piano roll state.

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
    Create a Scale-Locked Piano Roll Guide Generator in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate for the guide block.
        velocity_base: Base MIDI velocity for guide notes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the scale guide track.
    """
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key.upper()} {scale.capitalize()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Mute track so guide notes never output audio
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create Background MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate valid pitches across all MIDI octaves (0-127)
    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    valid_pitches = []
    for oct in range(11):
        for interval in scale_intervals:
            pitch = root_val + interval + (oct * 12)
            if 0 <= pitch <= 127:
                valid_pitches.append(pitch)

    start_qn = 0.0
    end_qn = bars * beats_per_bar
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # Draw continuous guide notes covering the item length
    for pitch in valid_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: UI Actions (Open MIDI Editor & Hide Unused Rows) ===
    # Isolate selection to the newly generated item
    RPR.RPR_SelectAllMediaItems(0, False)
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Retrieve active MIDI editor window and trigger "Hide unused note rows"
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        RPR.RPR_MIDIEditor_OnCommand(editor, 40452)

    return f"Created '{full_track_name}' guide track containing {len(valid_pitches)} mapped pitches over {bars} bars. Piano roll successfully locked to scale."
```