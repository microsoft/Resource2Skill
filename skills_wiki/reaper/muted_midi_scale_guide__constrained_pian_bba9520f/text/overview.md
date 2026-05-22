### 1. High-level Design Pattern Extraction

> **Skill Name**: Muted MIDI Scale Guide (Constrained Piano Roll Setup)

* **Core Musical Mechanism**: This technique uses a custom MIDI item populated with *muted* notes covering every valid pitch of a specified scale across all octaves. By opening this item and triggering REAPER's "Hide unused note rows" action, the Piano Roll is visually constrained to only show diatonic notes for that specific key and scale.
* **Why Use This Skill (Rationale)**: Composing in the Piano Roll can be visually overwhelming, especially when working outside of C Major / A minor or utilizing symmetrical scales (like the Whole Tone scale mentioned in the video). By hiding non-diatonic notes, you effectively turn your MIDI editor into a perfectly tuned instrument where it is impossible to click a "wrong" note. The muted notes serve as a structural backbone without interfering with your project's audio.
* **Overall Applicability**: Essential for melodic and harmonic composition, particularly for producers who are not traditionally trained keyboardists. It is highly useful when writing complex orchestral arrangements, cinematic scores, or electronic genres that rely heavily on specific modes (e.g., Dorian for Deep House, Phrygian Dominant for Trap, Whole Tone for dreamy cinematic transitions). 
* **Value Addition**: Instead of manually drawing and duplicating scale notes octave-by-octave and saving them in a folder (as the host demonstrates), this skill fully automates the creation of a "Scale Guide" track. It programmatically computes the scale, generates the muted notes, opens the MIDI editor, and snaps the view in one click.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythmic timing is irrelevant here. The item is simply generated to be 1 bar long (or the requested length) starting at `0.0`. 
  - The notes stretch the entire duration of the item to ensure they are easily visible at any zoom level.

* **Step B: Pitch & Harmony**
  - The technique applies to *any* scale. The script calculates intervals dynamically based on the requested root note (e.g., C = 0, C# = 1) and the scale type (Major, Minor, Dorian, Whole Tone, etc.).
  - It iterates over the entire MIDI pitch range (0 to 127). If `(pitch - root) % 12` is found in the scale's interval array, a muted note is inserted.

* **Step C: Sound Design & FX**
  - No instruments or FX are added. The notes are explicitly injected with the `muted` flag set to `True` so they do not trigger any synths or samplers if an instrument is later added to the track.

* **Step D: Mix & Automation (if applicable)**
  - UI Automation: The true power of this technique is the execution of REAPER Action **40452** (`View: Hide unused and unnamed note rows`) inside the MIDI editor, immediately configuring the user's workspace.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale Note Generation | MIDI note insertion | Allows programmatic generation of every valid diatonic note across all 10 octaves. |
| Non-destructive setup | Muted note parameter | Setting `muted=True` in `RPR_MIDI_InsertNote` ensures the guide item makes no sound, acting purely as UI data. |
| UI View Constraining | `MIDIEditor_LastFocused_OnCommand` | Automates the exact REAPER action the host uses (`40452`) to snap the piano roll to the chosen scale. |

> **Feasibility Assessment**: 100% reproduction. The code completely automates the manual workaround demonstrated by the host, achieving the Reddit user's exact original request ("choose a scale from a list and hide all note rows not in that scale").

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
    Create a Muted MIDI Scale Guide in the current REAPER project and snap the Piano Roll.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Length of the guide item.
        velocity_base: Base MIDI velocity (irrelevant as notes are muted, but required for API).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Format inputs
    key = key.upper()
    scale = scale.lower()
    
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
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'"
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'"

    root_val = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track after the scale so it's clearly identifiable
    full_track_name = f"{key} {scale.title()} - {track_name}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create the MIDI item natively
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Get PPQ (Pulses Per Quarter Note) positions for start and end
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # === Step 4: Populate with Muted Scale Notes ===
    note_count = 0
    for pitch in range(128):
        # Check if this pitch belongs to the scale
        if (pitch - root_val) % 12 in scale_intervals:
            # Insert note: (take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            # We set muted = True, selected = False, noSort = True (will sort after loop)
            RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateItemInProject(item)

    # === Step 5: Open in MIDI Editor & Hide Unused Rows ===
    # Unselect all items in the project to isolate our new item
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open the item in the built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0) # Item: Open in built-in MIDI editor
    
    # Trigger "View: Hide unused and unnamed note rows" in the active MIDI Editor
    # Action ID 40452
    RPR.RPR_MIDIEditor_LastFocused_OnCommand(40452, False)

    return f"Created '{full_track_name}' guide track with {note_count} muted notes. Piano roll constrained."
```