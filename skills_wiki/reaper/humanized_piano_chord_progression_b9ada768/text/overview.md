### 1. High-level Design Pattern Extraction

**Skill Name**: Humanized Piano Chord Progression

* **Core Musical Mechanism**: The central musical technique demonstrated in this tutorial is **velocity and timing humanization**. Rather than drawing block chords where every note triggers at the exact same time and maximum velocity (the "machine-gun" effect), the pattern introduces micro-variations. By adjusting the MIDI CC Velocity lane to form dynamic arcs (crescendos/decrescendos) and randomizing the individual note impacts, a synthesized or sampled instrument sounds remarkably more realistic.
* **Why Use This Skill (Rationale)**: Acoustic instruments, especially the piano, are highly dynamic. A pianist naturally hits the bass note with more weight, voices the outer melody notes clearer than the inner harmony notes, and plays with a slight rolling/strumming imperfection (notes don't trigger on the exact same millisecond). Emulating this through velocity curves and slight timing offsets bridges the gap between robotic MIDI data and an emotional, organic performance.
* **Overall Applicability**: Essential for any acoustic sampled instrument—pianos, orchestral strings, acoustic guitars, and drum kits. This technique shines in intros, breakdowns, and emotional ballads where the piano is exposed and exposed to critical listening. 
* **Value Addition**: Compared to a blank MIDI clip or a flat, snapped-to-grid chord progression, this skill encodes organic performance theory: chord voicings with an isolated bass note, micro-timing offsets (strumming), and arc-based velocity humanization.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically around 120 BPM.
  - **Rhythm**: Sustained block chords lasting 1 full bar each. 
  - **Humanization**: Note starts are staggered by a few milliseconds (10-20ms) from bottom to top to emulate a natural hand strike.
* **Step B: Pitch & Harmony**
  - **Progression**: A foundational diatonic progression (e.g., I - V - vi - IV).
  - **Voicing**: A split voicing demonstrated in the video. The root note is played an octave lower (Bass), accompanied by a triad an octave higher (Root, Third, Fifth). 
* **Step C: Sound Design & FX**
  - **Instrument**: The tutorial uses a "Grand Piano" VST. To ensure reproducibility without third-party plugins, we utilize REAPER's stock **ReaSynth**, shaping its ADSR envelope to mimic a piano/pluck decay (fast attack, moderate decay, low sustain, long release).
* **Step D: Mix & Automation**
  - **Velocity Automation (CC)**: Instead of uniform velocities (e.g., all 127), a macro curve is applied across the bars (creating movement). Additionally, micro-variations are applied per note (e.g., the bass note is consistently harder, the third is softer).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Chord Voicing** | MIDI note insertion | Allows programmatic stacking of Bass + Triad notes based on scale parameters. |
| **Velocity & Timing Humanization** | Math + MIDI note insertion | By calculating micro-offsets and a sine-wave velocity curve in Python, we directly implement the CC lane dragging shown in the video. |
| **Piano Timbre** | FX chain (ReaSynth ADSR) | Modifying ReaSynth's envelope parameters provides a stock-REAPER approximation of a piano's pluck/decay contour. |

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a Humanized Piano Chord Progression in the current REAPER project.
    Generates chords with staggered micro-timing and curved/randomized velocities 
    to emulate realistic human performance as demonstrated in the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C").
        scale: Scale type ("major", "minor", etc.).
        bars: Number of bars to generate (1 chord per bar).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    import math
    import random

    # 1. Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":          [0, 2, 4, 5, 7, 9, 11],
        "minor":          [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian":         [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":     [0, 2, 4, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.upper(), 0)

    def get_pitch(octave: int, degree: int) -> int:
        """Calculate MIDI pitch for a given scale degree (0-indexed)."""
        oct_shift = degree // len(scale_intervals)
        rem = degree % len(scale_intervals)
        return (octave + oct_shift) * 12 + root_val + scale_intervals[rem]

    # Standard Pop/Classical Progression: I - V - vi - IV (represented as 0-indexed scale degrees)
    progression = [0, 4, 5, 3]

    # 2. Track Setup
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth and shape ADSR to sound like a piano pluck
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 2: Attack (very fast)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.01)
    # Param 3: Decay (moderate)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.6)
    # Param 4: Sustain (low, to allow decay to shine)
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.15)
    # Param 5: Release (long enough for natural fade)
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.5)

    # 3. Item & Take Setup
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 4. Generate Notes with Humanization
    notes_created = 0

    for i in range(bars):
        deg = progression[i % len(progression)]
        
        # Calculate pitches (Bass down one octave, Triad up one octave)
        bass_pitch  = get_pitch(3, deg)
        root_pitch  = get_pitch(4, deg)
        third_pitch = get_pitch(4, deg + 2)
        fifth_pitch = get_pitch(4, deg + 4)
        
        # Base times for this chord
        start_time_sec = i * bar_length_sec
        # Leave a tiny 10% gap so chords don't bleed into each other entirely
        end_time_sec = start_time_sec + (bar_length_sec * 0.9)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)

        # Macro humanization: Create an overarching dynamic curve over the bars (like dragging the CC lane)
        # Sine wave peaking in the middle of the progression
        curve_factor = math.sin((i / max(1, bars - 1)) * math.pi) 
        macro_vel_offset = int(curve_factor * 15) # Up to +15 velocity at the peak
        
        # Assemble notes with micro-timing (strum) and micro-velocity (voicing weights)
        chord_notes = [
            # (pitch, timing_offset_sec, velocity_modifier)
            (bass_pitch,  0.000,  10),  # Bass hits exactly on beat, hardest
            (root_pitch,  0.015,  0),   # Root hits slightly after, normal vel
            (third_pitch, 0.025, -12),  # Inner third hits later, softer
            (fifth_pitch, 0.035, -5)    # Outer fifth hits last, medium-soft
        ]

        for pitch, time_offset, vel_mod in chord_notes:
            # Strum timing
            note_start_time = start_time_sec + time_offset
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            
            # Combine base, macro curve, structural voicing weight, and random human slop
            human_slop = random.randint(-4, 4)
            final_vel = velocity_base + macro_vel_offset + vel_mod + human_slop
            # Clamp velocity between 1 and 127
            final_vel = max(1, min(127, int(final_vel)))
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, final_vel, False
            )
            notes_created += 1

    # Sort the MIDI stream after insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} humanized piano notes over {bars} bars at {bpm} BPM in {key} {scale}."
```