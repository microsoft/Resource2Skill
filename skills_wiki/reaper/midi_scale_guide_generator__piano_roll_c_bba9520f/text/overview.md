### 1. High-level Design Pattern Extraction

> **Skill Name**: MIDI Scale Guide Generator (Piano Roll Collapser)

* **Core Musical Mechanism**: The tutorial demonstrates a clever REAPER workaround for "locking" the MIDI Editor to a specific scale. By creating a muted MIDI clip containing every valid note of a given scale (spanning all octaves) and keeping it active alongside your composition, you can use the built-in MIDI Editor action **"Hide unused note rows"** to visually collapse the piano roll. This hides all non-diatonic keys.
* **Why Use This Skill (Rationale)**: While REAPER has a "Key Snap" feature, it only grays out the piano keys without actually removing the wrong rows from the grid. Visually collapsing the piano roll removes the possibility of writing "wrong" (non-diatonic) notes entirely, dramatically speeding up melody writing, complex chord generation, and arpeggio programming. 
* **Overall Applicability**: This technique is universally useful for any MIDI-based workflow—especially for producers who rely heavily on the mouse/piano roll rather than playing a live MIDI keyboard, or when working with unfamiliar or exotic scales (like the Whole Tone scale mentioned in the video).
* **Value Addition**: Generating a full 10-octave scale manually is tedious. This code automatically builds a muted "Scale Guide" track populated with every diatonic note of the selected scale across the entire frequency spectrum, instantly prepping your project for the "Hide unused note rows" workflow.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Duration**: The notes span the entire duration of the generated MIDI item (e.g., 4 full bars) as continuous legato blocks.
  - **Rhythm**: No rhythm is needed. The notes exist purely as a visual template for the REAPER UI.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (Major, Minor, Whole Tone, Dorian, etc.).
  - **Voicing**: Every note belonging to the scale is generated across all octaves (MIDI note 0 through 127).

* **Step C: Sound Design & FX**
  - **Instrument**: None required.
  - **Routing**: The generated guide track is explicitly **muted** (`B_MUTE` = 1.0) so the guide notes do not trigger any sound or interfere with the mix.

* **Step D: Mix & Automation**
  - Not applicable.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Muted Scale Guide Track | Track creation + Mute property (`P_MUTE`) | Ensures the guide notes don't accidentally play back and ruin the mix. |
| 10-Octave Scale Generation | `RPR_MIDI_InsertNote()` with scale math | Generates every valid diatonic pitch accurately from note 0 to 127 based on scale arrays. |

> **Feasibility Assessment**: 100% — This code perfectly reproduces the scale-generation step of the tutorial. *Note: The final step of the tutorial—clicking "Hide unused note rows"—is a UI action. The script prepares the exact MIDI data required for that action, but the user must trigger the view toggle in their MIDI Editor depending on their layout.*

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
    Creates a muted Scale Guide track populated with every note in the selected scale 
    across all octaves. This enables the "Hide unused note rows" Piano Roll workflow.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate the guide block for.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the created scale guide.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Highlighted in the tutorial
    }

    # Validate inputs
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_key = scale.lower()
    scale_intervals = SCALES.get(scale_key, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Muted Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Format a descriptive name
    full_track_name = f"{track_name} ({key} {scale_key})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Explicitly MUTE the track so the guide block doesn't make sound
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    # Insert new MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Convert project time to MIDI PPQ (Pulses Per Quarter Note) for note insertion
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)

    # === Step 4: Insert All Diatonic Notes ===
    note_count = 0
    # Iterate through all standard MIDI octaves (0 to 10)
    for octave in range(11): 
        for interval in scale_intervals:
            pitch = (octave * 12) + root_val + interval
            
            # Ensure we don't exceed the max MIDI note (127)
            if pitch <= 127:
                # Insert note: take, selected, muted, start_ppq, end_ppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1

    # Sort MIDI events after batch insertion for optimal performance
    RPR.RPR_MIDI_Sort(take)

    return (f"Created muted '{full_track_name}' guide track with {note_count} notes over {bars} bars. "
            f"Select this item, open the MIDI Editor, and trigger action 'View: Hide unused note rows'.")
```