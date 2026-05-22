### 1. High-level Design Pattern Extraction

**Skill Name**: Notation-Ready Rhythmic Arpeggio

* **Core Musical Mechanism**: The tutorial demonstrates capturing a human-played keyboard performance (an ascending and descending arpeggio/scale fragment) and using REAPER's Musical Notation editor (`Alt+4` or `View -> Mode: musical notation`) to automatically interpret the raw MIDI data into standard sheet music. The core musical element here is a structured rhythmic pulse (8th notes) and clear harmonic intent (a chord arpeggiated over a 4/4 grid) that allows the software to accurately infer the time signature and beat grid.

* **Why Use This Skill (Rationale)**: Arpeggios break a static chord into a linear sequence of notes. When played with a consistent rhythmic grid (like straight 8th or 16th notes), they provide both harmonic context and rhythmic drive. From a workflow perspective, keeping MIDI notes strictly quantized or deliberately articulated ensures that when switching to Notation View, the generated sheet music is clean, readable, and accurately reflects the musical intent without cluttered rests or tied grace notes. The tutorial also highlights velocity sensitivity, which adds dynamic expression to an otherwise robotic sequence.

* **Overall Applicability**: This pattern is highly applicable for generating foundational synth arpeggios, classical piano motifs, or baseline structural melodies that can be easily handed off to session musicians reading sheet music. It is ideal for electronic music intros, cinematic ostinatos, and demonstrating REAPER's notation parsing capabilities.

* **Value Addition**: Compared to a blank MIDI clip, this skill encodes a dynamic, musically correct arpeggiated sequence (Root-3rd-5th-Octave) derived strictly from a provided scale and key, complete with velocity accents on the downbeats. It produces a perfect foundational item for viewing in the Notation Editor.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, adaptable BPM (defaulting to 120).
  - **Grid**: Straight 8th notes (two notes per beat).
  - **Articulation**: Slightly detached (staccato-legato) with note lengths at 90% of the grid division to ensure clean notation without overlapping note ties.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (defaults to C Major).
  - **Progression**: A standard up-and-down arpeggio over 8 notes: Root, 3rd, 5th, Octave, 5th, 3rd, Root, sub-octave 7th. 
  - **Dynamics**: Accented velocities on the strong beats (beats 1 and 3) to mimic the human "velocity sensitivity" noted by the tutorial author.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` to provide immediate auditory feedback for the MIDI notes.

* **Step D: Mix & Automation**
  - No advanced mixing or automation is required for the core notation concept.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Arpeggio Generation | MIDI note insertion | Allows precise mathematical placement of pitches, lengths, and velocities based on scale degrees, simulating the keyboard performance. |
| Sound generation | FX chain (`ReaSynth`) | Provides an immediate, stock-REAPER sound source so the pattern is audible without needing third-party VSTs. |
| Notation readability | Timing and Length offsets | Setting lengths to exactly 90% of the PPQ grid division ensures the Notation Editor parses clean 8th notes without tying overlapping data. |

**Feasibility Assessment**: 100% reproducible. While we cannot trigger the REAPER GUI action to force the window into Notation Mode automatically (as that requires user interface context), the generated MIDI item perfectly reproduces the musical material the tutorial author recorded to demonstrate the feature. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Notation Arpeggio",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 2,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a mathematically precise 8th-note arpeggio in the current REAPER project, 
    designed to be viewed cleanly in REAPER's Musical Notation Mode.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
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
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_GetNumTracks()
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument ===
    # Using standard ReaSynth to ensure sound is produced out-of-the-box
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)

    # === Step 5: Music Theory Math & Note Insertion ===
    base_midi_pitch = 60 + NOTE_MAP.get(key, 0) # Start around middle C
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_scale_note(degree):
        """Calculates exact MIDI pitch based on a given scale degree index."""
        octave_shift = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return base_midi_pitch + (octave_shift * 12) + scale_intervals[idx]

    # Arpeggio pattern degrees: Root, 3rd, 5th, Octave, 5th, 3rd, Root, 7th(octave down)
    degrees = [0, 2, 4, 7, 4, 2, 0, -1] 
    
    # Adjust for pentatonic scales which have fewer notes
    if len(scale_intervals) < 7:
        degrees = [0, 1, 2, 4, 2, 1, 0, -1]

    ticks_per_quarter = 960
    ticks_per_8th = ticks_per_quarter // 2
    
    for b in range(bars):
        for i in range(8):
            start_pos = (b * beats_per_bar * ticks_per_quarter) + (i * ticks_per_8th)
            # 90% length prevents overlap, making the Notation mode much cleaner to read
            end_pos = start_pos + int(ticks_per_8th * 0.9) 
            
            pitch = get_scale_note(degrees[i])
            
            # Accent velocity on strong beats (0 and 4, which equal beats 1 and 3)
            current_velocity = velocity_base + 25 if i % 4 == 0 else velocity_base
            current_velocity = min(127, max(1, current_velocity))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_pos, end_pos, 0, pitch, current_velocity, False)

    # Sort internal MIDI data structure
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with a notation-friendly arpeggio over {bars} bars at {bpm} BPM in {key} {scale}"
```