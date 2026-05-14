### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Restricted Piano Roll (Strict Diatonic Workspace)

* **Core Musical Mechanism**: Generating a full-range template of muted scale guide notes and utilizing REAPER's UI to hide non-scale notes. This essentially transforms the standard chromatic piano roll into a custom, scale-locked grid.
* **Why Use This Skill (Rationale)**: While REAPER has a built-in "Key Snap" feature, it only greys out the "wrong" notes—they are still clickable, and it's easy to accidentally place a note off-key. By physically creating muted guide notes and hiding the unused rows, you eliminate the visual clutter of out-of-scale intervals. This removes cognitive load, prevents dissonance, and forces strictly diatonic harmonic movement. As the tutorial notes, this is especially useful for symmetrical or exotic scales (like the Whole Tone scale, which provides a floaty, "flashback" cinematic sound).
* **Overall Applicability**: Rapid melodic and chordal sequencing, generative music preparation, or experimenting with unfamiliar modes (Dorian, Phrygian, Whole Tone) where your muscle memory for the keyboard might fail you.
* **Value Addition**: Automates the tedious process of writing a scale, copying it across 10 octaves, muting the notes, and triggering the specific MIDI editor actions. It instantly readies a blank, fool-proof composing canvas.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythmic grid is irrelevant for the template itself.
  - The script generates notes that are extremely short (5 ticks) at the absolute beginning of the item. This ensures they don't interfere with the user drawing new notes on top of them, while still registering as "used rows" to REAPER.
* **Step B: Pitch & Harmony**
  - Accepts any root key (`C`, `F#`, `Bb`, etc.).
  - Calculates intervals for a variety of modes (Major, Minor, Dorian, Mixolydian, Pentatonics, Blues, Whole Tone).
  - Iterates across all 128 MIDI pitches and inserts a note if it belongs to the calculated scale.
* **Step C: Sound Design & FX**
  - Notes are inserted with their `muted` property set to `True`. They will not trigger virtual instruments, serving purely as a visual scaffolding for the MIDI editor.
* **Step D: Mix & Automation**
  - The script automatically opens the MIDI Editor and triggers Action ID `40453` (`View: Hide unused note rows`) and `40466` (`View: Zoom to content`) to instantly format the workspace.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | MIDI note insertion | Math-based iteration ensures perfect pitch accuracy across all octaves without manual copying. |
| Non-intrusive template | Muted, 5-tick length notes | Muted notes still force rows to stay visible, but making them microscopic ensures they don't block the user from clicking/drawing new notes. |
| Workspace configuration | `MIDIEditor_OnCommand` | Directly executes the REAPER UI actions demonstrated in the tutorial (`Hide unused note rows`). |

> **Feasibility Assessment**: 100% reproduction. The script programmatically performs the exact workflow shown in the video (creating scale notes, duplicating them across the piano roll, and hiding unused rows), but does it instantly via Python logic rather than manual copying.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Scale-Restricted Piano Roll in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, whole_tone, etc.).
        bars: Number of bars for the empty template item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated template.
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

    # Normalize key and scale inputs
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])

    # Calculate all valid MIDI pitches for the given scale across all octaves
    valid_pitches = set()
    for octave in range(11):  # MIDI octaves 0-10
        for interval in intervals:
            pitch = (octave * 12) + root_pitch + interval
            if 0 <= pitch <= 127:
                valid_pitches.add(pitch)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    # Unselect all tracks first to ensure clean insertion
    RPR.RPR_Main_OnCommand(40297, 0) # Track: Unselect all tracks
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    formatted_scale_name = scale.replace('_', ' ').title()
    final_track_name = f"{key} {formatted_scale_name} ({track_name})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", final_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)

    # Convert start time to PPQ (ticks)
    start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    
    # Make notes microscopic (5 ticks) so they don't interfere with user drawing
    end_ppq = start_ppq + 5.0 

    # Insert muted guide notes for every valid pitch
    note_count = 0
    for pitch in valid_pitches:
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    # === Step 4: Configure MIDI Editor View ===
    # Open the item in the MIDI editor
    RPR.RPR_SetMediaItemSelected(item, True)
    RPR.RPR_Main_OnCommand(40153, 0) # Item: Open in built-in MIDI editor
    
    # Get the active MIDI editor window handle
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # Hide all rows that do not contain our generated scale notes
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40453) # View: Hide unused note rows
        # Zoom to fit the notes nicely
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40466) # View: Zoom to content

    return f"Created scale template '{final_track_name}' with {note_count} muted guide notes, unused rows hidden."
```