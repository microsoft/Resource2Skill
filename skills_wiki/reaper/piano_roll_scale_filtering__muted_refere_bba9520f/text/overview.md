### 1. High-level Design Pattern Extraction

> **Skill Name**: Piano Roll Scale Filtering (Muted Reference Track)

* **Core Musical Mechanism**: The tutorial demonstrates a clever workflow workaround to "Fold" the REAPER piano roll to a specific diatonic scale. By creating a MIDI item that contains every note of a specific scale across all octaves, placing it on a track, and using the MIDI Editor action `"View: Hide unused note rows"`, the piano roll collapses into a strictly diatonic grid where out-of-scale notes literally do not exist.
* **Why Use This Skill (Rationale)**: This technique turns the chromatic piano roll into a diatonic sandbox. It physically prevents the composer from drawing "wrong" notes, drastically speeding up the writing of complex melodies, dense chord voicings, and fast arpeggios. It is especially useful for navigating less familiar modes (like the Whole Tone scale highlighted in the video) without having to memorize the intervals. 
* **Overall Applicability**: Useful in all genres of MIDI composition. Whether laying down a sub-bass in a specific key, writing sprawling orchestral runs, or clicking in a rapid future-bass chord progression, restricting the visual grid to the chosen scale reduces cognitive load.
* **Value Addition**: Instead of manually drawing, duplicating, and saving MIDI files as shown in the video, this script *automates* the creation of the reference track. It mathematically computes the scale across 10 octaves and drops a muted reference item instantly into the project, ready to be used alongside your active composition.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: Any (defaults to 120 BPM, 4/4).
  - **Rhythm**: The timing is structural, not musical. A single 1-bar legato block is generated to represent the scale pitches.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Dynamically calculated. The script takes any root note (C to B) and matches it against interval arrays for Major, Minor, Dorian, Phrygian, Lydian, Mixolydian, Pentatonics, Blues, and the Whole Tone scale.
  - **Voicing**: Every valid scale degree is populated across MIDI octaves -1 to 9.
* **Step C: Sound Design & FX**
  - **Instrument**: None required.
  - **Track State**: The track is deliberately set to `Muted` (`B_MUTE = 1.0`) so the giant cluster of reference notes doesn't trigger audio or interfere with your project's mix.
* **Step D: Mix & Automation**
  - **Routing**: No special routing. It acts purely as a visual template for the MIDI Editor.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Creating the Scale Notes | `RPR_MIDI_InsertNote()` | Allows mathematically precise generation of the scale degrees across all 127 MIDI pitches without relying on external .mid files. |
| Non-destructive Reference | Track `B_MUTE` property | Muting the track ensures the reference item serves its visual purpose in the MIDI editor without causing massive audio clipping. |
| Scale Enforcement | REAPER Native Action | Once the generated item is visible in the MIDI Editor, the user simply runs REAPER's native `Hide unused note rows` action to fold the grid. |

> **Feasibility Assessment**: 100% — This script fully replicates and automates the manual workaround demonstrated in the tutorial. By running it, the user instantly obtains the "Scale MIDI" file the creator had to construct and load manually.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Reference",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a muted reference MIDI item containing all notes of a specified scale across all octaves.
    When opened in the MIDI Editor alongside an active item, running the action 
    'View: Hide unused note rows' will fold the piano roll to this exact scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars to generate the reference block.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string indicating the track and scale generated.
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
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "lydian":           [0, 2, 4, 6, 7, 9, 11],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "locrian":          [0, 1, 3, 5, 6, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
        "whole_tone":       [0, 2, 4, 6, 8, 10]
    }

    # Normalize inputs
    safe_key = key if key in NOTE_MAP else "C"
    safe_scale = scale if scale in SCALES else "major"
        
    root_pitch = NOTE_MAP[safe_key]
    scale_intervals = SCALES[safe_scale]
    
    # Calculate all valid MIDI pitches (0-127) for the selected scale
    valid_pitches = []
    for octave in range(-1, 10):
        for interval in scale_intervals:
            pitch = (octave + 1) * 12 + root_pitch + interval
            if 0 <= pitch <= 127:
                valid_pitches.append(pitch)
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Muted Reference Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{track_name}: {safe_key} {safe_scale}"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Mute the track to prevent the massive note cluster from playing audio
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_time = 0.0
    end_time = item_length
    
    # Convert absolute project time to MIDI PPQ (Pulses Per Quarter Note)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
    
    # Insert a full-length note for every single pitch in the scale
    for pitch in valid_pitches:
        # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
        
    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created muted reference track '{full_track_name}' containing {len(valid_pitches)} notes over {bars} bars at {bpm} BPM."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?