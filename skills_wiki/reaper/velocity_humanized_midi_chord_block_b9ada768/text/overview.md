### 1. High-level Design Pattern Extraction

> **Skill Name**: Velocity-Humanized MIDI Chord Block

* **Core Musical Mechanism**: The core pattern demonstrated in this tutorial is the transition from a rigid, robotic MIDI input to a dynamic, realistic performance using **Velocity Humanization**. Instead of hardcoding all MIDI notes to a flat, maximum velocity (e.g., 127), the velocity CC lane is manipulated so that individual notes within a chord hit at slightly different intensities. 
* **Why Use This Skill (Rationale)**: When a real pianist plays a chord, their fingers never strike the keys with exactly the same force. By varying the velocities of notes within a block chord, you emulate human playing dynamics, reducing the unnatural "machine-gun" effect. This also changes the harmonic balance of the chord, as the velocity usually drives a synthesizer's filter envelope (cutoff) or a sampler's layer selection, resulting in a richer, evolving timbre.
* **Overall Applicability**: Essential for piano/keys, orchestral strings, and organic synth pads. It is the fundamental difference between an amateur-sounding MIDI loop and a professional, grooving arrangement.
* **Value Addition**: This skill replaces flat, static MIDI blocks with a script that dynamically calculates and slightly randomizes the velocity of every individual note in a diatonic chord progression, bringing immediate life to stock virtual instruments.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid:** 4-bar progression, with chords changing exactly on the downbeat of each bar.
  - **Tempo:** 120 BPM (adjustable).
  - **Length:** Sustained block chords lasting the entire measure.
* **Step B: Pitch & Harmony**
  - **Key/Scale:** Parametric (e.g., C Major).
  - **Progression:** A foundational I - vi - IV - V diatonic progression. 
  - **Voicings:** Standard triads (Root, 3rd, 5th).
* **Step C: Sound Design & FX**
  - **Instrument:** Since the "Grand Piano" VSTi from the tutorial is an external plugin, this script falls back to REAPER's native `ReaSynth` to ensure zero external dependencies while accurately reproducing the MIDI data.
* **Step D: Mix & Automation**
  - **Velocity Automation (Crucial):** Individual note velocities are modulated via a Gaussian/random spread around a base velocity (e.g., base 100 ± 15) to simulate the tutorial's CC lane adjustments.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| MIDI Chord Creation | `RPR_MIDI_InsertNote` | Precise programmatic control over pitch and timing inside the MIDI item. |
| Velocity Humanization | Python `random` module | Replicates the tutorial's "click and drag" manual variation in the velocity lane by computationally randomizing each note's strike force. |
| Instrument Setup | `RPR_TrackFX_AddByName` | Loads ReaSynth automatically so the generated MIDI produces immediate audio. |

> **Feasibility Assessment**: 90% — The script perfectly recreates the MIDI editing, track setup, chord construction, and velocity humanization described in the tutorial. The only missing element is the specific third-party Grand Piano VST, which is replaced with a stock synth for guaranteed execution.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a diatonic chord progression with humanized MIDI velocities.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (1 chord per bar).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR
    import random

    # === Theory / Lookup Tables ===
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
    }

    # Normalize inputs
    key_upper = key.upper()
    root_val = NOTE_MAP.get(key_upper, 0)
    # Start around C3 (MIDI note 48) for chords
    root_midi = 48 + root_val 
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Common diatonic progression: I - vi - IV - V (0-indexed scale degrees)
    progression = [0, 5, 3, 4] 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup FX (Stock Synth) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower ReaSynth volume slightly to prevent harsh clipping on block chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Using CreateNewMIDIItemInProj ensures proper MIDI take initialization
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    notes_created = 0

    # === Step 5: Generate Chords and Humanize Velocities ===
    for i in range(bars):
        # Loop the progression if bars > length of progression
        degree = progression[i % len(progression)]
        
        # Calculate pitches for a 3-note triad
        chord_pitches = []
        for interval in [0, 2, 4]:
            scale_index = (degree + interval) % len(scale_intervals)
            octave_shift = (degree + interval) // len(scale_intervals)
            pitch = root_midi + scale_intervals[scale_index] + (octave_shift * 12)
            chord_pitches.append(pitch)

        # Timing for this chord
        start_time = i * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        # Insert notes with Humanized Velocity
        for pitch in chord_pitches:
            # Emulate the "click and drag" variance from the tutorial (±18 range)
            velocity_variance = random.randint(-18, 18)
            humanized_vel = max(1, min(127, velocity_base + velocity_variance))
            
            # Slightly offset the start time (strum effect) by 0-10 ticks to add realism
            strum_offset = random.randint(0, 15)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq + strum_offset, end_ppq, 
                0, int(pitch), int(humanized_vel), True
            )
            notes_created += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized MIDI notes across {bars} bars at {bpm} BPM in {key} {scale}."
```