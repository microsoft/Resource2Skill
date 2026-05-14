# Sound Design Variation Generator (Parametric Mutation)

## Analysis

### 1. High-level Design Pattern Extraction

**Skill Name**: Sound Design Variation Generator (Parametric Mutation)

* **Core Musical Mechanism**: The tutorial demonstrates a rapid sound-effect mutation workflow. A base composite sound (e.g., an impact, kick, or gunshot) is duplicated multiple times, and each instance is subjected to micro-randomizations across four specific axes: **Pitch**, **Pan**, **Time/Rate** (duration), and **Position** (timing offset).
* **Why Use This Skill (Rationale)**: Human hearing detects exact repetition instantly—a phenomenon known as the "machine-gun effect." By applying bounded random deviations to a base sound, producers simulate the organic variations found in acoustic instruments and real-world sound effects. This prevents ear fatigue and creates a sense of spatial and tonal depth.
* **Overall Applicability**: Essential for game audio and UI sound design (generating multiple footstep, gunshot, or impact variations). In music production, this pattern is highly effective for generating organic hi-hats, glitchy IDM micro-edits, or evolving percussion loops where no two hits sound exactly the same.
* **Value Addition**: Instead of manually tweaking parameters for dozens of audio clips (or relying on paid scripts like LKC Variator), this skill programmatically generates a sequence of MIDI/synth-based variations. It encodes the concept of "controlled randomness" into a reusable generator.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: Variations are spaced out sequentially (one per bar) to allow for easy rendering/export.
  - **Position Mutation**: A micro-timing offset of ±50ms is applied to the start of each event, mimicking a humanized or randomized trigger.
  - **Duration Mutation**: The length of the synthesized note is randomized (e.g., 100ms to 400ms) to emulate time-stretching and playrate variations.

* **Step B: Pitch & Harmony**
  - **Pitch Mutation**: Instead of a static note, each variation selects a random degree from the chosen scale/key, optionally jumping octaves. This creates a cluster of tonally related but distinct sounds.

* **Step C: Sound Design & FX**
  - **Base Instrument**: A punchy synthesized pluck/impact using `ReaSynth` (blending Sine and Square waves with a fast decay/zero sustain).
  - **Velocity Mutation**: The amplitude/velocity of each trigger is randomized.

* **Step D: Mix & Automation**
  - **Pan Mutation**: Each variation receives a randomized MIDI CC 10 (Pan) message, throwing the sound slightly left or right in the stereo field (±40%).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Base Sound Generation** | FX Chain (ReaSynth) | Synthesizes a base sound effect without relying on external sample libraries. |
| **Variation Duplication** | Looped MIDI Item Creation | Generates `N` isolated items spaced evenly on the timeline, mirroring the video's workspace. |
| **Parameter Mutation** | MIDI Note & CC Manipulation | Natively randomizes Pitch (Note number), Pan (CC 10), Timing (Item position), and Rate (Item duration) to emulate the paid "LKC Variator" plugin. |

> **Feasibility Assessment**: 85% — The video relies on paid plugins (NVK Create, LKC Variator) and external wav sample libraries. To make this 100% reproducible on any machine, the script replaces the sample layers with a native ReaSynth impact patch, and replaces the Variator plugin with a native Python randomization engine. The resulting workflow and parametric variations are functionally identical to the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SFX_Variations",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # In this context, 'bars' determines the number of variations to generate
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a sequence of mutated sound effect variations in the current REAPER project.
    Mimics the "Variator" workflow by randomizing Pitch, Pan, Length, and Timing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of variations to generate (1 per bar).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
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

    # === Step 1: Set Tempo & Environment ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    bar_length_sec = (60.0 / bpm) * 4.0
    
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 48  # C3 base
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 2: Create Track & Synth Setup ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth to generate our base SFX layer
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a punchy, aggressive pluck/impact
    # Normalized parameters: 0:Vol, 1:Tune, 2:Square, 3:Saw, 6:Attack, 7:Decay, 8:Sustain, 9:Release
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.8)   # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.4)   # Mix in Square wave for bite
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.0)   # Instant Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 7, 0.15)  # Fast Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 8, 0.0)   # No Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 9, 0.1)   # Short Release
    
    # Add EQ to shape the sound
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Give it some low-end punch
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 0, 0.6) # Low shelf gain boost

    # === Step 3: Generate Mutated Variations ===
    # Emulates the LKC Variator workflow shown in the video
    
    for i in range(bars):
        # Base position: middle of the bar to ensure item doesn't overlap zero
        base_time = (i + 0.5) * bar_length_sec
        
        # 1. POSITION MUTATION (Timing Offset ±50ms)
        pos_offset = random.uniform(-0.05, 0.05)
        start_time = base_time + pos_offset
        
        # 2. RATE/TIME MUTATION (Duration variation)
        duration = random.uniform(0.1, 0.4)
        end_time = start_time + duration
        
        # 3. PITCH MUTATION (Random scale degree & octave)
        interval = random.choice(scale_intervals)
        octave_shift = random.choice([-12, 0, 12])
        pitch = min(127, max(0, root_pitch + interval + octave_shift))
        
        # 4. PAN MUTATION (Random panning via CC10 ±40%)
        pan_val = min(127, max(0, 64 + random.randint(-40, 40)))
        
        # 5. VELOCITY MUTATION
        vel = min(127, max(1, velocity_base + random.randint(-25, 25)))

        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
        take = RPR.RPR_GetActiveTake(item)
        
        # Convert times to PPQ for MIDI insertion
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Insert Note
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
        
        # Insert Pan Control Change (CC 10)
        RPR.RPR_MIDI_InsertCC(take, False, False, start_ppq, 0xB0, 10, pan_val, 0)
        
        # Sort MIDI events
        RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' containing {bars} mutated SFX variations at {bpm} BPM."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (with intentional bounded randomization)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, it accurately mimics the programmatic mutation of audio properties via MIDI parameters).
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?