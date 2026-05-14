### 1. High-level Design Pattern Extraction

> **Skill Name**: Humanized Rhythmic Chords

* **Core Musical Mechanism**: The defining technique demonstrated in the tutorial is the programmatic entry of MIDI notes followed by detailed manipulation of the **Velocity CC Lane**. The pattern consists of repeating rhythmic chords where the dynamics (velocity) are shaped over time, creating a "ramp" or crescendo effect, while maintaining alternating accents (strong downbeats, weaker upbeats) to simulate human performance. 
* **Why Use This Skill (Rationale)**: Static, perfectly quantized MIDI with uniform velocity sounds robotic and lifeless. By introducing alternating macro-accents (groove theory) and a linear crescendo (tension building), the chord progression gains momentum and psychoacoustic depth. This transforms a rigid block of notes into a moving, breathing musical element.
* **Overall Applicability**: Excellent for intro synth pads, pulsing piano chords in house/EDM, rhythmic string stabs in pop, or any scenario where a repetitive harmonic element needs to build energy over several bars leading into a new section.
* **Value Addition**: Instead of a flat block of pasted notes, this skill mathematically encodes the exact "velocity ramping" and "humanization" workflow taught in the MIDI editor tutorial, applying it automatically to any scale or key.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid:** 8th note pulses.
  - **Duration:** Notes are slightly staccato (playing for 85% of an 8th note length) to ensure rhythmic separation and a "bouncy" feel.
  - **Time Signature & Length:** 4/4 time, spanning across 4 bars.
* **Step B: Pitch & Harmony**
  - **Voicing:** A root position triad (Root, Third, Fifth) based on the chosen key and scale, layered with an additional root bass note an octave lower for weight.
  - **Scale mapping:** Dynamically calculates scale intervals (Major, Minor, Dorian, etc.) to ensure chords stay strictly diatonic to the specified key.
* **Step C: Sound Design & FX**
  - **Instrument:** `ReaSynth` is used as a lightweight placeholder to guarantee immediate sound playback, replacing the third-party Grand Piano VST shown in the video. 
  - Volume is reduced natively via FX parameters to prevent clipping when multiple chord notes trigger simultaneously.
* **Step D: Mix & Automation**
  - **Velocity Automation:** The script implements a dual-layer velocity calculation:
    1. A persistent alternating accent (Downbeats get +15 velocity, upbeats get -15).
    2. A linear ramp (crescendo) that smoothly pushes the overall velocity base up by 40 points from the start of bar 1 to the end of bar 4.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chords & Rhythm | MIDI Note Insertion (`RPR_MIDI_InsertNote`) | Provides precise, sample-accurate control over pitch, length, and placement. |
| Velocity Ramp | Mathematical PPQ iteration | Accurately reproduces the manual "click and drag" CC lane velocity ramp demonstrated in the video editor. |
| Sound generation | Track FX (`ReaSynth`) | Native, completely self-contained REAPER plugin; requires no external sample libraries. |

> **Feasibility Assessment**: 95% — The code perfectly reproduces the MIDI entry, arrangement, and velocity lane manipulation workflows taught in the tutorial. The only deviation is substituting the user's specific third-party "Grand Piano" plugin with REAPER's native `ReaSynth` to guarantee execution safety.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Create Humanized Rhythmic Chords with a velocity crescendo ramp.

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
        Status string describing what was created.
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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_GetNumTracks()
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Native Synth Placeholder) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower ReaSynth volume to avoid clipping with dense chords (Param 0 = Volume)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.1) 

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Determine Pitch Strategy ===
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    chord_pitches = []
    octave = 4 
    
    # Build a diatonic root position triad (1st, 3rd, 5th degree of the scale)
    for i in [0, 2, 4]:
        idx = i % len(scale_intervals)
        oct_offset = i // len(scale_intervals)
        chord_pitches.append(root_val + scale_intervals[idx] + (octave + oct_offset) * 12)
        
    # Add a root bass note an octave lower for depth
    chord_pitches.append(root_val + scale_intervals[0] + (octave - 1) * 12)

    # === Step 6: Insert Notes with Velocity Automation ===
    total_8th_notes = bars * beats_per_bar * 2
    note_length_beats = 0.5 
    
    notes_added = 0
    for step in range(int(total_8th_notes)):
        start_beat = step * note_length_beats
        # Make the note slightly staccato (plays for 85% of its length)
        end_beat = start_beat + (note_length_beats * 0.85) 
        
        start_time = (60.0 / bpm) * start_beat
        end_time = (60.0 / bpm) * end_beat
        
        # Convert absolute time to MIDI PPQ (Pulses Per Quarter note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Calculate Humanized Velocity:
        # 1. Accent downbeats (+15), soften upbeats (-15)
        # 2. Linear crescendo ramp over the entire length (rises by 40 over time)
        accent = 15 if step % 2 == 0 else -15
        ramp_progress = step / max(1, (total_8th_notes - 1))
        
        # Start slightly below base to allow room for the ramp
        vel = int((velocity_base - 10) + accent + (ramp_progress * 40))
        vel = max(1, min(127, vel)) # Clamp to valid MIDI range
        
        for pitch in chord_pitches:
            # noSort=True during the loop for performance
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            notes_added += 1
            
    # Sort the MIDI note buffer after all insertions
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes across {bars} bars at {bpm} BPM, featuring a programmatic velocity crescendo."
```