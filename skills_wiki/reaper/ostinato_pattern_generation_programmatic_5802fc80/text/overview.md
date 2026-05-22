# Ostinato Pattern Generation (Programmatic Looping)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Ostinato Pattern Generation (Programmatic Looping)

* **Core Musical Mechanism**: The tutorial demonstrates how to optimize REAPER's workflow for looping media items (specifically a recorded staccato MIDI sequence) using the SWS extension and mouse modifiers. Musically, this represents the creation of an **Ostinato**—a persistently repeating motif or phrase that serves as a rhythmic and harmonic foundation. 

* **Why Use This Skill (Rationale)**: Looping short, quantized sequences is the backbone of modern electronic, hip-hop, and pop production. It creates a hypnotic, driving feel. While the video teaches a UI macro for dragging out item edges to loop them, the programmatic equivalent is algorithmically repeating a defined sequence of notes over a set duration. This ensures mathematically perfect timing and allows for instant variation.

* **Overall Applicability**: This technique is perfect for generating repeating baseline grooves, staccato synth arpeggios, or repetitive drum patterns where consistency and perfect quantization are required across multiple bars.

* **Value Addition**: Instead of relying on a third-party extension (SWS) and manual mouse dragging, this skill encodes the *concept* of the tutorial into a native, fully reproducible ReaScript. It generates a 1-bar staccato synth ostinato (similar to the one played in the video) and programmatically loops it to fill the requested number of bars, demonstrating precise grid math and loop logic.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/8th notes.
  - **Pattern Length**: 1 bar.
  - **Duration**: Staccato (notes are slightly shorter than a full 1/8th note to create a plucked/bouncy feel, roughly 80% of the grid division).
  - **Looping**: The 1-bar rhythm is perfectly duplicated for the total number of requested `bars`.

* **Step B: Pitch & Harmony**
  - **Scale Degrees**: A classic ascending/descending ostinato using the root, 3rd, 5th, and octave of the provided scale (e.g., `[0, 2, 4, 7]` in scale indices).
  - **Contour**: Root → 3rd → 5th → 3rd → Root → 3rd → 5th → Octave. 
  - **Base Octave**: Midi note 48 (C3) for mid-low synth presence.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` to mimic the basic virtual instrument tone used in the demonstration.
  - **Character**: Adjusted for a plucky sound (fast attack, short decay) to match the staccato playing style in the video.

* **Step D: Mix & Automation (if applicable)**
  - No complex automation; the focus is on raw MIDI item generation and mathematical pattern repetition.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Ostinato Pattern | Programmatic MIDI loops | While the tutorial uses the SWS Extension to drag-loop items, native ReaScript cannot guarantee SWS is installed. Programmatically calculating the loop repeats inside a single expanded item perfectly replicates the *musical result* (a looped sequence) with 100% native compatibility. |
| Staccato Articulation | MIDI note length truncation | Setting note lengths to 80% of their grid division mimics the choppy, rhythmic keyboard playing shown in the video. |
| Tone Generation | FX chain (ReaSynth) | Provides immediate audible feedback for the generated repeating pattern without needing external VSTs. |

> **Feasibility Assessment**: 100% reproducible. By translating the UI-based "click and drag" loop workflow into a mathematical `for` loop, we generate the exact same repeating musical structure cleanly and natively.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Looped Ostinato",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a repeating staccato synth ostinato in the current REAPER project,
    demonstrating programmatic looping across multiple bars.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the loop for.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory & Setup ===
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
    }

    if key not in NOTE_MAP:
        key = "C"
    if scale not in SCALES:
        scale = "minor"

    root_pitch = 48 + NOTE_MAP[key]  # Start around C3
    scale_intervals = SCALES[scale]

    # Helper function to get correct pitch from scale degree
    def get_pitch(degree):
        octave_offset = (degree // len(scale_intervals)) * 12
        scale_index = degree % len(scale_intervals)
        return root_pitch + octave_offset + scale_intervals[scale_index]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add ReaSynth to mimic the tutorial's virtual instrument
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a plucky, staccato sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)   # Fast Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.2)   # Short Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1)   # Low Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1)   # Short Release

    # === Step 3: Create Media Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Programmatic Looping Logic ===
    # 1-bar pattern using scale degrees: Root, 3rd, 5th, 3rd, Root, 3rd, 5th, Octave
    pattern_degrees = [0, 2, 4, 2, 0, 2, 4, 7] 
    
    # 8th notes
    steps_per_bar = 8
    step_length_sec = bar_length_sec / steps_per_bar
    
    # We make the note slightly shorter than the grid step for a staccato feel
    note_duration_sec = step_length_sec * 0.8 

    notes_created = 0

    # Mathematically loop the 1-bar pattern over the requested number of bars
    for current_bar in range(bars):
        bar_offset_sec = current_bar * bar_length_sec
        
        for step_idx, degree in enumerate(pattern_degrees):
            pitch = get_pitch(degree)
            
            # Add slight volume dynamics: accent the downbeats (0, 4)
            vel = velocity_base + 15 if (step_idx % 4 == 0) else velocity_base
            vel = min(127, max(1, vel))
            
            # Calculate absolute time in seconds
            start_time_sec = bar_offset_sec + (step_idx * step_length_sec)
            end_time_sec = start_time_sec + note_duration_sec
            
            # Convert seconds to PPQ (Pulses Per Quarter Note) for MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(
                take, 
                False,   # Selected
                False,   # Muted
                start_ppq, 
                end_ppq, 
                0,       # Channel
                int(pitch), 
                int(vel), 
                False    # No-sort (we'll sort at the end)
            )
            notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' ostinato: looped {bars} bars ({notes_created} notes) at {bpm} BPM in {key} {scale}."
```