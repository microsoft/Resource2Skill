### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Locked MIDI Canvas Generator

* **Core Musical Mechanism**: This pattern generates a "Scale Canvas"—a MIDI item prepopulated with muted guide notes for every single pitch within a specified musical scale across all octaves. By leveraging REAPER's "Hide unused note rows" action, the MIDI Editor visually collapses, hiding all out-of-key notes and effectively turning the Piano Roll into a custom diatonic grid.

* **Why Use This Skill (Rationale)**: Composing in unfamiliar scales or complex modes (like Whole Tone, Dorian, or Harmonic Minor) can be visually confusing on a standard chromatic piano roll. By inserting muted notes and hiding empty rows, we encode the *music theory directly into the UI*. It physically prevents you from clicking "wrong" notes, freeing your mind to focus purely on rhythmic syncopation and melodic contour rather than overthinking scale intervals.

* **Overall Applicability**: This is incredibly useful during the initial composing or beat-making phase. It works for writing complex arpeggios, building dense chord voicings in electronic music, or exploring exotic scales for cinematic scores. Instead of relying on the tutorial's downloaded MIDI templates, this skill dynamically generates the correct template for any scale and tempo instantly.

* **Value Addition**: Compared to a blank MIDI clip, this skill automatically maps out the full frequency spectrum of a chosen scale, mutes the setup data so it won't trigger your synths, and automates the UI layout to give you a pristine, scale-locked creative environment. 

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Muted guide notes are placed precisely at `0.0` (the very beginning of the item) with a short 1/8th note duration.
  - Because they are muted, they do not interrupt the timing or groove of the actual music you will compose. 

* **Step B: Pitch & Harmony**
  - The script calculates all pitches (0-127) for the provided `key` and `scale`.
  - Included scales map the intervals (e.g., Major: 0, 2, 4, 5, 7, 9, 11; Whole Tone: 0, 2, 4, 6, 8, 10).
  - Every valid diatonic pitch across all 10 octaves is inserted into the MIDI item.

* **Step C: Sound Design & FX**
  - The generated MIDI notes are explicitly set with the `muted = True` flag.
  - Velocity is set to `1` as a fail-safe, ensuring they are virtually invisible to the audio engine.

* **Step D: Mix & Automation**
  - The core "automation" here is triggering REAPER's UI actions:
    1. Unselect all items to avoid cross-contamination.
    2. Select the new canvas item.
    3. Open it in the Active MIDI Editor.
    4. Run `Action 40452` ("View: Hide unused and unnamed note rows") to collapse the piano roll.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Generating the scale notes | `RPR_MIDI_InsertNote` with `muted=True` | Creates the underlying data required to trick the MIDI editor into registering the rows as "used" without triggering sound. |
| Collapsing the Piano Roll | `RPR_MIDIEditor_OnCommand(40452)` | Matches the tutorial's exact workflow by automating the REAPER UI, saving the user from clicking through the action list. |
| Dynamic Scale Math | Python Dictionary Lookups | Replaces the need for the tutorial's static, downloaded MIDI template files, making the tool universal and self-contained. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly recreates the tutorial's core hack (using muted notes to hide rows) and improves upon it by eliminating the need for external template files, calculating the scales mathematically on the fly.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Canvas",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale-Locked MIDI Canvas in the current REAPER project.
    Inserts muted guide notes for every pitch in the scale and hides unused rows.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, whole_tone, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (not really used here as notes are muted).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the scale canvas.
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

    # Normalize inputs
    safe_key = key.capitalize() if len(key) == 1 else key[0].upper() + key[1:].lower()
    root_pitch = NOTE_MAP.get(safe_key, 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    final_track_name = f"{safe_key} {scale.replace('_', ' ').title()} Canvas"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", final_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate position for guide notes (short 1/8th note at the very beginning)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (60.0 / bpm) * 0.5)

    # === Step 4: Insert Muted Guide Notes ===
    note_count = 0
    for octave in range(11):  # 0 to 10 to cover 0-127 MIDI range
        for interval in intervals:
            pitch = root_pitch + (octave * 12) + interval
            if 0 <= pitch <= 127:
                # InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
                RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, 1, False)
                note_count += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate UI to Hide Unused Rows ===
    # Unselect all items to ensure we only open the one we just created
    RPR.RPR_Main_OnCommand(40289, 0)
    
    # Select our new canvas item
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) 
    
    # Trigger "View: Hide unused and unnamed note rows" in the active MIDI Editor
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)

    return f"Created '{final_track_name}' with {note_count} muted guide notes over {bars} bars. Unused piano roll rows have been collapsed to match the scale."
```