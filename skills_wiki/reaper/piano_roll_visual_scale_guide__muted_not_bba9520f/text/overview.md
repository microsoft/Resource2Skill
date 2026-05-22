### 1. High-level Design Pattern Extraction

> **Skill Name**: Piano Roll Visual Scale Guide (Muted Note Template)

* **Core Musical Mechanism**: Creating a visual reference of a musical scale across all octaves by inserting a vertical column of muted guide notes. The tutorial specifically highlights the **Whole Tone** scale (which divides the octave into 6 equal intervals) for creating "uneven & dreamy sounds" typical of flashback scenes.
* **Why Use This Skill (Rationale)**: Keeping your piano roll restricted to a specific scale (whether a standard diatonic scale or a symmetrical one like the whole-tone) prevents out-of-key errors and speeds up composing. REAPER has a native "Hide unused note rows" action in the MIDI Editor. By placing a stack of muted notes representing the scale in a MIDI item, REAPER interprets those rows as "used." When you trigger the hide action, the Piano Roll collapses to show *only* the safe scale degrees, acting as a custom scale snap/guide.
* **Overall Applicability**: This is a powerful setup step before composing melodies, basslines, or chord progressions. It is especially useful for exotic or custom scales that aren't natively highlighted by REAPER's default piano roll grid.
* **Value Addition**: Automates the tedious manual process shown in the tutorial (duplicating notes up a 2nd diatonic, then across octaves) by programmatically generating a template track with every note of the requested scale in a fraction of a second.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - A single column of short 1/16th notes is placed at the very start of a MIDI item.
  - The notes are muted so they do not produce any sound and do not interfere with playback.
* **Step B: Pitch & Harmony**
  - The script calculates every pitch from MIDI note 0 to 127 that belongs to the selected key and scale using a modulo-12 operation.
  - Supports standard modes (Major, Minor, Dorian, etc.) as well as the Whole Tone scale featured in the video.
* **Step C: Sound Design & FX**
  - N/A. This is purely a workflow and MIDI template skill. No synthesizers or FX are required.
* **Step D: Mix & Automation**
  - The notes are inserted with the `muted = True` flag via the ReaScript API, serving exclusively as visual anchors.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale note generation | MIDI note insertion | Generates the exact pitches required to map out the scale. |
| Invisible visual guides | Muted note flag (`muted=True`) | REAPER's "Hide unused note rows" considers muted notes as "used," allowing us to build a visual guide without introducing unwanted sound. |

> **Feasibility Assessment**: 100% — This script perfectly reproduces the tutorial's custom scale guide workflow. It provides the MIDI template programmatically, bypassing the need for the user to manually create or download `.mid` scale files. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Piano Roll Visual Scale Guide in the current REAPER project.
    
    Usage Tip: After running this script, double-click the generated MIDI item 
    to open the MIDI Editor, then run the action "View: Hide unused and unnamed note rows" 
    (Action ID 40453). The piano roll will collapse to show only the notes in your scale!

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate for the template item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Featured in the tutorial
    }

    import reaper_python as RPR

    # Format key and retrieve scale intervals
    key_formatted = key.capitalize()
    root_pitch = NOTE_MAP.get(key_formatted, 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    actual_track_name = f"{key_formatted} {scale.replace('_', ' ').title()} {track_name}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", actual_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # We make the guide notes a 1/16th note long at the very start of the item
    note_duration_sec = (60.0 / bpm) / 4 
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_duration_sec)

    # === Step 4: Insert Muted Guide Notes ===
    count = 0
    for pitch in range(128):
        # Check if the current pitch belongs to the selected scale
        if (pitch - root_pitch) % 12 in intervals:
            # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, custom)
            # We set muted to True (the 3rd argument)
            RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{actual_track_name}' track with {count} muted guide notes over {bars} bars at {bpm} BPM."
```