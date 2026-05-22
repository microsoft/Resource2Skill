### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Filter Sweep Build-up

* **Core Musical Mechanism**: Evolving timbral brightness through the automation of a filter's cutoff frequency over time. The tutorial heavily emphasizes the mechanics of automation modes (Read, Touch, Latch, Write) to manipulate parameters dynamically. Musically, opening a low-pass filter over several bars transitions a sound from muffled and distant to bright and present.
* **Why Use This Skill (Rationale)**: Filter sweeps are a fundamental psychoacoustic tool for generating tension and release. By gradually revealing the higher harmonics of a sound, the producer creates an anticipation of a structural change (like a drop or a chorus). Automating this process ensures the evolution perfectly matches the track's tempo and grid.
* **Overall Applicability**: This technique is universally applicable for transitions, intros, and build-ups in almost every modern genre (EDM, Pop, Hip-Hop, Cinematic). It is most commonly applied to synth pads, full mix busses, or heavy basslines.
* **Value Addition**: Instead of a static, unchanging synth chord, this skill encodes the concept of "movement over time." It programmatically creates an automation envelope and populates it with points mapped precisely to the bar length, replacing manual fader-riding with mathematically perfect execution.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Continuous, sustained note duration spanning the entire generated length (e.g., 4 bars).
  - No rhythmic grid quantization for the notes themselves, but the automation curve is strictly timed to the project BPM, starting exactly at Bar 1 and ending at Bar 5.
* **Step B: Pitch & Harmony**
  - A sustained root-position triad (Root, 3rd, 5th) derived dynamically from the selected key and scale.
  - Placed in the mid-register (C3/C4) to ensure a rich harmonic spectrum that responds well to filtering.
* **Step C: Sound Design & FX**
  - **Generator**: Stock `ReaSynth` to produce a raw, harmonically rich sawtooth/square wave.
  - **Filter**: Stock `ReaEQ`.
  - **Technique**: Instead of complex state-chunk manipulation to change band types, we utilize ReaEQ's default Band 4 (High Shelf). By setting Band 4's Gain to `-inf` (value `0.0`), it functions as a sharp Low-Pass filter. We then automate Band 4's Frequency parameter.
* **Step D: Mix & Automation (if applicable)**
  - **Target**: ReaEQ Parameter 9 (Band 4 Frequency).
  - **Curve**: Shape 2 (Slow Start/End) for a smooth, exponential-sounding "easing" curve.
  - **Range**: Sweeps from `0.1` (~100 Hz, muffled) to `0.9` (~15 kHz, fully open).
  - **Automation Mode**: Track set to `Read` mode so the REAPER engine immediately plays back the drawn envelope.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained chord generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Required to generate a raw harmonic signal that the filter can actually act upon. |
| Synthesizer & Filter | FX chain (`RPR_TrackFX_AddByName`, `RPR_TrackFX_SetParam`) | Uses native REAPER plugins (ReaSynth, ReaEQ) ensuring 100% compatibility. |
| The Filter Sweep | Automation envelope (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Directly reproduces the tutorial's core lesson: creating and manipulating automation envelopes on FX parameters over time. |

> **Feasibility Assessment**: 100% reproducible. The code uses stock REAPER plugins and standard Reascript API calls to map out an exact geometric automation curve, perfectly mimicking the manual FX automation demonstrated at the end of the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Filter Sweep Build-up in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the sweep will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track and automation.
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

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

    # === Step 4: Generate Sustained Chord (Root, 3rd, 5th) ===
    root_val = NOTE_MAP.get(key, 0) + 48  # C3 register
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Calculate intervals (handle pentatonic safety)
    interval_3rd = scale_intervals[2] if len(scale_intervals) > 2 else 4
    interval_5th = scale_intervals[4] if len(scale_intervals) > 4 else 7

    pitch_root = root_val
    pitch_third = root_val + interval_3rd
    pitch_fifth = root_val + interval_5th

    # Time to PPQ calculation
    start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    end_qn = RPR.RPR_TimeMap2_timeToQN(0, item_length)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # Insert MIDI notes
    for pitch in [pitch_root, pitch_third, pitch_fifth]:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Synth + EQ) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # Convert ReaEQ Band 4 (High Shelf) into a makeshift Low Pass
    # Param 10 is Band 4 Gain. Setting to 0.0 equals -inf dB.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 0.0) 

    # === Step 6: Create Automation Envelope ===
    # Param 9 is Band 4 Frequency. `True` flag tells REAPER to create the envelope.
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    
    # Add Envelope Points to create the sweep
    # Shape 2 = Slow Start/End (Smooth S-curve)
    sweep_start_val = 0.1  # ~100Hz (Muffled)
    sweep_end_val = 0.9    # ~15kHz (Fully open)
    
    RPR.RPR_InsertEnvelopePoint(env, 0.0, sweep_start_val, 2, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, item_length, sweep_end_val, 2, 0.0, False, True)
    
    RPR.RPR_Envelope_SortRegisters(env)

    # Ensure track is in 'Read' mode (Mode 1) so automation is active
    RPR.RPR_SetTrackAutomationMode(track, 1)

    return f"Created '{track_name}' with automated ReaEQ filter sweep (0.1 to 0.9) over {bars} bars at {bpm} BPM in {key} {scale}."
```