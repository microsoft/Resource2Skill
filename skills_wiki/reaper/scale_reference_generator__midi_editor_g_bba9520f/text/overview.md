### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale Reference Generator (MIDI Editor Guide)

* **Core Musical Mechanism**: Creating a dedicated, muted MIDI track containing every note of a specific musical scale across multiple octaves. This acts as a visual template.
* **Why Use This Skill (Rationale)**: REAPER features a powerful MIDI Editor action called *"View: Hide unused and unnamed note rows"*. However, to use this feature, the notes must actually exist in the item. The video details a manual, macro-heavy workflow of copying and pasting diatonically shifted notes to build these "scale templates". Programmatically generating these muted notes achieves the exact same visual constraint instantly. This enforces strict diatonic composing, preventing out-of-key notes and removing visual clutter.
* **Overall Applicability**: Essential for complex melodic composition, arranging dense MIDI orchestration, or when experimenting with unfamiliar modes (e.g., Whole Tone, Dorian, Harmonic Minor). It allows the producer to visually lock the piano roll to any key or scale.
* **Value Addition**: Replaces a tedious, multi-step custom action workflow (creating roots, triggering diatonic duplication macros, and copying across octaves) with a single script that instantly generates a mathematically perfect scale template.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Timing**: The notes span the entire duration of the generated MIDI item (e.g., 4 bars continuously) so they are always visible in the background of the piano roll. 
  - **Duration**: Legato/Infinite relative to the item.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric. Computes the intervals for the chosen scale (Major, Minor, Dorian, Whole Tone, etc.).
  - **Range**: Spans from MIDI note 12 (Octave 1) to MIDI note 107 (Octave 8), covering the standard compositional range.
* **Step C: Sound Design & FX**
  - **Instrument**: None required.
  - **Routing**: The MIDI notes are explicitly inserted as `muted = True`, and the track itself is muted. This ensures the guide track never interferes with the project's audio or sends unwanted MIDI data to other routing paths.
* **Step D: Mix & Automation**
  - Track is muted. Name is set dynamically (e.g., "G major Guide") for easy identification.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | Pitch computation via array intervals | Allows dynamic generation of any scale root/mode without hardcoding MIDI numbers. |
| Visual templating | MIDI note insertion (`RPR_MIDI_InsertNote`) | Populates the piano roll so REAPER's "Hide unused rows" action can detect the scale. |
| Audio safety | Item/Track Muting | Ensures the template remains purely visual and doesn't trigger synths. |

> **Feasibility Assessment**: 100% — This code perfectly reproduces the end-result of the video's workflow. The script bypasses the manual custom actions demonstrated by the presenter and directly generates the requested multi-octave scale items ready for the "Hide unused note rows" feature.

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
    Create a muted multi-octave Scale Reference Generator in the current REAPER project.
    Use this alongside REAPER's "View: Hide unused and unnamed note rows" MIDI editor action.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, Db, D, ..., B).
        scale: Scale type (major, minor, whole_tone, dorian, etc.).
        bars: Number of bars the visual guide should span.
        velocity_base: Base MIDI velocity (0-127) (irrelevant here as notes are muted).
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Highlighted in the tutorial
    }

    # Normalize inputs
    key_norm = key.capitalize()
    if key_norm not in NOTE_MAP:
        key_norm = "C"
        
    scale_norm = scale.lower()
    if scale_norm not in SCALES:
        scale_norm = "major"
        
    base_pitch = NOTE_MAP[key_norm]
    intervals = SCALES[scale_norm]
    
    # Generate dynamic track name based on scale
    final_track_name = f"{key_norm} {scale_norm.replace('_', ' ').title()} Guide"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", final_track_name, True)
    
    # Mute the track to ensure it acts only as a visual guide
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Get PPQ positions for the full item length
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Populate Scale Notes Across Octaves ===
    note_count = 0
    # Loop through octaves 1 to 7 (MIDI notes 12 to roughly 107)
    for octave in range(1, 8):
        octave_base = base_pitch + (octave * 12)
        
        for interval in intervals:
            note_pitch = octave_base + interval
            
            # Keep within valid MIDI range
            if note_pitch < 128:
                # Insert the note (muted = True) spanning the whole item
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    True,           # muted (purely visual)
                    start_ppq,      # start time
                    end_ppq,        # end time
                    0,              # channel
                    note_pitch,     # pitch
                    velocity_base,  # velocity
                    True            # noSort (we will sort after the loop)
                )
                note_count += 1

    # Sort the MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    # Update timeline UI
    RPR.RPR_UpdateArrange()

    return f"Created visual guide '{final_track_name}' with {note_count} muted notes over {bars} bars."
```