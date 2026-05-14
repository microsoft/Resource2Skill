### 1. High-level Design Pattern Extraction

> **Skill Name**: Workflow Macro: "Split and Elevate" (Custom Action Replication)

* **Core Musical Mechanism**: *Note: This video is a workflow and software configuration tutorial, not a music theory or composition lesson.* The most tangible, reproducible production technique demonstrated in the video (at 05:03) is the creation of a **Custom Action** to streamline editing. The creator demonstrates a macro called "Split and put item above," which splits an item at the time selection and automatically moves it to the track directly above. 
* **Why Use This Skill (Rationale)**: In digital audio production, keeping the creative flow uninterrupted is critical. Tedious mouse-work (slicing an item, creating a new track, dragging the item up, hoping you don't shift its timing) can cause "procrastination" and break the flow state. By bundling these into a single macro command, editors can extract transient hits, separate vocal comp takes, or layer specific melody notes instantly.
* **Overall Applicability**: This technique shines in vocal comping, drum loop chopping (e.g., extracting just the snares to a new track to apply a massive reverb), and arrangement staging (moving specific chorus elements to a new processing bus).
* **Value Addition**: While a standard skill outputs a static musical clip, this skill demonstrates how to translate a GUI-based Custom Action into programmatic ReaScript logic. It creates a baseline musical sequence and then programmatically executes the "Split and Move Up" workflow on it to demonstrate the result.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Context**: The macro relies on precise time selections.
  - **Implementation**: To demonstrate the macro additively, we will generate a continuous 4-bar 1/8th note arpeggio, and then simulate the macro isolating exactly Bar 2.

* **Step B: Pitch & Harmony**
  - **Context**: N/A for the workflow action itself.
  - **Implementation**: The placeholder media generated will automatically map to the user-provided `key` and `scale` parameters to prove the item contains valid musical data before it is sliced.

* **Step C: Sound Design & FX**
  - **Context**: The video emphasizes discovering layout configurations and native actions (using the `?` Actions menu) rather than specific sound design. 

* **Step D: Mix & Automation**
  - **Context**: The entire purpose of the "Split and Move Up" custom action is to isolate a specific audio/MIDI slice onto its own track so it can receive independent volume, panning, and FX processing without affecting the rest of the original track.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Placeholder Media | `RPR_MIDI_InsertNote` | Creates additive, self-contained media so the script has something to act upon without relying on external files. |
| "Split" Action | `RPR_SplitMediaItem` | Replicates the `Item: Split items at time selection` step of the video's custom action. |
| "Move Up" Action | `RPR_InsertTrackAtIndex` & `RPR_MoveMediaItemToTrack` | Replicates the `Item edit: Move items... up one track` step, ensuring the sliced item is isolated on a new track. |

> **Feasibility Assessment**: 100% reproduction of the logical workflow. Because the video does not provide a specific musical pattern, this script reconstructs the *editing workflow* (the "Split and put item above" custom action) by generating a procedural baseline track and programmatically applying the macro's slice-and-move logic to it. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Workflow_Source",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Simulates the 'Split and put item above' custom action demonstrated in the tutorial.
    It generates a baseline MIDI item, splits it at a specified bar, creates a new track 
    above the source, and moves the isolated slice to the new track.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created source track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of total bars to generate for the source media.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    # Music theory lookup tables for generating our placeholder media
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Source Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    src_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(src_track, "P_NAME", track_name, True)

    # === Step 3: Generate Baseline MIDI Item ===
    # We need media to perform the editing macro on.
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(src_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Populate the item with an 1/8th note arpeggio based on key/scale parameters
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 60 # Default to C4
    notes_per_bar = 8 
    note_length_ppq = 480 # 960 PPQ is 1/4 note, so 480 is 1/8th note
    
    for b in range(bars):
        for i in range(notes_per_bar):
            pitch = root_pitch + scale_intervals[i % len(scale_intervals)]
            start_ppq = int((b * notes_per_bar + i) * note_length_ppq)
            end_ppq = int(start_ppq + note_length_ppq - 10) # slight gap for articulation
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Execute "Split and Move Up" Macro Logic ===
    # The tutorial isolates an item at a time selection and moves it up a track.
    # We will simulate isolating "Bar 2" (from bar 2 start to bar 3 start)
    
    if bars >= 3:
        split_start = bar_length_sec * 1.0 # Start of Bar 2 (0-indexed 1)
        split_end = bar_length_sec * 2.0   # Start of Bar 3 (0-indexed 2)
        
        # Action: Split item at start of time selection
        # Note: RPR_SplitMediaItem returns the new item created to the RIGHT of the split point
        split_item_1 = RPR.RPR_SplitMediaItem(item, split_start) 
        
        # Action: Split the newly created remainder at the end of the time selection
        _ = RPR.RPR_SplitMediaItem(split_item_1, split_end)
        
        # Now, split_item_1 represents exactly the middle isolated slice (Bar 2)
        target_item = split_item_1
        
        # Action: Create track ABOVE source track
        # Since src_track is at track_idx, inserting at track_idx pushes src_track down to track_idx + 1
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        new_track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(new_track, "P_NAME", "Extracted_Slice (Macro Result)", True)
        
        # Action: Move isolated item to the new track
        RPR.RPR_MoveMediaItemToTrack(target_item, new_track)
        
        return f"Created base track, generated {bars} bars of media, and successfully executed 'Split and Move Up' macro logic on Bar 2."
    else:
        return f"Generated {bars} bars of media on '{track_name}'. (Need >= 3 bars to demonstrate the split macro logic properly)."
```