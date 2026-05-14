### 1. High-level Design Pattern Extraction

> **Skill Name**: Diatonic MIDI Editor Scale Guide

* **Core Musical Mechanism**: This pattern leverages a specific REAPER workflow hack to visually "snap" the Piano Roll to any musical scale. By creating a muted MIDI item containing every note of a target scale across multiple octaves, and then using REAPER's "Hide unused note rows" action, the MIDI Editor transforms into a custom diatonic grid.

* **Why Use This Skill (Rationale)**: Drawing MIDI in a traditional chromatic piano roll can be visually overwhelming and prone to "wrong note" errors if you aren't thoroughly trained in music theory. By hiding notes outside the scale, composing complex diatonic chord extensions (like 9ths and 11ths), arpeggios, and melodies becomes as simple as drawing within the visible lanes. The video specifically highlights the Whole Tone scale for its "dreamy" cinematic quality—which is normally hard to visualize, but trivialized by this setup.

* **Overall Applicability**: This is a setup/utility pattern useful at the start of any composition phase. It is especially powerful for EDM, Pop, and Cinematic scoring where staying strictly in key (or instantly accessing complex modes like Dorian or Whole Tone) accelerates the writing process.

* **Value Addition**: Instead of manually creating, copying, and saving MIDI files for every scale in every key as shown in the video, this code programmatically generates the exact reference block on demand, perfectly aligned to your project's chosen key and scale.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Rhythmic placement is arbitrary for a guide track, but the notes are generated as 1 quarter note in duration at the very start of the region to be visible but unobtrusive.
  - The Media Item itself is muted (`B_MUTE`) so these reference notes never produce audio, even if an instrument is accidentally added to the track.

* **Step B: Pitch & Harmony**
  - The script uses music theory lookup tables to build the specific scale (Major, Minor, Dorian, Whole Tone, etc.) starting from the defined root note.
  - The scale is duplicated across 5 octaves (MIDI pitches ~24 to ~84) to cover the typical compositional range of basslines, chords, and melodies.

* **Step C: Sound Design & FX**
  - No instruments or FX are applied. This is a purely structural/visual tool.

* **Step D: Mix & Automation**
  - None required.

* **Workflow Execution**: Once this item is created, you open it in the MIDI editor alongside your actual instrument tracks, and trigger the action `View: Hide unused note rows` (Action ID `40453` or `40452`).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale generation | MIDI note insertion | Requires discrete programmatic control to calculate and stack scale degrees across octaves. |
| Non-destructive reference | Muted Media Item | Muting the item (`B_MUTE`) guarantees the guide notes won't trigger VSTs while still being recognized by REAPER's MIDI editor display logic. |

> **Feasibility Assessment**: 100% reproduction. The script entirely bypasses the manual labor shown in the video (creating custom actions to copy notes diatonically, exporting MIDI files, organizing a folder) by generating the exact requested scale block programmatically.

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
    Creates a muted MIDI item containing all notes of a specified scale across multiple octaves.
    When opened in the MIDI Editor alongside your composition, you can use the action
    'View: Hide unused note rows' to snap the piano roll strictly to this scale.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars the item spans.
        velocity_base: Velocity of the guide notes (does not affect audio since muted).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated scale guide.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10], # Emphasized in the video for dreamy sequences
    }

    # Resolve scale and root
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)
    scale_key = scale.lower()
    scale_intervals = SCALES.get(scale_key, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    full_track_name = f"{track_name} ({key.upper()} {scale_key.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    # MUTE THE ITEM: Essential so the guide notes don't accidentally play
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Populate Scale Notes ===
    # Make the notes 1 quarter-note long at the very beginning
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (60.0 / bpm))

    note_count = 0
    # Generate across octaves 2 through 6 (standard composition range)
    for octave in range(2, 7):
        base_midi = (octave + 1) * 12 + root_pitch # +1 mapping (e.g., octave 2 = MIDI 36 for C)
        for interval in scale_intervals:
            pitch = base_midi + interval
            if pitch <= 127:
                # Insert note logic
                # args: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created guide track '{full_track_name}' with {note_count} muted notes. (Tip: Open this in MIDI Editor and trigger 'View: Hide unused note rows')"
```