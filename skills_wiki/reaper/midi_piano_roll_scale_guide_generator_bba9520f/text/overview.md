### 1. High-level Design Pattern Extraction

> **Skill Name**: MIDI Piano Roll Scale Guide Generator

* **Core Musical Mechanism**: Generating a structural scaffold of *muted* MIDI notes spanning multiple octaves to define a specific musical scale. This explicitly enables REAPER's "Hide unused note rows" action to visually lock the piano roll exclusively to diatonic notes, removing all out-of-scale "wrong" notes from the grid.

* **Why Use This Skill (Rationale)**: While REAPER has a "Key Snap" feature that grays out notes, visually navigating a standard chromatic piano roll can still be tedious. By placing muted notes on every valid scale degree across all octaves, you force the MIDI editor to only render the rows that belong to your chosen scale. This speeds up chord programming and melody writing. The video also touches on the distinct flavors of specific scales (e.g., the Whole Tone scale, which divides the octave symmetrically into 6, creating the classic "dreamy/flashback" sound).

* **Overall Applicability**: Essential for streamlining MIDI composition workflows. It is highly applicable when an AI agent or producer needs to lock a track strictly to a key (like C minor or G whole tone) before generating generative arpeggios, basslines, or complex diatonic chord voicings. 

* **Value Addition**: The video outlines a highly manual process: creating custom actions, duplicating notes diatonic-ally, copying them up and down octaves, muting them, and saving them as external templates. This skill encapsulates that entire 5-minute tedious workflow into a single, instant, parameterized execution. 

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: Agnostic (defaults to 120 BPM in 4/4).
  - **Rhythm**: Sustained whole notes that span the entire duration of the specified MIDI item boundary.
  - **Note Duration**: Equal to the total length of the generated track item (e.g., exactly 4 bars long).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable. The tutorial explicitly demonstrates Major, Minor, Dorian, and the Whole Tone scale.
  - **Voicing**: All scale degrees, mapped linearly across octaves 1 through 7.
  - **Pitch Math**: `Root Note + Scale Interval + (Octave * 12)`.

* **Step C: Sound Design & FX**
  - **Muted Notes**: The most critical sound design element here is *silence*. The MIDI notes are injected with the `muted=True` flag so they act strictly as visual anchors/guides without triggering any connected VST instruments.

* **Step D: Mix & Automation**
  - N/A. No automation is required; this is purely a MIDI data structure to manipulate REAPER's UI state.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale framework generation | MIDI note insertion | Allows precise mathematical placement of pitches across all octaves. |
| Non-audible guides | `muted=True` argument | `RPR_MIDI_InsertNote` accepts a boolean for mute state, perfectly replicating the video's trick of muting the guide notes. |

> **Feasibility Assessment**: 100% reproduction of the musical/structural pattern. The script perfectly replicates the outcome of the video's custom actions (stacking octaves of a scale and muting them) without requiring the user to set up external MIDI file templates or custom macros. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide (Muted)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 64,
    **kwargs,
) -> str:
    """
    Creates a 'Scale Guide' track containing muted MIDI notes across multiple octaves.
    This replicates the REAPER workflow trick to lock the Piano Roll strictly to a scale
    so the user can utilize the "Hide unused note rows" action.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate the guide for.
        velocity_base: Base MIDI velocity (doesn't matter much as notes are muted).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created guide item.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10] # Highlighted in the video for 'dreamy' sounds
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{key} {scale} {track_name}", True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate PPQ bounds for the length of the item
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Inject Muted Scale Notes ===
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    note_count = 0
    # Loop across typical audible octaves (1 to 7) to build the guide
    for octave in range(1, 8):
        for interval in intervals:
            pitch = root_pitch + interval + (octave * 12)
            if pitch <= 127:
                # Arguments: take, selected(False), muted(True), startPPQ, endPPQ, channel(0), pitch, velocity, noSort(True)
                # The 'muted=True' parameter is the core of this workflow trick.
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1

    # Finalize and sort MIDI events
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{key} {scale} {track_name}' track. Injected {note_count} muted notes over {bars} bars at {bpm} BPM to act as a Piano Roll scale lock."
```