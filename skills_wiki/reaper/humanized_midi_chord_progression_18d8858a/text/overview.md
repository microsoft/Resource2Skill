# Humanized MIDI Chord Progression

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Humanized MIDI Chord Progression

* **Core Musical Mechanism**: Transforming rigid, robotic MIDI programming into a realistic, human-like performance through micro-timing deviations (un-snapped editing) and velocity contouring (CC lane drawing). The pattern takes basic block chords and applies velocity curves and slight temporal offsets to mimic a real keyboard player's touch.

* **Why Use This Skill (Rationale)**: When MIDI notes are perfectly quantized to the grid and set to maximum velocity (127), the result sounds synthetic and lifeless. Real musicians naturally strike the downbeats slightly harder, roll their chords slightly (not all fingers hit exactly at the same millisecond), and play the bass/root note heavier than the upper voicings. By encoding these micro-variations and velocity "slopes," psychoacoustic realism is achieved, making digital instruments sit much better in a mix.

* **Overall Applicability**: Essential for piano, electric piano, orchestral strings, and acoustic drum programming. It shines in genres that require a live, organic feel, such as Neo-Soul, Lo-Fi Hip Hop, Pop, and Cinematic scoring.

* **Value Addition**: Compared to drawing static blocks in a piano roll, this skill automatically generates a full four-chord progression (I-V-vi-IV) equipped with the tutorial's exact humanization techniques: velocity staggering per chord tone, macro-velocity slopes over time, and grid-agnostic note lengths.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4 at a default 120 BPM.
  - **Rhythm**: Whole-note block chords falling on the downbeats.
  - **Humanization**: Note start and end times deviate randomly by +/- 15ms. This simulates the `Shift + Drag` un-snapped length adjustment technique demonstrated in the tutorial.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Fully parametric (defaults to C Major). 
  - **Progression**: Generates a standard pop/soul progression: I - V - vi - IV.
  - **Voicing**: 4-note wide voicings. The root note is doubled an octave lower to provide a strong fundamental bass, while the triad (root, 3rd, 5th) sits in the midrange.

* **Step C: Sound Design & FX**
  - **Instrument**: The tutorial utilizes a Grand Piano VST. For stock REAPER reproducibility, `ReaSynth` is used and configured with a fast attack and moderate decay to mimic a piano/pluck transient.
  - **Space**: `ReaVerbate` is added to place the dry synthesized piano into an acoustic room environment, further enhancing realism.

* **Step D: Mix & Automation**
  - **Velocity Automation**: Simulates the click-and-drag slanted lines in the CC Velocity lane. The base note is struck the hardest, with the 3rd and 5th struck softer. A macro sine-wave offset is applied across the bars to create a natural ebb and flow in dynamics.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord construction & timing | `RPR_MIDI_InsertNote` | Allows programmatic calculation of micro-timing offsets (un-snapped) and exact PPQ (pulses per quarter note) positioning. |
| Velocity curves | Math functions + MIDI Velocity | Reproduces the CC velocity lane "slopes" demonstrated in the tutorial without requiring complex envelope point manipulation. |
| Piano Sound | `RPR_TrackFX_AddByName` (ReaSynth + ReaVerbate) | Ensures the skill works out-of-the-box using stock plugins, adjusting synth parameters to approximate an electric piano. |

> **Feasibility Assessment**: 85% reproduction. The code perfectly reproduces the core MIDI humanization techniques (velocity slopes, un-snapped timings, chord copying) taught in the video. The remaining 15% is the literal "Grand Piano" third-party VST, which is approximated here using stock REAPER plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Humanized MIDI Chord Progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (loops a 4-chord progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import math
    import random
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure Scale & Harmony ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Generate an extended scale across 10 octaves to easily build chords
    ext_scale = []
    for oct in range(10):
        for interval in scale_intervals:
            ext_scale.append(interval + 12 * oct)
            
    # Anchor our progression around C3/C4 (MIDI note 48)
    anchor_note = 48 + root_val
    base_idx = 0
    for i, n in enumerate(ext_scale):
        if n >= anchor_note:
            base_idx = i
            break

    # I - V - vi - IV progression
    degrees = [0, 4, 5, 3]

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    notes_created = 0

    # === Step 5: Insert Humanized Notes ===
    for b in range(bars):
        degree = degrees[b % len(degrees)]
        start_time = b * bar_length_sec
        end_time = (b + 1) * bar_length_sec
        
        # 4-note voicing: Bass (root - 1 oct), Root, 3rd, 5th
        chord_pitches = [
            ext_scale[base_idx + degree - len(scale_intervals)], 
            ext_scale[base_idx + degree],                        
            ext_scale[base_idx + degree + 2],                    
            ext_scale[base_idx + degree + 4]                     
        ]
        
        for i, pitch in enumerate(chord_pitches):
            # 5a. Timing Humanization (Simulating Shift+Drag un-snapping)
            note_start = start_time + random.uniform(-0.015, 0.015)
            note_end = end_time - 0.05 + random.uniform(-0.015, 0.015)
            if note_start < 0: note_start = 0.0
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end)
            
            # 5b. Velocity Humanization (Simulating CC Lane drawing)
            # Bass is loudest, upper notes are softer
            if i == 0:
                vel = velocity_base + random.randint(0, 8)
            elif i == 1:
                vel = velocity_base - 10 + random.randint(-5, 5)
            elif i == 2:
                vel = velocity_base - 15 + random.randint(-5, 5)
            else:
                vel = velocity_base - 20 + random.randint(-5, 5)
                
            # Macro slope over the bars (Sine wave curve)
            slope_offset = int(12 * math.sin(b * math.pi / 2))
            vel += slope_offset
            
            # Clamp velocity
            vel = max(1, min(127, vel))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add FX Chain for Piano-like Sound ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth to sound like a muted electric piano pluck
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.0)  # Attack: instant
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.3)  # Decay: moderate
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.2)  # Sustain: low (plucky)
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.4)  # Release: natural fade
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.1)  # Square mix: low
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.4)  # Saw mix: medium
    
    # Add Space
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 1, 0, 0.15) # Wet mix
    RPR.RPR_TrackFX_SetParam(track, 1, 1, 0.9)  # Dry mix
    RPR.RPR_TrackFX_SetParam(track, 1, 2, 0.6)  # Room size

    return f"Created '{track_name}' with {notes_created} humanized chord notes over {bars} bars at {bpm} BPM in {key} {scale}"
```