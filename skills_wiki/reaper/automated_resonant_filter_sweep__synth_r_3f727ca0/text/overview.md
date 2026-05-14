### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Resonant Filter Sweep (Synth Riser)

* **Core Musical Mechanism**: This pattern applies a time-based automation envelope to an equalizer's frequency parameter. A sustained, harmonically rich chord is held while a resonant EQ band (or low-pass filter) sweeps from a low frequency to a high frequency over a set number of bars.
* **Why Use This Skill (Rationale)**: Automating a filter or EQ band is a fundamental technique for creating tension, movement, and transitions in music. By sweeping a boosted resonant peak across the frequency spectrum, you dynamically highlight different harmonics of the underlying synth chord. This psychoacoustically builds anticipation, making it a perfect device for buildups, risers, and song section transitions (e.g., moving from a verse into a heavy chorus). 
* **Overall Applicability**: Essential in EDM, pop, cinematic scoring, and hip-hop. It is used to generate risers, evolving pads, and transition effects without needing dedicated audio samples.
* **Value Addition**: Compared to a static synth patch, this skill encodes the production concept of *macro-modulation over time*. It demonstrates how to programmatically extract an FX parameter envelope in REAPER and draw precise geometric automation curves, executing perfectly timed sweeps that match the project grid.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: A single continuous event lasting exactly the length of the specified `bars`.
  - **Rhythm**: No internal rhythmic syncopation; relies entirely on the continuous motion of the automation curve.
* **Step B: Pitch & Harmony**
  - **Voicing**: Generates a thick 7th chord (Root, 3rd, 5th, 7th) derived from the specified `key` and `scale`.
  - **Function**: Provides a dense harmonic bed (fundamental plus many overtones) so the sweeping EQ filter has plenty of frequency content to act upon.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured with added saw and square waves for a buzzy, overtone-rich timbre.
  - **Processing**: `ReaEQ` inserted immediately after the synth. Band 2 is used as a sweeping bandpass/resonant peak filter (Gain boosted, Q narrowed).
* **Step D: Mix & Automation**
  - **Automation Envelope**: The core of the technique. An automation curve is attached to ReaEQ Band 2's Frequency parameter.
  - **Curve**: Sweeps linearly from `0.1` (around 100Hz) to `0.9` (around 15kHz) over the exact duration of the MIDI item.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Harmonic Bed | MIDI note insertion | Allows dynamic generation of chords locked to the user's key/scale parameters. |
| Synth Tone | FX Chain (`ReaSynth`) | Stock REAPER synth; tweaking shape parameters ensures a rich harmonic spectrum. |
| Parameter Automation | `RPR_GetFXEnvelope` & `RPR_InsertEnvelopePoint` | Exactly reproduces the tutorial's core lesson: taking a plugin parameter (EQ frequency) and driving it with an automation envelope over time. |

> **Feasibility Assessment**: 100% reproducible. The script uses completely native REAPER plugins (ReaSynth, ReaEQ) and the standard ReaScript automation API to programmatically recreate the exact kind of filter sweep automation demonstrated at the end of the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Riser",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Resonant Filter Sweep (Synth Riser) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the sweep will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated automation and MIDI item.
    """
    import reaper_python as RPR

    # === Step 1: Initialize Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Take ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Music Theory & Chord Generation ===
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

    root_midi = 48 + NOTE_MAP.get(key, 0)  # Anchor around C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # Build a thick 4-note chord (1st, 3rd, 5th, 7th scale degrees)
    chord_degrees = [0, 2, 4, 6]
    pitches = []
    for degree in chord_degrees:
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        pitch = root_midi + (octave_shift * 12) + scale_intervals[scale_idx]
        pitches.append(pitch)

    # Insert sustained MIDI notes
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for pitch in pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (ReaSynth & ReaEQ) ===
    # 5a. Add ReaSynth and mix in square/saw waves for harmonic richness
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.6)  # Saw shape
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5)  # Pulse shape

    # 5b. Add ReaEQ and prepare Band 2 as a resonant peak
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # In ReaEQ: Param 3 is Band 2 Freq, Param 4 is Gain, Param 5 is Q
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 4, 0.75)  # Boost Gain (creates the resonance)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 5, 0.8)   # Narrow Q

    # === Step 6: Parameter Automation ===
    # Retrieve/create the automation envelope for ReaEQ Band 2 Frequency (Param index 3)
    # The 4th argument 'True' tells REAPER to create the envelope if it doesn't exist
    env_freq = RPR.RPR_GetFXEnvelope(track, eq_idx, 3, True)

    # Insert envelope points to sweep from low to high
    # Values range from 0.0 (20Hz) to 1.0 (24kHz)
    start_val = 0.15  # Approx ~150 Hz
    end_val = 0.85    # Approx ~10 kHz
    
    # Point 1: Start of item
    RPR.RPR_InsertEnvelopePoint(env_freq, 0.0, start_val, 0, 0.0, False, True)
    # Point 2: End of item
    RPR.RPR_InsertEnvelopePoint(env_freq, item_length, end_val, 0, 0.0, False, True)

    # Sort envelope points to finalize the curve
    RPR.RPR_Envelope_Sort(env_freq)

    return f"Created '{track_name}' Riser: Automated EQ sweep across a {key} {scale} chord over {bars} bars at {bpm} BPM."
```