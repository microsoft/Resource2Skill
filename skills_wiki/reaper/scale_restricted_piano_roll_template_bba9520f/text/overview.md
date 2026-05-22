### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Restricted Piano Roll Template

* **Core Musical Mechanism**: Transforming the REAPER MIDI Editor into a custom scale-grid by inserting muted guide notes across the entire octaval range (0-127) and triggering the "View: Hide unused note rows" action. This entirely removes out-of-key note rows from the visual piano roll.
* **Why Use This Skill (Rationale)**: While REAPER has a native "Key Snap" feature (which grays out non-scale notes), it doesn't fundamentally change the piano roll's geometry. For complex or non-traditional scales (like the Whole Tone scale shown in the tutorial, or Middle Eastern scales), visually navigating past the standard black-and-white key layout can be confusing. By strictly hiding unused rows, the piano roll becomes an isomorphic grid where every visible row represents a valid diatonic/scale step, removing the cognitive load of avoiding "wrong" notes. 
* **Overall Applicability**: This is immensely useful for music theory novices, when composing in unfamiliar modal/exotic scales, or when doing rapid sequencing for genres like EDM, trap, or cinematic scoring where staying strictly locked to a scale is desired.
* **Value Addition**: Instead of manually drawing scale notes, copying them across 10 octaves, and saving them as external MIDI files (as demonstrated in the video), this code programmatically generates a guide track for *any* root and scale on the fly, immediately reconfiguring the user's MIDI editor layout.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythmic Grid: N/A for playback. The guide notes are drawn to span the entire length of the generated MIDI item (e.g., 4 bars) to ensure they overlap with any composition area.
* **Step B: Pitch & Harmony**
  - All pitches belonging to the requested scale (e.g., C Whole Tone, G Major, A Minor) are computed spanning from MIDI note 0 to 127. 
  - The notes are strictly added as *Muted* so they do not trigger actual VST instruments or affect the mix, acting purely as structural scaffolding.
* **Step C: Sound Design & FX**
  - No active instruments are applied to the guide track, as it is a visual tool. 
* **Step D: Mix & Automation**
  - The core automation here is interacting with the REAPER GUI via ReaScript: opening the created item in the built-in MIDI editor and programmatically triggering Action `40452` ("View: Hide unused note rows").

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Creating the Scale Guide | MIDI note insertion | Allows us to mathematically calculate and insert the exact MIDI pitches for any scale across all octaves. |
| Making it non-destructive | Note Properties (`muted=True`) | The REAPER API allows inserting notes natively as *muted*, providing visual guides without audio playback. |
| Hiding Out-of-Scale Rows | MIDI Editor Command Routing | Using `RPR_MIDIEditor_GetActive()` and `RPR_MIDIEditor_OnCommand()` directly simulates the UI hack shown in the tutorial. |

> **Feasibility Assessment**: 100% reproduction. The code completely automates the workflow the tutorial author achieves manually, replacing their workaround of storing predefined `.mid` files with a dynamic, on-demand REAPER script.

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
    Create a Scale-Restricted Piano Roll Template in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate the guide item for.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created template.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Demonstrated in tutorial
    }

    # Fallbacks for unrecognized inputs
    root_key = key if key in NOTE_MAP else "C"
    scale_type = scale if scale in SCALES else "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{root_key} {scale_type} {track_name}", True)

    # === Step 3: Create MIDI Item ===
    start_time = 0.0
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Ensure only our new item is selected to open it in the MIDI editor
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)

    # === Step 4: Calculate & Insert Muted Guide Notes ===
    root_val = NOTE_MAP[root_key]
    intervals = SCALES[scale_type]

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + item_length)

    note_count = 0
    for octave in range(11):
        for interval in intervals:
            pitch = (octave * 12) + root_val + interval
            if 0 <= pitch <= 127:
                # Signature: InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
                # Setting 'muted' to True (3rd param) creates the visual guide without audio playback
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Configure MIDI Editor View ===
    # Open the selected item in the built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Get the active MIDI editor window handle
    hwnd = RPR.RPR_MIDIEditor_GetActive()
    if hwnd:
        # Trigger 'View: Hide unused note rows' (Command ID: 40452)
        RPR.RPR_MIDIEditor_OnCommand(hwnd, 40452)

    return f"Created scale template '{root_key} {scale_type}' with {note_count} muted guide notes over {bars} bars. Unused piano roll rows have been hidden."
```