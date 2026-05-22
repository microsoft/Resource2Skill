### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Restricted Piano Roll Canvas (MIDI "Fold" Setup)

* **Core Musical Mechanism**: Diatonic/Scale Restriction. This pattern automates the creation of a muted "guide item" containing every note of a specific scale across multiple octaves. By opening this item and applying REAPER's "Hide unused note rows" action, the piano roll "folds" to display *only* the notes in that scale, hiding out-of-key pitches entirely.

* **Why Use This Skill (Rationale)**: From a music theory and workflow perspective, visualizing only the in-scale notes drastically reduces cognitive load. It prevents accidental dissonances, makes diatonic chord building (stacking thirds) visually immediate (just skip every other visible row), and encourages rapid melodic exploration. It is especially powerful for symmetric or non-traditional scales (like the Whole Tone scale highlighted in the tutorial) where the standard piano layout is counter-intuitive. 

* **Overall Applicability**: Useful at the start of any composition or beat-making session, particularly when writing complex MIDI sequences (arpeggios, dense chord voicings, or rapid lead lines) in unfamiliar keys or modes. 

* **Value Addition**: Compared to an empty MIDI clip where all 128 chromatic notes are visible, this skill programmatically encodes music theory (scale interval formulas) into the visual grid itself. It turns REAPER's default chromatic piano roll into a custom, scale-locked isomorphic layout.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: The notes themselves span the entire duration of the generated item (e.g., 4 bars) to ensure they dictate the rows for the whole length of the clip.
  - **Rhythm**: No rhythm is applied to the guide notes. They are purely structural.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Dynamic based on input parameters (Major, Minor, Dorian, Whole Tone, etc.).
  - **Voicing**: 100% dense clusters. Every diatonic pitch from octave 1 through 8 is generated simultaneously. 
  - **Playback**: The notes are placed inside an item that is explicitly **muted**, ensuring they do not produce any sound when playback occurs.

* **Step C: Sound Design & FX**
  - Not applicable to the sound design itself, as the item is muted. It serves exclusively as a GUI layout modifier.

* **Step D: Mix & Automation**
  - No mixing routing is required. 
  - **UI Automation**: The technique relies on specific REAPER Actions (`40153`: Open in built-in MIDI editor; and MIDI Editor Action `40453`: View: Hide unused note rows).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Generating the Scale** | MIDI note insertion | Requires precise insertion of pitches across 8 octaves using scale interval math. |
| **Silencing the Guide** | Item manipulation (`B_MUTE`) | Muting the item ensures the guide notes don't trigger the instrument, exactly as demonstrated in the video. |
| **Folding the Grid** | UI Action (`RPR_MIDIEditor_OnCommand`) | The only way to achieve the visual "scale lock" is by triggering REAPER's native "Hide unused note rows" action within the active MIDI editor. |

> **Feasibility Assessment**: 100% reproduction. The code completely automates the manual 4-step process shown in the video (creating notes, copying across octaves, muting the item, and triggering the hide action).

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
    Create Scale-Restricted Piano Roll Canvas in the current REAPER project.

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
        Status string describing the creation of the scale canvas.
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
    root_offset = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key} {scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create Media Item & Take ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # Mute the item so it acts purely as a visual GUI guide (as shown in tutorial)
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert Notes for Grid Population ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    note_count = 0
    # Generate scale notes across octaves 1 through 8
    for octave in range(1, 9):
        octave_base = 12 * octave
        for interval in scale_intervals:
            midi_pitch = octave_base + root_offset + interval
            if midi_pitch <= 127:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate MIDI Editor Layout ===
    # Unselect all items globally, then select ONLY our guide item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open selected item in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "Hide unused note rows" within the active MIDI editor
    hwnd = RPR.RPR_MIDIEditor_GetActive()
    if hwnd:
        RPR.RPR_MIDIEditor_OnCommand(hwnd, 40453) # View: Hide unused note rows

    return f"Created '{full_track_name}' with {note_count} scale notes over {bars} bars. MIDI Editor folded to scale."
```