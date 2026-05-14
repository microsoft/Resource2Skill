### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Velocity Swell Chords

* **Core Musical Mechanism**: Modulating MIDI velocity smoothly across a sequence of repeated notes or chords. Instead of every note hitting at a static velocity (which sounds robotic), the velocities are "drawn" in a curve (a crescendo leading into a decrescendo) over the duration of the phrase.
* **Why Use This Skill (Rationale)**: This technique simulates the natural phrasing and dynamic variation of a human performance. In acoustic instruments (like the piano shown in the tutorial), hitting keys harder changes not just the volume, but the harmonic content and attack characteristic of the sound. Sweeping the velocities adds emotional movement, tension, and release to an otherwise repetitive ostinato.
* **Overall Applicability**: Essential for any programmed MIDI performance involving repetition—piano stabs, string ostinatos, synth plucks, hi-hat patterns, or snare rolls. It bridges the gap between quantized "mouse-clicked" MIDI and organic-sounding arrangements.
* **Value Addition**: Compared to a basic MIDI clip with flat velocities, this skill encodes the concept of *musical phrasing*. It automatically maps a sine-wave curve to the note velocities to generate a realistic swell, saving the producer from manually drawing CC automation curves.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Rhythm**: 1/8th note repeated pulses.
  - **Length**: Configurable, defaults to 4 bars.
  - **Articulation**: Slightly staccato (note length is ~90% of the grid division) to ensure distinct rhythmic attacks.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (e.g., C Major).
  - **Voicing**: A simple root position triad (Root, 3rd, 5th) constructed from the selected scale, placed in the 3rd/4th octave (e.g., C3-E3-G3).

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` to represent the piano/keys.
  - **Space**: Stock `ReaVerbate` added to give the stabs some acoustic space and sustain, masking the robotic decay of raw synth notes.

* **Step D: Mix & Automation**
  - **Velocity Curve**: A mathematical sine curve applied to the MIDI note velocities, starting around 40% of the peak, swelling to the `velocity_base` maximum at the midpoint, and decaying back down by the end of the item.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Repetition | Programmatic loop calculating timing in seconds/beats | Allows for precise placement of 1/8th notes scaled to the BPM |
| Note insertion & quantization | `RPR_MIDI_InsertNote` with PPQ conversions | Standard REAPER API methodology for robust MIDI sequencing |
| Velocity Swelling | `math.sin()` applied to velocity | Perfectly reproduces the "click and drag a ramp" technique demonstrated in the tutorial's CC lane |
| Sound generation | `ReaSynth` + `ReaVerbate` | Provides a built-in, lightweight tonal sound source with acoustic tail |

> **Feasibility Assessment**: 100% reproduction of the core musical principle. While the tutorial user selects a third-party "Grand Piano" VST, we reproduce the exact MIDI data layout, rhythmic spacing, and velocity curve automation using stock REAPER instruments to guarantee it works in any environment.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Dynamic Swell Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create 'Dynamic Velocity Swell Chords' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Peak MIDI velocity (0-127) for the height of the swell.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created element.
    """
    import math
    import reaper_python as RPR

    # === Music theory lookup tables ===
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Chord Data ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Base octave (e.g., C3 = 48)
    base_midi = 48 + root_val
    
    # Root position triad: Root, 3rd, 5th
    # If the scale has less than 5 notes (e.g. pentatonic), just take safe indices
    i3 = 2 if len(scale_intervals) > 2 else 1
    i5 = 4 if len(scale_intervals) > 4 else 2
    chord_intervals = [scale_intervals[0], scale_intervals[i3], scale_intervals[i5]]
    chord_notes = [base_midi + interval for interval in chord_intervals]

    # === Step 5: Insert MIDI Notes with Velocity Swell ===
    division_beats = 0.5  # 1/8th notes
    num_notes = int((beats_per_bar * bars) / division_beats)
    note_len_beats = division_beats * 0.85  # Slightly staccato for defined attacks

    max_vel = min(127, max(10, velocity_base))
    min_vel = max(10, int(max_vel * 0.4)) # Swell starts/ends at 40% of peak
    
    notes_added = 0
    for i in range(num_notes):
        start_beats = i * division_beats
        end_beats = start_beats + note_len_beats
        
        start_sec = start_beats * (60.0 / bpm)
        end_sec = end_beats * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        # Calculate velocity swell (sine wave half-cycle over the sequence)
        progress = i / max(1, (num_notes - 1))
        swell_multiplier = math.sin(progress * math.pi)
        velocity = int(min_vel + (max_vel - min_vel) * swell_multiplier)
        
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(
                take,
                False,      # selected
                False,      # muted
                start_ppq,  # startppqpos
                end_ppq,    # endppqpos
                0,          # chan
                note,       # pitch
                velocity,   # vol
                False       # noSort
            )
            notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add FX Chain (Synth & Reverb) ===
    # Add simple synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add verb to give the stabs a realistic acoustic tail
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 0, 0.15) # Wet level
    RPR.RPR_TrackFX_SetParamNormalized(track, verb_idx, 1, 0.90) # Dry level

    return f"Created '{track_name}' with {notes_added} notes across {bars} bars at {bpm} BPM, peaking at velocity {max_vel}."
```