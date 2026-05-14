### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale Guide Template Generator (Piano Roll Constraint Workflow)

* **Core Musical Mechanism**: Diatonic/Scale Constraint Visualization. The pattern here is not a specific song element, but rather a powerful MIDI editor workflow technique. By populating a MIDI item with all the available notes of a specific scale (and muting them), and then triggering REAPER's "Hide unused note rows" action, the piano roll is visually transformed. It entirely removes out-of-key note rows, essentially turning the MIDI editor into a custom diatonic grid. 

* **Why Use This Skill (Rationale)**: This technique relies on the music theory concept of diatonicism. When composing complex melodies, basslines, or chord progressions, visual clutter from non-scale notes can slow down the creative process and lead to out-of-key mistakes. By completely hiding the "wrong" notes, producers can visually focus on the scale degrees, easily program parallel thirds/sixths, and explore advanced modes (like the Whole Tone scale or Mixolydian) without having to memorize their intervals on the traditional piano layout.

* **Overall Applicability**: This is universally applicable when starting a new section of a track (e.g., writing a complex arpeggio, a bassline, or a melody) in a specific key or mode. It is especially useful for producers lacking deep keyboard proficiency or when utilizing non-Western/exotic scales where the traditional white/black key piano roll paradigm is confusing.

* **Value Addition**: Instead of manually copy-pasting notes and building macros to map out a scale as shown in the video, this skill automatically computes the exact pitches of a chosen scale across 7 octaves, generates the muted reference notes, opens the item, and triggers the UI action in a single click.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Duration**: The reference notes are placed from the start of the item and stretched across the entire item length.
  - **Purpose**: Because the notes span the whole item, no matter where you zoom or scroll in the timeline, the row is considered "used" by REAPER, ensuring the layout remains locked.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (e.g., C Major, D Dorian, G Whole Tone).
  - **Pitch Selection**: The code computes every scale degree within the selected key and propagates it across multiple octaves (MIDI notes 12 to 108+).

* **Step C: Sound Design & FX**
  - **Muting**: Crucially, the generated MIDI notes are set to `muted = True` via the API. They produce no sound and will not trigger VST instruments; they exist purely as UI layout anchors.

* **Step D: Mix & Automation**
  - **UI Automation**: The script opens the newly generated MIDI item in the built-in MIDI editor and programmatically triggers command `40452` ("View: Hide unused note rows").

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | Python Math & List Iteration | Safely computes exact MIDI pitches based on scale intervals without manual placement. |
| Background Reference | `RPR_MIDI_InsertNote` (`muted=True`) | Muting the notes allows them to act as structural scaffolding for the MIDI editor without producing audio. |
| UI Customization | `RPR_MIDIEditor_OnCommand` | Replicates the exact core goal of the video: collapsing the piano roll to *only* show the specified scale. |

> **Feasibility Assessment**: 100% — The script perfectly automates the somewhat tedious manual workflow demonstrated in the video (drawing notes, copying them across octaves, muting them, and hitting the hide action).

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
    Create Scale Guide Template in the current REAPER project.
    Generates a track with muted notes defining a specific scale,
    then automatically hides unused note rows in the MIDI editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, whole_tone, etc.).
        bars: Number of bars the guide item should span.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., 'octaves' to define spread).

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
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Validate parameters
    if key not in NOTE_MAP: 
        key = "C"
    if scale not in SCALES: 
        scale = "major"
        
    octaves = kwargs.get("octaves", 8)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Label the track clearly so the user knows it's a structural guide
    full_track_name = f"{track_name} ({key} {scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Generate Muted Scale Notes ===
    root_pitch = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    notes_added = 0

    # Start from Octave 0/1 (MIDI note ~12) to avoid negative sub-bass errors
    for oct_offset in range(1, 1 + octaves):
        base_midi = (oct_offset * 12) + root_pitch
        
        for interval in scale_intervals:
            midi_pitch = base_midi + interval
            if midi_pitch <= 127:
                # Insert note with muted flag = True
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    True,           # MUTED (Critical for workflow)
                    start_ppq,      # start time
                    end_ppq,        # stretch across whole item
                    0,              # channel
                    int(midi_pitch),# pitch
                    velocity_base,  # velocity
                    False           # noSort
                )
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate MIDI Editor UI ===
    # Unselect all items in project, then select only our new item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open selected item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "View: Hide unused note rows" inside the active MIDI editor
    active_editor = RPR.RPR_MIDIEditor_GetActive()
    if active_editor:
        # Command ID 40452: View: Hide unused note rows
        RPR.RPR_MIDIEditor_OnCommand(active_editor, 40452)

    return f"Created '{full_track_name}' scale guide with {notes_added} muted notes spanning {octaves} octaves. Unused rows hidden."
```