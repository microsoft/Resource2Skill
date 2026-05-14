### 1. High-level Design Pattern Extraction

> **Skill Name**: Scale Guide Generator (Piano Roll Filter)

* **Core Musical Mechanism**: This technique uses a custom MIDI item filled with muted notes across all octaves to forcefully define the visible grid in REAPER's Piano Roll. By combining this "guide" item with the "View: Hide unused note rows" action, the MIDI editor is restricted strictly to the notes of a chosen scale. 
* **Why Use This Skill (Rationale)**: While REAPER features a "Key Snap" function at the bottom of the MIDI editor, standard Key Snap still displays all 12 chromatic rows (graying out the non-diatonic ones). By using muted guide notes and hiding unused rows, you completely collapse the Piano Roll into a purely diatonic grid. This visually removes the possibility of hitting wrong notes, making it incredibly fast to draw complex chords and melodies in any scale (like Whole Tone, Harmonic Minor, or Custom Modes).
* **Overall Applicability**: This is a foundational composition workflow enhancement. It is especially useful for producers creating intricate MIDI sequences, arpeggios, or rapid chord progressions in genres like EDM, Neo-Soul, or Cinematic music, where staying locked into a specific modality is crucial.
* **Value Addition**: The original tutorial shows a manual, tedious process of inserting notes, copying them up and down octaves, and saving them as MIDI file templates. This script automates that entire process algorithmically—instantly generating a perfect, mathematically correct scale guide across all 128 MIDI notes for any specified root and scale.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Item Length**: Generated dynamically (e.g., 4 bars). 
  - **Note Duration**: The generated muted notes stretch seamlessly across the entire length of the item so they are always present no matter where you are editing within that timeline.
  
* **Step B: Pitch & Harmony**
  - **Scale Generation**: The script calculates all valid pitches for the requested scale (e.g., Major, Minor, Dorian, Whole Tone) across octaves -1 to 9.
  - **Muted Pitch Placement**: Every diatonic note is inserted into the MIDI take with the `muted` property set to `True`. This ensures they act as architectural guides for the Piano Roll UI without generating unwanted sound.

* **Step C: Sound Design & FX**
  - A basic instance of **ReaSynth** is loaded on the track at a low volume. Because the guide notes are muted, the synth remains silent until the user actively draws their own active notes into the grid.

* **Step D: Mix & Automation**
  - The track is automatically colored light blue to denote it as a "Guide Track".
  - **Required User Action**: After the script runs, the user must double-click the MIDI item to open the MIDI Editor, and trigger the action **"View: Hide unused note rows"** (MIDI Editor Action ID `40452`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale calculation | Pitch Class Math | Algorithmically generates any scale without needing external MIDI files as suggested in the video. |
| Guide note creation | `RPR_MIDI_InsertNote` with `muted=True` | Matches the tutorial's exact trick: the notes exist to dictate the UI layout but won't trigger the synthesizer. |
| Item generation | `RPR_CreateNewMIDIItemInProj` | Creates a self-contained template item that can be looped or extended in the Arrange view. |

> **Feasibility Assessment**: 100% reproducible. The script completely replaces the manual workflow demonstrated in the video, generating a perfect, ready-to-use scale guide item directly on the timeline.

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
    Creates a 'Scale Guide' MIDI item filled with muted notes across all octaves.
    When opened in the MIDI Editor alongside the 'Hide unused note rows' action, 
    it visually collapses the piano roll to only show notes in the target scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C', 'F#', 'Bb').
        scale: Scale type ('major', 'minor', 'harmonic_minor', 'whole_tone', etc.).
        bars: Number of bars to generate for the guide item.
        velocity_base: Base MIDI velocity (100).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{key} {scale.capitalize()} Guide", True)
    
    # Set track color to a distinct light blue to identify it as a guide
    color = RPR.RPR_ColorToNative(100, 150, 255) | 0x1000000
    RPR.RPR_SetTrackColor(track, color)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    cursor_pos = RPR.RPR_GetCursorPosition()
    item = RPR.RPR_CreateNewMIDIItemInProj(track, cursor_pos, cursor_pos + item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos + item_length)

    # === Step 4: Calculate & Insert Muted Notes ===
    # Format the key safely (e.g., 'c#' -> 'C#')
    clean_key = key.capitalize() if len(key) == 1 else key[0].upper() + key[1:].lower()
    root_pitch_class = NOTE_MAP.get(clean_key, 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    valid_notes = []
    # MIDI note numbers range roughly from octaves -1 to 9 (0 to 127)
    for octave in range(-1, 10): 
        for interval in scale_intervals:
            note = ((octave + 1) * 12) + root_pitch_class + interval
            if 0 <= note <= 127:
                valid_notes.append(note)

    # Insert notes (muted = True) spanning the entire item length
    for note in valid_notes:
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, True, start_ppq, end_ppq, 0, note, velocity_base, True)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add basic Synth ===
    # Adds a synth so that when the user draws active notes over the guide grid, they can hear them.
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth volume slightly lower to prevent harsh peaks
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.1) 

    return f"Created '{key} {scale.capitalize()} Guide' track with {len(valid_notes)} muted notes over {bars} bars. Open in MIDI Editor and trigger 'View: Hide unused note rows'."
```