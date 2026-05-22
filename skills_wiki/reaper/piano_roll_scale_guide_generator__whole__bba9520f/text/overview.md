### 1. High-level Design Pattern Extraction

> **Skill Name**: Piano Roll Scale Guide Generator (Whole Tone Focus)

* **Core Musical Mechanism**: Generating a muted "guide" MIDI item that contains every valid note of a specific scale across all octaves. By opening this guide item in the REAPER MIDI Editor alongside an empty composition item, the user can use the "Hide unused note rows" action to visually snap the piano roll *strictly* to that scale's notes.
* **Why Use This Skill (Rationale)**: This technique eliminates the possibility of hitting "wrong notes" when composing diatonically. It is particularly valuable when writing in less common modes or symmetrical scales like the Whole Tone scale. As mentioned in the tutorial, the Whole Tone scale divides the octave into 6 equal intervals (all whole steps), yielding a very uneven, unresolved, and "dreamy" sound universally used in film score flashback sequences.
* **Overall Applicability**: Melody writing, chord progression building, and rapid composition. It is an excellent workflow enhancement for producers who aren't proficient keyboard players or want to experiment with unfamiliar exotic scales without referencing a chart.
* **Value Addition**: The tutorial demonstrates a manual, multi-step process: finding the root, running a custom action to generate scale degrees, copying across octaves, muting, and saving as a template. This skill mathematically encodes the intervals for major, minor, modes, and the whole tone scale, generating the perfect structural template instantly via code.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythm is not applicable here, as these are UI reference guides rather than playback elements. 
  - The generated MIDI notes stretch continuously across the entire requested bar length.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable. The script calculates the exact MIDI note numbers (0-127) based on the chosen root and scale formula.
  - **Highlighted Scale**: The Whole Tone scale (`0, 2, 4, 6, 8, 10`).

* **Step C: Sound Design & FX**
  - None required. The generated track and the individual MIDI notes are explicitly set to `muted` so they do not output any audio and only serve as visual anchors in the piano roll.

* **Step D: Mix & Automation**
  - Not applicable.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale Generation | MIDI note insertion | Programmatic generation of notes across all octaves replaces the manual copying process. |
| Non-destructive UI | Track & Item Muting | Ensures the guide notes do not trigger any synths or interfere with the mix. |

> **Feasibility Assessment**: 100%. The script perfectly automates the manual labor shown in the tutorial, instantly delivering the final product (a muted template of scale notes across all octaves) ready for the "Hide unused note rows" action.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a muted Piano Roll Scale Guide in the current REAPER project.
    
    After generation, open this item in the MIDI editor alongside your synth item,
    and trigger the REAPER action 'View: Hide unused and unnamed note rows' 
    to lock your piano roll visually to the specified scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate for the guide.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10],  # Highlighted in the tutorial
    }

    # Normalize key input
    key_upper = key.upper()
    if key_upper not in NOTE_MAP:
        key_upper = "C"
    
    root_val = NOTE_MAP[key_upper]
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Format track name (e.g., "C Whole Tone Guide")
    formatted_track_name = f"{key_upper} {scale.replace('_', ' ').title()} {track_name}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", formatted_track_name, True)
    
    # Mute the track entirely so it acts only as a visual reference
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", formatted_track_name, True)

    # === Step 4: Insert Diatonic Notes ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    notes_added = 0
    # Iterate across all standard MIDI octaves (-1 to 9)
    for octave in range(-1, 10):
        for interval in scale_intervals:
            note_num = (octave + 1) * 12 + root_val + interval
            # Ensure we only place notes within the 0-127 MIDI bounds
            if 0 <= note_num <= 127:
                # Parameters: take, selected(False), muted(True), start, end, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note_num, velocity_base, True)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{formatted_track_name}' track with {notes_added} muted guide notes over {bars} bars. Use 'Hide unused note rows' in the MIDI editor."
```