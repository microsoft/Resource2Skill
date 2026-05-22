### 1. High-level Design Pattern Extraction

> **Skill Name**: MIDI Piano Roll Scale Guide (Hide Non-Scale Notes)

* **Core Musical Mechanism**: Generating a background "scaffold" of muted MIDI notes that cover all octaves of a specific musical scale. By combining this with REAPER's "Hide unused note rows" action, the Piano Roll is dynamically restricted to display *only* the notes that belong to the chosen scale.
* **Why Use This Skill (Rationale)**: This is an incredibly powerful workflow hack for diatonic composition. By hiding all non-scale notes, you remove the visual clutter of the chromatic scale and make it impossible to accidentally click "wrong" or out-of-key notes. This accelerates the process of drawing chords, writing melodies, and programming arpeggios, while still leaving you free to change the key later.
* **Overall Applicability**: Useful for any genre relying heavily on the MIDI piano roll (EDM, Trap, Pop, Lo-Fi, Orchestral mockups). It is especially useful for quickly visualizing advanced or exotic scales (like the Whole Tone scale demonstrated in the video) without having to memorize their intervals across the keyboard.
* **Value Addition**: Compared to an empty MIDI clip, this skill automatically calculates the intervals for your requested key and scale across 7 octaves, injects them as muted "ghost" notes, and triggers the UI action to collapse the piano roll—instantly preparing your environment for in-scale writing.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - A single 1-bar item is generated.
  - The notes stretch across the entire bar to ensure they are present anywhere you might start clicking.
* **Step B: Pitch & Harmony**
  - A lookup table resolves the root note (e.g., C, D#) to a MIDI value.
  - A scale dictionary defines the intervals (Major, Minor, Dorian, Whole Tone, etc.).
  - A loop iterates through octaves 1 to 7, applying the intervals to the root note and inserting them into the item.
* **Step C: Sound Design & FX**
  - **Crucial step:** All generated notes are set to `muted=True`. This ensures the guide notes never trigger an instrument or make a sound, acting purely as visual UI anchors.
* **Step D: Mix & Automation**
  - The script uses ReaScript API commands to open the MIDI Editor and fire Action ID `40452` ("View: Hide unused note rows"), collapsing the visual grid.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale note generation | `RPR_MIDI_InsertNote()` | Allows mathematically perfect generation of any scale across all octaves. |
| Ghost note behavior | `muted=True` argument | The 3rd parameter of `RPR_MIDI_InsertNote` is `muted`. Setting it to `True` prevents the notes from making sound, matching the tutorial's technique. |
| Visual grid collapsing | `RPR_MIDIEditor_OnCommand()` | Programmatically triggers the exact "Hide unused note rows" action the video demonstrates. |

> **Feasibility Assessment**: 100% reproducible. The script fully automates the manual 4-step process shown in the video, dynamically adapting to the key and scale parameters provided.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 'Scale Guide' MIDI item populated with muted notes across 7 octaves,
    then opens the MIDI editor and hides all unused note rows, restricting the grid
    to only diatonic notes.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars for the guide item (usually 1 is enough).
        velocity_base: Base MIDI velocity (irrelevant here as notes are muted).
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
        "whole_tone":       [0, 2, 4, 6, 8, 10] # Highlighted in the tutorial
    }

    root_pitch = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale, SCALES["major"])
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    final_track_name = f"{key} {scale.capitalize()} Guide"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", final_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate MIDI ticks (PPQ) for the notes
    start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    end_qn = RPR.RPR_TimeMap2_timeToQN(0, item_length)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # === Step 4: Generate Muted Scale Notes ===
    note_count = 0
    # Loop across 7 octaves to provide a full-range guide
    for octave in range(1, 8):
        base_midi = (octave + 1) * 12 + root_pitch 
        for interval in intervals:
            pitch = base_midi + interval
            if pitch <= 127:
                # InsertNote parameters: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, 64, True)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate UI to Hide Unused Rows ===
    # Unselect all items first to ensure we only open our new item
    RPR.RPR_Main_OnCommand(40289, 0) 
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "View: Hide unused note rows" (Action ID 40452) in the MIDI editor
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)

    return f"Created '{final_track_name}' with {note_count} muted ghost notes. MIDI editor grid collapsed to scale."
```