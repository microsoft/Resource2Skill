### 1. High-level Design Pattern Extraction

> **Skill Name**: Piano Roll Scale Filter Generator 

* **Core Musical Mechanism**: Diatonic Row Filtering. The tutorial demonstrates a workflow technique where you place every note of a specific scale across all octaves into a MIDI item, and then mute them. When you open this item in the REAPER MIDI Editor and use the action "Hide unused note rows", the piano roll collapses to *only* display the notes in your chosen scale. 

* **Why Use This Skill (Rationale)**: Removing out-of-scale notes visually constraints the composition process, preventing "wrong" notes from being clicked or programmed. This is especially useful for complex modes or less familiar scales (like the Whole Tone scale mentioned in the video) where the visual pattern of black/white keys is not easily memorized. 

* **Overall Applicability**: Excellent for setting up composition templates, generating ghost tracks to guide other MIDI items, or quickly locking the MIDI editor grid to a new mode (e.g., Dorian, Phrygian) when starting a new track.

* **Value Addition**: The tutorial shows a manual process: inserting a root note, duplicating it diatonically 6 times, copying it up and down octaves, and then muting them. This script automates that entire process instantly. It encodes music theory (intervals for 12 different scales/modes) and programmatically generates the muted guide notes across the entire 128-note MIDI spectrum.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Timing**: Static. The notes span the entire length of the generated MIDI item (default 1 bar). 
  - **Rhythm**: None. The notes act as a visual scaffold, not a rhythm.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable. The tutorial demonstrates G Major, C Minor, and C Whole Tone.
  - **Pitches**: Every valid note of the target scale from octave 0 to 10 (MIDI note 0 to 127).

* **Step C: Sound Design & FX**
  - **Muting**: Crucially, every inserted note is explicitly flagged as `muted = True` via the API. This ensures the track makes no sound and doesn't trigger synths, acting purely as a visual template.

* **Step D: Mix & Automation**
  - None required.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale calculation | Dictionary lookup | Translates music theory into exact interval arrays. |
| Guide note generation | MIDI note insertion | Allows us to insert notes programmatically across all octaves. |
| Silent workflow | MIDI property `muted=True` | Matches the tutorial's technique of muting the guide notes so they don't trigger audio. |

> **Feasibility Assessment**: 100% reproduction. The code perfectly generates the muted scale scaffold shown in the video. (Note: To complete the workflow, the user or agent must simply open the created item in the MIDI editor and run `View: Hide unused note rows`).

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Piano Roll Scale Filter Generator in the current REAPER project.
    Generates explicitly muted notes for a specific scale across all octaves,
    allowing the user to use 'Hide unused note rows' in the MIDI Editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars the guide item should last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created guide track.
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
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "locrian":          [0, 1, 3, 5, 6, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Resolve scale and root
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])

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

    # Convert time to PPQ (ticks)
    start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    end_qn = RPR.RPR_TimeMap2_timeToQN(0, item_length)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # === Step 4: Generate Muted Scale Scaffold ===
    note_count = 0
    
    # Loop through 11 octaves to cover the entire MIDI spectrum (0-127)
    for octave in range(11):
        for interval in intervals:
            note_pitch = (octave * 12) + root_val + interval
            
            if 0 <= note_pitch <= 127:
                # Insert note. Parameter 3 is 'muted'. We set it to True.
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note_pitch, velocity_base, True)
                note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{full_track_name}' with {note_count} muted notes over {bars} bars. Open in MIDI editor and trigger 'Hide unused note rows'."
```