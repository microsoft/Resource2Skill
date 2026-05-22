### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale Lock / Ghost Note Template Generator

* **Core Musical Mechanism**: The tutorial demonstrates a workflow hack to force REAPER's MIDI Editor into a "scale-locked" mode. By generating a MIDI item containing every valid note of a specific scale across all octaves and muting them, you can use the DAW's "Hide Unused Note Rows" action. This collapses the Piano Roll so only diatonic notes are visible, making it impossible to click or play "out of key."

* **Why Use This Skill (Rationale)**: While standard Key Snap highlights the correct notes, it still leaves non-diatonic rows visible, which can lead to misclicks during rapid programming. Collapsing the view removes visual clutter and enforces strict diatonicism. This is especially useful for exploring complex or custom scales (like the Whole Tone scale mentioned in the video) where the standard visual layout of the piano keyboard can be unintuitive.

* **Overall Applicability**: This technique is invaluable during the early stages of composition, writing complex arpeggios, inputting rapid MIDI drum rolls (where only specific drum kit pieces are used), or generating generative/aleatoric sequences where you want to ensure all randomized notes fall perfectly within a chosen mode.

* **Value Addition**: The video creator manually constructs these scale templates by stacking diatonic seconds and copy-pasting across octaves, eventually offering them as downloadable MIDI files. This script bypasses that tedious manual labor entirely, instantly generating a scale-lock template for *any* key and scale dynamically on a new track.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: Independent of tempo, but the template spans a default duration (e.g., 4 bars) so it is easily visible in the arrangement.
  - **Note Duration**: The generated "ghost notes" span the entire length of the template item (one long sustained note per pitch).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable. The script calculates the valid pitches for the given root note and interval structure (Major, Minor, Dorian, Whole Tone, etc.).
  - **Range**: The notes are duplicated across the entire MIDI pitch range (notes 0 through 127) to ensure the piano roll is fully populated regardless of the instrument's active range.

* **Step C: Sound Design & FX**
  - No active sound design is intended. The notes are explicitly generated with their `muted` property set to `True`. They will not trigger connected VSTs or hardware, existing purely as structural data for the MIDI Editor's UI.

* **Step D: Mix & Automation**
  - The generated track acts as a non-playing reference layer. No mixing or automation is required.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation across octaves | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows programmatic calculation of scale degrees without manual copy-pasting. |
| Non-destructive reference notes | `muted=True` parameter | Muting the notes individually allows them to register as "used" by the MIDI Editor for the "Hide unused rows" action, while remaining completely silent during playback. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly automates the manual creation process shown in the video. Once the script runs, the user or agent simply opens the newly created MIDI item and triggers REAPER's native "Hide unused note rows" action to achieve the exact visual state demonstrated.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Lock Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a MIDI item filled with muted notes for every pitch in a specified scale.
    Used to collapse the MIDI editor via the "Hide unused note rows" action.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars the template should span.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10],  # Featured explicitly in the tutorial
    }

    # Resolve scale intervals and root note
    root_pitch = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Calculate all valid MIDI pitches (0-127) for the given scale
    scale_notes = set()
    for octave in range(11):
        for interval in intervals:
            note = (root_pitch + interval) + (octave * 12)
            if 0 <= note <= 127:
                scale_notes.add(note)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Reference Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    # Name track intelligently based on chosen scale
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
    
    # Calculate start and end times in PPQ (Pulses Per Quarter Note)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Insert Ghost Notes ===
    note_count = 0
    for pitch in scale_notes:
        # We set muted=True (the 3rd argument) so they are visually present but acoustically silent
        RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        note_count += 1

    # Sort MIDI data after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{full_track_name}' with {note_count} muted reference notes over {bars} bars at {bpm} BPM."
```

#### 3c. Verification Checklist
- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?