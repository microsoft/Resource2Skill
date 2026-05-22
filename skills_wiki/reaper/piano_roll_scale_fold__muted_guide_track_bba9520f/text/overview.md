### 1. High-level Design Pattern Extraction

> **Skill Name**: Piano Roll Scale Fold (Muted Guide Track)

* **Core Musical Mechanism**: Creating a "Folded" Piano Roll to enforce a diatonic scale constraint. This is achieved by generating a full-range MIDI item containing muted, sustained notes for every pitch in a chosen scale across 8 octaves, and then triggering the REAPER MIDI Editor action "Hide unused note rows". 

* **Why Use This Skill (Rationale)**: Writing melodies and chord progressions within a specific scale (especially non-standard scales like the Whole Tone scale or exotic modes) is much easier when visually constrained. By "folding" the piano roll to only show the valid pitches, the producer is free to experiment with melodic contour, rhythmic syncopation, and interval leaps without worrying about hitting out-of-scale "wrong" notes. It eliminates guesswork and accelerates pattern-based sequencing.

* **Overall Applicability**: Essential as a foundational step when starting a new track, writing complex diatonic basslines, or working with unfamiliar scales. It effectively replicates the popular "Fold" grid feature found in Ableton Live, adapting it into a native REAPER workflow.

* **Value Addition**: Instead of relying on REAPER's "Key Snap" (which only grays out invalid notes), this script automatically builds a physical, muted scale template and instantly collapses the editor layout to hide all non-scale notes, providing a perfectly clean canvas for composition.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - The pattern generates sustained notes that stretch exactly from the beginning to the end of the specified item length (e.g., 4 bars). They act as a static visual grid rather than a rhythmic sequence.

* **Step B: Pitch & Harmony**
  - Notes are programmatically generated using music theory interval arrays (Major, Minor, Dorian, Mixolydian, Pentatonics, Blues, and Whole Tone).
  - The script calculates every valid pitch from MIDI note 12 (Octave 1) up to MIDI note 108 (Octave 9) based on the chosen root key.

* **Step C: Sound Design & FX**
  - No instruments or audio effects are required. The generated notes have their `muted` property set to `True`, ensuring they act purely as visual guides without triggering any sound.

* **Step D: Mix & Automation**
  - None required. The primary automation is at the UI level (triggering Action `40452` to hide unused note rows in the active MIDI Editor).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Muted Scale Guide Generation | `RPR_MIDI_InsertNote()` | Allows programmatic insertion of precise MIDI pitches while explicitly setting the `muted` Boolean flag to `True`. |
| Piano Roll "Folding" | `RPR_MIDIEditor_OnCommand()` | Action `40452` ("View: Hide unused note rows") directly executes the workflow trick demonstrated in the tutorial to hide non-scale rows. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly automates the tutorial's end goal of creating a scale-constrained piano roll without the user having to manually copy/paste notes or create a library of MIDI files.

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
    Create a 'Folded' Piano Roll Scale Guide in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate for the guide item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created scale guide.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    root_note = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name} ({key} {scale})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Generate Muted Scale Notes Across Octaves ===
    note_count = 0
    # Cover MIDI range from Octave 1 to Octave 8
    for octave in range(1, 9):
        base_midi = octave * 12 + root_note
        for interval in scale_intervals:
            pitch = base_midi + interval
            if pitch <= 127:
                # Arguments: take, selected(False), muted(True), start, end, channel, pitch, velocity, noSort(True)
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, int(pitch), velocity_base, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Format MIDI Editor (Fold to Scale) ===
    # Unselect all other items to ensure only the new item is opened
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Get active MIDI editor and execute "Hide unused note rows"
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # Action 40452: View: Hide unused note rows
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)

    return f"Created '{full_track_name}' with {note_count} muted guide notes over {bars} bars. Piano roll folded to {key} {scale}."
```