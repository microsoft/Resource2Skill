### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Locked Piano Roll Generator

* **Core Musical Mechanism**: Creating a muted "dummy" MIDI item containing all diatonic notes of a specific key/scale across every octave. When selected alongside your actual composition item, this tricks REAPER's MIDI Editor into revealing all notes of the scale when the "Hide unused note rows" action is triggered.
* **Why Use This Skill (Rationale)**: While REAPER has a native "Key Snap" feature (which the tutorial points out only *grays out* non-scale notes), having a fully collapsed piano roll that physically removes incorrect notes vastly speeds up the workflow. It prevents misclicks, makes visualizing wide chord voicings easier, and eliminates the visual clutter of the 5 non-diatonic notes in every octave.
* **Overall Applicability**: Useful for any genre relying heavily on MIDI programming (EDM, Hip-Hop, Pop). It acts as a compositional safety net and a visual aid for writing complex extended chords and fast arpeggios strictly within a mode.
* **Value Addition**: Instead of manually creating a root note, duplicating it diatonically 6 times, copying it across 8 octaves, and saving it as a MIDI file (as shown in the 4-minute tutorial), this programmatic skill instantly generates the perfectly calculated reference item in one click for *any* root and scale. 

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Duration**: A single quarter note (960 PPQ) placed at the very beginning of the item. Timing is irrelevant for the audio output since the item acts solely as visual data for the MIDI editor.
  - **Muting**: The generated MIDI item is explicitly muted so it does not send pitch data to your synths or disrupt the actual mix.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Mathematically projects the chosen root and scale intervals (e.g., Major, Dorian, Whole Tone) across all 128 available MIDI notes. 
  - **Logic**: Modulo 12 arithmetic `(pitch - root) % 12` is used to check if every possible MIDI key belongs to the selected scale interval array.

* **Step C: Sound Design & FX**
  - N/A. This is a workflow and composition utility track, meant to be routed nowhere and kept silent.

* **Step D: Mix & Automation**
  - N/A.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale Note Generation | MIDI note insertion | Allows programmatic generation of the exact diatonic template without needing external `.mid` files. |
| Non-destructive Reference | Item manipulation (Mute) | `B_MUTE` ensures the reference data doesn't accidentally trigger instruments if the user routes the track. |

> **Feasibility Assessment**: 100% — The script flawlessly automates the manual, tedious "custom action and octave duplication" process demonstrated in the tutorial, producing a mathematically perfect scale reference item natively inside REAPER.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 1,
    velocity_base: int = 96,
    **kwargs,
) -> str:
    """
    Create a Scale-Locked Piano Roll Generator in the current REAPER project.
    
    Creates a muted reference MIDI item containing all valid notes of the chosen scale.
    Select this item along with your active item, open the MIDI editor, and trigger
    "View: Hide unused note rows" to collapse the piano roll to strictly diatonic notes.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars for the reference item (1 is sufficient).
        velocity_base: Base MIDI velocity for reference notes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]  # Featured in the tutorial
    }

    # === Parse Inputs ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # === Step 1: Create the Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track explicitly so the user knows what scale it holds
    display_name = f"[{key} {scale.replace('_', ' ').title()}] Guide"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", display_name, True)

    # === Step 2: Create a Muted MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Mute the item - crucial so it doesn't output sound if synth is added
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)

    # === Step 3: Populate Diatonic Notes Across All Octaves ===
    note_count = 0
    # Quarter note duration in PPQ (Pulses Per Quarter)
    note_length_ppq = 960.0 
    
    for pitch in range(128):
        # Calculate distance from root, wrapped to a single octave (0-11)
        interval_from_root = (pitch - root_val) % 12
        
        if interval_from_root in scale_intervals:
            # Insert note: take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort
            RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, note_length_ppq, 0, pitch, velocity_base, True)
            note_count += 1

    # Apply the insertions
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{display_name}' track with {note_count} muted reference notes. Select this alongside your active MIDI item and use 'Hide unused note rows'."
```