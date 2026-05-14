### 1. High-level Design Pattern Extraction

**Skill Name**: Expressive MIDI Chord Swell (Velocity Humanization)

* **Core Musical Mechanism**: The foundational technique demonstrated in this tutorial is transforming a static, robotic MIDI chord progression into a human-sounding performance using **macro-dynamic velocity curves**. Rather than letting every MIDI note hit at a default velocity of 127 (which sounds rigid and unnatural), the velocities are programmed in a continuous ramp/swell, simulating how a real pianist naturally increases and decreases striking force throughout a phrase.

* **Why Use This Skill (Rationale)**: In music theory and live performance, *dynamics* are just as important as pitch and rhythm for conveying emotion. When you draw a velocity curve (a crescendo or decrescendo) across a series of chords, it creates a sense of forward motion and breathing. Psychoacoustically, lower velocities on most virtual instruments don't just reduce volume—they also lower the cutoff frequency (less high-end harshness) and trigger softer, rounder sample layers. This prevents ear fatigue and gives your MIDI arrangements an organic, professional polish.

* **Overall Applicability**: This technique is essential for any genre relying heavily on programmed MIDI instruments, particularly cinematic orchestral arrangements, neo-soul electric pianos, ambient synth pads, and lo-fi hip-hop. It's the difference between a "demo" sound and a "finished" sound when working strictly in the box. 

* **Value Addition**: Compared to a blank MIDI clip, this skill encodes the concept of *musical phrasing*. It automatically computes a chord voicing (including a foundational bass octave) and applies a sine-wave mathematical ramp to the note velocities, creating an instant, organic dynamic swell over the generated loop.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo:** 120 BPM (as configured in the tutorial's arrangement view).
  - **Grid & Phrasing:** The tutorial highlights snapping to 16th notes but demonstrates copying/pasting chords on the quarter-note and half-note grids. 
  - **Note Duration:** Slightly staccato chords (playing for ~80% of the beat duration) to leave a brief gap, emphasizing the rhythmic pulse.

* **Step B: Pitch & Harmony**
  - **Key & Scale:** C Major is used as the prime example.
  - **Chord Voicing:** A simple root position triad (Root, 3rd, 5th) layered over a sub-octave bass note (Root - 12). For C Major, this equates to C2, C3, E3, G3.

* **Step C: Sound Design & FX**
  - **Instrument:** The tutorial uses a third-party "Grand Piano" VSTi. For guaranteed reproducibility in a blank REAPER setup, this will be replicated using `ReaSynth` configured with a fast attack and medium decay to emulate a basic piano/pluck envelope.

* **Step D: Mix & Automation**
  - **Velocity CC Lane:** This is the crux of the lesson. The velocities of the individual chord pulses are manipulated to form a curve. We will automate this by mapping a mathematical sine function across the loop to create a smooth swell (from velocity ~80 up to ~120 and back down).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Voicing | MIDI note insertion | Allows precise stacking of the triad and bass octave. |
| Pulse Rhythm | `for` loop over beats | Replicates the tutorial's copy-paste rhythmic repetition over the timeline. |
| Velocity Humanization | Mathematical sine ramp applied to the `vel` parameter | Accurately simulates the "click and drag" velocity curve shown in the CC lane, giving the performance organic movement. |
| Sound Design | ReaSynth parameters via `RPR_TrackFX_SetParam` | Ensures the track produces sound immediately without depending on external VSTs like the one shown in the video. |

> **Feasibility Assessment**: 95% reproducible. The exact third-party piano VSTi cannot be spawned unless the user has it installed, so REAPER's stock `ReaSynth` is used as a functional placeholder to prove the MIDI velocity dynamics.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Expressive Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 70,
    **kwargs,
) -> str:
    """
    Create Expressive MIDI Chord Swell (Velocity Humanization) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for the quietest part of the swell (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import math
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

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth to ensure we hear the chords
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth to have a piano-like pluck envelope so we can hear chords distinctly
    # Param 1: Attack (0 = fast), Param 2: Decay (0.5 = medium), Param 3: Sustain, Param 4: Release
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.2)
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.3)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = sec_per_beat * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Notes with Velocity Curve ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Base octave starts at MIDI 48 (C3)
    root_midi = 48 + root_val
    
    # Chord Voicing: Octave Bass, Root, 3rd, 5th
    chord_pitches = [
        root_midi - 12,                  # Bass
        root_midi,                       # Root
        root_midi + scale_intervals[2],  # 3rd
        root_midi + scale_intervals[4]   # 5th
    ]
    
    total_beats = bars * beats_per_bar
    note_duration_sec = sec_per_beat * 0.8  # Slight staccato gap between chords
    
    notes_added = 0
    
    for beat in range(total_beats):
        # Calculate dynamic velocity using a sine wave to create a natural swell
        # This replicates the "click and drag up and down" macro-dynamics shown in the tutorial
        swell_factor = math.sin(math.pi * (beat / max(1, (total_beats - 1))))
        
        # Velocity swells from `velocity_base` up to `velocity_base + 45`
        current_vel = int(velocity_base + (45 * swell_factor))
        current_vel = max(1, min(127, current_vel)) # Clamp to valid MIDI range
        
        start_time = beat * sec_per_beat
        end_time = start_time + note_duration_sec
        
        # Convert absolute time in seconds to PPQ (Pulses Per Quarter Note) for MIDI insertion
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for pitch in chord_pitches:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, current_vel, True)
            notes_added += 1

    # Sort the MIDI stream after adding notes with noSort=True
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM. Applied velocity swell peaking at center."
```