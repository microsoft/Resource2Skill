### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Filter Sweep (Evolving Pad / Riser)

* **Core Musical Mechanism**: The central technique is **parameter automation** over time. Instead of a static sound, a parameter (in this case, a Low Pass Filter cutoff frequency) is continuously modulated via an automation envelope. The sound begins muffled and dark, gradually opening up to reveal higher harmonics, creating a sense of forward motion and escalating energy.
* **Why Use This Skill (Rationale)**: Static synthesizers can sound lifeless. By automating the filter cutoff, you introduce "timbral rhythm" and evolutionary dynamics. From a psychoacoustic perspective, starting with a heavily low-passed signal focuses the listener on the fundamental harmony. As the filter opens, the introduction of high-frequency energy acts as an acoustic cue for building tension, which makes this pattern highly effective for transitions leading into a climax or chorus (the "drop").
* **Overall Applicability**: Essential for EDM risers, ambient music pads, cinematic transitions, and pop pre-choruses. It transforms a simple sustained chord into a complex, evolving texture.
* **Value Addition**: Compared to a static MIDI clip, this skill encodes the integration of **harmony (extended chords)** + **sound design (sawtooth harmonics)** + **mixing dynamics (automation envelopes)**. It demonstrates how to bring a track to life using REAPER's envelope system without needing external LFOs or specialized synth plugins.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Timing**: A single, sustained block over the entire requested duration (e.g., 4 or 8 bars). 
  - **Rhythm**: No internal rhythmic subdivision; the "rhythm" is purely dictated by the macro-movement of the automation curve over the bar count.
* **Step B: Pitch & Harmony**
  - **Harmony**: Uses a lush, extended 5-note voicing (Root, 3rd, 5th, 7th, 9th) based on the specified key and scale. A rich chord is necessary because a filter sweep requires abundant upper harmonics to be audible. 
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured to output bright waveforms (Sawtooth and Square mix) to ensure a dense harmonic spectrum. 
  - **Effect**: `ReaEQ` placed after the synth.
  - **Setup**: Band 1 of ReaEQ is converted from a Low Shelf to a **Low Pass Filter**.
* **Step D: Mix & Automation**
  - **Automation**: An envelope is generated for `ReaEQ` Band 1 Frequency (Parameter 0).
  - **Curve**: A linear sweep from `0.05` (very low frequency, dark) at the start of the item, to `0.85` (high frequency, bright) at the end of the item.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rich Pad Harmony | MIDI note insertion (`RPR_MIDI_InsertNote`) | Precise creation of a sustained 5-note extended chord spanning the exact time length. |
| Bright Source Tone | FX chain (`ReaSynth`) | Native REAPER synth; explicitly configured for saw/square waves to provide necessary harmonic density. |
| The Automation Sweep | Automation envelope (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Directly reproduces the tutorial's core concept: creating and drawing points on an FX parameter envelope over time. |

> **Feasibility Assessment**: 100%. The technique of assigning an automation envelope to a REAPER-native plugin (ReaEQ) and drawing a sweep maps perfectly to the ReaScript API and fully reproduces the musical concept shown in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Riser",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Filter Sweep (Evolving Pad) in the current REAPER project.

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
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # === Music Theory & Pitch Logic ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Extended 5-note chord structures (Root, 3, 5, 7, 9) built from scales
    CHORDS = {
        "major":            [0, 4, 7, 11, 14], # Maj9
        "minor":            [0, 3, 7, 10, 14], # Min9
        "harmonic_minor":   [0, 3, 7, 11, 14], # Min(maj7)9
        "dorian":           [0, 3, 7, 10, 14], # Min9
        "mixolydian":       [0, 4, 7, 10, 14], # Dom9
        "pentatonic_major": [0, 2, 4, 7, 9],   # 6/9 cluster
        "pentatonic_minor": [0, 3, 5, 7, 10],  # Min11 cluster
        "blues":            [0, 3, 6, 7, 10],  # Min7(b5) cluster
    }

    # Default to C minor if invalid inputs are provided
    root_val = NOTE_MAP.get(key, 0)
    chord_intervals = CHORDS.get(scale, CHORDS["minor"])
    
    # Base octave is C3 (note 48)
    base_note = 48 + root_val
    chord_notes = [base_note + interval for interval in chord_intervals]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item for Sustained Pad ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    # Insert the sustained chord notes
    for pitch in chord_notes:
        if 0 <= pitch <= 127:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments and Effects ===
    
    # 4a. Add ReaSynth (Setup for Brightness: Saw + Square)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 1: Tuning (0), Param 2: Sawtooth (1.0), Param 3: Square (0.5)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 1.0) 
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.5)

    # 4b. Add ReaEQ
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # ReaEQ Parameter logic:
    # Band 1 Freq = Param 0, Gain = Param 1, Q = Param 2, Type = Param 3
    # Type 3 = Low Pass filter
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 3, 3.0) 

    # === Step 5: Automate the Filter Sweep ===
    
    # Get the envelope for Band 1 Frequency (Param 0). True = create if not exists
    env_freq = RPR.RPR_GetFXEnvelope(track, fx_eq, 0, True)
    
    # Insert points to create the sweep (Shape 0 = linear transition)
    # Start closed (normalized frequency ~ 0.05 / very low Hz)
    RPR.RPR_InsertEnvelopePoint(env_freq, 0.0, 0.05, 0, 0.0, False, True)
    
    # End open (normalized frequency ~ 0.85 / ~ 10kHz)
    RPR.RPR_InsertEnvelopePoint(env_freq, item_length, 0.85, 0, 0.0, False, True)
    
    RPR.RPR_Envelope_Sort(env_freq)

    return f"Created '{track_name}' with automated Low-Pass filter sweep over {bars} bars at {bpm} BPM in {key} {scale}."
```