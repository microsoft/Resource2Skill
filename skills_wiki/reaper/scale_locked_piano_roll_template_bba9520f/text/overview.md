### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale-Locked Piano Roll Template

* **Core Musical Mechanism**: Diatonic/Scale Restriction Workflow. The tutorial demonstrates a technique to visually restrict the MIDI editor to only show notes belonging to a specific scale. By creating a template MIDI item containing every pitch of a scale across all octaves and utilizing REAPER's "Hide unused note rows" action, the piano roll effectively transforms into a custom, scale-locked grid.

* **Why Use This Skill (Rationale)**: This workflow removes the visual clutter of out-of-key notes (the "wrong" notes). By collapsing the piano roll into a purely diatonic space, intervals become strictly contextual to the key, making it significantly easier to draw chord progressions, build extended harmonies (like 7ths and 9ths, which appear as simple stacked every-other-row patterns), and write rapid, in-key melodies. 

* **Overall Applicability**: Essential for rapid composition in genres with strict diatonic boundaries (Pop, Trap, EDM) or when experimenting with exotic/symmetric scales (like the Whole Tone scale featured in the video) where the standard black/white key layout is visually counterintuitive. 

* **Value Addition**: Instead of manually building a scale template by copying and pasting intervals octave by octave (as shown in the tutorial), this script programmatically calculates the math for *any* key and scale, generates the guide notes, mutes them so they don't produce unwanted audio, and automatically triggers the REAPER MIDI Editor actions to hide the unused rows instantly.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythmic placement of the guide notes is irrelevant to the sound, as they will be muted. They are stretched across the entire duration of the template item (default 1 bar) so they act as solid visual guide rails.

* **Step B: Pitch & Harmony**
  - **Pitches**: 0-127 (Full MIDI range).
  - **Math**: Evaluates `(note_number - root_offset) % 12`. If the remainder matches a semitone interval in the selected scale's interval list, the note is generated.
  - **Scales featured/supported**: Major, Minor, Dorian, Whole Tone (divides the octave symmetrically in 6), Pentatonics, etc.

* **Step C: Sound Design & FX**
  - **Muted Attributes**: All template notes are initialized with the `muted = True` flag. This satisfies the "Hide unused note rows" action criteria without triggering the track's virtual instrument.

* **Step D: Mix & Automation**
  - No mix routing required. The script automates the UI (MIDI Editor view) rather than audio parameters.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | Python Modulo Math (`% 12`) | Accurately calculates any scale across all 10 MIDI octaves programmatically. |
| Guide rails | `RPR_MIDI_InsertNote` (muted) | Muted notes trick the MIDI editor into keeping the row visible while remaining completely silent. |
| Piano Roll lockdown | `RPR_MIDIEditor_OnCommand(40452)` | Automates the exact "Hide unused note rows" action highlighted by the creator. |

> **Feasibility Assessment**: 100% reproduction. The script achieves the exact workflow hack described in the 4-minute tutorial in a fraction of a second, without requiring the user to download external MIDI template files.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Scale-Locked Piano Roll Template in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, whole_tone, dorian, etc.).
        bars: Number of bars for the template item.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]  # Featured in the tutorial
    }

    # Format inputs
    key_upper = key.upper()
    root_offset = NOTE_MAP.get(key_upper, 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track explicitly to show the scale being used
    full_track_name = f"{track_name} ({key} {scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create Template MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate PPQ (ticks) bounds for the notes
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    # Generate all valid diatonic notes across the 0-127 MIDI spectrum
    valid_notes_inserted = 0
    for midi_note in range(128):
        if (midi_note - root_offset) % 12 in scale_intervals:
            # Insert the note.
            # Crucial feature: muted=True. This allows the row to stay visible when 
            # "Hide Unused Rows" is triggered, but prevents the note from making sound.
            # Signature: RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, midi_note, velocity_base, True)
            valid_notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Automate MIDI Editor UI ===
    # Unselect all media items in project
    RPR.RPR_Main_OnCommand(40289, 0) 
    
    # Select only our new template item
    RPR.RPR_SetMediaItemSelected(item, True)
    
    # Open selected item in MIDI Editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Get active MIDI Editor
    midi_editor = RPR.RPR_MIDIEditor_GetActive()
    if midi_editor:
        # Trigger Action 40452: "View: Hide unused note rows"
        RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40452)

    return f"Created '{full_track_name}' locked piano roll with {valid_notes_inserted} hidden guide notes."
```