### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale Guide Generator for Piano Roll Hiding

* **Core Musical Mechanism**: Creating a full-spectrum, muted "dummy" MIDI item containing every note of a specific musical scale across all octaves. When this dummy item is selected alongside a working track, the user can run REAPER's native "Hide unused note rows" action to instantly snap the Piano Roll view to show *only* the notes in that scale.
* **Why Use This Skill (Rationale)**: By default, REAPER's MIDI editor displays all 128 chromatic notes. While the "Key Snap" feature greys out out-of-scale notes, it doesn't remove them. Hiding non-scale rows makes composing diatonic melodies and chords visually cleaner and less error-prone. Because REAPER lacks a native "Hide non-scale rows" button, injecting a muted "scale reference" item tricks the existing "Hide unused notes" feature into creating the perfect diatonic Piano Roll layout.
* **Overall Applicability**: This utility pattern is applicable across all genres, particularly when composing complex chord progressions, programming fast arpeggios, or learning a new mode/scale (like Dorian, Whole Tone, or Harmonic Minor) where a clean visual guide is highly beneficial.
* **Value Addition**: Instead of manually writing and duplicating diatonic notes up and down octaves as demonstrated in the tutorial, this script instantly mathematically computes and inserts all valid MIDI notes (0-127) for any given key and scale.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature/Grid**: Not rhythmically dependent; the notes are inserted as sustained "dummy" blocks stretching across the entire length of the specified bars.
  - **Note Duration**: Full length of the item (e.g., 1 bar).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric. Computes the root note index (0-11) and adds scale intervals (e.g., `[0, 2, 4, 5, 7, 9, 11]` for Major).
  - **Octave Spread**: The pattern duplicates the scale across the entire MIDI spectrum (MIDI note 0 to 127).

* **Step C: Sound Design & FX**
  - **Instrument**: None required.
  - **Track State**: The generated track is explicitly **muted**. This ensures the guide notes do not trigger any synths or affect the audio mix if routed.

* **Step D: Mix & Automation (if applicable)**
  - No automation. The item acts purely as graphical UI scaffolding for the MIDI Editor.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise calculation of every allowed pitch across the 0-127 MIDI range. |
| Non-destructive UI hack | Track Muting (`RPR_SetMediaTrackInfo_Value`) | Ensures the scale template doesn't produce sound, acting purely as a visual template. |

> **Feasibility Assessment**: 100% — This code entirely replaces the manual workflow shown in the tutorial (creating items, running custom actions to build diatonic steps, duplicating up/down octaves). The agent can immediately create the required scale guide track.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale Guide in the current REAPER project to be used with the 
    'Hide unused note rows' action in the MIDI Editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate for the dummy item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Scale Guide (C major)' with 74 notes over 1 bars at 120 BPM"
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Normalize inputs
    key_upper = key.upper()
    root_pitch = NOTE_MAP.get(key_upper, 0)
    scale_lower = scale.lower()
    scale_intervals = SCALES.get(scale_lower, SCALES["major"])
    
    full_track_name = f"{track_name} ({key_upper} {scale_lower})"

    # === Step 1: Calculate all valid scale pitches from MIDI 0 to 127 ===
    valid_pitches = []
    for octave in range(-1, 10):  # Covers notes 0 to 127
        for interval in scale_intervals:
            pitch = root_pitch + interval + (octave * 12)
            if 0 <= pitch <= 127:
                valid_pitches.append(pitch)

    # === Step 2: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 3: Create Track & Mute it ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    # Mute the track so the dummy notes don't accidentally play
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Insert Dummy Notes ===
    # Notes will stretch across the entire item length
    start_ppq = 0
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    notes_created = 0
    for pitch in valid_pitches:
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        notes_created += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # Note: To use this visually, the user/agent must select this new item alongside 
    # their actual target item, open the MIDI editor, and trigger Action 40453 
    # ("MIDI Editor: Hide unused and unnamed note rows").

    return f"Created '{full_track_name}' (muted) with {notes_created} dummy notes over {bars} bars at {bpm} BPM"
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? *(Technique strictly reproduced).*
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?